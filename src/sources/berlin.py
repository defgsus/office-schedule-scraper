import time
from .base import *


MONTH_MAPPING = {
    "Januar": 1,
    "Februar": 2,
    "März": 3,
    "April": 4,
    "Mai": 5,
    "Juni": 6,
    "Juli": 7,
    "August": 8,
    "September": 9,
    "Oktober": 10,
    "November": 11,
    "Dezember": 12,
}


class Berlin(SourceBase):
    ID = "berlin"

    BASE_URL = "https://service.berlin.de"

    @classmethod
    def index_url(cls) -> str:
        return f"{cls.BASE_URL}/terminvereinbarung/"

    def make_snapshot(self):
        locations = self.get_locations()

        ret_data = []
        for loc in locations:
            time.sleep(1)
            dates = self.get_free_dates(loc["url"])
            ret_data.append({
                "loc": loc,
                "dates": dates
            })
        exit()
        return ret_data

    def get_locations(self) -> List:
        soup = self.get_html_soup(f"{self.BASE_URL}/standorte/buergeraemter/")

        locations = []
        for div in soup.find_all("div", {"class": "ort-group"}):
            district = div.find("h2").text.strip()
            if district.endswith("nach oben"):
                district = district[:-9].strip()

            for a in div.find_all("a"):
                href = a.get("href")
                if href and href.startswith("/standort/"):
                    locations.append({
                        "district": district,
                        "name": a.text.strip(),
                        "url": f"{self.BASE_URL}{href}"
                    })

        return locations

    def get_free_dates(self, location_url: str) -> List:
        soup = self.get_html_soup(location_url)

        alert = soup.find("div", {"class": "alert"})
        if alert:
            alert = alert.text
            if alert:
                if "bis auf Weiteres geschlossen" in alert:
                    print("closed")
                    return []

        # -- pick one service --

        form = soup.find("form", {"id": "termin_form"})
        if not form:
            print("no form")
            return []

        cb = form.find("input", {"type": "checkbox", "name": "anliegen[]"})
        if not cb:
            print("no checkbox")
            return []

        action_url = form.get('action').split('?')[0]
        query = {
            i.get("name"): i.get("value")
            for i in form.find_all("input", {"type": "hidden"})
        }
        query.update({
            "termin": 1,
            cb.get("name"): cb.get("value"),
        })

        # print(action_url, query)

        #for a in form.find_all("a", {"class": "referdienstleister"}):
        #    print(a)

        days = []

        time.sleep(1)
        soup = self.get_html_soup(action_url, data=query)
        soup_str = str(soup)

        if "Ihre Auswahl von Standort und Diensteistung hat sich geändert." in soup_str:
            restart_url = None
            for a in soup.find_all("a"):
                href = a.get("href")
                if href and href.startswith("/terminvereinbarung/termin/restart/?"):
                    restart_url = href
            if not restart_url:
                print("NO RESTART LINK FOUND")
                return []
            time.sleep(1)
            soup = self.get_html_soup(f"{self.BASE_URL}{restart_url}")
            soup_str = str(soup)

        if "<h1>Zu viele Zugriffe</h1>" in soup_str:
            print("THROTTLED")
            return []

        for div in soup.find_all("div", {"class": "calendar-month-table"}):
            month = div.find("th", {"class": "month"}).text.strip()
            month, year = MONTH_MAPPING[month.split()[0]], int(month.split()[1])

            for td in div.find_all("td"):#, {"class": "buchbar"}):
                klass = td.get("class") or []
                if "buchbar" in klass or "nichtbuchbar" in klass:
                    days.append({
                        "date": datetime.date(year, month, int(td.text.strip().lstrip("0"))),
                        "class": td.get("class")
                    })
                    a = td.find("a")
                    if a:
                        days[-1]["url"] = a.get("href")

        if not soup.find("div", {"class": "calendar-month-table"}):
            print(soup)

        for day in days:
            if day.get("url"):
                day["times"] = self.get_free_day_times(
                    f"{self.BASE_URL}{day['url']}"
                )

        return days

    def get_free_day_times(self, url: str) -> List:
        time.sleep(1)
        soup = self.get_html_soup(url)
        print(soup)

        return []
