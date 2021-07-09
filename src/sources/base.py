from pathlib import Path
import hashlib
import os
import json
import datetime
from typing import List, Dict, Type, Optional

import requests
import bs4


installed_sources: Dict[str, Type["SourceBase"]] = dict()


class SourceBase:

    CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "cache"

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

    def get_cache_filename(self, x, data: Optional[dict] = None) -> Path:
        x = str(x)
        if data:
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
                response = self.session.request(method, url, data=data, timeout=10)
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
            print(f"{type(e).__name__}: {e}\nGot: {text[:1000]}")
            raise

    def get_html_soup(self, url, encoding=None):
        text = self.get_url(url, encoding=encoding)
        soup = self.soup(text)
        return soup

    def soup(self, html: str):
        return bs4.BeautifulSoup(html, features="html.parser")
