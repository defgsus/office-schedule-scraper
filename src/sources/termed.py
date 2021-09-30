import json
from tqdm import tqdm
from .base import *


class Termed(SourceBase):
    """
    TerMed by Facharzt-Sofort-GmbH.

    It's an enormous amount of data. Downloading one snapshot takes
    already 15 minutes and results in 5mb of json. :((

    """
    ID = "termed"
    NAME = "TerMed"
    BASE_URL = "https://www.termed.de"
    NEEDS_INCLUDE = True  # this scraper is not part of official package

    DROP_IDS = {
        "3209",  # Max Mustermann
        # probably test for Radiologisches Zentrum Wiesloch
        "3662", "3663", "3664", "3666", "3662", "3668", "3669",
        # probably test accounts for DEGEDI Pro Physio GmbH
        "3697", "3699", "3700", "3701", "3702", "3703", "3704"
    }

    @classmethod
    def index_url(cls) -> str:
        return cls.BASE_URL

    @classmethod
    def _convert_snapshot(
            cls,
            dt: datetime.datetime,
            data: Union[dict, list],
            as_datetime: bool = False,
    ) -> Optional[List[dict]]:
        ret_data = []
        dates_dict = dict()
        for loc in tqdm(data):
            loc_id = loc["location_id"]
            if isinstance(loc["dates"], list):
                dates = loc["dates"]
                if as_datetime:
                    dates = [datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates]
                dates_dict[loc_id] = dates
            else:
                dates = dates_dict[loc["dates"]["eq"]]

            ret_data.append({
                "location_id": loc_id,
                "location_name": loc["location_id"],
                "dates": dates,
            })
        return ret_data

    def make_snapshot(self):
        locations = self.get_locations()

        #print(json.dumps(locations, indent=2))
        #print(len(locations))
        #exit()

        now = datetime.datetime.now()
        ret_data = []
        for loc in tqdm(locations, desc=self.NAME):
            if loc.get("treatment_reasons"):
                treatment_dates = {}
                for treatment in loc["treatment_reasons"]:
                    loc_tr_id = f"{loc['id']}-{treatment['id']}"
                    dates = self.get_dates(now, loc["id"], treatment["id"])
                    if dates is not None:

                        # just store that this is a copy of another calendar to save space
                        for other_loc_tr_id, other_dates in treatment_dates.items():
                            if other_dates == dates:
                                dates = {"eq": other_loc_tr_id}
                                break

                        if isinstance(dates, list):
                            treatment_dates[loc_tr_id] = dates

                        name = loc["scraped_name"]
                        if treatment.get("reason"):
                            name += " - " + treatment["reason"]
                        ret_data.append({
                            "location_id": loc_tr_id,
                            # "location_name": name,
                            "dates": dates,
                        })
                        #print(ret_data[-1]["location_name"])
                        #print(len(ret_data[-1]["dates"]))
            else:
                dates = self.get_dates(now, loc["id"])
                if dates is not None:
                    ret_data.append({
                        "location_id": loc["id"],
                        # "location_name": loc["scraped_name"],
                        "dates": dates,
                    })
                    #print(ret_data[-1]["location_name"])
                    #print(len(ret_data[-1]["dates"]))

        return ret_data

    def get_locations(self):
        locations = []
        for i in range(0, 4000):
            if str(i) in self.DROP_IDS:
                continue
            loc = self.get_location(i)
            if loc.get("id"):
                names = (loc.get("praxis") or "") + " " + (loc.get("name") or "")
                if "Test" in names and not "Testzentrum" in names:
                    continue
                if "@termed.de" in (loc.get("email") or ""):
                    continue
                if "termed.de" in (loc.get("url") or ""):
                    continue

                name = []
                if loc.get("name"):
                    name.append(loc["name"])
                if loc.get("surname"):
                    name.append(loc["surname"])
                if loc.get("praxis"):
                    if name:
                        name.append("-")
                    name.append(loc["praxis"])

                loc["scraped_name"] = " ".join(name)

                locations.append(loc)

        return locations

    def get_location(self, loc_id: int):
        cache_dir = self.get_cache_dir() / "locations"
        cache_filename = cache_dir / f"{loc_id}.json"
        if cache_filename.exists():
            return json.loads(cache_filename.read_text())

        url = f"https://api.termed.de/v2/public/doc/{loc_id}"
        data = self.get_json(url)

        os.makedirs(cache_dir, exist_ok=True)
        cache_filename.write_text(json.dumps(data))
        return data

    def get_dates(
            self,
            start_date: datetime.datetime,
            loc_id: int,
            treatment_id: Optional[int] = None
    ) -> Optional[List[str]]:
        ts = int(start_date.timestamp())
        # ts = int(datetime.datetime(2021, 9, 28, 22, 0, 0).timestamp())
        ts_end = ts + 60 * 60 * 24 * 7 * self.num_weeks

        url = f"https://api.termed.de/v2/public/doc/{loc_id}/events/open/10/{ts}/{ts_end}"
        if treatment_id:
            url += f"/{treatment_id}"
        try:
            data = self.get_json(url)
            return [
                e["start"]
                for e in data
            ]
        except Exception as e:
            print(f"ERROR {url}: {type(e).__name__}: {e}")
