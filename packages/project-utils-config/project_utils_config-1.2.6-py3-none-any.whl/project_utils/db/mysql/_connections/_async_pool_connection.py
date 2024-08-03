import asyncio
import traceback

from aiomysql.pool import Pool
from typing import Optional, Iterable
from asyncio import AbstractEventLoop
from aiomysql.connection import Connection

from project_utils.exception import MysqlException
from ._base import BaseConnection
from .._cursors import AsyncCursor
from .._result import MySQLResult


class AsyncPoolConnection(BaseConnection):
    pool: Pool
    cursor: AsyncCursor
    connect: Connection

    def __init__(self, max_connections: int = 10, loop: Optional[AbstractEventLoop] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if loop is None:
            loop = asyncio.get_event_loop()
        db: str = self.config.pop("database")
        self.pool = Pool(1, max_connections, False, -1, loop, db=db, **self.config)

    async def start(self):
        self.connect = await self.pool._acquire()
        await self.connect._connect()

    async def stop(self):
        self.connect.close()

    def context(self):
        class Cursor(AsyncCursor):
            __instance__ = None

            def __init__(this, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.cursor = this

            @classmethod
            def __new__(cls, *args, **kwargs):
                if cls.__instance__ is None:
                    cls.__instance__ = object.__new__(cls)
                return cls.__instance__

            async def __aenter__(self):
                await self.start()
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                await self.stop()
                return False

        return Cursor(self.connect)

    async def get_cursor(self):
        self.cursor = self.context()
        await self.cursor.start()
        return self.cursor

    async def running(self, sentence: str, data: Optional[Iterable] = None, many: bool = False):
        async with self.context() as cursor:
            result: MySQLResult
            if many:
                result = await cursor.execute_many(sentence, data)
            else:
                result = await cursor.execute(sentence, data)
        try:
            await self.commit()
        except Exception as e:
            result.status = -1
            result.data.clear()
            result.exception = e
        return result

    async def commit(self):
        try:
            await self.connect.commit()
        except Exception as e:
            await self.connect.rollback()
            raise MysqlException(str(e), traceback.format_exc())

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
        return False
