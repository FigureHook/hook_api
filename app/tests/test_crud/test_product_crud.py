from app import crud
from app.schemas.product import ProductCreate, ProductUpdate
from app.tests.utils.faker import faker
from app.tests.utils.product import create_random_product
from sqlalchemy.orm import Session


def _create_product_obj():
    order_period_start = faker.date_time_ad()
    order_period_end = faker.date_time_between(start_date=order_period_start)
    obj_in = ProductCreate(
        name=faker.name(),
        size=faker.pyint(min_value=1, max_value=1000),
        scale=faker.pyint(min_value=1, max_value=1000),
        rerelease=faker.boolean(chance_of_getting_true=20),
        adult=faker.boolean(chance_of_getting_true=25),
        copyright=faker.paragraph(nb_sentences=1),
        url=faker.uri(),
        jan=faker.ean13(),
        checksum=faker.lexify(text="???????????????????"),
        series=faker.name(),
        category=faker.name(),
        manufacturer=faker.name(),
        releaser=faker.name(),
        distributer=faker.name(),
        sculptors=[faker.name() for _ in range(2)],
        paintworks=[faker.name() for _ in range(2)],
        official_images=[faker.uri() for _ in range(5)],
        order_period_start=order_period_start,
        order_period_end=order_period_end,
        # release_infos=[ProductReleaseInfoCreate(
        #     price=faker.pyint(min_value=1),
        #     tax_including=faker.boolean(chance_of_getting_true=20),
        #     initial_release_date=faker.date_this_year(),
        #     adjusted_release_date=None,
        #     announced_at=None,
        #     shipped_at=None
        # ) for _ in range(faker.pyint(min_value=1, max_value=4))]
    )

    return obj_in


def _create_update_product_obj():
    order_period_start = faker.date_time_ad()
    order_period_end = faker.date_time_between(start_date=order_period_start)
    obj_in = ProductUpdate(
        name=faker.name(),
        size=faker.pyint(min_value=1, max_value=1000),
        scale=faker.pyint(min_value=1, max_value=1000),
        rerelease=faker.boolean(chance_of_getting_true=20),
        adult=faker.boolean(chance_of_getting_true=25),
        copyright=faker.paragraph(nb_sentences=1),
        url=faker.uri(),
        jan=faker.ean13(),
        checksum=faker.lexify(text="???????????????????"),
        series=faker.name(),
        category=faker.name(),
        manufacturer=faker.name(),
        releaser=faker.name(),
        distributer=faker.name(),
        sculptors=[faker.name() for _ in range(2)],
        paintworks=[faker.name() for _ in range(2)],
        order_period_start=order_period_start,
        order_period_end=order_period_end,
    )

    return obj_in


def test_create_product(db: Session):
    obj_in = _create_product_obj()
    db_obj = crud.product.create(db=db, obj_in=obj_in)

    assert db_obj.name == obj_in.name
    assert db_obj.size == obj_in.size
    assert db_obj.scale == obj_in.scale
    assert db_obj.rerelease == obj_in.rerelease
    assert db_obj.adult == obj_in.adult
    assert db_obj.copyright == obj_in.copyright
    assert db_obj.url == obj_in.url
    assert db_obj.jan == obj_in.jan
    assert db_obj.checksum == obj_in.checksum
    assert db_obj.order_period_end == obj_in.order_period_end
    assert db_obj.order_period_start == obj_in.order_period_start

    assert db_obj.series.name == obj_in.series
    assert db_obj.category.name == obj_in.category
    assert db_obj.manufacturer.name == obj_in.manufacturer
    assert db_obj.releaser.name == obj_in.releaser
    assert db_obj.distributer.name == obj_in.distributer

    if obj_in.sculptors:
        for s in db_obj.sculptors:
            assert s.name in obj_in.sculptors

    if obj_in.paintworks:
        for p in db_obj.paintworks:
            assert p.name in obj_in.paintworks

    if obj_in.official_images:
        for i in db_obj.official_images:
            assert i.url in obj_in.official_images


def test_get_product(db: Session):
    db_obj = create_random_product(db)
    fetched_db_obj = crud.product.get(db=db, id=db_obj.id)

    assert db_obj == fetched_db_obj


def test_update_product(db: Session):
    db_obj = create_random_product(db)
    obj_in = _create_update_product_obj()
    updated_db_obj = crud.product.update(db=db, db_obj=db_obj, obj_in=obj_in)

    assert updated_db_obj.name == obj_in.name
    assert updated_db_obj.size == obj_in.size
    assert updated_db_obj.scale == obj_in.scale
    assert updated_db_obj.rerelease == obj_in.rerelease
    assert updated_db_obj.adult == obj_in.adult
    assert updated_db_obj.copyright == obj_in.copyright
    assert updated_db_obj.url == obj_in.url
    assert updated_db_obj.jan == obj_in.jan
    assert updated_db_obj.checksum == obj_in.checksum
    assert updated_db_obj.order_period_end == obj_in.order_period_end
    assert updated_db_obj.order_period_start == obj_in.order_period_start

    assert updated_db_obj.series.name == obj_in.series
    assert updated_db_obj.category.name == obj_in.category
    assert updated_db_obj.manufacturer.name == obj_in.manufacturer
    assert updated_db_obj.releaser.name == obj_in.releaser
    assert updated_db_obj.distributer.name == obj_in.distributer

    if obj_in.sculptors:
        for s in updated_db_obj.sculptors:
            assert s.name in obj_in.sculptors

    if obj_in.paintworks:
        for p in updated_db_obj.paintworks:
            assert p.name in obj_in.paintworks


def test_remove_product(db: Session):
    db_obj = create_random_product(db)
    deleted_db_obj = crud.product.remove(db=db, id=db_obj.id)
    fetched_db_obj = crud.product.get(db=db, id=db_obj.id)

    assert not fetched_db_obj
    if deleted_db_obj:
        assert deleted_db_obj == db_obj
