from pydantic import BaseModel
from datetime import datetime


class ModelBase(BaseModel):

    class Config:
        orm_mode = True


class ModelCreate(ModelBase):
    id: int


class ModelRead(ModelBase):
    id: int
    model_name: str
    created_date: datetime
    updated_date: datetime


class ModelUpdateParameters(BaseModel):
    model_name: str
