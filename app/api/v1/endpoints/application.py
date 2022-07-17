import uuid

from app import crud
from app.api import deps
from app.models import Application
from app.schemas.application import ApplicationCreate, ApplicationInDB
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


def check_application_exist(application_id: uuid.UUID, db: Session = Depends(deps.get_db)) -> Application:
    app = crud.application.get(db=db, id=application_id)
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified application(id: {application_id}) didn't exist."
        )
    return app


@router.get('/', response_model=list[ApplicationInDB])
def get_applications(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    apps = crud.application.get_multi(db=db, skip=skip, limit=limit)
    return [
        ApplicationInDB.from_orm(app)
        for app in apps
    ]


@router.post('/', response_model=ApplicationInDB, status_code=status.HTTP_201_CREATED)
def create_applications(
    *,
    db: Session = Depends(deps.get_db),
    application_in: ApplicationCreate
):
    app = crud.application.create(db=db, obj_in=application_in)
    return ApplicationInDB.from_orm(app)


@router.get('/{application_id}', response_model=ApplicationInDB)
def get_application(*, application: Application = Depends(check_application_exist)):
    return ApplicationInDB.from_orm(application)


@router.delete('/{application_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    *,
    db: Session = Depends(deps.get_db),
    application: Application = Depends(check_application_exist)
):
    crud.application.remove(db=db, id=application.id)


@router.post('/{application_id}/refresh', response_model=ApplicationInDB)
def refresh_application(
    *,
    db: Session = Depends(deps.get_db),
    application: Application = Depends(check_application_exist)
):
    application.refresh_token()
    db.add(application)
    db.commit()
    db.refresh(application)
    return ApplicationInDB.from_orm(application)
