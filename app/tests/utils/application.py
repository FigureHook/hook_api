from app import crud
from app.schemas.application import ApplicationCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_application(db: Session):
    obj_data = ApplicationCreate(name=faker.name())
    return crud.application.create(db=db, obj_in=obj_data)
