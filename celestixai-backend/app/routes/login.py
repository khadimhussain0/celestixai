from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.auth import create_jwt_token, verify_password
from app.schemas.user import Token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post("/")
def login(user_login: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_login.username).first()

    if not db_user or not verify_password(user_login.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token and include it in the response
    token_data = {"sub": str(db_user.id)}
    token = create_jwt_token(token_data)

    return Token(access_token=token, token_type="Bearer")
