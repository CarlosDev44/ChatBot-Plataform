from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest
from app.services.chat_service import send_message
from app.db.dependencies import get_db
from app.models.conversation import Conversation


router = APIRouter()


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    conversation = Conversation(title = request.message)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    response = send_message(request.message)
    return {"response": response}