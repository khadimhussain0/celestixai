from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(UserCreate):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
