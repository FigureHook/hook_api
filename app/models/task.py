from app.db.model_base import PkModel, UniqueMixin
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Query
from sqlalchemy.sql import func

__all__ = [
    "Task"
]


class Task(UniqueMixin, PkModel):
    __tablename__ = "periodic_task"
    __datetime_callback__ = func.now

    name = Column(String)
    executed_at = Column(
        DateTime,
        default=__datetime_callback__()
    )

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query: Query, name):
        return query.filter(cls.name == name)
