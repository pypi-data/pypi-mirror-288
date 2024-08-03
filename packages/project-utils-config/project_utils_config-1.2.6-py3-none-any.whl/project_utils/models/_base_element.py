import zlib
import base64

from abc import ABC

from project_utils.io import md5_encode

from ._base import BaseModel


class BaseElement(BaseModel, ABC):
    def __base64__(self, encoding: str = "utf-8"):
        return base64.b64encode(self.__bytes__(encoding=encoding))

    def __compress__(self, encoding: str = "utf-8"):
        return zlib.compress(self.__base64__(encoding=encoding))

    def __code__(self, encoding: str = "utf-8"):
        return md5_encode(self.__base64__(encoding=encoding).decode(encoding=encoding))

    @classmethod
    def from_base64(cls, data: bytes, encoding: str = "utf-8"):
        return cls.from_bytes(base64.b64decode(data), encoding)

    @classmethod
    def decompress(cls, data: bytes, encoding: str = "utf-8"):
        return cls.from_base64(zlib.decompress(data), encoding)
    