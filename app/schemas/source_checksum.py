from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SourceChecksumBase(BaseModel):
    source: str
    checksum: str
    checked_at: datetime


class SourceChecksumCreate(SourceChecksumBase):
    pass


class SourceChecksumUpdate(BaseModel):
    source: Optional[str] = Field(nullable=True)
    checksum: Optional[str] = Field(nullable=True)
    checked_at: Optional[datetime] = Field(nullable=True)


class SourceChecksumInDB(SourceChecksumBase):
    id: int

    class Config:
        orm_mode = True
