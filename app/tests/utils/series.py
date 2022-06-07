from app import crud
from app.schemas.series import SeriesCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_series(db: Session):
    obj_data = SeriesCreate(name=faker.name())
    return crud.series.create(db=db, obj_in=obj_data)
