from pathlib import Path
import hashlib
import os
import json
import datetime
import traceback
from typing import Tuple, List, Dict, Type, Optional, Union, Generator

import requests
import bs4


installed_sources: Dict[str, Type["SourceBase"]] = dict()


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
    ID = None

    def __init_subclass__(cls, **kwargs):
        if "Base" not in cls.__name__:
            assert cls.ID, f"Must define {cls.__name__}.ID"
            installed_sources[cls.ID] = cls

    def __init__(self, num_weeks: int = 4, use_cache: bool = False):
        self.session = requests.Session()
        self.use_cache = use_cache
        self.num_weeks = num_weeks

        self.session.headers = {
            "User-Agent": "Mozilla/5.0 Gecko/20100101 Firefox/74.0"
        }

    def make_snapshot(self):
        raise NotImplementedError

    def now(self) -> datetime.datetime:
        return datetime.datetime.now()

    def get_cache_dir(self) -> Path:
        return self.CACHE_DIR / self.ID

    def get_cache_filename(self, x, data: Optional[Union[str, dict]] = None) -> Path:
        x = str(x)
        if data:
            if isinstance(data, str):
                x += data
            else:
                x += json.dumps(data)
        hash = hashlib.md5(x.encode("utf-8")).hexdigest()
        return self.get_cache_dir() / hash

    def get_url(self, url, method="GET", data=None, encoding=None) -> str:
        if self.use_cache:
            cache_filename = self.get_cache_filename(url, data)
            if cache_filename.exists():
                with open(str(cache_filename)) as fp:
                    return fp.read()

        for try_num in range(3):
            try:
                print("downloading", url)
                response = self.session.request(method, url, data=data, timeout=10, verify=self.VERIFY_CERTIFICATE)
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

    def get_json(self, url, method="GET", data=None, encoding=None) -> dict:
        text = self.get_url(url, method, data, encoding)
        try:
            return json.loads(text)
        except Exception as e:
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

    def get_html_soup(self, url, method="GET", data=None, encoding=None):
        text = self.get_url(url, method=method, data=data, encoding=encoding)
        soup = self.soup(text)
        return soup

    def soup(self, html: str):
        return bs4.BeautifulSoup(html, features="html.parser")

    def iter_snapshot_filenames(self) -> Generator[Tuple[datetime.datetime, Path], None, None]:
        for fn in (self.SNAPSHOT_DIR / self.ID).glob("*/*.json"):
            dt = datetime.datetime.strptime(fn.name[:19], "%Y-%m-%d-%H-%M-%S")
            yield dt, fn

    def iter_error_filenames(self) -> Generator[Tuple[datetime.datetime, Path], None, None]:
        for fn in (self.ERROR_DIR / self.ID).glob("*/*.json"):
            dt = datetime.datetime.strptime(fn.name[:19], "%Y-%m-%d-%H-%M-%S")
            yield dt, fn
