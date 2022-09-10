import logging
from typing import Generator

from app import crud
from app.core.config import settings
from app.db.session import pgsql_db
from app.utils.logging.log_filters import application_name, application_uuid
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

API_TOKEN_NAME = "x-api-token"
api_token = APIKeyHeader(name=API_TOKEN_NAME, auto_error=False)


logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    with pgsql_db.Session() as session:
        yield session
        session.close()


async def verify_token(
    api_token: str = Security(api_token), db: Session = Depends(get_db)
):
    if api_token and api_token == settings.API_TOKEN:
        app_name = settings.MANAGEMENT_APP_NAME
        app_id = settings.MANAGEMENT_UUID
        application_name.set(app_name)
        application_uuid.set(app_id)
        return

    if api_token and api_token != settings.API_TOKEN:
        app = crud.application.get_by_token(db=db, token=api_token)
        if app:
            application_uuid.set(str(app.id))
            application_name.set(app.name)
            app.was_seen()
            db.add(app)
            db.commit()
            db.refresh(app)
            return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token."
    )
