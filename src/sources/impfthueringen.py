from .base import *


class ImpfThueringen(SourceBase):
    """
    Covid-19 vaccination appointment for Thuringia.

    There is actually a lot going on and data changes every couple of seconds.
    They seem to provide a 3 minute slot for each appointment so it's
    likely that the number of appointees can still be counted even
    when scraping *only* every minute.

    """
    ID = "impfthueringen"

    BASE_URL = "https://www.impfen-thueringen.de/terminvergabe"

    def make_snapshot(self):
        locations = self.get_locations()

        ret_data = []
        for loc, loc_name in locations.items():
            dates = self.get_free_dates(loc)
            ret_data.append({
                "loc": loc,
                "loc_name": loc_name,
                "dates": dates
            })

        return ret_data

    def get_locations(self):
        soup = self.get_html_soup(f"{self.BASE_URL}/index.php")

        div = soup.find("div", {"class": "select-ort-area"})
        locations = dict()
        for o in div.find_all("option"):
            value = o.get("value")
            if value != "0":
                locations[value] = o.text.strip()

        return locations

    def get_free_dates(self, location: str):

        response = self.get_url(
            f"{self.BASE_URL}/func.php", "POST",
            {
                "typ": "1",
                "ort": location,
                "pos": 0,
                "timestamp": str(int(self.now().timestamp() * 1000)),
            }
        )
        soup = self.soup(response)
        dates = []
        for opt in soup.find_all("option"):
            dates.append((
                opt.get("value"),
                opt.get("data-folge-termin"),
            ))
        return dates
