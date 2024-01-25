from pydantic import BaseModel
from app.utils.as_form import as_form


class ModelConstellation(BaseModel):
    uuid: str
    icon_uuid: str
    model_name: str
    filename: str
    file_size: int
    parameters: str
    model_class: str
    model_task: str

    class Config:
        orm_mode = True


@as_form
class ModelConstellationCreate(BaseModel):
    model_name: str
    parameters: str
    model_class: str
    model_task: str

    class Config:
        orm_mode = True


class ModelConstellationRead(BaseModel):
    id: int
    uuid: str
    icon_uuid: str
    icon_filename: str
    model_name: str
    filename: str
    parameters: str
    model_class: str
    model_task: str

    class Config:
        orm_mode = True
