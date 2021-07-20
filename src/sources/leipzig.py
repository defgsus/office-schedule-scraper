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


class Leipzig(SourceBase):
    """
    TODO: Leipzig uses a very *verwurschtelt* session system
        which is quite hard to query

    """
    ID = "leipzig"
    BASE_URL = "https://tnv.leipzig.de/tnv"

    REQUEST_DELAY = 1

    @classmethod
    def index_url(cls) -> str:
        return "https://leipzig.de/fachanwendungen/termine/index.html"

    def make_snapshot(self):
        locations = self.get_locations()

        for loc in locations:
            self.new_session()
            print("\n\n----------\n", loc)
            loc.update(self.get_location_dates(loc.pop("button_name")))
            print(loc)

        return locations

    def get_locations(self) -> List:
        soup = self._get_location_soup()
        locations = []
        for div in soup.find_all("div", {"class": "CLASS_TREEVIEWSEARCH_HEAD_LEVEL_2"}):
            button = div.find("button")
            loc = {
                "name": button.text.strip(),
                "button_name": button.get("name"),
                "id": button.get("name").split("-")[-1],
            }
            if loc["name"] not in ("Bürgerämter", "Ordnungsamt"):
                locations.append(loc)

        return locations

    def get_location_dates(self, button_name: str) -> dict:
        soup = self._get_location_soup()

        # -- open the location --
        form = soup.find("form")
        action_url = form.get("action")
        query = {
            i.get("name"): i.get("value")
            for i in form.find_all("input", {"type": "hidden"})
        }
        query.update({
            "SELECTED_LANGUAGE": "de",
            button_name: "Öffnen",
            "OFFICESELECT_TERMID": "",
            "OFFICESELECT_RESERVATIONPIN": "",
        })

        soup = self.get_html_soup(f"{self.BASE_URL}/{action_url}", method="POST", data=query)
        print("\n3", soup.find("h2", {"class": "ekolStepBox2"}))

        return self._book_location(soup)

    def _get_location_soup(self):
        """Will start a new jsession with the server and navigate to the locations page"""
        soup = self.get_html_soup(self.BASE_URL)
        print("\n1", soup.find("h2", {"class": "ekolStepBox2"}))

        # -- accept data protection --

        form = soup.find("form")
        action_url = form.get("action")
        query = {
            i.get("name"): i.get("value")
            for i in form.find_all("input", {"type": "hidden"})
        }
        query.update({
            "SELECTED_LANGUAGE": "de",
            "AGREEMENT_ACCEPT":	"on",
            "AGREEMENT_REQUIRED": "true",
            "ACTION_INFOPAGE_NEXT":	"",
        })

        soup = self.get_html_soup(
            f"{self.BASE_URL}/{action_url}", method="POST", data=query
        )
        print("\n2", soup.find("h2", {"class": "ekolStepBox2"}))
        return soup

    def _book_location(self, soup) -> dict:

        # click the appointment button
        button = soup.find("button", {"class": "class_BuergerAuswahlDienststelle_office-button"})
        if not button:
            print(soup)
            exit(1)
        assert button.text.strip() == "Termin vereinbaren"

        form = soup.find("form")
        action_url = form.get("action")
        query = {
            i.get("name"): i.get("value")
            for i in form.find_all("input", {"type": "hidden"})
        }
        query.update({
            "SELECTED_LANGUAGE": "de",
        })
        query[button.get("name")] = ""
        query.update({
            "OFFICESELECT_TERMID": "",
            "OFFICESELECT_RESERVATIONPIN": "",
        })

        soup = self.get_html_soup(f"{self.BASE_URL}/{action_url}", method="POST", data=query)

        return self._get_location_dates(soup)

    def _get_location_dates(self, soup) -> dict:
        # "Auswahl des Anliegens"
        print("\n4", soup.find("h2", {"class": "ekolStepBox2"}))

        form = soup.find("form")
        action_url = form.get("action")
        query = {
            i.get("name"): i.get("value")
            for i in form.find_all("input", {"type": "hidden"})
        }

        # select first service
        services = dict()
        for td in soup.find_all("td", {"class": "CLASS_METADATAGRIDENTRY_VALUECONTAINER"}):
            select = td.find("select")
            if select:
                services[select.get("name")] = "1" if not services else "0"

        if not services:
            print("NO SERVICES FOUND")
            return {}

        query.update(services)
        query.update({
            "SELECTED_LANGUAGE": "de",
            "ACTION_CONCERNSELECT_NEXT": "",
        })

        prev_action_url = f"{self.BASE_URL}/{action_url}"
        soup = self.get_html_soup(prev_action_url, method="POST", data=query)
        print("\n5", soup.find("h2", {"class": "ekolStepBox2"}))

        # click "Weiter"
        form = soup.find("form")
        action_url = form.get("action")
        query = {
            i.get("name"): i.get("value")
            for i in form.find_all("input", {"type": "hidden"})
        }
        query.update({
            "SELECTED_LANGUAGE": "de",
            "ACTION_CONCERNCOMMENTS_NEXT": "",
        })

        soup = self.get_html_soup(
            f"{self.BASE_URL}/{action_url}",
            method="POST",
            data=query,
        )
        # "Auswahl des Termins"
        print("\n6", soup.find("h2", {"class": "ekolStepBox2"}))

        days = []

        for table in soup.find_all("table", {"class": "ekolCalendarMonthTable"}):
            month = table.find("caption").text.strip()
            month, year = MONTH_MAPPING[month.split()[0]], int(month.split()[1])
            for td in table.find_all("td", {"class": "eKOLCalendarCellInRange"}):
                day = int(td.find("div", {"class": "ekolCalendarDayNumberInRange"}).text)
                num_free = int(td.find("div", {"class": "ekolCalendarFreeTimeContainer"}).text.split()[0])

                days.append({
                    "date": datetime.date(year, month, day),
                    "num_free": num_free,
                })

        return {
            "days": days
        }
