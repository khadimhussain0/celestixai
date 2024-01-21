from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(UserCreate):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
