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
        from_attributes = True
        protected_namespaces = ()


@as_form
class ModelConstellationCreate(BaseModel):
    model_name: str
    ollama_name: str
    hf_id: str
    parameters: str
    model_class: str
    model_task: str
    is_vision: bool

    class Config:
        from_attributes = True
        protected_namespaces = ()


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
    is_vision: bool

    class Config:
        from_attributes = True
        protected_namespaces = ()
