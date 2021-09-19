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
    def _convert_snapshot(
            cls,
            dt: datetime.datetime,
            data: Union[dict, list],
            as_datetime: bool = False,
    ) -> Optional[List[dict]]:
        if not data["cnc"]:
            return None

        cal_id_2_name = dict()
        for c in data["cnc"]:
            if c.get("calendar"):
                for c_id in c["calendar"].split("|"):
                    if not c.get("md"):
                        # old snapshot version before adding md
                        cal_id_2_name[c_id] = c.get("title", c_id)
                    else:
                        name = data["md"][c["md"]]
                        if c_id not in cal_id_2_name:
                            cal_id_2_name[c_id] = f"{name} / {c.get('title')}"

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
                        date = start_date + datetime.timedelta(minutes=int(minutes))
                        dates.append(date if as_datetime else str(date))

            ret_data.append({
                "location_id": cal_id,
                "location_name": cal_id_2_name.get(cal_id, cal_id),
                "dates": dates,
            })
        return ret_data

    def make_snapshot(self):
        now = self.now()

        md_ids = self.get_tevis_md()

        ret_data = {
            "v": 2,  # v2: fixed selection of location
            "md": md_ids,
            "cnc": [],
            "calendar": dict(),
        }

        for md, title in md_ids.items():
            cnc_items = self.get_tevis_cnc(md)
            ret_data["cnc"] += cnc_items

            calendars = dict()

            for cnc in cnc_items:
                if cnc.get("calendar"):
                    for c in cnc["calendar"].split("|"):
                        if c not in calendars:
                            calendars[c] = (cnc["mdt"], cnc["cnc"])
                else:
                    calendars[f"mdt-{cnc['mdt']}"] = (cnc["mdt"], cnc["cnc"])

            for cal_id, (cal_mdt, cal_cnc) in calendars.items():
                if cal_id == "0":
                    continue

                update_mdt = True
                if cal_id.startswith("mdt-"):
                    # we got no calendar value, see if it's embedded in the page
                    cal_id = self.get_tevis_location_calendar(cal_mdt, cal_cnc)
                    update_mdt = False

                for i in range(self.num_weeks):
                    year, week, _ = (now + datetime.timedelta(days=7 * i)).isocalendar()
                    data = self.get_tevis_caldiv(
                        cal_id, cal_mdt, cal_cnc, year, week,
                        update_mdt=update_mdt and i == 0
                    )
                    if data:
                        data.pop("html", None)
                        #print(json.dumps(data, indent=2))
                        #exit()
                        if cal_id not in ret_data["calendar"]:
                            ret_data["calendar"][cal_id] = []
                        ret_data["calendar"][cal_id].append(data)

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
                "cnc": cnc_item.get("name"),
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
                    "cnc": i.get("name"),
                    #"cnc_id": i.get("data-tevis-cncid"),
                    "calendar": i.get("data-tevis-calendars"),
                    "location": self._short_set(i.get("data-tevis-locations")),
                }
                a = i.parent.parent.find("a", {"data-html": "true"})
                if a:
                    data["name"] = a.text.strip()
                else:
                    if i.get("data-tevis-cncname"):
                        data["name"] = i.get("data-tevis-cncname")

                cnc.append(data)

        return cnc

    def _short_set(self, s: Optional[str]) -> Optional[str]:
        if not s:
            return s
        return "|".join(sorted(set(s.split("|"))))

    def get_tevis_caldiv(
            self, calendar: str, mdt: str, cnc: str, year: int, week: int, update_mdt: bool
    ) -> Optional[dict]:
        if update_mdt:
            url = f"{self.BASE_URL}/calendar?mdt={mdt}&select_cnc=1&{cnc}=1"
            self.get_url(url)

        url = f"{self.BASE_URL}/caldiv?cal={calendar}&cnc=0&cncdata=&week={year:04d}{week:02d}&json=1&offset=1"
        try:
            return self.get_json(url)
        except ScraperError as e:
            if "JSONDecodeError" in str(e):
                print(f"TEVIS JSON DECODE ERROR for {url}")
                return None
            raise

    def get_tevis_location_calendar(self, mdt: str, cnc: Iterable[str]) -> str:
        url = f"{self.BASE_URL}/calendar?mdt={mdt}&select_cnc=1&{cnc}=1"
        html = self.get_url(url)

        try:
            idx = html.index("window.tevis = window.tevis || {")
        except ValueError:
            # some locations require registration before showing the calendar
            if "Eingabe der persönlichen Daten für den Termin" in html:
                return "0"
            if "Der ausgewählte Kalender existiert nicht oder kann nicht ausgewählt werden." in html:
                return "0"
            if ("Kein gültiger Mandant gefunden" in html or "Es wurde kein Mandantor empfangen" in html):
                print("TEVIS SESSION ERROR or something")
                return "0"
            if "Es ist ein Datenbank-Fehler aufgetreten" in html:
                print("TEVIS DATABASE ERROR")
                return "0"
            print(html)
            raise ValueError(f"Missing tevis script data for mdt '{mdt}'")
        script = html[idx+31:]
        script = script[:script.index("$(document).ready(")]

        cal = script[script.index("calendar:")+9:]
        cal = cal[:cal.index(",")].strip()

        return cal
