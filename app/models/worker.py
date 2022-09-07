from typing import List, Type, TypeVar

from sqlalchemy import Column, String
from sqlalchemy.orm import Session, Mapped

from ..db.model_base import PkModel, UniqueMixin

__all__ = [
    "Paintwork",
    "Sculptor"
]

Worker_T = TypeVar('Worker_T', bound='Worker')


class Worker(UniqueMixin, PkModel):
    __abstract__ = True

    name: Mapped[str] = Column(String, nullable=False)  # type: ignore

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(cls.name == name)

    @classmethod
    def multiple_as_unique(cls: Type[Worker_T], session: Session, worker_names: List[str]) -> List[Worker_T]:
        workers: List[Worker_T] = []
        for name in worker_names:
            worker = cls.as_unique(session, name=name)
            if worker:
                workers.append(worker)

        return workers


class Paintwork(Worker):
    __tablename__ = "paintwork"


class Sculptor(Worker):
    __tablename__ = "sculptor"
