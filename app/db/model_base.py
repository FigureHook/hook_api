import uuid
from typing import Any, Callable, Optional, Type, TypeVar

from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Query, Session
from sqlalchemy_mixins.repr import ReprMixin
from sqlalchemy_mixins.serialize import SerializeMixin
from sqlalchemy_mixins.timestamp import TimestampsMixin

T = TypeVar('T')
Model_T = TypeVar('Model_T', bound='Model')


class Model(ReprMixin, SerializeMixin):
    """Base model class."""

    __abstract__ = True


class PkModel(Model):
    """Model class with a `primary key` column in auto-increment interger named `id`."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class PkModelWithTimestamps(PkModel, TimestampsMixin):
    """Model class with a `primary key` column in auto-increment interger named `uuid` timestamps.
    """
    __abstract__ = True


class UUIDPkModel(Model, TimestampsMixin):
    """Model class with a `primary key` column in UUID named `uuid` with timestamps.
    """
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class UniqueMixin:
    """
    https://github.com/sqlalchemy/sqlalchemy/wiki/UniqueObject
    """
    __abstract__ = True

    @classmethod
    def unique_hash(cls, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def unique_filter(cls, query: Query, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def as_unique(cls, session: Session, *arg: Any, **kw: Any):
        return _unique(
            session,
            cls,
            cls.unique_hash,
            cls.unique_filter,
            cls,
            arg, kw
        )


def _unique(
        session: Session,
        cls: Type[T],
        hashfunc: Callable,
        queryfunc: Callable,
        constructor, arg, kw) -> Optional[T]:
    cache = getattr(session, '_unique_cache', None)
    if cache is None:
        cache = {}
        setattr(session, '_unique_cache', cache)

    hash_value = hashfunc(*arg, **kw)
    if not hash_value:
        return None

    key = (cls, hash_value)
    if key in cache:
        return cache[key]
    else:
        with session.no_autoflush:
            q = session.query(cls)
            q = queryfunc(q, *arg, **kw)
            obj = q.first()
            if not obj:
                obj = constructor(*arg, **kw)
                session.add(obj)
        cache[key] = obj
        return obj
