from typing import Type, TypeVar, Union, cast

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from ..db.model_base import Model

__all__ = [
    "SourceChecksum"
]

T = TypeVar('T', bound='SourceChecksum')


class SourceChecksum(Model):
    __tablename__ = "source_checksum"
    __datetime_callback__ = func.now

    source = Column(String, primary_key=True)
    checksum = cast(str, Column(String))
    checked_at = Column(
        DateTime,
        default=__datetime_callback__()
    )

    @classmethod
    def get_by_site(cls: Type[T], session: Session,  source: str) -> Union[T, None]:
        return session.query(cls, cls.source == source).scalar()
