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

    NEEDS_INCLUDE = True  # currently disable by default
    
    _RE_URL_DATE = re.compile(r".*datum=(\d\d\d\d-\d\d-\d\d).*")
    _RE_LOC_ID = re.compile(r".*standortrowid=(\d+).*")
    _RE_QUEUE_ID = re.compile(r".*schlangennr=(\d+).*")
    _RE_QUEUES_ID = re.compile(r".*schlangen=([\d-]+).*")
    _RE_TASKS = re.compile(r".*tasks=(\d+).*")
    _RE_TIME = re.compile(r".*(\d\d:\d\d).*")

    @classmethod
    def index_url(cls) -> str:
        return f"{cls.BASE_URL}?anlagennr={cls.TEMPUS_ID}"

    @classmethod
    def _convert_snapshot(
            cls,
            dt: datetime.datetime,
            data: Union[dict, list],
            as_datetime: bool = False,
    ) -> Optional[List[dict]]:
        ret_data = []
        for cal in data["calendars"]:
            dates = []
            for day, times in cal["dates"].items():
                for time in times:
                    dates.append(f"{day} {time}:00")

            name = cal["category"]
            if cal.get("sub_category"):
                name = f'{cal["sub_category"]}|{name}'

            for key in ("loc", "task", "queue"):
                name = f"{name}|{cal.get(key) or '-'}"

            ret_data.append({
                "location_id": f'{cal.get("loc") or "-"}/{cal.get("task") or "-"}',
                "location_name": name,
                "dates": dates,
            })
        return ret_data

    def make_snapshot(self):
        options = self.tempus_get_options()
        # print(json.dumps(options, indent=2))

        calendars = self.tempus_get_calendars(options)
        #exit()
        return {
            "options": options["options"],
            "calendars": calendars
        }

    def tempus_get_options(self) -> dict:
        soup = self.get_html_soup(self.index_url())
        form = soup.find("form", {"id": "formular"})

        options_list = (
            self.tempus_get_options_list_1(soup, form)
            or self.tempus_get_options_list_2(soup, form)
            #or self.tempus_get_options_list_3(soup, form)
        )

        return {
            "url": form.attrs["action"],
            "options": options_list,
        }

    def tempus_get_options_list_1(self, soup, form):
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
                    form_id = None
                    input = li.find("input", {"type": "radio"})
                    if input:
                        form_id = input.attrs["value"]
                    else:
                        input = li.find("input", {"type": "checkbox"})
                        if input:
                            form_id = input.attrs["value"]
                        else:
                            input = li.find("select")
                            if input:
                                form_id = input.attrs["name"]

                    name = li.text.strip()
                    div = li.find("div", {"class": "liContent"})
                    if div:
                        name = div.text.strip()
                    if form_id:
                        entry = {
                            "category": category,
                            "name": name,
                            "id": form_id,
                        }
                        options_list.append(entry)
        return options_list

    def tempus_get_options_list_2(self, soup, form):
        def _label_select(tag):
            if tag.name != "label":
                return False
            klass = tag.attrs["class"] or ""
            return "menuepunkt" in klass or "untermenuepunkt" in klass

        options_list = []
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
        return options_list

    def tempus_get_calendars(self, options: dict) -> List[dict]:
        categories = {}
        for o in options["options"]:
            categories.setdefault(o["category"], []).append(o)

        ret_calendars = []
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
                    ret_calendars.append({**cal_id, "dates": calendar})

        return ret_calendars

    def tempus_yield_calendar(
            self, category: str, url: str, form_data: dict
    ) -> Generator[Tuple[Dict, Dict[str, List[str]]], None, None]:
        # print("\nYIELD", category, url)
        soup = self.get_html_soup(self._full_url(url), method="POST", data=form_data)
        soup = self.tempus_skip_information(soup)
        soup_str = str(soup)

        if "Leider können wir Ihnen im Moment an keinem Standort einen Termin anbieten." in soup_str:
            return

        if not (
                "Der stadtweit früheste Termin ist" in soup_str
                or "Standorte und frühestmögliche Termine" in soup_str
                or "Standorte und<br/>frühestmögliche Termine" in soup_str
                or "Bürgerbüros und<br/>frühestmögliche Termine" in soup_str
                or "Bürgerbüros und frühestmögliche Termine" in soup_str
                or "Bürgerämter und<br/>frühestmögliche Termine" in soup_str
                or "Zulassungsstelle und<br/>frühestmögliche Termine" in soup_str
                or "Bäder und<br/>frühestmögliche Schwimmzeit" in soup_str
        ):
            cal_id, dates = self.tempus_get_calendar_page(soup)
            if cal_id:
                cal_id["category"] = category
                yield cal_id, dates

        # split into different locations
        else:
            a_tags = []
            for a in soup.find_all("a", {"class": "infolink"}):
                if "Uhr" not in a.text:
                    a_tags.append(a)

            if not a_tags:
                ul = soup.find("ul", {"id": "nav_menu2"})
                for li in ul.find_all("li"):
                    a = li.find("a")
                    if a and not a.text.endswith("Uhr"):
                        a_tags.append(a)

            if not a_tags:
                print(soup)
                raise ValueError(f"{self.ID}/{self.TEMPUS_ID} No locations found for {category} {url}")

            for a in a_tags:
                sub_category = a.text.strip()
                if sub_category.startswith("Termine in "):
                    sub_category = sub_category[11:]

                href = a.attrs["href"]
                sub_soup = self.get_html_soup(self._full_url(href))
                cal_id, dates = self.tempus_get_calendar_page(sub_soup)
                if cal_id:
                    cal_id["category"] = category
                    cal_id["sub_category"] = sub_category
                    yield cal_id, dates

    def get_tempus_calendar_url_id(self, url: str) -> Dict[str, str]:
        ret = {}
        for key, expr in (
                ("date", self._RE_URL_DATE),
                ("loc", self._RE_LOC_ID),
                ("queue", self._RE_QUEUE_ID),
                ("task", self._RE_TASKS),
        ):
            match = expr.match(url)
            ret[key] = match.groups()[0] if match else None
        return ret

    def tempus_get_calendar_page(self, soup) -> Tuple[Optional[Dict], Dict[str, List[str]]]:
        soup = self.tempus_skip_information(soup)

        event_dates = []
        table = soup.find("table", {"class": "cal"})
        if not table:
            # then it's probably the cancellation screen
            if soup.find("table", {"class": "appointment"}):
                return None, {}

            print(soup)
            raise ValueError("No table found")

        cal_id = None

        for table in soup.find_all("table", {"class": "cal"}):
            for td in table.find_all("td", {"class": "monatevent"}):
                url = td.find("a").attrs["href"]

                if not cal_id:
                    cal_id = self.get_tempus_calendar_url_id(url)
                    cal_id.pop("date")
                    # print("WILL", cal_id, url)

                match = self._RE_URL_DATE.match(url)
                event_dates.append({
                    "date": match.groups()[0],
                    "url": url,
                })

        event_dates.sort(key=lambda e: e["date"])

        # generate new URLs for specified self.num_weeks
        if event_dates:
            max_date = str((self.now() + datetime.timedelta(days=self.num_weeks * 7)).date())
            while event_dates[-1]["date"] < max_date:
                next_date = str((
                    datetime.datetime.strptime(event_dates[-1]["date"], "%Y-%m-%d")
                    + datetime.timedelta(days=1)
                ).date())
                event_dates.append({
                    "date": next_date,
                    "url": event_dates[-1]["url"].replace(
                        f"datum={event_dates[-1]['date']}", f"datum={next_date}"
                    )
                })

        ret_dates = {}
        for event in event_dates:
            times = self.tempus_get_calendar_day_times(event)
            if times:
                ret_dates[event["date"]] = times

        return cal_id, ret_dates

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
            or "value=\"Habe ich zur Kenntnis genommen\"" in soup_str
            or "value=\"Ich möchte gern vorbei kommen\"" in soup_str
            or "value=\"Bestätigen und weiter zur Terminauswahl\"" in soup_str
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
