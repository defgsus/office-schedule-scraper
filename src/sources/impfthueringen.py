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
    NAME = "Impftermin Thüringen"

    BASE_URL = "https://www.impfen-thueringen.de/terminvergabe"

    @classmethod
    def _convert_snapshot(
            cls,
            dt: datetime.datetime,
            data: Union[dict, list],
            as_datetime: bool = False,
    ) -> Optional[List[dict]]:
        ret_data = []
        for row in data:
            ret_data.append({
                "location_id": cls.to_id(row["loc"]),
                "location_name": row["loc_name"],
                "dates": [
                    (
                        datetime.datetime.strptime(d[0], "%Y-%m-%d %H:%M")
                        if as_datetime else d[0] + ":00"
                    )
                    for d in row["dates"]
                ]
            })
        return ret_data

    @classmethod
    def _convert_snapshot_meta(cls, data: Union[dict, list]) -> dict:
        #print(json.dumps(data, indent=2))
        #exit()
        ret = {}
        for loc in data:
            ret[loc["loc"]] = {
                "name": loc["loc_name"]
            }
        return ret

    @classmethod
    def make_export_table(cls, data_list: List[Tuple[datetime.datetime, dict]], all_dates: List[str]):
        """
        Compress the free dates to 15 minutes snapshots because of the
        enormous amount of data
        """
        date_dict = {}
        for dt, locations in data_list:
            dt = dt.replace(minute=(dt.minute // 15) * 15, second=0, microsecond=0)
            for loc in locations:
                key = (dt, loc["source_id"], loc["location_id"])
                if key not in date_dict:
                    date_dict[key] = set()
                for d in loc["dates"]:
                    date_dict[key].add(d)

        rows = []
        for (dt, source_id, location_id), dates in date_dict.items():
            rows.append(
                [
                    dt,
                    source_id,
                    location_id,
                ] + [
                    "1" if date in dates else ""
                    for date in all_dates
                ]
            )
        return rows

    @classmethod
    def compare_snapshot_location(
            cls,
            prev_timestamp: datetime.datetime, prev_data: dict,
            timestamp: datetime.datetime, data: dict,
            working_data: dict,
    ) -> Tuple[set, set, bool]:
        appointments = set()
        cancellations = set()
        bookings = working_data

        for d, pd in zip(data["dates"], prev_data["dates"]):

            # a date on the website means it's free
            if bookings.get("d") == "booked":
                cancellations.add(d)
            bookings[d] = "free"

            # if the date is larger than the previous one, the previous one is booked
            if d > pd:
                appointments.add(pd)
                bookings[pd] = "booked"

        return appointments, cancellations, prev_data != data

    @classmethod
    def compare_snapshot_location_NAIVE(
            cls,
            prev_timestamp: datetime.datetime, prev_data: dict,
            timestamp: datetime.datetime, data: dict,
            working_data: dict,
    ) -> Tuple[set, set]:
        sorted_prev_dates = sorted(prev_data["dates"])
        sorted_dates = sorted(data["dates"])

        appointments, cancellations = set(), set()

        if sorted_dates[0] < sorted_prev_dates[0]:
            d = sorted_prev_dates[0]
            while d > sorted_dates[0]:
                if cls.is_business_hour(d):
                    cancellations.add(d)
                d -= datetime.timedelta(minutes=3)

        elif sorted_dates[0] > sorted_prev_dates[0]:
            d = sorted_prev_dates[0]
            while d < sorted_dates[0]:
                if d > timestamp and cls.is_business_hour(d):
                    appointments.add(d)
                d += datetime.timedelta(minutes=3)

        return appointments, cancellations

    @classmethod
    def is_business_hour(cls, dt: datetime.datetime) -> bool:
        weekday = dt.isoweekday()
        if weekday in (6, 7):
            return False
        if not 8 <= dt.hour <= 16:
            return False
        return True

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
