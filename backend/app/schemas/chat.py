from pydantic import BaseModel
from typing import List

from app.schemas.messages import MessageResponse


class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None


class ConversationResponse(BaseModel):

    id: int
    title: str
    messages: List[MessageResponse]

    class Config:
        from_attributes = True
