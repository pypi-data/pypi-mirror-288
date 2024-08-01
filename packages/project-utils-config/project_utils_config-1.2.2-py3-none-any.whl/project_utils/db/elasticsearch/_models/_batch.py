import json
from abc import ABC
from typing import Optional

from project_utils.models import BaseBatch


class ElasticSearchBatchModel(BaseBatch, ABC):
    index: Optional[str] = None
    element_type: object

    def __data__(self):
        result: list = []
        for model in self.data:
            head: dict = self.get_head(model.id)
            result.append("\n".join((json.dumps(head), model.__json__())))
        return "\n".join(result) + "\n"

    def get_head(self, doc_id: str):
        return {"index": {"_index": self.index, "_type": "_doc", "_id": doc_id}}
