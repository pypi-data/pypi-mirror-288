import uuid
from typing import Optional

from project_utils.exception import DBException

from ._base import BaseContext


class ElasticSearchContext(BaseContext):
    async def create(self):
        settings: Optional[dict] = await self.model_info("settings")
        mappings: Optional[dict] = await self.model_info("mappings")
        index: str = await self.model_info()
        if settings is None:
            settings = {}
        if mappings is None:
            mappings = {}
        return await self.operation.create(index, settings, mappings)

    async def index(self):
        index: str = await self.model_info()
        return await self.operation.index(index)

    async def drop(self):
        index: str = await self.model_info()
        return await self.operation.drop(index)

    async def insert(self):
        index: str = await self.model_info()
        primary_key: Optional[str] = await self.model_info("primary_key")
        if primary_key is None:
            data_id: str = uuid.uuid4().hex
        else:
            data_id: str = getattr(self.model, primary_key)
        data: dict = self.model.__data__()
        data.pop("objects")
        data.pop("meta")
        return await self.operation.insert(index, data_id, data)

    async def batch_insert(self, data: str):
        index: str = await self.model_info()
        return await self.operation.batch_insert(index, data)

    async def update(self):
        index: str = await self.model_info()
        primary_key: Optional[str] = await self.model_info("primary_key")
        if primary_key is None:
            raise DBException("Not extra primary key value...")
        doc_id: str = getattr(self.model, primary_key)
        data: dict = self.model.__data__()
        data.pop("objects")
        data.pop("meta")
        return await self.operation.update(index, doc_id, data)

    async def delete(self):
        index: str = await self.model_info()
        primary_key: Optional[str] = await self.model_info("primary_key")
        if primary_key is None:
            raise DBException("Not extra primary key value...")
        doc_id: str = getattr(self.model, primary_key)
        return await self.operation.delete(index, doc_id)

    async def batch_delete(self, mode: str = "match", **query):
        index: str = await self.model_info()
        return await self.operation.batch_delete(index, query, mode)

    async def all(self):
        if self.model.__class__.__name__ == "ABCMeta":
            self.model = self.model()
        index: str = await self.model_info()
        result: list = await self.operation.all(index)
        model_class: any = self.model.__class__
        batch: any = model_class.Batch()
        for res in result:
            batch.add(res['_source'])
        return batch

    async def get(self, doc_id: str):
        if self.model.__class__.__name__ == "ABCMeta":
            self.model = self.model()
        index: str = await self.model_info()
        res: dict = await self.operation.get(index, doc_id)
        data: dict = res['_source']
        return self.model.__class__(**data)

    async def filter(self, mode: str = "match", **query):
        if self.model.__class__.__name__ == "ABCMeta":
            self.model = self.model()
        index: str = await self.model_info()
        res: dict = await self.operation.filter(index, query, mode)
        data: list = res['hits']['hits']
        batch: any = self.model.__class__.Batch()
        batch.add_items([item['_source'] for item in data])
        return batch

    async def filter_by(self, query):
        if self.model.__class__.__name__ == "ABCMeta":
            self.model = self.model()
        index: str = await self.model_info()
        res: dict = await self.operation.filter_by(index, query)
        data: list = res['hits']['hits']
        batch: any = self.model.__class__.Batch()
        batch.add_items([item['_source'] for item in data])
        return batch

    def iter(self, scroll: int = 1000, mode: str = "match_all", size: int = 10000, **query):
        from .._models import ElasticSearchIter
        if self.model.__class__.__name__ == "ABCMeta":
            self.model = self.model()
        index: str = self.m_info()
        batch: any = self.model.__class__.Batch()
        return ElasticSearchIter(self.operation, batch, index, size=size, scroll=scroll, mode=mode, query=query)
