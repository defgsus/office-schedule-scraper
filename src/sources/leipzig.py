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
    NAME = "Stadt Leipzig"
    BASE_URL = "https://tnv.leipzig.de/tnv"

    #REQUEST_DELAY = .1

    @classmethod
    def index_url(cls) -> str:
        return "https://leipzig.de/fachanwendungen/termine/index.html"

    def make_snapshot(self) -> List[dict]:
        session = EkolSession(self)
        session.start()  # go to office selection

        locations = session.get_locations()

        ret_data = []
        for loc in locations:
            session.select_location(loc)
            session.select_concern()

            days = session.get_free_days()
            loc.pop("button_name")
            loc["days"] = days

            ret_data.append(loc)

            while session.page() != session.PAGE_OFFICE_SELECT:
                session.step_back()

        return ret_data

    @classmethod
    def _convert_snapshot(
            cls,
            dt: datetime.datetime,
            data: Union[dict, list],
            as_datetime: bool = False,
    ) -> Optional[List[dict]]:
        ret_data = []
        for loc in data:
            dates = []
            for day in loc["days"]:
                for ti in day["times"]:
                    if as_datetime:
                        dates.append(datetime.datetime.strptime(
                            day["date"] + ti, "%Y-%m-%d%H:%M"
                        ))
                    else:
                        dates.append(day["date"] + " " + ti + ":00")
            ret_data.append({
                "location_id": loc["id"],
                "location_name": loc["name"],
                "dates": dates,
            })
        return ret_data


class EkolSession:
    """
    Scraper utility for the "eKOL Terminverwaltung by Telecomputer GmbH"
    """
    PAGE_INFO_PAGE = "INFOPAGE"
    PAGE_OFFICE_SELECT = "OFFICESELECT"
    PAGE_CONCERN_SELECT = "CONCERNSELECT"
    PAGE_CONCERN_COMMENTS = "CONCERNCOMMENTS"
    PAGE_CALENDAR_SELECT = "CALENDARSELECT"

    def __init__(self, scraper: SourceBase):
        self.scraper = scraper
        self.soup = None

    def title(self) -> str:
        return self.soup.find("h2", {"class": "ekolStepBox2"}).text.strip()

    def page(self) -> str:
        title = self.title()
        if title == "Allgemeine Informationen":
            return self.PAGE_INFO_PAGE
        elif title == "Termin vereinbaren bei":
            return self.PAGE_OFFICE_SELECT
        elif title == "Auswahl des Anliegens":
            return self.PAGE_CONCERN_SELECT
        elif title == "Zusatzinformationen zu den Anliegen":
            return self.PAGE_CONCERN_COMMENTS
        elif title == "Auswahl des Termins":
            return self.PAGE_CALENDAR_SELECT
        else:
            return "UNKNOWN"

    def start(self):
        """
        Starts a new jsession with the server and navigates to the locations page
        """
        self.soup = self.scraper.get_html_soup(self.scraper.BASE_URL)

        # -- accept data protection --
        self.submit({
            "AGREEMENT_ACCEPT":	"on",
            "AGREEMENT_REQUIRED": "true",
            "ACTION_INFOPAGE_NEXT":	"",
        })

    def step_back(self):
        page = self.page()
        self.submit({f"ACTION_{page}_PREVIOUS": ""})

    def step_forward(self):
        page = self.page()
        self.submit({f"ACTION_{page}_NEXT": ""})

    def submit(self, params: dict):
        """
        Submit the current form with all hidden fields and the given params.
        Load new self.soup
        """
        form = self.soup.find("form")
        action_url = form.get("action")
        query = {
            i.get("name"): i.get("value")
            for i in form.find_all("input", {"type": "hidden"})
        }
        query.update({
            "SELECTED_LANGUAGE": "de",
        })
        query.update(params)

        self.soup = self.scraper.get_html_soup(
            f"{self.scraper.BASE_URL}/{action_url}", method="POST", data=query
        )

    def get_locations(self):
        assert self.page() == self.PAGE_OFFICE_SELECT

        locations = []
        for div in self.soup.find_all("div", {"class": "CLASS_TREEVIEWSEARCH_HEAD_LEVEL_2"}):
            button = div.find("button")
            loc = {
                "name": button.text.strip(),
                "button_name": button.get("name"),
                "id": button.get("name").split("-")[-1],
            }
            if loc["name"] not in ("Bürgerämter", "Ordnungsamt"):
                locations.append(loc)

        return locations

    def select_location(self, location: dict):
        """
        Select one specific location and navigate to concern-select.

        :param location: one single dict from get_locations()
        """
        assert self.page() == self.PAGE_OFFICE_SELECT, f"Got {self.page()}"

        # -- open location panel --

        self.submit({
            location["button_name"]: "Öffnen",
            "OFFICESELECT_TERMID": "",
            "OFFICESELECT_RESERVATIONPIN": "",
        })

        # -- click the appointment button --

        button = None
        for but in self.soup.find_all("button", {"class": "class_BuergerAuswahlDienststelle_office-button"}):
            if location["id"] in but.get("name"):
                button = but
                break

        self.submit({
            button.get("name"): "",
            "OFFICESELECT_TERMID": "",
            "OFFICESELECT_RESERVATIONPIN": "",
        })
        assert self.page() == self.PAGE_CONCERN_SELECT, f"Got {self.page()}"

    def select_concern(self):
        """
        Select the first concern and navigate to calendar selection
        """
        assert self.page() == self.PAGE_CONCERN_SELECT, f"Got {self.page()}"

        # select first service
        params = dict()
        for td in self.soup.find_all("td", {"class": "CLASS_METADATAGRIDENTRY_VALUECONTAINER"}):
            select = td.find("select")
            if select:
                params[select.get("name")] = "1" if not params else "0"

        params["ACTION_CONCERNSELECT_NEXT"] = ""
        self.submit(params)

        assert self.page() in (self.PAGE_CONCERN_COMMENTS, self.PAGE_CALENDAR_SELECT), f"Got {self.page()}"
        if self.page() == self.PAGE_CONCERN_COMMENTS:
            self.step_forward()

        assert self.page() == self.PAGE_CALENDAR_SELECT, f"Got {self.page()}"

    def get_free_days(self):
        assert self.page() == self.PAGE_CALENDAR_SELECT, f"Got {self.page()}"

        days = []

        for table in self.soup.find_all("table", {"class": "ekolCalendarMonthTable"}):
            month = table.find("caption").text.strip()
            month, year = MONTH_MAPPING[month.split()[0]], int(month.split()[1])
            for td in table.find_all("td", {"class": "eKOLCalendarCellInRange"}):
                day = int(td.find("div", {"class": "ekolCalendarDayNumberInRange"}).text)
                num_free = int(td.find("div", {"class": "ekolCalendarFreeTimeContainer"}).text.split()[0])
                if num_free:
                    days.append({
                        "date": datetime.date(year, month, day),
                        "num_free": num_free,
                    })

                    # -- click day --
                    button = td.find("div", {"class": "ekolCalendarDayNumberInRange"}).parent
                    self.submit({button.get("name"): ""})

                    # -- read times --

                    select = self.soup.find("select", {"name": "ekolCalendarTimeSelect"})
                    days[-1]["times"] = [
                        o.text.strip()
                        for o in select.find_all("option")
                        if o.get("value")
                    ]

                    # -- close popup --

                    button = self.soup.find("button", {"class": "messagebox_buttonclose"})
                    self.submit({button.get("name"): ""})

        return days
