from pydantic import BaseModel
from typing import List

from app.schemas.messages import MessageResponse


class ConversationResponse(BaseModel):

    id: int
    title: str
    message: List[MessageResponse]

    class Config:
        from_attributes = True