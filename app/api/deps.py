from typing import Generator
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import pgsql_db
from fastapi import Depends


def get_db() -> Generator[Session, None, None]:
    with pgsql_db.Session() as session:
        yield session
