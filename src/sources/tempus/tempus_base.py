from ..base import *


class TempusBaseScraper(SourceBase):
    """
    Unified code to scrape all "tempus-termine.com" pages.

    Need to subclass and define class-attribute TEMPUS_ID.

    """
    SCRAPER_TYPE = "tempus"
    MULTI_PROCESS_GROUP = "tempus"  # do not scrape the website in parallel

    BASE_URL = "https://tempus-termine.com/termine/index.php"
    TEMPUS_ID = None  # replace with "anlagennr"

    _RE_URL_DATE = re.compile(r".*datum=(\d\d\d\d-\d\d-\d\d).*")
    _RE_TIME = re.compile(r".*(\d\d:\d\d).*")

    @classmethod
    def index_url(cls) -> str:
        return f"{cls.BASE_URL}?anlagennr={cls.TEMPUS_ID}"

    def make_snapshot(self):
        options = self.tempus_get_options()
        # print(json.dumps(options, indent=2))

        calendars = self.tempus_get_calendars(options)
        options.pop("url")
        return {
            "options": options,
            "calendars": calendars
        }

    def tempus_get_options(self) -> dict:
        soup = self.get_html_soup(self.index_url())
        form = soup.find("form", {"id": "formular"})
        if not form:
            pass

        options_list = []

        main_menu = form.find("ul", {"class": "menuepunkt"})
        if main_menu:
            for sub_menu_container in main_menu.find_all("li", recursive=False):
                ul = sub_menu_container.find("ul", {"class": "untermenuepunkt"})
                if ul:
                    category = sub_menu_container.text.splitlines()[0].strip()
                    for li in ul.find_all("li"):
                        entry = {
                            "category": category,
                            "name": li.find("span").text.strip(),
                            "id": None,
                        }

                        select = li.find("select")
                        if select:
                            entry["id"] = select.attrs["id"]

                        options_list.append(entry)

                else:
                    category = "default"
                    li = sub_menu_container
                    input = li.find("input", {"type": "radio"})
                    if input:
                        entry = {
                            "category": category,
                            "name": li.text.strip(),
                            "id": input.attrs["value"],
                        }
                        options_list.append(entry)
        else:
            def _label_select(tag):
                if tag.name != "label":
                    return False
                klass = tag.attrs["class"] or ""
                return "menuepunkt" in klass or "untermenuepunkt" in klass

            menu_labels = form.find_all("label", {"class": "menuepunkt"})
            sub_menu_labels = form.find_all("label", {"class": "untermenuepunkt"})
            if not sub_menu_labels:
                for label in menu_labels:
                    entry = {
                        "category": "default",
                        "name": label.find("span").text.strip(),
                        "id": None,
                    }
                    select = label.find("select")
                    if select:
                        entry["id"] = select.attrs["id"]

                    options_list.append(entry)
            else:
                category = "-"
                for label in form.find_all(_label_select):
                    if "menuepunkt" in label.attrs["class"]:
                        category = label.text.strip()
                    else:
                        entry = {
                            "category": category,
                            "name": label.find("span").text.strip(),
                            "id": None,
                        }
                        select = label.find("select")
                        if select:
                            entry["id"] = select.attrs["id"]

                        options_list.append(entry)
        return {
            "url": form.attrs["action"],
            "options": options_list,
        }

    def tempus_get_calendars(self, options: dict) -> dict:
        categories = {}
        for o in options["options"]:
            categories.setdefault(o["category"], []).append(o)

        ret_calendars = {}
        for category, cat_options in categories.items():
            form_data = {}
            for o in cat_options:
                if o["id"]:
                    # pick first option for each category
                    if not form_data:
                        form_data[o["id"]] = "1"
                    else:
                        form_data[o["id"]] = "0"

            if form_data:
                for cal_id, calendar in self.tempus_yield_calendar(category, options["url"], form_data):
                    ret_calendars[cal_id] = calendar

        return ret_calendars

    def tempus_yield_calendar(
            self, category: str, url: str, form_data: dict
    ) -> Generator[Tuple[str, Dict[str, List[str]]], None, None]:
        soup = self.get_html_soup(self._full_url(url), method="POST", data=form_data)
        soup = self.tempus_skip_information(soup)
        soup_str = str(soup)

        if not (
                "Standorte und<br/>frühestmögliche Termine" in soup_str
                or "Bürgerbüros und<br/>frühestmögliche Termine" in soup_str
        ):
            yield category, self.tempus_get_calendar_page(soup)

        # split into different locations
        else:
            num_locations = 0
            for a in soup.find_all("a", {"class": "infolink"}):
                if "Uhr" not in a.text:
                    sub_category = a.text.strip()
                    href = a.attrs["href"]
                    sub_soup = self.get_html_soup(self._full_url(href))
                    yield f"{category}|{sub_category}", self.tempus_get_calendar_page(sub_soup)
                    num_locations += 1

            if not num_locations:
                ul = soup.find("ul", {"id": "nav_menu2"})
                for li in ul.find_all("li"):
                    a = li.find("a")
                    if a:
                        sub_category = a.text.strip()
                        if sub_category.startswith("Termine in "):
                            sub_category = sub_category[11:]
                            href = a.attrs["href"]
                            sub_soup = self.get_html_soup(self._full_url(href))
                            yield f"{category}|{sub_category}", self.tempus_get_calendar_page(sub_soup)
                            num_locations += 1

    def tempus_get_calendar_page(self, soup) -> Dict[str, List[str]]:
        soup = self.tempus_skip_information(soup)

        event_dates = []
        table = soup.find("table", {"class": "cal"})

        for td in table.find_all("td", {"class": "monatevent"}):
            url = td.find("a").attrs["href"]
            match = self._RE_URL_DATE.match(url)
            event_dates.append({
                "date": match.groups()[0],
                "url": url,
            })

        ret_dates = {}
        for event in event_dates:
            times = self.tempus_get_calendar_day_times(event)
            if times:
                ret_dates[event["date"]] = times
        return ret_dates

    def tempus_get_calendar_day_times(self, event: dict) -> List[str]:
        soup = self.get_html_soup(self._full_url(event["url"]))
        table = soup.find("table", {"class": "termine"})

        times = set()
        for td in table.find_all("td"):
            text = (td.text or "").strip()
            match = self._RE_TIME.match(text)
            if match:
                times.add(match.groups()[0])
        return sorted(times)

    def tempus_skip_information(self, soup):
        soup_str = str(soup)

        if not (
            "<h1>Wichtiger Hinweis</h1>" in soup_str
            or "value=\"Ich habe die Hinweise zur Kenntnis genommen\"" in soup_str
            or "value=\"Ich möchte gern vorbei kommen\"" in soup_str
        ):
            return soup

        input = soup.find("input", {"type": "button"})
        if not input:
            input = soup.find("input", {"type": "submit"})
            
        on_click = input.attrs["onclick"]
        url = on_click[on_click.index("href='?")+6:-2]
        url = self._full_url(url)
        return self.get_html_soup(url)

    def _full_url(self, url: str) -> str:
        if url.startswith("index.php"):
            full_url = self.BASE_URL
            full_url = full_url[:full_url.index("index.php")] + url
        elif url.startswith("?"):
            full_url = self.BASE_URL + url
        else:
            raise ValueError(f"Can not determine full url for '{url}'")

        return full_url
