from .base import *


class ImpfTerminService(SourceBase):
    """
    NOT IMPLEMENTED

    Scraper for https://www.impfterminservice.de/impftermine

    Well, they do not actually provide appointment data except
    the availability of an appointment at all. Thought i'd do a
    dump of all the registered vaccination centers and the
    availability of services once but there
    is some browser-specific stuff with javascript, POSTs
    and cookies that i could not re-create in script.

    The website is a disgusting one, anyways
    https://defgsus.github.io/blog/2021/07/23/vaccination-data.html
    """
    ID = "impftermin"
    NAME = "Impftermin Service KBV"

    BASE_URL = "https://www.impfterminservice.de"

    REQUEST_DELAY = .7

    @classmethod
    def index_url(cls) -> str:
        return f"{cls.BASE_URL}/impftermine"

    def make_snapshot(self):
        locations = self.get_json(f"{self.BASE_URL}/assets/static/impfzentren.json")
        print(json.dumps(locations, indent=2))

        vacc_list = None
        for state, state_locations in locations.items():
            for loc in state_locations:
                if not vacc_list:
                    vacc_list = self.get_json(f"{loc['URL']}assets/static/its/vaccination-list.json")

                self.it_get_location(loc)
            #

    def it_get_location(self, loc: dict):
        self.new_session()
        html = self.get_url(
            f"{loc['URL']}impftermine/service?plz={loc['PLZ']}"
        )
        data = self.get_json(
            f"{loc['URL']}rest/suche/termincheck?plz={loc['PLZ']}&leistungsmerkmale=L920,L921,L922,L923"
        )
        print("\n", loc)
        #print(self.session.cookies)
        print("X", data)