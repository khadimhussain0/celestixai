from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.chat import Chat
from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse
import time
import json
from typing import List


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.chat import Chat
from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse
import time
import json
from typing import List

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    form_data: ChatRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_id = form_data.chat_id

    # If chat_id is 0 or not provided, create a new chat
    if not chat_id:
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

        # Read the newly created chat content
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

    else:
        # If chat_id is provided, process the existing chat
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        chat_messages = json.loads(chat.chat)
        chat_messages["messages"].append(form_data.messages[0].dict())

        chat.chat = json.dumps(chat_messages)
        db.commit()
        db.refresh(chat)

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


@router.get("/", response_model=List[ChatResponse])
def get_chats(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).all()

    if not chats:
        raise HTTPException(status_code=404, detail="Chat not found")

    chats_ = []
    for chat in chats:
        chat_messages = json.loads(chat.chat)
        chat_messages["chat_id"] = chat.id
        chats_.append(chat_messages)

    return chats_


@router.delete("/delete-all")
def delete_all_chats(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.query(Chat).filter(Chat.user_id == current_user.id).delete()
    db.commit()
    return {"message": "All chats deleted successfully"}


@router.delete("/{chat_id}")
def delete_chat_by_id(
    chat_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(chat)
    db.commit()
    return {"message": f"Chat with ID {chat_id} deleted successfully"}
