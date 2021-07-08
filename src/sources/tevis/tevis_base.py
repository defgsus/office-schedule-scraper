from ..base import *


class TevisBaseScraper(SourceBase):
    """
    Unified code to scrape all "tevis" pages.

    Need to subclass and define class-attribute BASE_URL (w/o trailing slash).

    Tevis seems to be a software by "Kummunix GmbH" https://www.kommunix.de/produkte/tevis/.

    The list of references is here: https://www.kommunix.de/referenzen/
    """
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
                #print(data)
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
            #print(form)
            cnc.append({
                "mdt": form.find("input", {"name": "mdt"}).get("value"),
                "calendar": form.find("input", {"class": "cnc-item"}).get("data-tevis-calendars"),
                "title": form.find("a").text.strip(),
            })

        if not cnc:
            for i in soup.find_all("input", {"class": "cnc-item"}):
                data = {
                    "calendar": i.get("data-tevis-calendars"),
                }
                a = i.parent.parent.find("a", {"data-html": "true"})
                if a:
                    data["name"] = a.text.strip()

                cnc.append(data)

        return cnc

    def get_tevis_caldiv(self, calendar: str, year, week) -> dict:
        url = f"{self.BASE_URL}/caldiv?cal={calendar}&cnc=0&cncdata=&week={year:04d}{week:02d}&json=1&offset=1"
        return self.get_json(url)
