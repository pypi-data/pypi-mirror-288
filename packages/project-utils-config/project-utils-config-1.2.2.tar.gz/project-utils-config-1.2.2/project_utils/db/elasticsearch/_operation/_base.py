from typing import Optional
from abc import ABCMeta, abstractmethod

from aiohttp import BasicAuth

from project_utils.conf.addr_config.es_config import ElasticSearchConfig


class BaseOperation(metaclass=ABCMeta):
    es_config: ElasticSearchConfig

    def __init__(self, es_config: ElasticSearchConfig):
        self.es_config = es_config

    async def auth(self):
        request_auth: Optional[BasicAuth] = None
        auth: Optional[dict] = self.es_config.auth()
        if auth:
            request_auth = BasicAuth(auth['username'], auth['password'])
        return request_auth

    @abstractmethod
    def create(self, index: str, settings: Optional[dict] = None, mappings: Optional[dict] = None):
        ...

    @abstractmethod
    def index(self, index: str):
        ...

    @abstractmethod
    def indexes(self):
        ...

    @abstractmethod
    def drop(self, index: str):
        ...

    @abstractmethod
    def insert(self, index: str, uuid: str, data: dict):
        ...

    @abstractmethod
    def batch_insert(self, index: str, data: str):
        ...

    @abstractmethod
    def update(self, index: str, doc_id: str, data: dict):
        ...

    @abstractmethod
    def delete(self, index: str, doc_id: str):
        ...

    @abstractmethod
    def batch_delete(self, index: str, query: dict, mode: str = "match"):
        ...

    @abstractmethod
    def all(self, index: str):
        ...

    @abstractmethod
    def get(self, index: str, doc_id: str):
        ...

    @abstractmethod
    def filter(self, index: str, query: dict, mode: str = "match"):
        ...

    @abstractmethod
    def filter_by(self, index: str, query: dict):
        ...

    @abstractmethod
    def iter(self, index: str, scroll: int = 1000, scroll_id: Optional[str] = None, mode: str = "match_all",
             size: int = 10000, **query):
        ...
