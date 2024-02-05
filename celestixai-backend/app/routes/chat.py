from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.chat import Chat
from app.schemas.chat import ChatRequest
import uuid
from typing import List
import json
import datetime
from pytz import utc

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def create_chat(
    form_data: ChatRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    print(form_data)
    chat = Chat(
        user_id=current_user.id,
        title=form_data.chat_title,
        chat=json.dumps({form_data}),
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)
    ml_str = """"""
    data = json.loads(ml_str)
    print(data)
    print(type(data))
    return {"message": "chat added"}
