import traceback

import pymysql

from typing import List, Optional, Iterable
from dbutils.pooled_db import PooledDB
from dbutils.steady_db import SteadyDBConnection

from project_utils.exception import MysqlException
from ._base import BaseConnection
from .._cursors import Cursor as SyncCursor
from .._result import MySQLResult


class PoolConnection(BaseConnection):
    pool: PooledDB
    cursor: SyncCursor
    connect: SteadyDBConnection

    def __init__(
            self,
            max_connections: int = 10,
            min_cached: int = 5,
            max_cached: int = 10,
            max_shared: int = 10,
            blocking: bool = False,
            set_session: Optional[List] = None,
            ping: int = 0,
            *args, **kwargs
    ):
        """
        :param max_connections: 连接池允许的最大连接数，0和None表示不限制连接数
        :param min_cached: 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        :param max_cached: 链接池中最多闲置的链接，0和None不限制
        :param max_shared: 一个链接最多被重复使用的次数，None表示无限制
        :param blocking: 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        :param set_session: 开始会话前执行的命令列表。
        :param ping: ping MySQL服务端，检查是否服务可用。
            - 0 = None = never
            - 1 = default = whenever it is requested
            - 2 = when a cursor is created
            - 4 = when a query is executed
            - 7 = always
        """
        super().__init__(*args, **kwargs)
        self.pool = PooledDB(pymysql, min_cached, max_cached, max_shared, max_connections, blocking,
                             setsession=set_session, ping=ping, **self.config)

    def start(self):
        self.connect = self.pool.connection()

    def stop(self):
        self.connect.close()

    def context(self):
        class Cursor(SyncCursor):
            __instance__ = None

            def __init__(this, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.cursor = this

            def __new__(cls, *args, **kwargs):
                if cls.__instance__ is None:
                    cls.__instance__ = object.__new__(cls)
                return cls.__instance__

            def __enter__(self):
                self.start()
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.stop()
                return False

        return Cursor(self.connect)

    def get_cursor(self):
        self.cursor = self.context()
        self.cursor.start()
        return self.cursor

    def running(self, sentence: str, data: Optional[Iterable] = None, many: bool = False):
        with self.context() as cursor:
            result: MySQLResult
            if many:
                result = cursor.execute_many(sentence, data)
            else:
                result = cursor.execute(sentence, data)
        try:
            self.commit()
        except Exception as e:
            result.status = -1
            result.exception = e
        return result

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.stop()
        self.stop()
        return False

    def commit(self):
        try:
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            raise MysqlException(str(e), traceback.format_exc())
