from pymysql.cursors import DictCursor
from pymysql.connections import Connection
from pymysql.cursors import Cursor as SyncCursor
from typing import Optional, Iterable, List, Union

from ._base import BaseCursor
from .._result import MySQLResult


class Cursor(BaseCursor):
    connect: Connection
    cursor: SyncCursor

    def start(self):
        self.cursor = self.connect.cursor(DictCursor)

    def stop(self):
        self.cursor.close()

    def execute(self, sentence: str, data: Optional[Iterable] = None):
        result: MySQLResult = MySQLResult(0)
        try:
            self.cursor.execute(sentence, data)
            res: List[dict] = self.cursor.fetchall()
            if len(res) > 0:
                result.status = 1
            result.data = res
        except Exception as e:
            result.status = -1
            result.exception = e
        return result

    def execute_many(self, sentence: str, data: Union[list, tuple] = None):
        result: MySQLResult = MySQLResult(0)
        try:
            self.cursor.executemany(sentence, data)
        except Exception as e:
            result.status = -1
            result.exception = e
        return result
