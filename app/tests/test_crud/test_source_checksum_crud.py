from app import crud
from app.schemas.source_checksum import (SourceChecksumCreate,
                                         SourceChecksumUpdate)
from app.tests.utils.faker import faker
from app.tests.utils.source_checksum import create_random_source_checksum
from sqlalchemy.orm import Session


def test_create_source_checksum(db: Session):
    obj_in = SourceChecksumCreate(
        source=faker.name(),
        checksum=faker.lexify(text='???????????????????'),
        checked_at=faker.date_time_ad(),
    )

    db_obj = crud.source_checksum.create(db=db, obj_in=obj_in)
    assert db_obj.source == obj_in.source
    assert db_obj.checksum == obj_in.checksum
    assert db_obj.checked_at == obj_in.checked_at


def test_get_source_checksum(db: Session):
    db_obj = create_random_source_checksum(db=db)
    fetched_db_obj = crud.source_checksum.get(db, db_obj.id)

    assert fetched_db_obj == db_obj


def test_update_source_checksum(db: Session):
    db_obj = create_random_source_checksum(db=db)
    obj_in = SourceChecksumUpdate(
        source=faker.name(),
        checksum=faker.lexify(text='???????????????????'),
        checked_at=faker.date_time_ad(),
    )

    updated_db_obj = crud.source_checksum.update(
        db=db, db_obj=db_obj, obj_in=obj_in)
    assert obj_in.source == updated_db_obj.source
    assert obj_in.checksum == updated_db_obj.checksum
    assert obj_in.checked_at == updated_db_obj.checked_at


def test_remove_source_checksum(db: Session):
    db_obj = create_random_source_checksum(db=db)

    deleted_db_obj = crud.source_checksum.remove(db=db, id=db_obj.id)
    fetched_db_obj = crud.source_checksum.get(db=db, id=db_obj.id)

    assert not fetched_db_obj
    if deleted_db_obj:
        assert deleted_db_obj == db_obj
