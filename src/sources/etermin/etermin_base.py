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

    @classmethod
    def convert_snapshot(cls, data: Union[dict, list]) -> List[dict]:
        ret_data = []
        for cal in data["calendars"]:
            ret_data.append({
                "location_id": cal["id"],
                "location_name": cal["name"],
                "dates": [datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in cal["dates"]],
            })
        return ret_data

    def make_snapshot(self):
        services = self.et_get_services()

        ret_data = {
            "services": [],
            "calendars": [],
        }
        groups = dict()

        for s in services:
            if s.get("s"):
                group_id, service_id, name = s["sgid"], s["sid"], s["s"]
                duration = s.get("duration")
                ret_data["services"].append({
                    "group_id": group_id,
                    "service_id": service_id,
                    "name": name,
                    "duration": duration,
                })
                # pick service with smallest duration per group
                if duration:
                    if group_id not in groups or duration < groups[group_id]["duration"]:
                        groups[group_id] = {"duration": duration, "service_id": service_id}

        now = self.now()

        calendars_retrieved = set()
        calendar_timeslots = dict()

        for group_id, group in groups.items():
            cals = self.et_get_calendar_list(group["service_id"])
            for cal in cals:
                if cal["calendarid"] not in calendars_retrieved:
                    cal_data = {
                        "group_id": group_id,
                        "name": cal["calendarname"],
                        "service_id": group["service_id"],
                        "duration": group["duration"],
                    }

                    timeslot_days = self.et_get_time_slot_days(
                        date=now.date(),
                        calendar_id=cal["calendarid"], service_id=group["service_id"],
                        duration=group["duration"]
                    )
                    for day in timeslot_days:
                        if day.get("available"):
                            timeslots = self.et_get_time_slots(
                                date=day["start"][:10],
                                calendar_id=cal["calendarid"], service_id=group["service_id"],
                                duration=group["duration"]
                            )
                            for ts in timeslots:
                                if ts["calendarid"] not in calendar_timeslots:
                                    calendar_timeslots[ts["calendarid"]] = {
                                        "name": ts["calendarname"],
                                        "dates": set(),
                                    }
                                calendar_timeslots[ts["calendarid"]]["dates"].add(
                                    ts["start"]
                                )
                                # print(ts["start"], ts["cap"], ts["available"], ts["f"], ts["calendarid"])

        ret_data["calendars"] = [
            {
                "id": calendar_id,
                "name": cal["name"],
                "dates": sorted(cal["dates"]),
            }
            for calendar_id, cal in calendar_timeslots.items()
        ]

        return ret_data

    def et_get_settings(self) -> dict:
        return self.get_json(
            f"{self.BASE_URL}/api/settingbs?t=",
        )

    def et_get_services(self) -> List[dict]:
        return self.get_json(
            f"{self.BASE_URL}/api/servicegroupservice?cache=1&w={self.et_id()}&vlang=de",
        )

    def et_get_calendar_list(self, service_id) -> List[dict]:
        return self.get_json(
            f"{self.BASE_URL}/api/calendar?availablecal=1&lang=de&serviceid={service_id}&calendarid=undefined",
        )

    def et_get_time_slot_days(self, date: datetime.date, calendar_id: str, service_id: str, duration: int) -> List[dict]:
        return self.get_json(
            f"{self.BASE_URL}/api/timeslots?date={date}&serviceid={service_id}&rangesearch=1&caching=false&capacity="
            f"&duration={duration}&cluster=false&slottype=0&fillcalendarstrategy=0&showavcap=true"
            f"&appfuture={self.num_weeks*7}&appdeadline=0&appdeadlinewm=0&msdcm=0&calendarid={calendar_id}"
        )

    def et_get_time_slots(self, date: datetime.date, calendar_id: str, service_id: str, duration: int) -> List[dict]:
        return self.get_json(
            f"{self.BASE_URL}/api/timeslots?date={date}&serviceid={service_id}&capacity=1&caching=false"
            f"&duration={duration}&cluster=false&slottype=0&fillcalendarstrategy=0&showavcap=true&appfuture=14"
            f"&appdeadline=0&msdcm=0&appdeadlinewm=0&tz=W.%20Europe%20Standard%20Time&tzaccount=W.%20Europe%20Standard%20Time"
            f"&calendarid={calendar_id}"
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
            "Host": "www.etermin.net",
            "Cache-Control": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            "Referer": f"https://www.etermin.net/{self.ET_URL}",
            "webid": self.et_id(),
        })
        return super().get_json(url, method, data=data, headers=headers, encoding=encoding)
