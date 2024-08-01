from abc import ABCMeta, abstractmethod
from typing import Union, Optional, Iterable
from pymysql.cursors import Cursor as SyncCursor
from aiomysql.cursors import Cursor as AsyncCursor
from pymysql.connections import Connection as SyncConnect
from aiomysql.connection import Connection as AsyncConnect
from dbutils.steady_db import SteadyDBCursor as PoolCursor
from dbutils.steady_db import SteadyDBConnection as PoolConnect


class BaseCursor(metaclass=ABCMeta):
    cursor: Union[SyncCursor, AsyncCursor, PoolCursor]
    connect: Union[SyncConnect, AsyncConnect, PoolConnect]

    def __init__(self, connect: Union[SyncConnect, AsyncConnect, PoolConnect]):
        self.connect = connect

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...

    @abstractmethod
    def execute(self, sentence: str, data: Optional[Iterable] = None):
        ...

    @abstractmethod
    def execute_many(self, sentence: str, data: Union[list, tuple] = None):
        ...
