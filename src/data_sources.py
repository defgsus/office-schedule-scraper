import fnmatch
import json
import datetime
import os
import traceback
from multiprocessing.pool import Pool
from pathlib import Path
from typing import Generator, Optional, List, Type, Union

from .sources.base import installed_sources, SourceBase, ScraperError


class DataSources:

    def __init__(
            self,
            use_cache: bool = False,
            include: Optional[Union[str, List[str]]] = None,
            exclude: Optional[Union[str, List[str]]] = None,
            include_type: Optional[str] = None,
            date_from: Optional[str] = None,
            date_to: Optional[str] = None,
    ):
        self.use_cache = use_cache
        self.include = include
        self.exclude = exclude
        self.include_type = include_type
        self.date_from = date_from
        self.date_to = date_to

        self.source_classes: List[Type[SourceBase]] = []
        for cls in installed_sources.values():
            if exclude and (_string_filter(cls.ID, exclude) or _string_filter(cls.NAME, exclude)):
                continue
            if include and not _string_filter(cls.ID, include) and not _string_filter(cls.NAME, include):
                continue
            if include_type and not _string_filter(cls.SCRAPER_TYPE, include_type):
                continue
            
            if cls.NEEDS_INCLUDE and not (include or include_type):
                continue

            self.source_classes.append(cls)

        self.source_classes.sort(key=lambda s: s.ID)

    @classmethod
    def create(cls, source_id: str, num_weeks: int = 4, use_cache: bool = False) -> SourceBase:
        return installed_sources[source_id](
            num_weeks=num_weeks, use_cache=use_cache
        )

    def sources(self, num_weeks: int = 4) -> List[SourceBase]:
        return [
            c(use_cache=self.use_cache, num_weeks=num_weeks)
            for c in self.source_classes
        ]

    def dump_list(self):
        import pandas as pd
        rows = []
        for i, s in enumerate(self.source_classes):
            url = s.index_url()
            url_split = url.split("/")
            final_part = url_split[-1]
            if len(url_split) > 3 and "." in final_part or "?" in final_part:
                short_url = url[:-len(final_part)] + "..."
            else:
                if not url.endswith("/"):
                    url += "/"
                short_url = url

            if short_url.startswith("http://"):
                short_url = short_url[7:]
            elif short_url.startswith("https://"):
                short_url = short_url[8:]

            rows.append({
                "index": i+1,
                "name": s.NAME,
                "scraper": s.SCRAPER_TYPE,
                "url": f"[{short_url}]({url})",
            })
        df = (
            pd.DataFrame(rows)
            .set_index("index")
            .sort_values("name")
        )
        print(df.to_markdown(index=False))
        print(len(df))

    def dump_snapshot(self, num_weeks: int = 4):
        for s in self.sources(num_weeks=num_weeks):
            try:
                data = s.make_snapshot()
            except:
                print(f"\nERROR IN {s.ID}\n")
                raise
            print(f"---------- {s.ID} ----------")
            print(json.dumps(data, indent=2))

    def dump_snapshot_table(self, num_weeks: int = 4):
        import pandas as pd
        import numpy as np

        dic = dict()
        for s in self.sources(num_weeks=num_weeks):
            data = s.make_snapshot()
            data = s.convert_snapshot(datetime.datetime.now(), data)
            for loc in data:
                for d in loc["dates"]:
                    if d not in dic:
                        dic[d] = dict()
                    dic[d][s.ID + "|" + loc["location_id"]] = "X"
        df = (
            pd.DataFrame(dic).transpose().sort_index()
            .replace({np.nan: ""})
        )
        print(df.to_markdown())

    def dump_snapshot_tables(self):
        import pandas as pd
        import numpy as np

        dic = dict()
        for s in self.sources():

            for dt, _, data in s.iter_snapshot_data(
                    date_from=self.date_from, date_to=self.date_to, with_unchanged=False
            ):
                data = s.convert_snapshot(dt, data)
                for loc in data:
                    for d in loc["dates"]:
                        if d not in dic:
                            dic[d] = dict()
                        dic[d][s.ID + "|" + loc["location_id"][:10]] = "X"

                df = (
                    pd.DataFrame(dic).transpose().sort_index()
                        .replace({np.nan: ""})
                )
                print("\n")
                print(s.ID, "@", dt)
                print(df.to_markdown())

    def dump_snapshot_dates(self):
        import pandas as pd
        rows = []
        for s in self.sources():
            for dt, fn in s.iter_snapshot_filenames(date_from=self.date_from, date_to=self.date_to):
                rows.append({"date": dt, "source_id": s.ID})
        df = pd.DataFrame(rows)
        df = df.sort_values("date").set_index("date")
        print(df.to_string())

    def make_snapshot(self, num_weeks: int = 4, processes: int = 1):
        sources = self.sources(num_weeks=num_weeks)

        if processes <= 1:
            for s in sources:
                self._make_and_store_snapshot(s)
        else:
            source_groups = dict()
            group_indices = dict()
            for s in sources:
                if not s.MULTI_PROCESS_GROUP:
                    source_groups[s.ID] = [s]
                else:
                    group_id = s.MULTI_PROCESS_GROUP

                    if s.MULTI_PROCESS_MAX:
                        group_idx = group_indices.get(s.MULTI_PROCESS_GROUP, 0)
                        group_id = f"{group_id}-{group_idx}"
                        group_indices[s.MULTI_PROCESS_GROUP] = (group_idx + 1) % s.MULTI_PROCESS_MAX

                    source_groups.setdefault(group_id, []).append(s)
            
            #for key, value in source_groups.items():
            #    print(key, value)
            pool = Pool(processes)
            pool.map(self._make_and_store_snapshot, list(source_groups.values()))

    def _make_and_store_snapshot(self, sources: Union[SourceBase, List[SourceBase]]):
        if not isinstance(sources, list):
            sources = [sources]

        for s in sources:
            error = False
            try:
                data = s.make_snapshot()
            except Exception as e:
                print(f"ERROR: {type(e).__name__}: {e}")
                data = {
                    "class": type(e).__name__,
                    "message": str(e),
                    "stacktrace": traceback.format_exc(limit=3),
                }
                if hasattr(e, "data") and isinstance(e.data, dict):
                    data.update(e.data)
                error = True

            self._store_snapshot(s, data, error)

    def _store_snapshot(self, s: SourceBase, data: dict, error: bool = False):
        now = datetime.datetime.now()

        snapshot_dir = (SourceBase.SNAPSHOT_DIR if not error else SourceBase.ERROR_DIR) / s.ID / now.strftime("%Y-%m")
        os.makedirs(snapshot_dir, exist_ok=True)

        # save some disk space
        filename = snapshot_dir / now.strftime("%Y-%m-%d-%H-%M-%S.json")
        if self._is_same_data(data, snapshot_dir):
            print(f"{s.ID}: unchanged")
            data = {}
            filename = snapshot_dir / now.strftime("%Y-%m-%d-%H-%M-%S-unchanged.json")

        print(f"writing {filename}")
        with open(filename, "w") as fp:
            json.dump(data, fp, cls=JsonEncoder)

    def _is_same_data(self, data: dict, path: Path) -> bool:
        files = sorted(filter(
            lambda n: "unchanged" not in str(n),
            path.glob("*.json")
        ))
        if not files:
            return False

        file = files[-1]
        # print("comparing against", file)
        with open(str(file)) as fp:
            unchanged = data == json.load(fp)
            # if unchanged:
            #     print("SAMES AS", file)
            return unchanged

    def dump_snapshot_status(self):
        df = self.get_snapshot_status()
        print(df.to_string(max_rows=df.shape[0]))#, max_cols=df.shape[1]))

    def get_snapshot_status(self):
        import pandas as pd
        sources = self.sources()
        rows = []
        for s in sources:
            num_snapshots = 0
            num_unchanged_snapshots = 0
            num_errors = len(list(s.iter_error_filenames(date_from=self.date_from, date_to=self.date_to)))

            for dt, fn in s.iter_snapshot_filenames(date_from=self.date_from, date_to=self.date_to):
                num_snapshots += 1
                unchanged = "-unchanged.json" in str(fn)
                if unchanged:
                    num_unchanged_snapshots += 1

            num_changed = num_snapshots - num_unchanged_snapshots
            num_changed_p = num_changed / max(num_snapshots, 1) * 100
            num_changed_p = f"{num_changed_p:.2f}%"
            rows.append({
                "source_id": s.ID,
                "scraper": s.SCRAPER_TYPE,
                "snapshots": num_snapshots,
                "changed": num_changed,
                "changed %": num_changed_p,
                "errors": num_errors,
            })
        df = pd.DataFrame(rows).set_index("source_id").sort_index()
        return df

    def dump_convert_snapshots(self):
        data = self.convert_snapshots()
        print(json.dumps(data, indent=2, cls=JsonEncoder))

    def dump_convert_snapshots_meta(self, with_unchanged: bool = False):
        from tqdm import tqdm
        sources = self.sources()
        for s in tqdm(sources):
            for dt, unchanged, snapshot_data in s.iter_snapshot_data(
                    date_from=self.date_from, date_to=self.date_to,
                    with_unchanged=with_unchanged
            ):
                try:
                    data = s.convert_snapshot_meta(snapshot_data)
                except Exception as e:
                    print(f"\nERROR in {s.ID} @ {dt}")
                    print(snapshot_data)
                    raise

                print(f"\nSNAPSHOT META {s.ID} @ {dt}")
                print(json.dumps(data, indent=2))

    def convert_snapshots(
            self,
            with_unchanged: bool = False,
            with_invalid: bool = False,
    ) -> dict:
        from tqdm import tqdm

        sources = self.sources()
        sources_data = {s.ID: None for s in sources}
        for s in tqdm(sources):
            for dt, unchanged, snapshot_data in s.iter_snapshot_data(
                    date_from=self.date_from, date_to=self.date_to,
                    with_unchanged=with_unchanged
            ):
                try:
                    data = self.convert_snapshot(s, dt, snapshot_data)
                except Exception as e:
                    print(f"\nERROR in {s.ID} @ {dt}")
                    print(snapshot_data)
                    raise

                if data is None and not with_invalid:
                    continue

                if sources_data[s.ID] is None:
                    sources_data[s.ID] = []
                sources_data[s.ID].append({
                    "date": dt,
                    "source_id": s.ID,
                    "snapshot_date": dt,
                    "unchanged": unchanged,
                    "valid": data is not None,
                    "data": data,
                })

        return sources_data

    def dump_snapshot_changes(self, with_zeros: bool = True, resample: Optional[str] = None):
        import pandas as pd
        changes = self.get_snapshot_changes(with_zeros=with_zeros)
        df = pd.DataFrame(changes).set_index("date")

        for source_id in sorted(df["source_id"].unique()):
            for loc_name in sorted(df["location_name"].unique()):
                df2 = df[df["source_id"] == source_id]
                df2 = df2[df2["location_name"] == loc_name]
                if resample:
                    df2 = df2.resample(resample).sum()
                    df2 = pd.DataFrame({
                        "date": df2.index,
                        #"source_id": source_id,
                        #"location_id": df2["location_id"],
                        #"location_name": loc_name,
                        "appointments": df2["appointments"],
                        "cancellations": df2["cancellations"],
                        "changed": df2["changed"],
                    }).set_index("date")
                if df2.shape[0] > 1:
                    print("\n---------", source_id, "|", loc_name, "---------\n")
                    df2.drop(["location_name", "location_id", "source_id"], inplace=True, axis=1, errors="ignore")
                    print(df2.to_string(max_rows=max(1, df.shape[0])))

    def get_snapshot_changes(self, days_ahead: int = 0, with_zeros: bool = False):
        from tqdm import tqdm

        sources = self.sources()
        working_data = {}
        ret_data = []
        for s in tqdm(sources):
            prev_locations = dict()
            for idx, (dt, unchanged, snapshot_data) in enumerate(s.iter_snapshot_data(
                    date_from=self.date_from, date_to=self.date_to,
                    with_unchanged=False
            )):
                try:
                    data = self.convert_snapshot(s, dt, snapshot_data)
                except Exception as e:
                    new_e = e.__class__(f"in {s.ID}@{dt}: {e}")
                    new_e.__traceback__ = e.__traceback__
                    raise new_e

                if data is None:
                    continue

                dt_day = dt.replace(hour=0, minute=0)
                for location in data:
                    loc_id = location["location_id"]

                    if days_ahead:
                        location["dates"] = filter(
                            lambda d: (d.replace(hour=0, minute=0) - dt_day).days <= days_ahead,
                            location["dates"],
                        )
                    location["dates"] = set(location["dates"])

                    if len(location["dates"]) == 0:
                        continue

                    appointments = set()
                    cancellations = set()
                    has_changed = False

                    if loc_id in prev_locations:
                        if loc_id not in working_data:
                            working_data[loc_id] = {}

                        prev_date, prev_location = prev_locations[loc_id]

                        appointments, cancellations, has_changed = s.compare_snapshot_location(
                            prev_date, prev_location, dt, location, working_data[loc_id],
                        )

                    prev_locations[loc_id] = (dt, location)

                    if idx == 0 or with_zeros or appointments or cancellations or has_changed:
                        ret_data.append({
                            "source_id": s.ID,
                            "office_id": location["office_id"],
                            "location_id": location["location_id"],
                            "location_name": location["location_name"],
                            "date": dt,
                            "free_dates": len(location["dates"]),
                            "appointments": len(appointments),
                            "cancellations": len(cancellations),
                            "changed": 1 if has_changed else 0,
                            #"appointments_s": str(appointments),
                            "min_free": sorted(location['dates'])[0],
                            "max_free": sorted(location['dates'])[-1],
                        })
        return ret_data

    def convert_snapshot(self, s: SourceBase, dt: datetime.datetime, snapshot_data: Union[dict, list]) -> Optional[List[dict]]:
        data = s.convert_snapshot(dt, snapshot_data, as_datetime=True)
        if data is None:
            return data
        return data

    def dump_changes_status(self):
        import pandas as pd
        changes = (
            pd.DataFrame(self.get_snapshot_changes())
            .set_index("source_id")#, "location_id"])
            .groupby("source_id").sum()
            .to_dict()
        )

        rows = []
        for s in self.sources():
            num_snapshots = 0
            num_unchanged_snapshots = 0
            num_errors = len(list(s.iter_error_filenames(date_from=self.date_from, date_to=self.date_to)))

            min_date = None
            max_date = None
            for dt, fn in s.iter_snapshot_filenames(date_from=self.date_from, date_to=self.date_to):
                if min_date is None:
                    min_date = max_date = dt
                max_date = max(max_date, dt)
                num_snapshots += 1
                unchanged = "-unchanged.json" in str(fn)
                if unchanged:
                    num_unchanged_snapshots += 1

            num_changed = num_snapshots - num_unchanged_snapshots
            num_changed_p = round(num_changed / max(num_snapshots, 1) * 100, 2)

            rows.append({
                "source_id": s.ID,
                "scraper": s.SCRAPER_TYPE,
                "snapshots": num_snapshots,
                "unchanged": num_unchanged_snapshots,
                "changed %": num_changed_p,
                "errors": num_errors,
                "appointments": changes["appointments"].get(s.ID, 0),
                "cancellations": changes["cancellations"].get(s.ID, 0),
                "first snapshot": min_date,
                "last snapshot": max_date,
            })

        df = pd.DataFrame(rows)
        # print(df.to_string(max_rows=df.shape[0]))#, max_cols=df.shape[1]))
        print(df.to_markdown())


class JsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        try:
            return super().default(o)
        except Exception:
            print("X", type(o))
            raise


def _string_filter(s: str, filter: Optional[Union[str, List[str]]]):
    if not filter:
        return True
    if isinstance(filter, str):
        filter = [filter]
    for f in filter:
        if fnmatch.fnmatchcase(s, f):
            return True
    return False
