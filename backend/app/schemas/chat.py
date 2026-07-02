from pydantic import BaseModel


class ConversationResponse(BaseModel):

    id: int
    title: str

    class Config:
        from_attributes = True