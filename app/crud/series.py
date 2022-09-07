from app.models import Series
from app.schemas.series import SeriesCreate, SeriesUpdate

from .base import CRUDBase


class CRUDCategory(CRUDBase[Series, SeriesCreate, SeriesUpdate]):
    pass


series = CRUDCategory(Series)
