import copy
import math

from typing import Optional

from project_utils.models import BaseBatch
from ._batch import ElasticSearchBatchModel
from .._operation import ElasticSearchOperation
from project_utils.conf.addr_config.es_config import ElasticSearchConfig


class ElasticSearchIter(BaseBatch):
    __count: int
    __start: int
    __current: int
    __index: str
    __scroll: int = 1000
    __scroll_id: Optional[str] = None
    __mode: str = "match_all",
    __query: dict
    __size: int
    __total: int
    __batch: ElasticSearchBatchModel
    __operation: ElasticSearchOperation

    def __init__(self, operation: ElasticSearchOperation,
                 batch: ElasticSearchBatchModel, index: str, size: int = 10000, **kwargs):
        super().__init__()
        self.__operation = operation
        self.__batch = batch
        self.__index = index
        self.__size = size
        self.__scroll = kwargs.get("scroll", 1000)
        self.__mode = kwargs.get("mode", "match_all")
        self.__query = kwargs.get("query", {})
        self.__count = 0
        self.__start = 0
        self.__current = 0

    async def init_iter(self):
        resp: dict = await self.__operation.iter(self.__index, self.__scroll, mode=self.__mode, **self.__query,
                                                 size=self.__size)
        self.__scroll_id = resp['_scroll_id']
        self.__count = math.ceil(resp['hits']['total']['value'] / self.__size)
        hits: list = resp['hits']['hits']
        self.__batch.add_items([item['_source'] for item in hits])

    async def __aenter__(self):
        await self.init_iter()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.__batch.clear()
        return False

    def __aiter__(self):
        self.__current = self.__start
        return self

    async def __anext__(self):
        if self.__current >= self.__count:
            self.__start = 0
            self.__current = 0
            raise StopAsyncIteration
        else:
            batch: ElasticSearchBatchModel = copy.deepcopy(self.__batch)
            self.__batch.clear()
            resp: dict = await self.__operation.iter(self.__index, self.__scroll, self.__scroll_id, self.__mode,
                                                     self.__size)
            hits: list = resp['hits']['hits']
            self.__scroll_id = resp['_scroll_id']
            self.__batch.add_items([item['_source'] for item in hits])
            self.__current += 1
            return batch
