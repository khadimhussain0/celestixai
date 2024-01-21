from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import User
from datetime import datetime


class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # owner = relationship("User", back_populates="datasets")
    uuid = Column(String, unique=True, index=True)
    filename = Column(String, index=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow)
    file_size = Column(Integer)
