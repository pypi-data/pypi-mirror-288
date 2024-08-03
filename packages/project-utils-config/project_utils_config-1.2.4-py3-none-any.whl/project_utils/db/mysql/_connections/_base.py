from abc import ABCMeta, abstractmethod
from typing import Union, Iterable, Optional
from aiomysql.pool import Pool as AsyncPoolConnect
from pymysql.connections import Connection as SyncConnect
from aiomysql.connection import Connection as AsyncConnect
from dbutils.steady_db import SteadyDBConnection as PoolConnect


class BaseConnection(metaclass=ABCMeta):
    __config: dict
    connect: Union[SyncConnect, AsyncConnect, PoolConnect, AsyncPoolConnect]

    def __init__(self, user: str, password: str, database: str, host: str = "localhost", port: int = 3306,
                 character: str = "utf8"):
        self.__config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "charset": character
        }

    @property
    def config(self):
        return self.__config

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...

    @abstractmethod
    def context(self):
        ...

    @abstractmethod
    def get_cursor(self):
        ...

    @abstractmethod
    def running(self, sentence: str, data: Optional[Iterable] = None, many: bool = False):
        ...

    @abstractmethod
    def commit(self):
        ...
