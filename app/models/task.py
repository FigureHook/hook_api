from datetime import datetime
from sqlite3 import Date
from app.db.model_base import PkModel, UniqueMixin
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Query
from sqlalchemy.sql import func

__all__ = [
    "Task"
]


class Task(UniqueMixin, PkModel):
    __tablename__ = "periodic_task"
    __datetime_callback__ = func.now

    name: Mapped[str] = Column(String)  # type: ignore
    executed_at: Mapped[datetime] = Column(
        DateTime,
        default=__datetime_callback__()
    )  # type: ignore

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query: Query, *args, **kwargs):
        return query.filter(cls.name == kwargs.get('name'))
