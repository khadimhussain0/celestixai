from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String, unique=True, nullable=True)
    filename = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="model")
    model_constellation_id = Column(Integer, ForeignKey('model_constellation.id'))
    model_constellation = relationship("ModelConstellation", back_populates="model")
    fine_tuned_model_path = Column(String, nullable=True)
    fine_tuned = Column(Boolean, nullable=True)
    train = Column(Boolean, nullable=True)
    model_name = Column(String, index=True)
    parameters = Column(String, index=True)
    is_vision = Column(Boolean, default=False)
    custom_name = Column(String, nullable=False)
    deploy = Column(Boolean, default=False)

    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="model")