import logging
from typing import Optional

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.getLogger('sqlalchemy.engine').setLevel(
    logging.INFO if settings.ENVIRONMENT == 'development' else logging.WARNING
)


engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == 'development',
    future=True
)


class PostgreSQLDB:
    __instance__: Optional['PostgreSQLDB'] = None

    def __new__(cls):
        if not cls.__instance__:
            cls._engine = engine
            cls._sessionmaker = sessionmaker(
                autocommit=False, autoflush=False, bind=engine)
            cls.__instance__ = super().__new__(cls)

        return cls.__instance__

    @property
    def engine(self):
        return self._engine

    @property
    def Session(self):
        return self._sessionmaker


pgsql_db = PostgreSQLDB()
