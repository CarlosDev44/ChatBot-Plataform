from email.message import Message

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest
from app.services.chat_service import send_message
from app.db.dependencies import get_db
from app.models.conversation import Conversation


router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    if request.conversation_id is None:
        conversation = Conversation(title = request.message)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    else:
        conversation = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()

    message = Message(conversation_id=conversation.id, content=request.message, role="user")
    db.add(message)
    db.commit()
    db.refresh(message)

    response = send_message(request.message)

    assistant_message = Message(conversation_id = conversation.id, content=response, role="assistant")
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {"response": response}