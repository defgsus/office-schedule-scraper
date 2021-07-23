from ..base import *


class TevisBaseScraper(SourceBase):
    """
    Unified code to scrape all "tevis" pages.

    Need to subclass and define class-attribute BASE_URL (w/o trailing slash).

    Tevis seems to be a software by "Kummunix GmbH" https://www.kommunix.de/produkte/tevis/.

    The list of references is here: https://www.kommunix.de/referenzen/
    """
    SCRAPER_TYPE = "tevis"

    @classmethod
    def convert_snapshot(cls, data: Union[dict, list]) -> Optional[List[dict]]:
        if not data["cnc"]:
            return None

        cal_id_2_name = dict()
        for c in data["cnc"]:
            for c_id in c["calendar"].split("|"):
                if not c.get("md"):
                    # old snapshot version before adding md
                    cal_id_2_name[c_id] = c.get("name", c.get("title", c_id))
                else:
                    cal_id_2_name[c_id] = data["md"][c["md"]]

        ret_data = []
        for cal_id, cals in data["calendar"].items():
            cal_id = cal_id.split("|")[0]
            dates = []
            if not isinstance(cals, list):
                cals = [cals]
            for cal in cals:
                for day, valid in zip(cal["days"], cal["valid"]):
                    start_date = datetime.datetime.strptime(day, "%Y%m%d")
                    #start_date = datetime.datetime(int(cal["year"]), int(cal["month"]), int(cal["day"]))
                    for minutes in valid:
                        dates.append(start_date + datetime.timedelta(minutes=int(minutes)))

            ret_data.append({
                "location_id": cal_id,
                "location_name": cal_id_2_name[cal_id],
                "dates": dates,
            })
        return ret_data

    def make_snapshot(self):
        now = self.now()

        calendars = set()

        md_ids = self.get_tevis_md()
        cnc_items = []
        for md, title in md_ids.items():
            cnc_items += self.get_tevis_cnc(md)

        for cnc in cnc_items:
            for c in cnc["calendar"].split("|"):
                calendars.add(c)

        calendars = sorted(calendars)

        ret_data = {
            "md": md_ids,
            "cnc": cnc_items,
            "calendar": dict(),
        }

        for calendar in calendars:
            if calendar == "0":
                continue
            for i in range(self.num_weeks):
                year, week, _ = (now + datetime.timedelta(days=7 * i)).isocalendar()
                data = self.get_tevis_caldiv(calendar, year, week)

                data.pop("html", None)

                if calendar not in ret_data["calendar"]:
                    ret_data["calendar"][calendar] = []
                ret_data["calendar"][calendar].append(data)

        return ret_data

    def get_tevis_md(self) -> Dict[str, str]:
        md_ids = dict()
        soup = self.get_html_soup(f"{self.BASE_URL}/")
        for a in soup.find_all("a"):
            if a.get("href") and a.get("href").startswith("select2?md="):
                md_id = a.get("href")[11:]
                md_ids[md_id] = a.text.strip()
        return md_ids

    def get_tevis_cnc(self, md) -> List[dict]:
        cnc = list()
        soup = self.get_html_soup(f"{self.BASE_URL}/select2?md={md}")
        for form in soup.find_all("form", {"class": "cnc-form"}):
            cnc_item = form.find("input", {"class": "cnc-item"})
            cnc.append({
                "md": md,
                "mdt": form.find("input", {"name": "mdt"}).get("value"),
                "calendar": cnc_item.get("data-tevis-calendars"),
                "location": self._short_set(cnc_item.get("data-tevis-locations")),
                "title": form.find("a").text.strip(),
            })

        if not cnc:
            mdt = soup.find("input", {"name": "mdt"}).get("value")
            # select_cnc = soup.find("input", {"name": "select_cnc"}).get("value")
            for i in soup.find_all("input", {"class": "cnc-item"}):
                data = {
                    "md": md,
                    "mdt": mdt,
                    "cnc_id": i.get("data-tevis-cncid"),
                    "location": self._short_set(i.get("data-tevis-locations")),
                }
                a = i.parent.parent.find("a", {"data-html": "true"})
                if a:
                    data["name"] = a.text.strip()
                else:
                    if i.get("data-tevis-cncname"):
                        data["name"] = i.get("data-tevis-cncname")

                cnc.append(data)

            cnc_ids = sorted(set(i["cnc_id"] for i in cnc))
            cal = str(self.get_tevis_location_calendar(mdt, cnc_ids))
            for c in cnc:
                c["calendar"] = cal

        return cnc

    def _short_set(self, s: Optional[str]) -> Optional[str]:
        if not s:
            return s
        return "|".join(sorted(set(s.split("|"))))

    def get_tevis_caldiv(self, calendar: str, year, week) -> dict:
        url = f"{self.BASE_URL}/caldiv?cal={calendar}&cnc=0&cncdata=&week={year:04d}{week:02d}&json=1&offset=1"
        return self.get_json(url)

    def get_tevis_location_calendar(self, mdt: str, cnc_ids: Iterable[str]) -> str:
        query = {
            "mdt": mdt,
            "select_cnc": 1,
        }
        # select first 'concern'
        for i, id in enumerate(cnc_ids):
            query[f"cnc-{id}"] = 1 if i == 0 else 0

        html = self.get_url(f"{self.BASE_URL}/calendar", data=query)

        try:
            idx = html.index("window.tevis = window.tevis || {")
        except ValueError:
            # some locations required registration before showing the calendar
            if "Eingabe der persönlichen Daten für den Termin" in html:
                return "0"
            if "Der ausgewählte Kalender existiert nicht oder kann nicht ausgewählt werden." in html:
                return "0"

            print(html)
            raise ValueError(f"Missing tevis script data for mdt '{mdt}'")
        script = html[idx+31:]
        script = script[:script.index("$(document).ready(")]

        cal = script[script.index("calendar:")+9:]
        cal = cal[:cal.index(",")].strip()

        return cal
