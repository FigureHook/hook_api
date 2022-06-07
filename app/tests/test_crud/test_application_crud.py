from app import crud
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from app.tests.utils.faker import faker
from app.tests.utils.application import create_random_application
from sqlalchemy.orm import Session


def test_create_application(db: Session):
    obj_in = ApplicationCreate(name=faker.name())
    db_obj = crud.application.create(db=db, obj_in=obj_in)
    assert db_obj.name == obj_in.name


def test_get_application(db: Session):
    db_obj = create_random_application(db)
    fetched_db_obj = crud.application.get(db=db, id=db_obj.id)
    assert fetched_db_obj == db_obj


def test_update_application(db: Session):
    db_obj = create_random_application(db)
    update_obj = ApplicationUpdate(name=faker.name())
    updated_db_obj = crud.application.update(
        db=db, db_obj=db_obj, obj_in=update_obj
    )
    assert updated_db_obj.name == update_obj.name


def test_delete_application(db: Session):
    db_obj = create_random_application(db)
    deleted_application = crud.application.remove(db=db, id=db_obj.id)
    fetched_application = crud.application.get(db=db, id=db_obj.id)

    assert not fetched_application
    if deleted_application:
        assert deleted_application == db_obj
