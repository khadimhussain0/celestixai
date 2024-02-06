from typing import List, Dict, Union, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    message_id: str
    role: str
    content: str
    images: Optional[List[bytes]] = []


class ChatRequest(BaseModel):
    model: str
    model_id: int
    timestamp: int
    chat_id: int
    chat_title: str
    messages: List[ChatMessage]


# # Example usage:
# request_data = {
#     "model": "model name",
#     "timestamp": 390238390843,
#     "chat_id": 3,
#     "chat_title":"new chat"
#     "messages": [
#         {
#             'role': 'user',
#             'content': 'Why is the sky blue?',
#             "message_id": "uuid"
#             'images': ["image in bytes"]
#         },
#     ]
# }

# # Validate the request data using the Pydantic schema
# chat_request = ChatRequest(**request_data)
# print(chat_request.dict())
