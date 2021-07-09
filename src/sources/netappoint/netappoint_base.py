import urllib.parse
import time

from ..base import *


class NetAppointBase(SourceBase):
    """
    Unified code to scrape all "netappoint" pages.

    Need to subclass and define class-attribute BASE_URL (w/o trailing slash).
    """
    BASE_URL = None
    NA_COMPANY = None

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
            case_dict[location["cases"][0]] = 1

            day_times = []
            days = self.get_na_days(next_url, case_dict)

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
        soup = self.get_html_soup(
            f"{self.BASE_URL}/index.php?company={self.NA_COMPANY}"
        )
        if soup.find("form", {"name": "frm_casetype"}):
            return self._get_na_cases_v2(soup)

    def _get_na_cases_v2(self, soup):
        locations = {}
        for ul in soup.find_all("ul", {"class": "nat_casetypelist"}):
            loc_id = ul.get("id")
            loc_name = soup.find("a", {"href": f"javascript:toggle('{loc_id}');"}).text.strip()
            if loc_name.startswith("Kategorie "):
                loc_name = loc_name[10:]

            cases = []
            for select in ul.find_all("select", {"class": "nat_casetypelist_casetype"}):
                cases.append(select.get("name"))

            if not cases:
                for input in ul.find_all("input", {"class": "nat_casetypelist_casetype casetype_checkbox"}):
                    cases.append(input.get("name"))

            locations[loc_id] = {
                "name": loc_name,
                "cases": cases,
            }

        next_url = soup.find("form", {"name": "frm_casetype"}).get("action")
        next_url = self.full_url(next_url)
        return locations, next_url

    def get_na_days(self, url: str, cases: dict) -> List[dict]:
        cases["sentcasetypes"] = "Weiter"
        soup = self.get_html_soup(url, method="POST", data=cases)

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

