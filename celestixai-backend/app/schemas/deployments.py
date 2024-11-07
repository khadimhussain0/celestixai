from pydantic import BaseModel
from datetime import datetime


class ModelBase(BaseModel):

    class Config:
        from_attributes = True

