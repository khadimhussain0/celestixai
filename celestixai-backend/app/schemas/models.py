from pydantic import BaseModel
from datetime import datetime


class ModelBase(BaseModel):

    class Config:
        orm_mode = True


class ModelCreate(ModelBase):
    id: int


class ModelRead(ModelBase):
    id: int
    custom_name: str
    is_vision: bool
    created_date: datetime
    updated_date: datetime


class ModelUpdateParameters(BaseModel):
    model_name: str


class ModelsRead(BaseModel):
    id: int
    uuid: str
    icon_uuid: str
    icon_filename: str
    custom_name: str
    filename: str
    parameters: str
    model_class: str
    model_task: str
    is_vision: bool

    class Config:
        orm_mode = True
