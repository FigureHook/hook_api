from app import crud
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.tests.utils.company import create_random_company
from app.tests.utils.faker import faker
from sqlalchemy.orm import Session


def test_create_company(db: Session):
    obj_in = CompanyCreate(name=faker.name())
    db_obj = crud.company.create(db=db, obj_in=obj_in)
    assert db_obj.name == obj_in.name


def test_get_company(db: Session):
    db_obj = create_random_company(db)
    fetched_db_obj = crud.company.get(db=db, id=db_obj.id)

    assert fetched_db_obj == db_obj


def test_update_company(db: Session):
    db_obj = create_random_company(db)
    update_obj = CompanyUpdate(name=faker.name())
    updated_db_obj = crud.company.update(
        db=db, db_obj=db_obj, obj_in=update_obj)

    assert update_obj.name == updated_db_obj.name


def test_delete_company(db: Session):
    db_obj = create_random_company(db)
    deleted_company = crud.company.remove(db=db, id=db_obj.id)
    fetched_company = crud.company.get(db=db, id=db_obj.id)

    assert not fetched_company
    if deleted_company:
        assert deleted_company.name == db_obj.name
