from project_utils.db.mysql import MySQL
from project_utils.conf import ConfigTemplate
from .test_config import TestConfig


class Config(ConfigTemplate):
    test_config: TestConfig
    system_field = "TEST"
    mysql: MySQL

    def config_init(self, base_url: str) -> None:
        super().config_init(base_url)
        self.config_object.load_es(**self.parser['ELASTICSEARCH'])
        self.config_object.load_faiss(**self.parser['FAISS'])
        self.config_object.load_graph(**self.parser['GRAPH'])
        self.config_object.load_hbase(**self.parser['HBASE'])
        self.config_object.load_kafka(**self.parser['KAFKA'])
        self.config_object.load_milvus(**self.parser['MILVUS'])
        self.config_object.load_mysql(**self.parser['MYSQL'])
        self.config_object.load_redis(**self.parser['REDIS'])

    def mysql_init(self) -> None:
        self.mysql = MySQL(**self.config_object.mysql_config.to_dict())
