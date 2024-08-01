from typing import Any

from project_utils.conf.addr_config.es_config import ElasticSearchConfig

from .._operation import ElasticSearchOperation


class ElasticSearchConnection:
    es_config: ElasticSearchConfig

    def __init__(self, es_config: ElasticSearchConfig):
        self.es_config = es_config

    def session(self):
        return ElasticSearchSession(self)


class ElasticSearchSession:
    connect: ElasticSearchConnection

    def __init__(self, conn: ElasticSearchConnection):
        self.connect = conn

    def from_model(self, model: Any):
        from .._context import ElasticSearchContext
        operation: ElasticSearchOperation = ElasticSearchOperation(self.connect.es_config)
        context: ElasticSearchContext = ElasticSearchContext(operation, model)
        model.objects = context
        model.meta = model.Meta()
        return model
