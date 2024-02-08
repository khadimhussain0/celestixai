from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.chat import Chat
from app.schemas.chat import ChatMessage, ChatRequest
import time
import json


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/new")
def create_new_chat(
    form_data: ChatRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = Chat(
        user_id=current_user.id,
        model_name=form_data.model,
        model_id=form_data.model_id,
        title=form_data.chat_title,
        chat=json.dumps(form_data.dict()),
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return {"message": "chat added", "status_code":200}


@router.post("/")
def chat(
    form_data: ChatRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    chat_id = form_data.chat_id
    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat_messages = json.loads(chat.chat)
    chat_messages["messages"].append(form_data.messages[0].dict())

    chat.chat = json.dumps(chat_messages)
    db.commit()
    db.refresh(chat)

    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    chat_messages = json.loads(chat.chat)
    messages = chat_messages["messages"]

    modified_messages = []
    for message in messages:
        modified_message = message.copy()
        modified_message.pop('message_id')
        modified_messages.append(modified_message)

    model_input = {
        "model": form_data.model,
        "messages": modified_messages
    }

    # Stub function to process model output
    def process_model_output(model_input):
        return {
            "response": {
                "content": "This is model response"
            }
        }

    model_response = process_model_output(model_input)

    assistant_message = ChatMessage(
        role="assistant",
        content=model_response["response"]["content"],
        message_id=int(time.time() * 1000)
    )

    chat_messages["messages"].append(assistant_message.dict())
    chat.chat = json.dumps(chat_messages)
    db.commit()
    db.refresh(chat)

    return assistant_message
