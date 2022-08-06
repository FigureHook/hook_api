from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped

from ..db.model_base import PkModel, UniqueMixin

__all__ = ["Series"]


class Series(UniqueMixin, PkModel):
    __tablename__ = "series"

    name: Mapped[str] = Column(String, unique=True)  # type: ignore

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Series.name == name)
