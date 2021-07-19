import urllib.parse
import time

from ..base import *


class NetAppointBase(SourceBase):
    """
    Unified code to scrape all "netappoint" pages.

    Need to subclass and define class-attribute BASE_URL (w/o trailing slash).
    """
    SCRAPER_TYPE = "netappoint"

    BASE_URL = None
    NA_COMPANY = None
    NA_EXTRA_PARAMS = None

    NA_ERROR_INVALID_SERVICE = (
        "Die von Ihnen gewählte Dienstleistungs-Kombination kann nicht an einem Standort bearbeitet werden"
    )
    NA_ERROR_NO_SERVICE_SELECTED = (
        "Bitte geben Sie mindestens 1 Dienstleistung an."
    )

    @classmethod
    def index_url(cls) -> str:
        return f"{cls.BASE_URL}/index.php?company={cls.NA_COMPANY}"

    @classmethod
    def convert_snapshot(cls, data: Union[dict, list]) -> Optional[List[dict]]:
        ret_data = []
        for row in data:
            ret_data.append({
                "location_id": cls.to_id(row["location"]),
                "location_name": row["location"],
                "dates": [
                    datetime.datetime.strptime(d, "%Y-%m-%d %H:%M")
                    for d in row["dates"]
                ]
            })
        return ret_data

    def full_url(self, url_part: str) -> str:
        return self.BASE_URL.split("/")[0] + "//" + self.BASE_URL.split("/")[2] + url_part

    def make_snapshot(self):
        ret_data = []

        cases, next_url = self.get_na_cases()
        for location in cases.values():

            # create form and select first entry of each location
            case_dict = {
                case: "0"
                for case in location["cases"]
            }
            case_dict[location["cases"][0]] = "1"

            day_times = []
            try:
                days = self.get_na_days(next_url, case_dict)
            except Exception:
                if len(case_dict) > 1:
                    case_dict[location["cases"][0]] = "0"
                    case_dict[location["cases"][1]] = "1"
                    days = self.get_na_days(next_url, case_dict)
                else:
                    raise

            # for some reason this is important,
            #   otherwise the day-select-screen comes up again
            self.session.cookies.clear()

            for day in days:
                day_times += self.get_na_day_times(day["url"], day["date"])

            ret_data.append({
                "location": location["name"],
                "dates": day_times
            })
        return ret_data

    def get_na_cases(self) -> Tuple[dict, str]:
        url = self.index_url()
        if self.NA_EXTRA_PARAMS:
            url += "&" + "&".join(self.NA_EXTRA_PARAMS)
        soup = self.get_html_soup(url)

        locations = {}
        for ul in soup.find_all("ul", {"class": "nat_casetypelist"}):
            loc_id = ul.get("id")
            loc_name = soup.find("a", {"href": f"javascript:toggle('{loc_id}');"}).text.strip()
            if loc_name.startswith("Kategorie "):
                loc_name = loc_name[10:]

            cases = []
            for select in ul.find_all("select", {"class": "nat_casetypelist_casetype"}):
                cases.append(select.get("name"))

            for input in ul.find_all("input", {"class": "nat_casetypelist_casetype casetype_checkbox"}):
                cases.append(input.get("name"))

            locations[loc_id] = {
                "name": loc_name,
                "cases": cases,
            }

        next_url = soup.find("form", {"name": "frm_casetype"}).get("action")
        next_url = self.full_url(next_url)
        return locations, next_url

    def get_na_step_3(self, soup) -> str:
        for li in soup.find_all("li", {"class": "nat_casetypelist_casetype_li"}):
            next_url = li.find("a").get("href")
            if next_url and "step=3&" in next_url:
                return self.full_url(next_url)
        raise ValueError(f"step=3 url not found!\nContent: {soup}")

    def get_na_days(self, url: str, cases: dict) -> List[dict]:
        cases["sentcasetypes"] = "Weiter"
        soup = self.get_html_soup(url, method="POST", data=cases)

        # has clickable days?
        if not soup.find("a", {"class": "nat_calendar_weekday_bookable"}):
            # has empty table?
            if soup.find("table", {"class": "nat_calendar"}):
                return []

            # some service selections lead to error messages
            text = soup.text
            if self.NA_ERROR_INVALID_SERVICE in text \
                    or self.NA_ERROR_NO_SERVICE_SELECTED in text:
                return []

            # otherwise we need to select a location first
            soup = self.get_html_soup(
                self.get_na_step_3(soup)
            )

        days = []
        for a in soup.find_all("a", {"class": "nat_calendar_weekday_bookable"}):
            next_url = self.full_url(a.get("href"))
            # move to time slot
            next_url = next_url.replace("&step=4&", "&step=3&")

            query = urllib.parse.parse_qs(next_url)
            date = datetime.date(int(query["year"][0]), int(query["month"][0]), int(query["day"][0]))
            days.append({
                "date": date,
                "url": next_url,
            })

        return days

    def get_na_day_times(self, url: str, date: datetime.date) -> List[str]:
        soup = self.get_html_soup(url)
        table = soup.find("table", {"class": "nat_timeslist"})
        if not table:
            print(soup.find("table").attrs)
            return []

        day_times = []
        for abbr in table.find_all("abbr"):
            time_str = abbr.text.strip()
            dt = date.strftime("%Y-%m-%d ") + time_str
            day_times.append(dt)
        return day_times

