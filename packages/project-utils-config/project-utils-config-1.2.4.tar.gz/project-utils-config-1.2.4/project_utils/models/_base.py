import json
from abc import ABCMeta, abstractmethod


class BaseModel(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        try:
            variables: dict = self.__annotations__
            for key, type_ in variables.items():
                if key in kwargs:
                    self.__setattr__(key, kwargs[key])
                else:
                    try:
                        self.__setattr__(key, self.__getattribute__(key))
                    except:
                        self.__setattr__(key, None)
        except Exception:
            pass

    def __data__(self):
        return {key: val for key, val in self.__dict__.items() if not key.startswith("__")}

    def __json__(self):
        return json.dumps(self.__data__(), ensure_ascii=False)

    def __bytes__(self, encoding: str = "utf-8"):
        return self.__json__().encode(encoding=encoding)

    @classmethod
    def from_data(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_json(cls, data: str):
        return cls.from_data(json.loads(data))

    @classmethod
    def from_bytes(cls, data: bytes, encoding: str = "utf-8"):
        return cls.from_json(data.decode(encoding))

    def items(self):
        return self.__data__().items()
