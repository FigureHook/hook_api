from app.models import (Category, Company, Paintwork, Product,
                        ProductOfficialImage, Sculptor, Series)
from app.schemas.product import ProductCreate, ProductUpdate
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create(self, *, db: Session, obj_in: ProductCreate) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["series"] = Series.as_unique(db, name=obj_in.series)
        obj_in_data["manufacturer"] = Company.as_unique(
            db, name=obj_in.manufacturer)
        obj_in_data["category"] = Category.as_unique(
            db, name=obj_in.category)
        obj_in_data["releaser"] = Company.as_unique(
            db, name=obj_in.releaser)
        obj_in_data["distributer"] = Company.as_unique(
            db, name=obj_in.distributer)

        if obj_in.paintworks:
            obj_in_data["paintworks"] = Paintwork.multiple_as_unique(
                db, obj_in.paintworks)
        if obj_in.sculptors:
            obj_in_data["sculptors"] = Sculptor.multiple_as_unique(
                db, obj_in.sculptors)

        if obj_in.official_images:
            obj_in_data["official_images"] = [
                ProductOfficialImage(url=url)
                for url in obj_in.official_images
            ]

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, *, db: Session, db_obj: Product, obj_in: ProductUpdate) -> Product:
        foreign_key = [
            'series',
            'manufacturer',
            'category',
            'releaser',
            'distributer',
            'paintworks',
            'sculptors'
        ]

        db_obj_data = db_obj.to_dict()
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            if field in db_obj_data and field not in foreign_key:
                setattr(db_obj, field, update_data[field])

        db_obj.series = Series.as_unique(  # type: ignore
            db, name=obj_in.series)
        db_obj.manufacturer = Company.as_unique(  # type: ignore
            db, name=obj_in.manufacturer)
        db_obj.category = Category.as_unique(  # type: ignore
            db, name=obj_in.category)
        db_obj.releaser = Company.as_unique(  # type: ignore
            db, name=obj_in.releaser)
        db_obj.distributer = Company.as_unique(  # type: ignore
            db, name=obj_in.distributer)

        if obj_in.paintworks:
            db_obj.paintworks = Paintwork.multiple_as_unique(
                db, obj_in.paintworks)
        if obj_in.sculptors:
            db_obj.sculptors = Sculptor.multiple_as_unique(
                db, obj_in.sculptors)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


product = CRUDProduct(Product)
