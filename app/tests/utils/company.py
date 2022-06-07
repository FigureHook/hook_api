from app import crud
from app.schemas.company import CompanyCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_company(db: Session):
    obj_data = CompanyCreate(name=faker.name())
    return crud.company.create(db=db, obj_in=obj_data)
