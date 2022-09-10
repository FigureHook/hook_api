from app import crud
from app.schemas.series import SeriesCreate, SeriesUpdate
from app.tests.utils.faker import faker
from app.tests.utils.series import create_random_series
from sqlalchemy.orm import Session


def test_create_category(db: Session):
    obj_in = SeriesCreate(name=faker.name())
    db_obj = crud.series.create(db=db, obj_in=obj_in)
    assert db_obj.name == obj_in.name


def test_get_category(db: Session):
    db_obj = create_random_series(db)
    fetched_db_obj = crud.series.get(db=db, id=db_obj.id)

    assert fetched_db_obj == db_obj


def test_update_category(db: Session):
    db_obj = create_random_series(db)
    update_obj = SeriesUpdate(name=faker.name())
    updated_db_obj = crud.series.update(db=db, db_obj=db_obj, obj_in=update_obj)

    assert update_obj.name == updated_db_obj.name


def test_delete_category(db: Session):
    db_obj = create_random_series(db)
    deleted_series = crud.series.remove(db=db, id=db_obj.id)
    fetched_series = crud.series.get(db=db, id=db_obj.id)

    assert not fetched_series
    if deleted_series:
        assert deleted_series.name == db_obj.name
