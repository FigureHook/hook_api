import logging
import uuid
from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models import Application
from app.schemas.application import ApplicationCreate, ApplicationInDB

router = APIRouter()
logger = logging.getLogger(__name__)


def check_application_exist(
    application_id: uuid.UUID, db: Session = Depends(deps.get_db)
) -> Application:
    app = crud.application.get(db=db, id=application_id)
    if not app:
        logger.info(f"Specified application didn't exist. (id={str(application_id)})")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified application(id: {application_id}) didn't exist.",
        )
    return app


@router.get("/", response_model=Sequence[ApplicationInDB])
async def get_applications(
    *, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100
):
    apps = crud.application.get_multi(db=db, skip=skip, limit=limit)
    logger.info(f"Fetched the applications. (count={len(apps)})")
    return [ApplicationInDB.from_orm(app) for app in apps]


@router.post("/", response_model=ApplicationInDB, status_code=status.HTTP_201_CREATED)
async def create_applications(
    *, db: Session = Depends(deps.get_db), application_in: ApplicationCreate
):
    app = crud.application.create(db=db, obj_in=application_in)
    logger.info(f"Created the application. (id={app.id})")
    return ApplicationInDB.from_orm(app)


@router.get("/{application_id}", response_model=ApplicationInDB)
async def get_application(
    *, application: Application = Depends(check_application_exist)
):
    logger.info(f"Fetched the application. (id={application.id})")
    return ApplicationInDB.from_orm(application)


@router.delete("/{application_id}")
async def delete_application(
    *,
    db: Session = Depends(deps.get_db),
    application: Application = Depends(check_application_exist),
):
    crud.application.remove(db=db, id=application.id)
    logger.info(f"Removed the application. (id={application.id})")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{application_id}/refresh", response_model=ApplicationInDB)
async def refresh_application(
    *,
    db: Session = Depends(deps.get_db),
    application: Application = Depends(check_application_exist),
):
    application.refresh_token()
    db.add(application)
    db.commit()
    db.refresh(application)
    logger.info(f"Refresh the application's token. (id={application.id})")
    return ApplicationInDB.from_orm(application)
