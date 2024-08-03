from abc import ABC

from project_utils.models import BaseElement

from ._meta import BaseMeta
from ._batch import ElasticSearchBatchModel
from .._context import ElasticSearchContext


class ElasticSearchModel(BaseElement):
    class Meta(BaseMeta):
        ...

    class Base(BaseMeta):
        ...

    class Batch(ElasticSearchBatchModel, ABC):
        ...

    batch: Batch
    objects: ElasticSearchContext
    base: Base = Base()
