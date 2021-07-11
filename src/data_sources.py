import fnmatch
import json
import datetime
import os
import traceback
from multiprocessing.pool import Pool
from pathlib import Path
from typing import Generator, Optional, List, Type, Union

from tqdm import tqdm

from .sources.base import installed_sources, SourceBase, ScraperError


class DataSources:

    def __init__(
            self,
            use_cache: bool = False,
            include: Optional[str] = None,
            exclude: Optional[str] = None,
    ):
        self.use_cache = use_cache
        self.include = include
        self.exclude = exclude

        self.source_classes: List[Type[SourceBase]] = []
        for name, cls in installed_sources.items():
            if exclude and fnmatch.fnmatchcase(name, exclude):
                continue
            if include and not fnmatch.fnmatchcase(name, include):
                continue

            self.source_classes.append(cls)

        self.source_classes.sort(key=lambda s: s.ID)

    def dump_list(self):
        max_id_len = max(len(s.ID) for s in self.source_classes)
        max_type_len = max(len(s.SCRAPER_TYPE) for s in self.source_classes)
        for i, s in enumerate(self.source_classes):
            print(f"{i+1:3} {s.SCRAPER_TYPE:{max_type_len}} {s.ID:{max_id_len}}")

    def sources(self, num_weeks: int = 4):
        return [
            c(use_cache=self.use_cache, num_weeks=num_weeks)
            for c in self.source_classes
        ]

    def dump_snapshot(self, num_weeks: int = 4):
        for s in self.sources(num_weeks=num_weeks):
            data = s.make_snapshot()
            print(f"---------- {s.ID} ----------")
            print(json.dumps(data, indent=2))

    def make_snapshot(self, num_weeks: int = 4, processes: int = 1):
        sources = self.sources(num_weeks=num_weeks)

        if processes <= 1:
            for s in sources:
                self._make_and_store_snapshot(s)
        else:
            pool = Pool(processes)
            pool.map(self._make_and_store_snapshot, sources)

    def _make_and_store_snapshot(self, s: SourceBase):
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
        sources = self.sources()
        max_id_len = max(len(s.ID) for s in sources)
        max_type_len = max(len(s.SCRAPER_TYPE) for s in sources)
        for s in sources:
            num_snapshots = 0
            num_unchanged_snapshots = 0
            num_errors = len(list(s.iter_error_filenames()))

            for dt, fn in s.iter_snapshot_filenames():
                num_snapshots += 1
                unchanged = "-unchanged.json" in str(fn)
                if unchanged:
                    num_unchanged_snapshots += 1

            num_changed = num_snapshots - num_unchanged_snapshots
            num_changed_p = num_changed / max(num_snapshots, 1) * 100
            num_changed_p = f"{num_changed_p:.2f}%"
            print(
                f"{s.ID:{max_id_len}} {s.SCRAPER_TYPE:{max_type_len}}"
                f"{num_snapshots:5d} snapshots {num_changed:5d} changes ({num_changed_p:7}) "
                f"errors: {num_errors}"
            )

    def dump_convert_snapshots(self):
        data = self.convert_snapshots()
        print(json.dumps(data, indent=2, cls=JsonEncoder))

    def convert_snapshots(
            self,
            with_unchanged: bool = False,
            with_invalid: bool = False,
    ) -> dict:
        sources = self.sources()
        sources_data = {s.ID: None for s in sources}
        for s in tqdm(sources):
            for dt, unchanged, snapshot_data in s.iter_snapshot_data(with_unchanged=with_unchanged):
                try:
                    data = self.convert_snapshot(s, snapshot_data)
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

    def dump_snapshot_changes(self, with_zeros: bool = False, resample: Optional[str] = None):
        import pandas as pd
        changes = self.get_snapshot_changes(with_zeros=with_zeros)
        df = pd.DataFrame(changes).set_index("date")

        for source_id in sorted(df["source_id"].unique()):
            for loc_id in sorted(df["location_id"].unique()):
                df2 = df[df["source_id"] == source_id]
                df2 = df2[df2["location_id"] == loc_id]
                if resample:
                    df2 = df2.resample(resample).sum()
                    df2 = pd.DataFrame({
                        "date": df2.index, "source_id": source_id, "location_id": loc_id,
                        "appointments": df2["appointments"],
                        "cancellations": df2["cancellations"],
                    }).set_index("date")
                if not df2.empty:
                    print(df2.to_string(max_rows=max(1, df.shape[0])))
                    print()

    def get_snapshot_changes(self, days_ahead: int = 0, with_zeros: bool = False):
        sources = self.sources()
        working_data = {}
        ret_data = []
        for s in tqdm(sources):
            prev_locations = dict()
            for idx, (dt, unchanged, snapshot_data) in enumerate(s.iter_snapshot_data(with_unchanged=False)):
                data = self.convert_snapshot(s, snapshot_data)
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

                    if loc_id in prev_locations:
                        if loc_id not in working_data:
                            working_data[loc_id] = {}

                        prev_date, prev_location = prev_locations[loc_id]

                        appointments, cancellations = s.compare_snapshot_location(
                            prev_date, prev_location, dt, location, working_data[loc_id],
                        )

                    prev_locations[loc_id] = (dt, location)

                    if idx == 0 or with_zeros or appointments or cancellations:
                        ret_data.append({
                            "source_id": s.ID,
                            "location_id": location["location_id"],
                            "date": dt,
                            "free_dates": len(location["dates"]),
                            "appointments": len(appointments),
                            "cancellations": len(cancellations),
                            #"appointments_s": str(appointments),
                            "min_free": sorted(location['dates'])[0],
                            "max_free": sorted(location['dates'])[-1],
                        })
        return ret_data

    def convert_snapshot(self, s: SourceBase, snapshot_data: Union[dict, list]) -> Optional[List[dict]]:
        data = s.convert_snapshot(snapshot_data)
        if data is None:
            return data
        for row in data:
            row["office_id"] = f"{s.ID}-{row['location_id']}"
        return data


class JsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        try:
            return super().default(o)
        except Exception:
            print("X", type(o))
            raise
