from ..base import *


class ETerminBase(SourceBase):
    """
    Unified code to scrape all "www.etermin.net" pages.

    Need to subclass and define class-attribute ET_ID
    """
    SCRAPER_TYPE = "etermin"
    MULTI_PROCESS_GROUP = "etermin"

    BASE_URL = "https://www.etermin.net"
    ET_URL = None

    @classmethod
    def index_url(cls) -> str:
        return f"{cls.BASE_URL}/{cls.ET_URL}"

    @classmethod
    def et_id(cls) -> str:
        return cls.ET_URL.lower()

    def make_snapshot(self):
        services = self.ek_get_services()

        for s in services:
            print(s["sgid"], s["sid"], s["s"])

    def ek_get_settings(self) -> dict:
        return self.get_json(
            f"{self.BASE_URL}/api/settingbs?t=",
            headers={
                "Referer": f"https://www.etermin.net/{self.ET_URL}",
                "webid": self.et_id(),
            }
        )

    def ek_get_services(self) -> List[dict]:
        return self.get_json(
            f"{self.BASE_URL}/api/servicegroupservice?cache=1&w={self.et_id()}&vlang=de",
            headers={
                "Referer": f"https://www.etermin.net/{self.ET_URL}",
                "webid": self.et_id(),
            }
        )

    def ek_get_calendar_list(self, service_id) -> List[dict]:
        return self.get_json(
            f"{self.BASE_URL}/api/calendar?availablecal=1&lang=de&serviceid={service_id}&calendarid=undefined",
            headers={
                "Referer": f"https://www.etermin.net/{self.ET_URL}",
                "webid": self.et_id(),
            }
        )

    def get_json(self, url, method="GET", data=None, headers=None, encoding=None) -> Union[list, dict]:
        if not headers:
            headers = {}
        headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Accept": "application/json, text/plain",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Pragma": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            #"Referer": f"https://www.etermin.net/{url_part}",
            "Host": "www.etermin.net",
            "Cache-Control": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            #"webid": url_part.lower(),
        })
        return super().get_json(url, method, data=data, headers=headers, encoding=encoding)

