import fnmatch
import json
import datetime
import os
import io
from pathlib import Path
from typing import Generator, Optional, List, Type

from .sources.base import installed_sources, SourceBase


class DataSources:

    SNAPSHOT_DIR = Path(__file__).resolve().parent.parent / "snapshots"

    def __init__(
            self,
            use_cache: bool = False,
            include: Optional[str] = None,
    ):
        self.use_cache = use_cache
        self.include = include

        self.source_classes: List[Type[SourceBase]] = []
        for name, cls in installed_sources.items():
            if include and not fnmatch.fnmatchcase(name, include):
                continue

            self.source_classes.append(cls)

        self.source_classes.sort(key=lambda s: s.ID)

    def dump_list(self):
        for i, s in enumerate(self.source_classes):
            print(f"{i+1}. {s.ID}")

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

    def make_snapshot(self, num_weeks: int = 4):
        for s in self.sources(num_weeks=num_weeks):
            self._store_snapshot(s)

    def _store_snapshot(self, s: SourceBase):
        now = datetime.datetime.now()
        data = s.make_snapshot()

        snapshot_dir = self.SNAPSHOT_DIR / s.ID / now.strftime("%Y-%m")
        os.makedirs(snapshot_dir, exist_ok=True)

        with open(snapshot_dir / now.strftime("%Y-%m-%d-%H-%M-%S.json"), "w") as fp:
            json.dump(data, fp, cls=JsonEncoder)



class JsonEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            return super().default(o)
        except Exception:
            print("X", type(o))
            raise