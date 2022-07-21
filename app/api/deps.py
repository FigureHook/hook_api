from typing import Generator

from app.core.config import settings
from app.db.session import pgsql_db
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    with pgsql_db.Session() as session:
        yield session
        session.close()


def verify_token(x_auth_token: str = Header(), db: Session = Depends(get_db)):
    if not x_auth_token == settings.API_TOKEN:
        raise HTTPException(status_code=403, detail="Authentication failed.")
