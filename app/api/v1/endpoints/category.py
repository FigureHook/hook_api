from app.models import Category
from app.api import deps
from app import crud
from app.schemas.category import CategoryCreate, CategoryInDB, CategoryUpdate
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

router = APIRouter()


def check_category_exist(category_id: int, db: Session = Depends(deps.get_db)) -> Category:
    category = crud.category.get(db=db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified category(id: {category_id}) didn't exist."
        )
    return category


@router.get('/', response_model=list[CategoryInDB])
def get_categories(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    categories = crud.category.get_multi(db=db, skip=skip, limit=limit)
    return [
        CategoryInDB.from_orm(category)
        for category in categories
    ]


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
    category = db.query(Category).filter(
        Category.name == category_in.name
    ).first()

    if category:
        return RedirectResponse(
            url=request.url_for('get_category', category_id=category.id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    category = crud.category.create(db=db, obj_in=category_in)
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
    return CategoryInDB.from_orm(category)


@router.delete(
    '/{category_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category: Category = Depends(check_category_exist)
):
    crud.category.remove(db=db, id=category.id)