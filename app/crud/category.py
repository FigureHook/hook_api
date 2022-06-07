from app.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


category = CRUDCategory(Category)
