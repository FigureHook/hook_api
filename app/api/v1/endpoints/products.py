from typing import Any

from app import crud
from app.api import deps
from app.models import Product
from app.schemas.category import CategoryInDB
from app.schemas.company import CompanyInDB
from app.schemas.page import Page, PageParamsBase
from app.schemas.product import (ProductCreate, ProductInDBRich,
                                 ProductOfficialImageInDB, ProductUpdate)
from app.schemas.release_info import (ProductReleaseInfoCreate,
                                      ProductReleaseInfoInDB)
from app.schemas.series import SeriesInDB
from app.schemas.worker import WorkerInDB
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


def check_product_exist(product_id: int, db: Session = Depends(deps.get_db)) -> Product:
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified product(id:{product_id}) didn't exist."
        )
    return product


@router.get(
    '/',
    response_model=Page[ProductInDBRich]
)
def get_products(
    *,
    db: Session = Depends(deps.get_db),
    params: PageParamsBase = Depends()
):
    skip = (params.page - 1) * params.size
    products = crud.product.get_multi(
        db=db,
        skip=skip,
        limit=params.size
    )
    products_count = crud.product.count(db=db)
    products_out = [
        map_product_model_to_schema(product)
        for product in products
    ]
    return Page.create(
        products_out,
        total_results=products_count,
        params=params
    )


@router.post(
    '/',
    response_model=ProductInDBRich,
    status_code=status.HTTP_201_CREATED)
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
    product: Product = Depends(check_product_exist),
):
    obj_out = map_product_model_to_schema(product)
    return obj_out


@router.put('/{product_id}', response_model=ProductInDBRich)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist),
    product_in: ProductUpdate,
):
    updated_product = crud.product.update(
        db=db, db_obj=product, obj_in=product_in)

    obj_out = map_product_model_to_schema(updated_product)
    return obj_out


@router.delete(
    '/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT)
def deleted_product(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist),
):
    crud.product.remove(db=db, id=product.id)


@router.post(
    '/{product_id}/release-infos',
    response_model=ProductReleaseInfoInDB,
    status_code=status.HTTP_201_CREATED)
def create_product_release_info(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist),
    release_info: ProductReleaseInfoCreate
):
    obj_out = crud.release_info.create_with_product(
        db=db, obj_in=release_info, product_id=product.id)
    return ProductReleaseInfoInDB.from_orm(obj_out)


@router.get(
    '/{product_id}/release-infos',
    response_model=list[ProductReleaseInfoInDB])
def get_product_release_infos(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist),
):
    release_infos = crud.release_info.get_by_product(
        db=db, product_id=product.id)
    return [
        ProductReleaseInfoInDB.from_orm(info)
        for info in release_infos
    ]


@router.get(
    '/{product_id}/official-images',
    response_model=list[ProductOfficialImageInDB])
def get_official_images(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist)
):
    return [
        ProductOfficialImageInDB.from_orm(image)
        for image in product.official_images
    ]


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
