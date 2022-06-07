from tabnanny import check

from app import crud
from app.schemas.source_checksum import SourceChecksumCreate
from sqlalchemy.orm import Session

from .faker import faker


def create_random_source_checksum(db: Session):
    obj_data = SourceChecksumCreate(
        source=faker.name(),
        checksum=faker.lexify(text='???????????????????'),
        checked_at=faker.date_time_ad()
    )
    return crud.source_checksum.create(db=db, obj_in=obj_data)
