import logging

from app import crud
from app.api import deps
from app.models import Category
from app.schemas.category import CategoryCreate, CategoryInDB, CategoryUpdate
from app.schemas.page import Page, PageParamsBase
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter()
logger = logging.getLogger(__name__)


def check_category_exist(category_id: int, db: Session = Depends(deps.get_db)) -> Category:
    category = crud.category.get(db=db, id=category_id)
    if not category:
        logger.info(f"Specified category didn't exist. (id={category_id})")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified category(id: {category_id}) didn't exist."
        )
    return category


@router.get('/', response_model=Page[CategoryInDB])
def get_categories(
    *,
    db: Session = Depends(deps.get_db),
    params: PageParamsBase = Depends()
):
    skip = (params.page - 1) * params.size
    categories = crud.category.get_multi(db=db, skip=skip, limit=params.size)
    categories_count = crud.category.count(db=db)
    categories_out = [
        CategoryInDB.from_orm(category)
        for category in categories
    ]
    logger.info(f"Fetched the categories. (count={len(categories_out)})")
    return Page.create(
        results=categories_out,
        total_results=categories_count,
        params=params
    )


@router.post(
    '/',
    response_model=CategoryInDB,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate
):
    stmt = select(Category).filter_by(name=category_in.name).limit(1)
    category = db.scalars(stmt).first()
    if category:
        logger.info(
            f"The category already exists. (id={category.id}, name={category.name})")
        return RedirectResponse(
            url=request.url_for('get_category', category_id=category.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    category = crud.category.create(db=db, obj_in=category_in)
    logger.info(f"Created the category. (id={category.id})")
    return CategoryInDB.from_orm(category)


@router.get(
    '/{category_id}',
    response_model=CategoryInDB
)
def get_category(
    *,
    db: Session = Depends(deps.get_db),
    category: Category = Depends(check_category_exist)
):
    logger.info(f"Fetched the category. (id={category.id})")
    return CategoryInDB.from_orm(category)


@router.put(
    '/{category_id}',
    response_model=CategoryInDB
)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category: Category = Depends(check_category_exist),
    category_in: CategoryUpdate
):
    category = crud.category.update(db=db, db_obj=category, obj_in=category_in)
    logger.info(f"Updated the category. (id={category.id})")
    return CategoryInDB.from_orm(category)


@router.delete(
    '/{category_id}'
)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category: Category = Depends(check_category_exist)
):
    crud.category.remove(db=db, id=category.id)
    logger.info(f"Removed the category. (id={category.id})")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
