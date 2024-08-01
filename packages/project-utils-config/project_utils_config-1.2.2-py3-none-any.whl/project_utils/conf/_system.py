from abc import ABCMeta
from typing import Any, Optional, List


class SystemConfig(metaclass=ABCMeta):
    __instance__: Any = None
    __debug: bool
    __id_field: Optional[List[str]]

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self, debug: Optional[str] = None, id_fields: Optional[str] = None):
        self.__debug = debug is None
        if id_fields:
            self.__id_field = id_fields.split(",")
        else:
            self.__id_field = None
