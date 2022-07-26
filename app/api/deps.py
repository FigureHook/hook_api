from typing import Generator

from app import crud
from app.core.config import settings
from app.db.session import pgsql_db
from app.utils.log_filters import AccessApplicationFilter
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

API_TOKEN_NAME = "x-api-token"
api_token = APIKeyHeader(name=API_TOKEN_NAME, auto_error=False)


def get_db() -> Generator[Session, None, None]:
    with pgsql_db.Session() as session:
        yield session
        session.close()


def verify_token(api_token: str = Security(api_token), db: Session = Depends(get_db)):
    if api_token == settings.API_TOKEN:
        app_name = settings.MANAGEMENT_APP_NAME
        app_id = settings.MANAGEMENT_UUID
        AccessApplicationFilter.set_app_name(app_name)
        AccessApplicationFilter.set_app_uuid(app_id)
        return

    if api_token != settings.API_TOKEN:
        app = crud.application.get_by_token(db=db, token=api_token)
        if app:
            AccessApplicationFilter.set_app_uuid(str(app.id))
            AccessApplicationFilter.set_app_name(app.name)
            app.was_seen()
            db.add(app)
            db.commit()
            db.refresh(app)
            return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect token."
    )
