import os
import csv
import json
import glob
import tarfile
import datetime
import argparse
from pathlib import Path
from typing import Optional, Type, List, Tuple, Union

from tqdm import tqdm

from src.data_sources import DataSources
from src.sources.base import installed_sources, SourceBase


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--include", type=str, nargs="+",
        help="wildcard pattern for sources to include"
    )
    parser.add_argument(
        "-e", "--exclude", type=str, nargs="+",
        help="wildcard pattern for sources to exclude"
    )
    parser.add_argument(
        "-it", "--include-type", type=str, nargs="+",
        help="wildcard pattern for scraper types to include"
    )
    parser.add_argument(
        "-d", "--days-back", type=int, default=8,
        help="Number of days in the past to start export"
    )
    parser.add_argument(
        "--export-raw", type=str, default="export-raw",
        help="Export directory for CSV files per isoweek"
    )
    parser.add_argument(
        "--export", type=str, default="export",
        help="Export directory for tar.gz files per isoweek"
    )
    parser.add_argument(
        "-nc", "--no-compressed", type=bool, default=False, const=True, nargs="?",
        help="Do not run compression"
    )
    parser.add_argument(
        "-ic", "--incomplete", type=bool, default=False, const=True, nargs="?",
        help="Export incomplete final week (for development)"
    )

    return parser.parse_args()


class Exporter:

    def __init__(
            self,
            days_back: int,
            include: Optional[Union[str, List[str]]] = None,
            exclude: Optional[Union[str, List[str]]] = None,
            include_type: Optional[Union[str, List[str]]] = None,
            with_unchanged: bool = True,
            export_raw_path: Union[str, Path] = "export_raw",
            export_path: Union[str, Path] = "export",
    ):
        self.days_back = days_back
        self.sources = DataSources(include=include, exclude=exclude, include_type=include_type)
        self.with_unchanged = with_unchanged
        self.date_from = datetime.datetime.now() - datetime.timedelta(days=self.days_back)
        self.date_from = self.date_from.replace(hour=0, minute=0, second=0, microsecond=0)
        self.export_raw_path = Path(export_raw_path)
        self.export_path = Path(export_path)
        self.meta_data = dict()

    def export(self, incomplete: bool = False):
        """
        Exports only full iso-weeks from the raw snapshots to canonical csv files.

        A file for each source_id is only exported when a new week starts and
        ends, that is, if there are snapshots before and after the week.

        :param incomplete: bool, export the final week even if there is no follow-up snapshot
        """
        meta_data_filename = self.export_path / "metadata.json"
        if meta_data_filename.exists():
            with open(meta_data_filename) as fp:
                self.meta_data = json.load(fp)
        else:
            self.meta_data = dict()

        for source_idx, source in enumerate(self.sources.source_classes):
            source_description = f"{source_idx+1}/{len(self.sources.source_classes)} {source.ID}"

            do_export = False
            old_iso_week = None
            last_week_data = []
            for dt, unchanged, data in tqdm(source.iter_snapshot_data(
                    date_from=self.date_from.isoformat(),
                    with_unchanged=self.with_unchanged,
            ), f"scanning {source_description}"):
                iso_week = dt.isocalendar()[:2]
                if old_iso_week is None:
                    old_iso_week = iso_week
                else:
                    #if str(dt) == "2021-09-29 15:27:38" or str(dt) == "2021-09-30 10:43:03":
                    if iso_week > old_iso_week:
                        do_export = True
                        if last_week_data:
                            self._export_week(source, old_iso_week, last_week_data, source_description)
                        old_iso_week = iso_week
                        last_week_data.clear()

                    if do_export:
                        last_week_data.append((dt, data))

            if incomplete and last_week_data:
                self._export_week(source, old_iso_week, last_week_data, source_description)

        self._sort_meta_data()

        if self.meta_data:
            print(f"storing {meta_data_filename}")
            os.makedirs(self.export_path, exist_ok=True)
            with open(meta_data_filename, "w") as fp:
                json.dump(self.meta_data, fp, indent=2)

    def _export_week(
            self,
            source: Type[SourceBase],
            iso_week: Tuple[int, int],
            snapshot_data_list: List,
            source_description: str,
    ):
        export_path = self.export_raw_path / str(iso_week[0]) / f"{iso_week[0]}-{iso_week[1]:02d}"
        filename = export_path / f"{source.ID}.csv"
        if filename.exists():
            print(f"{source_description}: skip existing {filename}")
            return

        # print(f"{source_description}: exporting week {iso_week}, snapshots {len(snapshot_data_list)}")

        location_data_list = []
        all_dates = set()

        for dt, snapshot_data in snapshot_data_list:
                #desc=f"{source_description}: converting week {iso_week}",
            try:
                locations = source.convert_snapshot(dt, snapshot_data)
            except Exception as e:
                print(f"{source_description}: ERROR converting {source.ID} @ {dt}: {type(e).__name__}: {e}")
                continue

            if locations:
                location_data_list.append((dt, locations))
                for loc in locations:
                    loc["dates"] = set(str(d) for d in loc["dates"])
                    all_dates |= loc["dates"]

            try:
                meta_data = source.convert_snapshot_meta(snapshot_data)
            except Exception as e:
                meta_data = None
                print(f"{source_description}: ERROR converting metadata {source.ID} @ {dt}: {type(e).__name__}: {e}")

            if meta_data:
                self._merge_meta_data(source, meta_data)

        if not location_data_list:
            print(f"{source_description}: NO DATES in {source.ID} {iso_week}")
            return

        all_dates = [str(d) for d in sorted(all_dates)]
        
        #if all_dates:
        #    print(f"\n\n{source_description} {all_dates[0]} {all_dates[-1]} {len(all_dates)}\n")

        print(f"{source_description}: storing {filename}")
        os.makedirs(export_path, exist_ok=True)
        try:
            with open(filename, "w") as fp:
                writer = csv.writer(fp)
                writer.writerow(["date", "source_id", "location_id"] + all_dates)
                for row in tqdm(
                        source.iter_export_rows(location_data_list, all_dates),
                        desc=f"{source_description}: writing rows"
                ):
                    writer.writerow(row)
        except:
            if filename.exists():
                os.remove(filename)
            raise

    def _merge_meta_data(self, source: Type[SourceBase], data: dict):
        for location_id, loc in data.items():
            if source.ID not in self.meta_data:
                self.meta_data[source.ID] = {
                    "name": source.NAME,
                    "scraper": source.SCRAPER_TYPE,
                    "url": source.index_url(),
                    "locations": dict(),
                }
            source_data = self.meta_data[source.ID]
            source_locations = source_data["locations"]
            if location_id not in source_locations:
                source_data["locations"][location_id] = {
                    "name": loc.get("name") or None,
                    "services": set(loc.get("services") or []),
                }
            else:
                source_location = source_locations[location_id]
                if loc.get("name") and not source_location["name"]:
                    source_location["name"] = loc["name"]

                if not isinstance(source_location["services"], set):
                    source_location["services"] = set(source_location["services"])
                for s in (loc.get("services") or []):
                    source_location["services"].add(s)

    def _sort_meta_data(self):
        meta_data = {}
        for source_id in sorted(self.meta_data.keys()):
            source = self.meta_data[source_id]
            source["locations"] = {
                location_id: {
                    **source["locations"][location_id],
                    "services": sorted(source["locations"][location_id]["services"])
                }
                for location_id in sorted(source["locations"])
            }
            meta_data[source_id] = source

        self.meta_data = meta_data

    def export_compressed(self):
        # iter through every 'year/isoweek/' directory
        for fn in sorted(glob.glob(str(self.export_raw_path / "*/*"))):
            year, date_name = fn.split("/")[-2:]

            # create a tar.gz of all csv files per isoweek
            export_filename = self.export_path / year / f"{date_name}.tar.gz"
            csv_files = sorted(glob.glob(fn + "/*.csv"))
            if not csv_files:
                continue

            if export_filename.exists():
                mtime = max(*(Path(f).stat().st_mtime for f in csv_files))
                if mtime <= export_filename.stat().st_mtime:
                    continue

            os.makedirs(export_filename.parent, exist_ok=True)
            try:
                with tarfile.open(export_filename, "w:gz") as tf:
                    for i, source_name in enumerate(csv_files):
                        print(f"compressing into {export_filename}: {i+1}/{len(csv_files)} {source_name}")
                        tf.add(source_name, Path(source_name).name)
            except:
                if export_filename.exists():
                    os.remove(export_filename)
                raise


if __name__ == "__main__":
    args = parse_args()
    exporter = Exporter(
        include=args.include,
        include_type=args.include_type,
        exclude=args.exclude,
        days_back=args.days_back,
        export_raw_path=args.export_raw,
        export_path=args.export,
    )

    exporter.export(incomplete=args.incomplete)

    if not args.no_compressed:
        exporter.export_compressed()
