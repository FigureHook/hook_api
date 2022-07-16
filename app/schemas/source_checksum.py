from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SourceChecksumBase(BaseModel):
    source: str
    checksum: str
    checked_at: datetime


class SourceChecksumCreate(SourceChecksumBase):
    pass


class SourceChecksumUpdate(BaseModel):
    source: Optional[str]
    checksum: Optional[str]
    checked_at: Optional[datetime]


class SourceChecksumInDB(SourceChecksumBase):
    id: int

    class Config:
        orm_mode = True
