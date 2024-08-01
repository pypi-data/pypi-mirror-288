import json
import zlib
import base64
import traceback

from typing import List, Tuple, Union, Any

from project_utils.exception import CollectionException

from ._base import BaseModel
from ._base_element import BaseElement


class BaseBatch(BaseModel):
    element_type = BaseElement

    __data: List[element_type]
    __codes: List[str]
    __start: int
    __current: int
    __count: int

    def __init__(self, data: Union[List, Tuple, None] = None, skip: bool = True):
        super().__init__()
        self.__data = []
        self.__codes = []
        self.__start = 0
        self.__current = 0
        self.__count = 0
        if data:
            for item in data:
                element: Any = self.element_type.from_data(item)
                if element.__code__() not in self.__codes:
                    self.__data.append(element)
                    self.__codes.append(element.__code__())
                    self.__count += 1
                else:
                    if not skip:
                        raise CollectionException("Source data need remove repeat item.")

    def __data__(self):
        return [item.__data__() for item in self.__data]

    @classmethod
    def from_json(cls, data: str):
        this: cls = cls()
        this.add_items(json.loads(data))
        return this

    def __base64__(self, encoding: str = "utf-8"):
        return base64.b64encode(self.__bytes__(encoding=encoding))

    def __compress__(self, encoding: str = "utf-8"):
        return zlib.compress(self.__base64__(encoding=encoding))

    @classmethod
    def from_base64(cls, data: bytes, encoding: str = "utf-8"):
        return cls.from_bytes(base64.b64decode(data), encoding)

    @classmethod
    def decompress(cls, data: bytes, encoding: str = "utf-8"):
        return cls.from_base64(zlib.decompress(data), encoding)

    @property
    def count(self):
        return self.__count

    def add(self, data: Any, skip: bool = True):
        if type(data) == dict:
            element: Any = self.element_type.from_data(data)
        else:
            element: Any = data
        if element.__code__() not in self.__codes:
            self.__data.append(element)
            self.__codes.append(element.__code__())
            self.__count += 1
        else:
            if not skip:
                raise CollectionException("Source data need remove repeat item.")

    def add_items(self, data: Union[list, tuple]):
        for item in data:
            self.add(item)

    def remove_from_index(self, index: int):
        if index > self.__count - 1:
            raise CollectionException("Element not find!")
        element: Any = self.__data.pop(index)
        self.__codes.pop(index)
        self.__count -= 1
        return element

    def remove_from_element(self, element: Any):
        try:
            code: str = element.__code__()
            index: int = self.__codes.index(code)
        except Exception as e:
            raise CollectionException(str(e), traceback.format_exc())
        element: Any = self.__data.pop(index)
        self.__codes.pop(index)
        self.__count -= 1
        return element

    def edit(self, index: int, item: Any):
        if index > self.__count - 1:
            raise CollectionException("Element not find!")
        self.__data[index] = item
        self.__codes[index] = item.__code__()

    def index(self, element: Any):
        code: str = element.__code__()
        if code in self.__codes:
            return self.__codes.index(code)
        else:
            return -1

    def clear(self):
        self.__data.clear()
        self.__codes.clear()
        self.__start = 0
        self.__current = 0
        self.__count = 0

    def __iter__(self):
        self.__current = self.__start
        return self

    def __next__(self):
        if self.__current >= self.__count:
            self.__start = 0
            self.__current = 0
            raise StopIteration
        else:
            index: int = self.__current
            self.__current += 1
            return self.__codes[index], self.__data[index]

    def __aiter__(self):
        return self.__iter__()

    async def __anext__(self):
        try:
            return self.__next__()
        except StopIteration:
            raise StopAsyncIteration
        except Exception:
            raise Exception

    @property
    def data(self):
        return self.__data
