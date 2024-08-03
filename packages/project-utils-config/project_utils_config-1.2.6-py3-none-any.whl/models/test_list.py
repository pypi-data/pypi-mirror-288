from project_utils.models import BaseBatch

from .test import TestBaseModel


class TestList(BaseBatch):
    element_type = TestBaseModel
