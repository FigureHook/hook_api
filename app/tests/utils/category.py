from app import crud
from app.schemas.category import CategoryCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_category(db: Session):
    obj_data = CategoryCreate(name=faker.name())
    return crud.category.create(db=db, obj_in=obj_data)
