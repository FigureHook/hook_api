import random

from app import crud
from app.schemas.release_info import (ProductReleaseInfoCreate,
                                      ProductReleaseInfoUpdate)
from app.tests.utils.faker import faker
from app.tests.utils.product import create_random_product
from app.tests.utils.release_info import \
    create_random_release_info_own_by_product
from sqlalchemy.orm import Session


def test_create_release_info(db: Session):
    obj_in = ProductReleaseInfoCreate(
        price=faker.pyint(min_value=1),
        tax_including=faker.boolean(chance_of_getting_true=20),
        initial_release_date=faker.date_this_year(),
        adjusted_release_date=None,
        announced_at=None,
        shipped_at=None
    )
    product = create_random_product(db)
    db_obj = crud.release_info.create_with_product(
        db=db, obj_in=obj_in, product_id=product.id)

    assert db_obj.price == obj_in.price
    assert db_obj.tax_including == obj_in.tax_including
    assert db_obj.initial_release_date == obj_in.initial_release_date
    assert db_obj.adjusted_release_date == obj_in.adjusted_release_date
    assert db_obj.announced_at == obj_in.announced_at
    assert db_obj.shipped_at == obj_in.shipped_at
    assert db_obj.product_id == product.id


def test_get_release_info(db: Session):
    obj_in = ProductReleaseInfoCreate(
        price=faker.pyint(min_value=1),
        tax_including=faker.boolean(chance_of_getting_true=20),
        initial_release_date=faker.date_this_year(),
        adjusted_release_date=None,
        announced_at=None,
        shipped_at=None
    )
    product = create_random_product(db)
    db_obj = crud.release_info.create_with_product(
        db=db, obj_in=obj_in, product_id=product.id)
    fetched_db_obj = crud.release_info.get(db, db_obj.id)

    assert fetched_db_obj == db_obj


def test_update_release_info(db: Session):
    create_obj_in = ProductReleaseInfoCreate(
        price=faker.pyint(min_value=1),
        tax_including=faker.boolean(chance_of_getting_true=20),
        initial_release_date=faker.date_this_year(),
        adjusted_release_date=None,
        announced_at=None,
        shipped_at=None
    )
    obj_in = ProductReleaseInfoUpdate(
        price=faker.pyint(min_value=1),
        tax_including=faker.boolean(chance_of_getting_true=20),
        initial_release_date=faker.date_this_year(),
        adjusted_release_date=None,
        announced_at=None,
        shipped_at=None
    )
    product = create_random_product(db)
    db_obj = crud.release_info.create_with_product(
        db=db, obj_in=create_obj_in, product_id=product.id)
    updated_db_obj = crud.release_info.update(
        db=db, db_obj=db_obj, obj_in=obj_in)

    assert updated_db_obj.price == obj_in.price
    assert updated_db_obj.tax_including == obj_in.tax_including
    assert updated_db_obj.initial_release_date == obj_in.initial_release_date
    assert updated_db_obj.adjusted_release_date == obj_in.adjusted_release_date
    assert updated_db_obj.announced_at == obj_in.announced_at
    assert updated_db_obj.shipped_at == obj_in.shipped_at
    assert updated_db_obj.product_id == product.id


def test_remove_release_info(db: Session):
    obj_in = ProductReleaseInfoCreate(
        price=faker.pyint(min_value=1),
        tax_including=faker.boolean(chance_of_getting_true=20),
        initial_release_date=faker.date_this_year(),
        adjusted_release_date=None,
        announced_at=None,
        shipped_at=None
    )
    product = create_random_product(db)
    db_obj = crud.release_info.create_with_product(
        db=db, obj_in=obj_in, product_id=product.id)

    deleted_db_obj = crud.release_info.remove(db=db, id=db_obj.id)
    fetched_db_obj = crud.release_info.get(db=db, id=db_obj.id)
    assert not fetched_db_obj
    if deleted_db_obj:
        assert deleted_db_obj == db_obj


def test_get_release_infos_by_product(db: Session):
    count = random.randint(0, 5)
    product = create_random_product(db)
    for _ in range(count):
        create_random_release_info_own_by_product(db, product_id=product.id)

    release_infos = crud.release_info.get_by_product(
        db=db, product_id=product.id)

    assert len(release_infos) is count
