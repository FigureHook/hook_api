from typing import Generator

from app import crud
from app.core.config import settings
from app.db.session import pgsql_db
from app.utils.log_filter import application_name, application_uuid
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
        application_name.set(app_name)
        application_uuid.set(app_id)
        return

    if api_token != settings.API_TOKEN:
        app = crud.application.get_by_token(db=db, token=api_token)
        if app:
            application_name.set(app.name)
            application_uuid.set(str(app.id))
            app.was_seen()
            db.add(app)
            db.commit()
            db.refresh(app)
            return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect token."
    )
