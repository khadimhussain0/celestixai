from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from passlib.context import CryptContext

# CryptContext for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, default="")
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    dataset = relationship("Dataset", back_populates="owner")
    model = relationship("Model", back_populates="user")
    chat = relationship("Chat", back_populates="user")

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)
