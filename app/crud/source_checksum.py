from app.models import SourceChecksum
from app.schemas.source_checksum import (SourceChecksumCreate,
                                         SourceChecksumUpdate)

from .base import CRUDBase


class CRUDSourceChecksum(CRUDBase[SourceChecksum, SourceChecksumCreate, SourceChecksumUpdate]):
    pass


source_checksum = CRUDSourceChecksum(SourceChecksum)
