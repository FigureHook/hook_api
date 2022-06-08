from app import crud
from app.schemas.product import ProductCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_product(db: Session):
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
        checksum=faker.lexify(text='???????????????????'),
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
    db_obj = crud.product.create(db=db, obj_in=obj_in)
    return db_obj
