from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Query
from sqlalchemy.sql import func

from ..db.model_base import Model, UniqueMixin

__all__ = [
    "Task"
]


class Task(UniqueMixin, Model):
    __tablename__ = "periodic_task"
    __datetime_callback__ = func.now

    name = Column(String, primary_key=True)
    executed_at = Column(
        DateTime,
        default=__datetime_callback__(),
        onupdate=__datetime_callback__()
    )

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query: Query, name):
        return query.filter(cls.name == name)
