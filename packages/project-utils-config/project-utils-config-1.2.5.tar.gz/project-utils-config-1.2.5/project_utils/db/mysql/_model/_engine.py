import traceback

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine as OrmEngine

from project_utils.exception import MysqlException
from project_utils.conf.addr_config import MysqlConfig


class Engine:
    __engine: OrmEngine
    __session: Session

    def __init__(self, mysql: MysqlConfig, pool_pre_ping: bool = True, pool_size: int = 10, max_overflow: int = 20):
        self.__engine = create_engine(mysql.to_url(), pool_pre_ping=pool_pre_ping, pool_size=pool_size,
                                      max_overflow=max_overflow)
        self.__session = sessionmaker(bind=self.__engine)()

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session

    def commit(self):
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise MysqlException(str(e), traceback.format_exc())
