from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import OLLAMA_SERVER_URL
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.chat import Chat
from app.models.models import Model
from app.models.model_constellation import ModelConstellation
from app.schemas.chat import ChatRequest, ChatResponse, AssistantChatMessage
from app.core.config import OLLAMA_SERVER_URL, QDRANT_SERVER_URL
from app.utils.preprocess_chat_messages import base64_to_bytes
from app.services.retreiver import RAGChat
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
import time
import json
from typing import List
from ollama import Client

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=AssistantChatMessage)
def chat(
    form_data: ChatRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    client = Client(host=OLLAMA_SERVER_URL)

    models_metadata = db.query(
        Model.id,
        ModelConstellation.is_vision,
        ModelConstellation.ollama_name
    ).join(
        ModelConstellation, ModelConstellation.id == Model.model_constellation_id
    ).filter(
        Model.id == form_data.model_id
    ).first()

    chat_id = form_data.chat_id
    rag = form_data.rag
    start = time.time()
    
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

        chat_messages = json.loads(chat.chat)
        messages = chat_messages["messages"]
        modified_messages = preprocess_messages(messages, models_metadata)

        if rag:
            rag_chat_instance = RAGChat(OllamaEmbeddings(base_url=OLLAMA_SERVER_URL, model="nomic-embed-text"),
                                        Ollama(base_url=OLLAMA_SERVER_URL, model=models_metadata.ollama_name))
            model_response, docs = rag_chat_instance.ask_question(query=form_data.messages[0].content, 
                                                            qdrant_url=QDRANT_SERVER_URL,
                                                            collection_name=str(current_user.id))
            model_response = {"message":{"content": model_response}}
        else:
            model_response = client.chat(model=models_metadata.ollama_name, messages=modified_messages)

        assistant_message = AssistantChatMessage(
            chat_id=chat.id,
            role="assistant",
            content=model_response['message']['content'],
            message_id=int(time.time() * 1000)
        )

        chat_messages["messages"].append(assistant_message.dict())
        chat.chat = json.dumps(chat_messages)
        db.commit()
        db.refresh(chat)

        return assistant_message

    else:
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        chat_messages = json.loads(chat.chat)
        chat_messages["messages"].append(form_data.messages[0].dict())

        chat.chat = json.dumps(chat_messages)
        db.commit()
        db.refresh(chat)

        messages = chat_messages["messages"]
        modified_messages = preprocess_messages(messages, models_metadata)

        if rag:
            rag_chat_instance = RAGChat(OllamaEmbeddings(base_url=OLLAMA_SERVER_URL, model="nomic-embed-text"),
                                        Ollama(base_url=OLLAMA_SERVER_URL, model=models_metadata.ollama_name))
            model_response, docs = rag_chat_instance.ask_question(query=form_data.messages[0].content, 
                                                            qdrant_url=QDRANT_SERVER_URL,
                                                            collection_name=str(current_user.id))
            model_response = {"message":{"content": model_response}}
        else:
            model_response = client.chat(model=models_metadata.ollama_name, messages=modified_messages)

        assistant_message = AssistantChatMessage(
            chat_id=chat.id,
            role="assistant",
            content=model_response['message']['content'],
            message_id=int(time.time() * 1000)
        )

        chat_messages["messages"].append(assistant_message.dict())
        chat.chat = json.dumps(chat_messages)
        db.commit()
        db.refresh(chat)

        print("Took (s): ", time.time()-start)
        return assistant_message


def preprocess_messages(messages, models_metadata):
    modified_messages = []
    for message in messages:
        modified_message = message.copy()
        modified_message.pop('message_id')
        try:
            modified_message["images"] = [base64_to_bytes(modified_message["images"][0])]
        except Exception as e:
            print(f"Exception occurred: {e}")
        if not models_metadata.is_vision:
            modified_message.pop("images")
        modified_messages.append(modified_message)
    return modified_messages


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
