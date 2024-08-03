import traceback

from pymysql import connect
from typing import Optional, Iterable

from project_utils.exception import MysqlException

from ._base import BaseConnection
from .._result import MySQLResult
from .._cursors import Cursor as SyncCursor


class Connection(BaseConnection):
    cursor: SyncCursor

    def start(self):
        self.connect = connect(**self.config)

    def stop(self):
        self.connect.close()

    def context(self):
        class Cursor(SyncCursor):
            __instance__ = None

            def __init__(this, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.cursor = this

            @classmethod
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
