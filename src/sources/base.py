from pathlib import Path
import hashlib
import os
import json
import datetime
import traceback
import unicodedata
import re
import time
from copy import deepcopy
from typing import Tuple, List, Dict, Type, Optional, Union, Generator, Iterable, Set

import requests
import bs4


installed_sources: Dict[str, Type["SourceBase"]] = dict()


_re_double_minus = re.compile(r"--+")


class ScraperError(Exception):
    def __init__(self, *args, data: Optional[dict] = None):
        super().__init__(*args)
        if not data:
            data = dict()
        data["stacktrace"] = traceback.format_exc(limit=3)
        self.data: dict = data


class SourceBase:

    CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "cache"
    SNAPSHOT_DIR = Path(__file__).resolve().parent.parent.parent / "snapshots"
    ERROR_DIR = Path(__file__).resolve().parent.parent.parent / "errors"

    SCRAPER_TYPE = "custom"
    VERIFY_CERTIFICATE = True
    REQUEST_DELAY = 0
    # provide a name to exclude from parallel processing
    MULTI_PROCESS_GROUP: Optional[str] = None
    # if in process group, how many in parallel?
    MULTI_PROCESS_MAX: Optional[int] = None

    # set to True if this scraper should not be used by default
    NEEDS_INCLUDE = False

    ID: str = None
    NAME: str = None
    BASE_URL: str = None

    def __init_subclass__(cls, **kwargs):
        if "Base" not in cls.__name__:
            assert cls.ID, f"Must define {cls.__name__}.ID"
            assert cls.NAME, f"Must define {cls.__name__}.NAME"
            if cls.ID in installed_sources:
                raise AssertionError(
                    f"Duplicate scraper ID '{cls.ID}' used in {installed_sources[cls.ID].__name__} and {cls.__name__}"
                )
            installed_sources[cls.ID] = cls

    def __init__(self, num_weeks: int = 4, use_cache: bool = False):
        self.session = requests.Session()
        self.use_cache = use_cache
        self.num_weeks = num_weeks

        self.new_session()

    def __repr__(self):
        return f"{type(self).__name__}({self.ID})"

    @classmethod
    def index_url(cls) -> str:
        return cls.BASE_URL

    @classmethod
    def convert_snapshot(
            cls,
            dt: datetime.datetime,
            data: Union[dict, list],
            as_datetime: bool = False,
    ) -> Optional[List[dict]]:
        data = cls._convert_snapshot(dt, data, as_datetime=as_datetime)
        if not data:
            return data
        for i, loc in enumerate(data):
            data[i] = {
                "source_id": cls.ID,
                "office_id": "%s-%s" % (cls.ID, loc["location_id"]),
                **loc
            }
        return data

    # ----------- override these ------------

    def make_snapshot(self):
        raise NotImplementedError

    @classmethod
    def _convert_snapshot(
            cls,
            dt: datetime.datetime,
            data: Union[dict, list],
            as_datetime: bool = False,
    ) -> Optional[List[dict]]:
        raise NotImplementedError

    @classmethod
    def _convert_snapshot_meta(cls, data: Union[dict, list]) -> dict:
        raise NotImplementedError

    # ---------------------------------------

    @classmethod
    def convert_snapshot_meta(cls, data: Union[dict, list]) -> dict:
        """
        Returns dictionary with all location_ids and associated info

        :param data: the original snapshot data
        """
        return {
            str(location_id): {
                "name": loc.get("name") or None,
                "services": sorted(loc.get("services") or []),
            }
            for location_id, loc in cls._convert_snapshot_meta(data).items()
        }

    @classmethod
    def iter_export_rows(cls, data_list: List[Tuple[datetime.datetime, List[dict]]], all_dates: List[str]):
        for locations in data_list:
            locations[1].sort(key=lambda l: l["location_id"])
            locations[1].sort(key=lambda l: l["source_id"])
        data_list.sort(key=lambda t: t[0])

        for dt, locations in data_list:
            for loc in locations:
                yield [
                        dt,
                        str(loc["source_id"]),
                        str(loc["location_id"]),
                    ] + [
                        "1" if date in loc["dates"] else ""
                        for date in all_dates
                    ]

    @classmethod
    def compare_snapshot_location(
            cls,
            prev_timestamp: datetime.datetime, prev_data: dict,
            timestamp: datetime.datetime, data: dict,
            working_data: dict,
    ) -> Tuple[set, set, bool]:
        appointments, cancellations = set(), set()

        #df = get_calendar_table(data["dates"])
        #print(df)

        sorted_dates = sorted(data["dates"])
        for d in prev_data["dates"]:
            if d not in data["dates"] and sorted_dates[0] <= d <= sorted_dates[-1]:
                appointments.add(d)

        sorted_prev_dates = sorted(prev_data["dates"])
        for d in data["dates"]:
            if d not in prev_data["dates"] and sorted_prev_dates[0] <= d <= sorted_prev_dates[-1]:
                cancellations.add(d)

        if sorted_dates == sorted_prev_dates:
            changed = False
        else:
            sorted_dates = [d for d in sorted_dates if d >= prev_timestamp]
            changed = sorted_dates != sorted_prev_dates
        return appointments, cancellations, changed

    @classmethod
    def get_raw_snapshot(
            cls,
            snapshot_date_wildcard: str
    ) -> Tuple[Optional[datetime.datetime], Optional[Union[list, dict]]]:
        if not snapshot_date_wildcard.endswith("*"):
            snapshot_date_wildcard += "*"
        dt, filename = None, None
        for fn in sorted((cls.SNAPSHOT_DIR / cls.ID).glob(f"*/{snapshot_date_wildcard}.json")):
            date_str = fn.name[:19]
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d-%H-%M-%S")
            filename = fn
        if not dt:
            return None, None

        unchanged = "unchanged.json" in str(filename)
        if unchanged:
            all_files = sorted((cls.SNAPSHOT_DIR / cls.ID).glob(f"*/*.json"))
            idx = all_files.index(filename)
            while idx and "unchanged.json" in str(all_files[idx]):
                idx -= 1
            filename = all_files[idx]
            if "unchanged.json" in str(filename):
                return None, None

        data = json.loads(filename.read_text())
        return dt, data

    @classmethod
    def get_snapshot(cls, snapshot_date_wildcard: str) -> Tuple[Optional[datetime.datetime], Optional[dict]]:
        dt, data = cls.get_raw_snapshot(snapshot_date_wildcard)
        if data:
            data = cls.convert_snapshot(dt, data)
        return dt, data

    @classmethod
    def iter_snapshot_filenames(
            cls,
            date_from: Optional[str] = None,
            date_to: Optional[str] = None,
    ) -> Generator[Tuple[datetime.datetime, Path], None, None]:

        date_paths = sorted((cls.SNAPSHOT_DIR / cls.ID).glob("*"))
        if date_from:
            date_paths = list(filter(
                lambda p: str(p).split("/")[-1] >= date_from[:7],
                date_paths
            ))

        filenames = []
        for d in date_paths:
            for fn in (cls.SNAPSHOT_DIR / cls.ID).glob(f"{str(d).split('/')[-1]}/*.json"):
                filenames.append(fn)

        for fn in sorted(filenames):
            date_str = fn.name[:19]
            if date_from and not date_str >= date_from:
                continue
            if date_to and not date_str < date_to:
                break
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d-%H-%M-%S")
            yield dt, fn

    @classmethod
    def iter_error_filenames(
            cls,
            date_from: Optional[str] = None,
            date_to: Optional[str] = None,
    ) -> Generator[Tuple[datetime.datetime, Path], None, None]:
        for fn in (cls.ERROR_DIR / cls.ID).glob("*/*.json"):
            date_str = fn.name[:19]
            if date_from and not date_str >= date_from:
                continue
            if date_to and not date_str < date_to:
                continue
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d-%H-%M-%S")
            yield dt, fn

    @classmethod
    def iter_snapshot_data(
            cls,
            date_from: Optional[str] = None,
            date_to: Optional[str] = None,
            with_unchanged: bool = False,
            verbose: bool = False,
    ) -> Generator[Tuple[datetime.datetime, bool, Union[dict, list]], None, None]:
        previous_data = None

        date_paths = sorted((cls.SNAPSHOT_DIR / cls.ID).glob("*"))
        if date_from:
            date_paths = list(filter(
                lambda p: str(p).split("/")[-1] >= date_from[:7],
                date_paths
            ))

        filenames = []
        for d in date_paths:
            for fn in (cls.SNAPSHOT_DIR / cls.ID).glob(f"{str(d).split('/')[-1]}/*.json"):
                filenames.append(fn)
        filenames.sort()

        iterable = filenames
        if verbose:
            from tqdm import tqdm
            iterable = tqdm(iterable)

        for fn in iterable:
            date_str = fn.name[:19]
            skip = False
            if date_from and not date_str >= date_from:
                skip = True
            if date_to and not date_str < date_to:
                break

            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d-%H-%M-%S")
            unchanged = "unchanged.json" in str(fn)
            if not unchanged:
                data = json.loads(fn.read_text())
                if not (isinstance(data, dict) and "unchanged" in data):
                    if not skip:
                        yield dt, False, data
                    previous_data = data
                    continue

            # yield unchanged data
            if with_unchanged and not skip:
                assert previous_data is not None, f"unchanged data before real data @ {dt} / {fn}"
                yield dt, True, previous_data

    @classmethod
    def iter_converted_data(
            cls,
            date_from: Optional[str] = None,
            date_to: Optional[str] = None,
            with_unchanged: bool = False,
            verbose: bool = False,
    ) -> Generator[Tuple[datetime.datetime, bool, List[dict]], None, None]:
        for dt, unchanged, snapshot_data in cls.iter_snapshot_data(
                date_from=date_from, date_to=date_to, with_unchanged=with_unchanged,
                verbose=verbose,
        ):
            data = cls.convert_snapshot(dt, snapshot_data)
            if data:
                yield dt, unchanged, data

    @classmethod
    def get_dataframe(
            cls,
            date_from: Optional[str] = None,
            date_to: Optional[str] = None,
            with_unchanged: bool = False,
            verbose: bool = False,
    ):
        import pandas as pd
        import numpy as np
        rows = []
        for dt, unchanged, locations in cls.iter_converted_data(
                date_from=date_from,
                date_to=date_to,
                with_unchanged=with_unchanged,
                verbose=verbose,
        ):
            for loc in locations:
                rows.append({
                    "date": dt,
                    "source_id": str(loc["source_id"]),
                    "location_id": str(loc["location_id"]),
                    **{str(date): 1 for date in loc["dates"]}
                })
        df = (
            pd.DataFrame(rows)
            .set_index(["date", "source_id", "location_id"])
            .sort_index(axis=1)
            .replace(np.nan, 0)
        )
        for column in df.columns:
            if df[column].dtype == 'float64':
                df[column] = df[column].astype(np.int)
        return df

    # ---- below are all helpers for derived classes ----

    def now(self) -> datetime.datetime:
        return datetime.datetime.now()

    def new_session(self):
        if self.session:
            self.session.close()
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/84.0"
        }

    @classmethod
    def to_id(cls, name: str) -> str:
        name = str(name).lower()
        name = name.replace("ß", "ss")
        name = unicodedata.normalize('NFKD', name).encode("ascii", "ignore").decode("ascii")

        name = "".join(
            c if c.isalnum() or c in " \t" else "-"
            for c in name
        ).replace(" ", "-")

        return _re_double_minus.sub("-", name).strip("-")

    def get_cache_dir(self) -> Path:
        return self.CACHE_DIR / self.ID

    def get_cache_filename(
            self,
            x,
            data: Optional[Union[str, dict]] = None,
            headers: Optional[dict] = None
    ) -> Path:
        x = str(x)
        if data:
            if isinstance(data, str):
                x += data
            else:
                x += json.dumps(data)
        if headers:
            x += json.dumps(headers)
        hash = hashlib.md5(x.encode("utf-8")).hexdigest()
        return self.get_cache_dir() / hash

    def get_url(self, url, method="GET", data=None, headers: Optional[dict] = None, encoding=None) -> str:
        if self.use_cache:
            cache_filename = self.get_cache_filename(url, data, headers)
            if cache_filename.exists():
                with open(str(cache_filename)) as fp:
                    return fp.read()

        for try_num in range(3):
            try:
                print("downloading", url, data or "")
                kwargs = dict(
                    timeout=10,
                    verify=self.VERIFY_CERTIFICATE,
                    headers=headers,
                )
                if data:
                    if method == "GET":
                        kwargs["params"] = data
                    else:
                        kwargs["data"] = data
                if self.REQUEST_DELAY:
                    time.sleep(self.REQUEST_DELAY)
                response = self.session.request(method, url, **kwargs)
                if encoding is None:
                    text = response.text
                else:
                    text = response.content.decode(encoding)
                break
            except requests.ConnectionError:
                if try_num == 2:
                    raise

        if self.use_cache:
            os.makedirs(str(self.get_cache_dir()), exist_ok=True)
            with open(str(cache_filename), "w") as fp:
                fp.write(text)

        return text

    def get_json(self, url, method="GET", data=None, headers=None, encoding=None) -> dict:
        text = self.get_url(url, method, data=data, encoding=encoding, headers=headers)
        try:
            return json.loads(text)
        except Exception as e:
            print(text[:1000])
            raise ScraperError(
                f"{type(e).__name__}: {e}", data={
                    "text": self._get_html_error_text(text)
                }
            )

    def _get_html_error_text(self, text: str) -> str:
        if "<title>" in text:
            msg = text[text.index("<title>")+7:]
            if "</title>" in msg:
                return msg[:msg.index("</title>")]
        else:
            msg = text
        return msg[:10000]

    def get_html_soup(self, url, method="GET", data=None, headers: Optional[dict] = None, encoding=None):
        text = self.get_url(url, method=method, data=data, headers=headers, encoding=encoding)
        soup = self.soup(text)
        return soup

    def soup(self, html: str):
        return bs4.BeautifulSoup(html, features="html.parser")


def get_calendar_table(dates: List[str]):
    import numpy as np
    import pandas as pd
    dates_dic = {}
    times = set()
    for d in sorted(dates):
        if isinstance(d, datetime.datetime):
            d = d.isoformat()
        date = d[:10]
        time = d[11:16]
        if date not in dates_dic:
            dates_dic[date] = {}
        dates_dic[date][time] = 1
        times.add(time)

    df = (
        pd.DataFrame(dates_dic)
        .rename({0: "date"})
        .replace(np.nan, 0)
        #.set_index(0)
        .sort_index()
    )
    return df
