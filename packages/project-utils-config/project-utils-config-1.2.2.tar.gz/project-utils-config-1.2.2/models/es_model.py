import json

from project_utils.db.elasticsearch import BaseModel,BaseBatch

from conf import config


class Test1(BaseModel):
    id: int
    name: str
    age: int

    class Meta:
        primary_key: str = "id"
        mappings: dict = {
            "properties": {
                "id": {
                    "type": "keyword",
                    "index": True
                },
                "name": {
                    "type": "text",
                    "index": True
                },
                "age": {
                    "type": "long",
                    "index": True
                }
            }
        }

    class Batch(BaseBatch):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.index = config.config_object.es_config.get_index(Test1.__name__)
            self.element_type = Test1
