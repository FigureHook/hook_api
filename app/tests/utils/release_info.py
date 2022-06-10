from app import crud
from app.schemas.release_info import ProductReleaseInfoCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_release_info_own_by_product(db: Session, product_id: int):
    obj_in = ProductReleaseInfoCreate(
        price=faker.pyint(min_value=1),
        tax_including=faker.boolean(chance_of_getting_true=20),
        initial_release_date=faker.date_this_year(),
        adjusted_release_date=None,
        announced_at=None,
        shipped_at=None
    )
    db_obj = crud.release_info.create_with_product(
        db=db, obj_in=obj_in, product_id=product_id)
    return db_obj
