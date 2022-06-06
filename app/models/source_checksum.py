from typing import TypeVar, cast

from app.db.model_base import PkModel, UniqueMixin
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Query
from sqlalchemy.sql import func

__all__ = [
    "SourceChecksum"
]

T = TypeVar('T', bound='SourceChecksum')


class SourceChecksum(UniqueMixin, PkModel):
    __tablename__ = "source_checksum"
    __datetime_callback__ = func.now

    source = Column(String)
    checksum = cast(str, Column(String))
    checked_at = Column(
        DateTime,
        default=__datetime_callback__()
    )

    @classmethod
    def unique_hash(cls, source):
        return source

    @classmethod
    def unique_filter(cls, query: Query, source):
        return query.filter(cls.source == source)
