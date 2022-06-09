from typing import Any

from app import crud
from app.api import deps
from app.models import Product
from app.schemas.category import CategoryInDB
from app.schemas.company import CompanyInDB
from app.schemas.product import (ProductCreate, ProductInDBRich,
                                 ProductOfficialImageInDB, ProductUpdate)
from app.schemas.series import SeriesInDB
from app.schemas.worker import WorkerInDB
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/')
def get_items(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    products = crud.product.get_multi(db=db, skip=skip, limit=limit)
    return products


@router.post('/', response_model=ProductInDBRich, status_code=status.HTTP_201_CREATED)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: ProductCreate,
) -> Any:
    db_obj = crud.product.create(db=db, obj_in=product_in)
    obj_out = map_product_model_to_schema(db_obj)
    return obj_out


@router.get('/{product_id}', response_model=ProductInDBRich)
def get_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int
):
    db_obj = crud.product.get(db=db, id=product_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    obj_out = map_product_model_to_schema(db_obj)
    return obj_out


@router.put('/{product_id}')
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: ProductUpdate,
    product_id: int
):
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_product = crud.product.update(
        db=db, db_obj=product, obj_in=product_in)

    obj_out = map_product_model_to_schema(updated_product)
    return obj_out


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def deleted_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int
):
    db_obj = crud.product.remove(db=db, id=product_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def map_product_model_to_schema(db_obj: Product) -> ProductInDBRich:
    series = SeriesInDB.from_orm(db_obj.series)
    category = CategoryInDB.from_orm(db_obj.category)
    manufacturer = CompanyInDB.from_orm(db_obj.manufacturer)
    releaser = CompanyInDB.from_orm(db_obj.releaser)
    distributer = CompanyInDB.from_orm(db_obj.distributer)
    sculptors = [
        WorkerInDB.from_orm(s)
        for s in db_obj.sculptors
    ]
    paintworks = [
        WorkerInDB.from_orm(p)
        for p in db_obj.paintworks
    ]
    official_images = [
        ProductOfficialImageInDB.from_orm(i)
        for i in db_obj.official_images
    ]

    return ProductInDBRich(
        **db_obj.to_dict(),
        series=series,
        category=category,
        manufacturer=manufacturer,
        releaser=releaser,
        distributer=distributer,
        sculptors=sculptors,
        paintworks=paintworks,
        official_images=official_images
    )
