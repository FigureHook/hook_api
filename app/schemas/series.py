from pydantic import BaseModel


class SeriesBase(BaseModel):
    name: str


class SeriesCreate(SeriesBase):
    pass


class SeriesUpdate(SeriesBase):
    pass


class SeriesInDB(SeriesBase):
    id: int
