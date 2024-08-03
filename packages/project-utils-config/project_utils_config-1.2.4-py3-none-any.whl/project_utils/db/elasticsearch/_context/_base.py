from typing import Any
from abc import ABCMeta, abstractmethod

from .._operation import ElasticSearchOperation


class BaseContext(metaclass=ABCMeta):
    operation: ElasticSearchOperation
    model: Any

    def __init__(self, operation: ElasticSearchOperation, model: Any):
        self.operation = operation
        self.model = model

    async def model_info(self, key: str = "name"):
        try:
            meta_value: Any = getattr(self.model.meta, key)
        except Exception:
            meta_value: Any = None
        if meta_value is None:
            if key == "name":
                return self.operation.es_config.get_index(self.model.__class__.__name__)
            else:
                return getattr(self.model.base, key)
        else:
            return meta_value

    def m_info(self, key: str = "name"):
        try:
            meta_value: Any = getattr(self.model.meta, key)
        except Exception:
            meta_value: Any = None
        if meta_value is None:
            if key == "name":
                return self.operation.es_config.get_index(self.model.__class__.__name__)
            else:
                return getattr(self.model.base, key)
        else:
            return meta_value

    @abstractmethod
    def create(self):
        """Create index"""

    @abstractmethod
    def index(self):
        """Query index info"""

    @abstractmethod
    def drop(self):
        """Drop index"""

    @abstractmethod
    def insert(self):
        """Insert data to index"""

    @abstractmethod
    def batch_insert(self, data: str):
        """Batch insert data to index """

    @abstractmethod
    def update(self):
        """update data info in index"""

    @abstractmethod
    def delete(self):
        """Delete data from index by doc_id"""

    @abstractmethod
    def batch_delete(self, query: dict, mode: str = "match"):
        """Delete batch data from index by query"""

    @abstractmethod
    def all(self):
        """Query all data in index."""

    @abstractmethod
    def get(self, doc_id: str):
        """Query data by primary key"""

    @abstractmethod
    def filter(self, mode: str = "match", **query):
        """Query data by query"""

    @abstractmethod
    def filter_by(self, query):
        """Query data by dsl sentence."""

    @abstractmethod
    def iter(self, index: str, scroll: int = 1000, mode: str = "match_all", **query):
        """Iter data in index."""
