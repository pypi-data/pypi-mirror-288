import json
from typing import Optional
from aiohttp.client import BasicAuth
from aiohttp.client import ClientSession

from project_utils.exception import DBException

from ._base import BaseOperation


class ElasticSearchOperation(BaseOperation):
    headers: dict = {"content-type": "application/json"}

    async def create(self, index: str, settings: Optional[dict] = None, mappings: Optional[dict] = None):
        request_url: str = self.es_config.to_url(index=index)
        request_params: dict = {"settings": settings, "mappings": mappings}
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession() as session:
            async with session.put(request_url, data=json.dumps(request_params), headers=self.headers,
                                   auth=request_auth) as response:
                resp: dict = await response.json()
                if "error" in resp:
                    return False
                else:
                    return index

    async def index(self, index: str):
        request_url: str = self.es_config.to_url(index)
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession() as session:
            async with session.get(request_url, auth=request_auth) as response:
                resp: dict = await response.json()
                return resp.get(index, {})

    async def indexes(self):
        request_url: str = self.es_config.to_url(path="_cat/indices?v")
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession() as session:
            async with session.get(request_url, auth=request_auth) as response:
                return await response.text()

    async def drop(self, index: str):
        request_url: str = self.es_config.to_url(index)
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession() as session:
            async with session.delete(request_url, auth=request_auth) as response:
                resp: dict = await response.json()
                if "error" in resp:
                    return False
                else:
                    return True

    async def insert(self, index: str, uuid: str, data: dict):
        request_url: str = self.es_config.to_url(index, f"_doc/{uuid}")
        request_params: str = json.dumps(data)
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession() as session:
            async with session.post(request_url, data=request_params, headers=self.headers,
                                    auth=request_auth) as response:
                return await response.json()

    async def batch_insert(self, index: str, data: str):
        request_url: str = self.es_config.to_url(index, "_bulk")
        request_params: str = data
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession() as session:
            async with session.post(request_url, data=request_params, headers=self.headers,
                                    auth=request_auth) as response:
                return await response.json()

    async def update(self, index: str, doc_id: str, data: dict):
        request_url: str = self.es_config.to_url(index, f"_update/{doc_id}")
        request_params: str = json.dumps({"doc": data})
        request_headers: dict = self.headers
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession() as session:
            async with session.post(request_url, data=request_params, headers=request_headers,
                                    auth=request_auth) as response:
                return await response.json()

    async def delete(self, index: str, doc_id: str):
        request_url: str = self.es_config.to_url(index, f"_doc/{doc_id}")
        request_headers: dict = self.headers
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession(headers=request_headers, auth=request_auth) as session:
            async with session.delete(request_url) as response:
                return await response.json()

    async def batch_delete(self, index: str, query: dict, mode: str = "match"):
        assert mode.lower() in ("match", "term"), DBException(
            "Params \"mode\" value require in match or term,not other!")
        request_url: str = self.es_config.to_url(index, "_delete_by_query")
        request_body: dict = {"query": {mode: query}}
        request_headers: dict = self.headers
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession(headers=request_headers, auth=request_auth) as session:
            async with session.post(request_url, data=json.dumps(request_body)) as response:
                return await response.json()

    async def all(self, index: str):
        request_url: str = self.es_config.to_url(index, "_search")
        request_headers: dict = self.headers
        request_auth: Optional[BasicAuth] = await self.auth()
        request_params: dict = {"query": {"match_all": {}}}
        async with ClientSession(headers=request_headers, auth=request_auth) as session:
            async with session.get(request_url, data=json.dumps(request_params)) as response:
                res: dict = await response.json()
                return res['hits']['hits']

    async def get(self, index: str, doc_id: str):
        request_url: str = self.es_config.to_url(index, f"_doc/{doc_id}")
        request_headers: dict = self.headers
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession(headers=request_headers, auth=request_auth) as session:
            async with session.get(request_url) as response:
                return await response.json()

    async def filter(self, index: str, query: dict, mode: str = "match"):
        request_url: str = self.es_config.to_url(index, "_search")
        request_headers: dict = self.headers
        request_auth: Optional[BasicAuth] = await self.auth()
        request_body: str = json.dumps({"query": {mode: query}})
        async with ClientSession(headers=request_headers, auth=request_auth) as session:
            async with session.get(request_url, data=request_body) as response:
                return await response.json()

    async def filter_by(self, index: str, query: dict):
        request_url: str = self.es_config.to_url(index, "_search")
        request_headers: dict = self.headers
        request_auth: Optional[BasicAuth] = await self.auth()
        request_body: str = json.dumps(query)
        async with ClientSession(headers=request_headers, auth=request_auth) as session:
            async with session.get(request_url, data=request_body) as response:
                return await response.json()

    async def iter(self, index: str, scroll: int = 1000, scroll_id: Optional[str] = None, mode: str = "match_all",
                   size: int = 10000,
                   **query):
        request_headers: dict = self.headers
        request_auth: Optional[BasicAuth] = await self.auth()
        async with ClientSession(headers=request_headers, auth=request_auth) as session:
            if scroll_id is None:
                request_url: str = self.es_config.to_url(index, f"_search?scroll={scroll}m")
                request_body: dict = {"query": {mode: query}, "size": size}
            else:
                request_url: str = self.es_config.to_url(path="_search/scroll")
                request_body: dict = {"scroll": f"{scroll}m", "scroll_id": scroll_id}
            async with session.post(request_url, data=json.dumps(request_body)) as response:
                return await response.json()
