from aiomysql.connection import Connection
from aiomysql.cursors import Cursor, DictCursor
from typing import Union, Optional, Iterable, List

from ._base import BaseCursor
from .._result import MySQLResult


class AsyncCursor(BaseCursor):
    cursor: Cursor
    connect: Connection

    async def start(self):
        self.cursor = self.connect.cursor(DictCursor)

    async def stop(self):
        # await self.cursor.close()
        ...

    async def execute(self, sentence: str, data: Optional[Iterable] = None):
        result: MySQLResult = MySQLResult(0)
        try:
            result.data = []
            async with self.cursor as cursor:
                await cursor.execute(sentence, data)
                async for item in cursor:
                    result.data.append(item)
            if len(result.data) > 0:
                result.status = 1
        except Exception as e:
            result.status = -1
            result.exception = e
        return result

    async def execute_many(self, sentence: str, data: Union[list, tuple] = None):
        result: MySQLResult = MySQLResult(0)
        try:
            await self.cursor.executemany(sentence, data)
        except Exception as e:
            result.status = -1
            result.exception = e
        return result
