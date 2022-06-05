from typing import Any, List

from app.api import deps
from app.models import Product
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/')
def get_items(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    products = db.query(Product).offset(skip).limit(limit).all()
    return products
