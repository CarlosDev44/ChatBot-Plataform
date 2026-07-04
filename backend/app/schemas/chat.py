from pydantic import BaseModel
from typing import List

from app.schemas.messages import MessageResponse

# Esta clase representa la solicitud de chat que se envía desde el cliente al servidor.
class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None

# Esta clase representa la respuesta de chat que se envía desde el servidor al cliente.
class ConversationResponse(BaseModel):

    id: int
    title: str
    messages: List[MessageResponse]

    class Config:
        from_attributes = True
