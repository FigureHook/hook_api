from pydantic import BaseModel
from datetime import datetime


class SourceChecksumBase(BaseModel):
    source: str
    checksum: str
    checked_at: datetime


class SourceChecksumCreate(SourceChecksumBase):
    pass


class SourceChecksumUpdate(SourceChecksumBase):
    pass


class SourceChecksumInDB(SourceChecksumBase):
    id: int
