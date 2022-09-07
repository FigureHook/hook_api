from app.models import SourceChecksum
from app.schemas.source_checksum import (SourceChecksumCreate,
                                         SourceChecksumUpdate)
from sqlalchemy.orm import Session
from .base import CRUDBase
from typing import List


class CRUDSourceChecksum(CRUDBase[SourceChecksum, SourceChecksumCreate, SourceChecksumUpdate]):
    def get_multi_filter_by_source(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        source: str
    ) -> List[SourceChecksum]:
        return db.query(self.model).filter(
            self.model.source.ilike(f"%{source}%")
        ).offset(skip).limit(limit).all()


source_checksum = CRUDSourceChecksum(SourceChecksum)
