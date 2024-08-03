from abc import ABCMeta
from typing import Optional


class BaseMeta(metaclass=ABCMeta):
    primary_key: Optional[str] = None
    name: Optional[str] = None
    settings: Optional[dict] = None
    mappings: Optional = None
