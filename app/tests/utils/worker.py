from app import crud
from app.schemas.worker import WorkerCreate
from sqlalchemy.orm import Session

from .faker import faker


def _generate_random_worker():
    return WorkerCreate(name=faker.name())


def create_random_sculptor(db: Session):
    obj_data = _generate_random_worker()
    return crud.sculptor.create(db=db, obj_in=obj_data)


def create_random_paintwork(db: Session):
    obj_data = _generate_random_worker()
    return crud.paintwork.create(db=db, obj_in=obj_data)
