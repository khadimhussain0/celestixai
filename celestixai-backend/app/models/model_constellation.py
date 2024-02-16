from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class ModelConstellation(Base):
    __tablename__ = "model_constellation"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String, unique=True, index=True)
    icon_uuid = Column(String, index=True)
    icon_filename = Column(String, index=True)
    filename = Column(String, index=True)
    model_name = Column(String, index=True)
    ollama_name = Column(String, nullable=True)
    hf_id = Column(String, nullable=True)
    parameters = Column(String, index=True)
    model_class = Column(String, nullable=True, server_default=None)
    model_task = Column(String, nullable=True)
    file_size = Column(Integer)
    is_vision = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow)

    model = relationship("Model", back_populates="model_constellation")
