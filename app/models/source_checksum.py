from datetime import datetime
from typing import TypeVar, cast

from app.db.model_base import PkModel, UniqueMixin
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Mapped, Query
from sqlalchemy.sql import func

__all__ = [
    "SourceChecksum"
]

T = TypeVar('T', bound='SourceChecksum')


class SourceChecksum(UniqueMixin, PkModel):
    __tablename__ = "source_checksum"
    __datetime_callback__ = func.now

    source: Mapped[str] = Column(String)  # type: ignore
    checksum = cast(str, Column(String))
    checked_at: Mapped[datetime] = Column(
        DateTime,
        default=__datetime_callback__()
    )  # type: ignore

    @classmethod
    def unique_hash(cls, source):
        return source

    @classmethod
    def unique_filter(cls, query: Query, *args, **kwargs):
        return query.filter(cls.source == kwargs.get('source'))
