from pydantic import BaseModel
from datetime import datetime


class ModelBase(BaseModel):

    class Config:
        orm_mode = True

