from app.models import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

from .base import CRUDBase


class CRUDCategory(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    pass


company = CRUDCategory(Company)
