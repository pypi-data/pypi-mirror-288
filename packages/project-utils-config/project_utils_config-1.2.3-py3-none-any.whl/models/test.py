from project_utils.models import BaseElement


class TestBaseModel(BaseElement):
    test_id: str
    test_name: str

    def __init__(self, test_id: str, test_name: str):
        self.test_id = test_id
        self.test_name = test_name

    def __data__(self):
        return {
            "test_id": self.test_id,
            "test_name": self.test_name
        }

    def __str__(self):
        return self.__json__()
