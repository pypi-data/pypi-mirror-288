from typing import Dict, Union, Optional
from urllib.parse import quote_plus as urlquote

from .base_config import BaseConfig


class MysqlConfig(BaseConfig):
    user: str
    password: str
    database: str
    pool: bool

    def __init__(self, host: str, user: str, password: str, database: str, port: str = "3306",
                 pool: Optional[str] = None):
        super().__init__(host=host, port=port)
        self.user = user
        self.password = password
        self.database = database
        self.pool = pool is None

    def to_dict(self) -> Dict[str, Union[str, int]]:
        result: Dict[str, Union[str, int]] = super().to_dict()
        result.update({
            "user": self.user,
            "password": self.password,
            "database": self.database
        })
        return result

    def to_url(self, index: Optional[str] = None, path: Optional[str] = None, is_ssl: bool = False) -> str:
        return f"mysql+pymysql://{self.user}:{urlquote(self.password)}@{self.host}:{self.port}/{self.database}"
