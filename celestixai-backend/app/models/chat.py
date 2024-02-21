from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import json
from datetime import datetime


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="chat")
    title = Column(String)
    model_id = Column(Integer, ForeignKey("model.id"))
    model = relationship("Model", back_populates="chat")
    model_name = Column(String)
    chat = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def save_chat_data(self, data):
        self.chat = json.dumps(data)
        self.updated_at = func.now()

    def get_chat_data(self):
        return json.loads(self.chat)

    @property
    def timestamp_epoch(self):
        return int((self.created_at - datetime(1970, 1, 1)).total_seconds())
