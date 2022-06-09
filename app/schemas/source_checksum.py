from datetime import datetime

from pydantic import BaseModel


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

    class Config:
        orm_mode = True
