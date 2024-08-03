import json
from abc import ABCMeta

from typing import Optional, Union, Dict, List


class BaseResult(metaclass=ABCMeta):
    __status: int
    __exception: Optional[Exception]
    __data: Optional[Union[Dict, List]]

    def __init__(self, status: int, data: Optional[Union[Dict, List]] = None, exception: Optional[Exception] = None):
        """
            数据库响应对象基类
        :param status: 状态，有3种取值，分别为：-1:出现异常;0:数据库操作成功，但没有数据返回;1:数据库操作成功，并且有数据返回
        :param data: 返回的数据
        :param exception: 异常信息
        """
        self.__status = status
        self.__data = data
        self.__exception = exception

    @property
    def status(self):
        return self.__status

    @property
    def data(self):
        return self.__data

    @property
    def exception(self):
        return self.__exception

    @status.setter
    def status(self, value):
        self.__status = value

    @data.setter
    def data(self, value):
        self.__data = value

    @exception.setter
    def exception(self, value):
        self.__exception = value

    def __str__(self):
        return json.dumps({"status": self.status, "data": self.data, "exception": str(self.exception)})
