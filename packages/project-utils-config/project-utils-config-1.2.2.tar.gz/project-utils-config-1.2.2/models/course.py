from project_utils.db.mysql import Base, Types
from project_utils.models import BaseElement

from sqlalchemy import Column, Integer, VARCHAR


class Course(Base):
    __tablename__ = "course"
    id: Types.integer = Column("id", Integer, primary_key=True, autoincrement=True)
    course_id: Types.integer = Column("course_id", Integer, nullable=False)
    course_name: Types.varchar = Column("course_name", VARCHAR(40))
