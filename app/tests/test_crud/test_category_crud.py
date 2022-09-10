from app import crud
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.tests.utils.category import create_random_category
from app.tests.utils.faker import faker
from sqlalchemy.orm import Session


def test_create_category(db: Session):
    obj_in = CategoryCreate(name=faker.name())
    db_obj = crud.category.create(db=db, obj_in=obj_in)
    assert db_obj.name == obj_in.name


def test_get_category(db: Session):
    db_obj = create_random_category(db)
    fetched_db_obj = crud.category.get(db=db, id=db_obj.id)
    assert fetched_db_obj == db_obj


def test_update_category(db: Session):
    db_obj = create_random_category(db)
    update_obj = CategoryUpdate(name=faker.name())
    updated_db_obj = crud.category.update(db=db, db_obj=db_obj, obj_in=update_obj)
    assert update_obj.name == updated_db_obj.name


def test_delete_category(db: Session):
    db_obj = create_random_category(db)
    deleted_category = crud.category.remove(db=db, id=db_obj.id)
    fetched_category = crud.category.get(db=db, id=db_obj.id)

    assert not fetched_category
    if deleted_category:
        assert deleted_category.name == db_obj.name
