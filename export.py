import os
import csv
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
        "-i", "--include", type=str,
        help="wildcard pattern for sources to include"
    )
    parser.add_argument(
        "-e", "--exclude", type=str,
        help="wildcard pattern for sources to exclude"
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

    return parser.parse_args()


class Exporter:

    def __init__(
            self,
            days_back: int,
            include: Optional[str] = None,
            exclude: Optional[str] = None,
            with_unchanged: bool = True,
            export_raw_path: Union[str, Path] = "export_raw",
            export_path: Union[str, Path] = "export",
    ):
        self.days_back = days_back
        self.sources = DataSources(include=include, exclude=exclude)
        self.with_unchanged = with_unchanged
        self.date_from = datetime.datetime.now() - datetime.timedelta(days=self.days_back)
        self.date_from = self.date_from.replace(hour=0, minute=0, second=0, microsecond=0)
        self.export_raw_path = Path(export_raw_path)
        self.export_path = Path(export_path)

    def export(self):
        """
        Exports only full iso-weeks from the raw snapshots to canonical csv files
        """
        for source_idx, source in enumerate(self.sources.source_classes):
            source_description = f"{source_idx+1}/{len(self.sources.source_classes)} {source.ID}"

            do_export = False
            old_iso_week = None
            last_week_data = []
            for dt, unchanged, data in source.iter_snapshot_data(
                    date_from=self.date_from.isoformat(),
                    with_unchanged=self.with_unchanged,
            ):
                iso_week = dt.isocalendar()[:2]
                if old_iso_week is None:
                    old_iso_week = iso_week
                else:
                    if iso_week > old_iso_week:
                        do_export = True
                        if last_week_data:
                            self._export_week(source, old_iso_week, last_week_data, source_description)
                        old_iso_week = iso_week
                        last_week_data.clear()
                    if do_export:
                        last_week_data.append((dt, data))

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

        for dt, snapshot_data in tqdm(
                snapshot_data_list,
                desc=f"{source_description}: converting week {iso_week}",
        ):
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

        if not location_data_list:
            print(f"{source_description}: NO DATES in {source.ID} {iso_week}")
            return

        all_dates = [str(d) for d in sorted(all_dates)]

        rows = source.make_export_table(location_data_list, all_dates)
        rows.sort(key=lambda row: row[2])
        rows.sort(key=lambda row: row[0])

        print(f"{source_description}: snapshot dates: {rows[0][0]} to {rows[-1][0]}")

        print(f"{source_description}: storing {filename}")
        os.makedirs(export_path, exist_ok=True)
        try:
            with open(filename, "w") as fp:
                writer = csv.writer(fp)
                writer.writerow(["date", "source_id", "location_id"] + all_dates)
                writer.writerows(rows)
        except:
            if filename.exists():
                os.remove(filename)
            raise

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
        exclude=args.exclude,
        days_back=args.days_back,
        export_raw_path=args.export_raw,
        export_path=args.export,
    )

    exporter.export()
    exporter.export_compressed()
