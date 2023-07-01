from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.model_base import Model

Model_T = TypeVar("Model_T", bound=Model)

CreateSchema_T = TypeVar("CreateSchema_T", bound=BaseModel)
UpdateSchema_T = TypeVar("UpdateSchema_T", bound=BaseModel)


class CRUDBase(Generic[Model_T, CreateSchema_T, UpdateSchema_T]):
    def __init__(self, model: Type[Model_T]):
        self.model = model

    def get(self, *, db: Session, id: Any) -> Optional[Model_T]:
        return db.get(self.model, id)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Sequence[Model_T]:
        stmt = select(self.model).limit(limit).offset(skip)
        result = db.execute(stmt)
        return result.scalars().all()

    def create(self, *, db: Session, obj_in: CreateSchema_T) -> Model_T:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, *, db: Session, db_obj: Model_T, obj_in: UpdateSchema_T
    ) -> Model_T:
        db_obj_data = db_obj.to_dict()
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            if field in db_obj_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, *, db: Session, id: Any) -> Optional[Model_T]:
        db_obj = db.get(self.model, id)
        db.delete(db_obj)
        db.commit()
        return db_obj

    def count(self, *, db: Session) -> int:
        return db.query(self.model).count()
