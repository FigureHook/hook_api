import logging
from typing import Any, Optional

from app import crud
from app.api import deps
from app.models import (Company, Product, ProductOfficialImage,
                        ProductReleaseInfo, Series)
from app.schemas.category import CategoryInDB
from app.schemas.company import CompanyInDB
from app.schemas.page import Page, PageParamsBase
from app.schemas.product import (ProductCreate, ProductInDBRich,
                                 ProductOfficialImageInDB, ProductUpdate)
from app.schemas.release_feed import ReleaseFeed
from app.schemas.release_info import (ProductReleaseInfoCreate,
                                      ProductReleaseInfoInDB,
                                      ProductReleaseInfoUpdate)
from app.schemas.series import SeriesInDB
from app.schemas.worker import WorkerInDB
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

router = APIRouter()
logger = logging.getLogger(__name__)


def check_product_exist(product_id: int, db: Session = Depends(deps.get_db)) -> Product:
    product = crud.product.get(db=db, id=product_id)
    if not product:
        logger.info(f"Specified product doesn't exist. (id={product_id})")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified product doesn't exist. (id={product_id})",
        )
    return product


def check_release_exist(
    product_id: int, release_id: int, db: Session = Depends(deps.get_db)
) -> ProductReleaseInfo:
    releases = crud.release_info.get_by_product(db=db, product_id=product_id)
    for r in releases:
        if r.id == release_id:
            return r
    msg = f"Specified release-info doesn't exist. (id={release_id}, product_id={product_id})"
    logger.info(msg)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


@router.get("/", response_model=Page[ProductInDBRich])
async def get_products(
    *,
    db: Session = Depends(deps.get_db),
    page_params: PageParamsBase = Depends(),
    source_url: Optional[str] = None,
):
    if source_url:
        stmt = (
            select(Product)
            .filter(Product.url.like(f"%{source_url}%"))
            .limit(page_params.size)
            .offset(page_params.skip)
        )

        products = db.scalars(stmt).unique().all()
    else:
        products = crud.product.get_multi(
            db=db, skip=page_params.skip, limit=page_params.size
        )

    products_count = crud.product.count(db=db)
    products_out = [map_product_model_to_schema(product) for product in products]
    logger.info(f"Fetched the products. (count={len(products_out)})")
    return Page.create(products_out, total_results=products_count, params=page_params)


@router.post("/", response_model=ProductInDBRich, status_code=status.HTTP_201_CREATED)
async def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: ProductCreate,
) -> Any:
    db_obj = crud.product.create(db=db, obj_in=product_in)
    logger.info(f"Created the product. (id={db_obj.id})")
    obj_out = map_product_model_to_schema(db_obj)
    return obj_out


@router.get("/{product_id}", response_model=ProductInDBRich)
async def get_product(
    *,
    product: Product = Depends(check_product_exist),
    product_id: int,
):
    logger.info(f"Fetched the product. (id:{product_id})")
    obj_out = map_product_model_to_schema(product)
    return obj_out


@router.put("/{product_id}", response_model=ProductInDBRich)
async def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist),
    product_in: ProductUpdate,
    product_id: int,
):
    updated_product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    logger.info(f"Updated the product. (id={product_id})")
    obj_out = map_product_model_to_schema(updated_product)
    return obj_out


@router.delete("/{product_id}")
async def deleted_product(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist),
    product_id: int,
):
    crud.product.remove(db=db, id=product.id)
    logger.info(f"Removed the product. (id={product_id})")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{product_id}/release-infos",
    response_model=ProductReleaseInfoInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_release_info(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist),
    release_info: ProductReleaseInfoCreate,
    product_id: int,
):
    obj_out = crud.release_info.create_with_product(
        db=db, obj_in=release_info, product_id=product.id
    )
    logger.info(f"Created the release-info. (id={obj_out.id}, product_id={product_id})")
    return ProductReleaseInfoInDB.from_orm(obj_out)


@router.patch(
    "/{product_id}/release-infos/{release_id}",
    response_model=ProductReleaseInfoInDB,
)
async def patch_product_release_info(
    *,
    db: Session = Depends(deps.get_db),
    release_info: ProductReleaseInfo = Depends(check_release_exist),
    incoming_release: ProductReleaseInfoUpdate,
):
    updated_release_info = crud.release_info.update(
        db=db, db_obj=release_info, obj_in=incoming_release
    )
    logger.info(
        f"Updated the release-info. (release_info_id={updated_release_info.id}, product_id={release_info.product_id})"
    )
    return ProductReleaseInfoInDB.from_orm(updated_release_info)


@router.get("/{product_id}/release-infos", response_model=list[ProductReleaseInfoInDB])
async def get_product_release_infos(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist),
    product_id: int,
):
    release_infos = crud.release_info.get_by_product(db=db, product_id=product.id)
    logger.info(
        f"Fetched the release-infos. (count={len(release_infos)}, product_id={product_id})"
    )
    return [ProductReleaseInfoInDB.from_orm(info) for info in release_infos]


@router.get(
    "/{product_id}/release-infos/{release_info_id}/feed",
    response_model=ReleaseFeed,
    tags=["release-feed"],
)
async def get_release_info_feed(
    *, db: Session = Depends(deps.get_db), product_id: int, release_info_id: int
):
    # FIXME: need to check the generated SQL query is efficient or not.
    stmt = (
        select(ProductReleaseInfo)
        .filter_by(product_id=product_id, id=release_info_id)
        .join(Product)
        .join(Company, Company.id == Product.manufacturer_id)
        .join(Series, Series.id == Product.series_id, isouter=True)
        .join(
            ProductOfficialImage,
            and_(
                Product.id == ProductOfficialImage.product_id,
                ProductOfficialImage.order == 1,
            ),
        )
    )
    release: Optional[ProductReleaseInfo] = db.scalars(stmt).first()
    if not release:
        logger.info(
            f"Specified release-info doesn't exist. (id={release_info_id}, product_id={product_id})"
        )
        raise HTTPException(
            status_code=404,
            detail=f"Specified release-info doesn't exist. (id={release_info_id}, product_id={product_id})",
        )

    logger.info(f"Fetched feed of release-info. (id={release_info_id})")
    return ReleaseFeed(
        product_id=product_id,
        release_info_id=release_info_id,
        name=release.product.name,
        source_url=release.product.url,
        is_nsfw=release.product.adult,
        is_rerelease=release.product.rerelease,
        series=release.product.series.name,
        manufacturer=release.product.manufacturer.name,
        size=release.product.size,
        scale=release.product.scale,
        price=release.price,
        release_date=release.release_date,
        image_url=release.product.official_images[0].url,
        manufacturer_logo=None,
    )


@router.get(
    "/{product_id}/official-images", response_model=list[ProductOfficialImageInDB]
)
def get_official_images(
    *,
    db: Session = Depends(deps.get_db),
    product: Product = Depends(check_product_exist),
    product_id: int,
):
    logger.info(
        f"Fetched the official-images. (count={len(product.official_images)}, product_id={product_id})"
    )
    return [
        ProductOfficialImageInDB.from_orm(image) for image in product.official_images
    ]


def map_product_model_to_schema(db_obj: Product) -> ProductInDBRich:
    series = SeriesInDB.from_orm(db_obj.series)
    category = CategoryInDB.from_orm(db_obj.category)
    manufacturer = CompanyInDB.from_orm(db_obj.manufacturer)
    releaser = CompanyInDB.from_orm(db_obj.releaser)
    distributer = CompanyInDB.from_orm(db_obj.distributer)
    sculptors = [WorkerInDB.from_orm(s) for s in db_obj.sculptors]
    paintworks = [WorkerInDB.from_orm(p) for p in db_obj.paintworks]
    official_images = [
        ProductOfficialImageInDB.from_orm(i) for i in db_obj.official_images
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
        official_images=official_images,
    )
