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
        now = self.now()

        options = self.tempus_get_options()
        # print(json.dumps(options, indent=2))

        calendars = self.tempus_get_calendars(options)
        return {
            "options": options,
            "calendars": calendars
        }

    def tempus_get_options(self) -> dict:
        soup = self.get_html_soup(self.index_url())
        form = soup.find("form", {"id": "formular"})

        main_menu = form.find("ul", {"class": "menuepunkt"})
        #for ul in main_menu.find_all("ul", {"class": "untermenuepunkt"}):
        #    print(ul.previos_siblings)

        options_list = []

        for sub_menu_container in main_menu.find_all("li", recursive=False):
            category = sub_menu_container.text.splitlines()[0].strip()

            ul = sub_menu_container.find("ul", {"class": "untermenuepunkt"})
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

        return {
            "url": form.attrs["action"],
            "options": options_list,
        }

    def tempus_get_calendars(self, options: dict):
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
                calendar = self.tempus_get_calendar(options["url"], form_data)
                ret_calendars[category] = calendar

        return ret_calendars

    def tempus_get_calendar(self, url: str, form_data: dict) -> Dict[str, List[str]]:
        soup = self.get_html_soup(self._full_url(url), method="POST", data=form_data)

        if "<h1>Wichtiger Hinweis</h1>" in str(soup):
            soup = self.tempus_skip_information(soup)
        #print(soup)
        #exit()

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

        dates = []
        for td in table.find_all("td"):
            text = (td.text or "").strip()
            match = self._RE_TIME.match(text)
            if match:
                dates.append(match.groups()[0])
        return dates

    def tempus_skip_information(self, soup):
        input = soup.find("input", {"type": "button"})
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
