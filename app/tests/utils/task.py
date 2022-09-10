from app import crud
from app.schemas.task import TaskCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_task(db: Session):
    obj_data = TaskCreate(name=faker.name(), executed_at=faker.date_time_ad())
    return crud.task.create(db=db, obj_in=obj_data)
