from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, Query

from ..db.model_base import PkModel, UniqueMixin

__all__ = ["Company"]


class Company(UniqueMixin, PkModel):
    __tablename__ = "company"

    name: Mapped[str] = Column(String, nullable=False, unique=True)  # type: ignore

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query: Query, *args, **kwargs):
        return query.filter(Company.name == kwargs.get("name"))

    def __repr__(self):
        return self.name
