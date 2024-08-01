from sqlalchemy.ext.declarative import declarative_base

from ._engine import Engine

BaseModel = declarative_base()


class Base(BaseModel):
    __tablename__: str
    __abstract__: bool = True

    def __init__(self, *args, **kwargs):
        BaseModel.__init__(self, *args, **kwargs)

    @classmethod
    def select(cls, engine: Engine, value: any):
        return engine.session.get(cls, value)

    @classmethod
    def all(cls, engine: Engine):
        return engine.session.query(cls).all()

    @classmethod
    def filter(cls, engine: Engine, *args, **kwargs):
        engine.session.query(cls).filter(*args, **kwargs)

    def insert(self, engine: Engine, autocommit: bool = False):
        engine.session.add(self)
        if autocommit:
            engine.commit()

    def update(self, engine: Engine, autocommit: bool = False):
        if autocommit:
            engine.commit()

    def delete(self, engine: Engine, autocommit: bool = False):
        engine.session.delete(self)
        if autocommit:
            engine.commit()

    @property
    def data(self):
        return {key: val for key, val in self.__dict__.items() if not key.startswith("_")}
