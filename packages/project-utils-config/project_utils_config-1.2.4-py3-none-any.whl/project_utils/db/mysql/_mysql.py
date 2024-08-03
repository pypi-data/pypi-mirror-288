from typing import Union

from ._connections import Connection, AsyncConnection, PoolConnection, AsyncPoolConnection


class MysqlUtils:
    __instance__ = None
    __connection: Union[Connection, AsyncConnection, AsyncPoolConnection, PoolConnection]

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self, host: str, port: int, user: str, password: str, database: str, character: str = "utf8",
                 pool: bool = False, is_async: bool = False, *args, **kwargs):
        if pool and is_async:
            """使用连接池使用异步"""
            self.__connection = AsyncPoolConnection(host=host, port=port, user=user, password=password,
                                                    database=database, character=character, *args, **kwargs)
        elif pool and not is_async:
            """使用连接池不使用异步"""
            self.__connection = PoolConnection(host=host, port=port, user=user, password=password,
                                               database=database, character=character, *args, **kwargs)
        elif not pool and is_async:
            """不使用连接池使用异步"""
            self.__connection = AsyncConnection(user, password, database, host, port, character)
        else:
            """不使用连接池不使用异步"""
            self.__connection = Connection(user, password, database, host, port, character)

    @property
    def connection(self):
        return self.__connection

    def start(self):
        return self.__connection.start()

    def stop(self):
        return self.__connection.stop()

    def context(self):
        return self.__connection.context()

    def running(self, *args, **kwargs):
        return self.__connection.running(*args, **kwargs)

    def get_cursor(self):
        return self.__connection.get_cursor()

    def commit(self):
        return self.__connection.commit()

    async def async_start(self):
        return await self.__connection.start()

    async def async_stop(self):
        return await self.__connection.stop()

    async def async_running(self, *args, **kwargs):
        return await self.__connection.running(*args, **kwargs)

    async def async_get_cursor(self):
        return await self.__connection.get_cursor()

    async def async_commit(self):
        return await self.__connection.commit()
