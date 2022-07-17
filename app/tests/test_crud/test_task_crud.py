from app import crud
from app.schemas.task import TaskCreate, TaskUpdate
from app.tests.utils.faker import faker
from app.tests.utils.task import create_random_task
from sqlalchemy.orm import Session


def test_create_task(db: Session):
    obj_in = TaskCreate(
        name=faker.name(),
        executed_at=faker.date_time_ad(),
    )
    db_obj = crud.task.create(db=db, obj_in=obj_in)

    assert db_obj.name == obj_in.name
    assert db_obj.executed_at == obj_in.executed_at


def test_get_task(db: Session):
    db_obj = create_random_task(db)
    fetched_db_obj = crud.task.get(db=db, id=db_obj.id)

    assert fetched_db_obj == db_obj


def test_update_task(db: Session):
    db_obj = create_random_task(db)
    obj_in = TaskUpdate(name=faker.name(), executed_at=faker.date_time_ad())
    updated_db_obj = crud.task.update(db=db, db_obj=db_obj, obj_in=obj_in)

    assert updated_db_obj.name == obj_in.name
    assert updated_db_obj.executed_at == obj_in.executed_at


def test_remove_task(db: Session):
    db_obj = create_random_task(db)
    deleted_db_obj = crud.task.remove(db=db, id=db_obj.id)
    fetched_db_obj = crud.task.get(db=db, id=db_obj.id)

    assert not fetched_db_obj
    if deleted_db_obj:
        assert db_obj == deleted_db_obj
