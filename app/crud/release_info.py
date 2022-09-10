from app.models import ProductReleaseInfo
from app.schemas.release_info import ProductReleaseInfoCreate, ProductReleaseInfoUpdate
from sqlalchemy.orm import Session
from .base import CRUDBase
from fastapi.encoders import jsonable_encoder


class CRUDReleaseInfo(
    CRUDBase[ProductReleaseInfo, ProductReleaseInfoCreate, ProductReleaseInfoUpdate]
):
    def create_with_product(
        self, *, db: Session, obj_in: ProductReleaseInfoCreate, product_id: int
    ) -> ProductReleaseInfo:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, product_id=product_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_product(
        self, *, db: Session, product_id: int
    ) -> list[ProductReleaseInfo]:
        return db.query(self.model).filter(self.model.product_id == product_id).all()


release_info = CRUDReleaseInfo(ProductReleaseInfo)
