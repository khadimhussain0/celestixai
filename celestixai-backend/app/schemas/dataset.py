from pydantic import BaseModel
from datetime import datetime


class DatasetBase(BaseModel):
    uuid: str
    filename: str
    file_size: int

    class Config:
        orm_mode = True


class DatasetCreate(DatasetBase):
    pass


class DatasetRead(DatasetBase):
    id: int
    created_date: datetime
    updated_date: datetime
