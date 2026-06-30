from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest
from app.services.chat_service import send_message
from app.db.dependencies import get_db
from app.models.conversation import Conversation
from app.models.messages import Message


router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    if request.conversation_id is None:
        conversation = Conversation(title = request.message)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    else:
        conversation = db.get(Conversation, request.conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")

    user_message = Message(conversation_id=conversation.id, content=request.message, role="user")
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    history = []
    
    for message in conversation.messages:
        history.append({"role": message.role, "content": message.content})
    response = send_message(history)

    assistant_message = Message(conversation_id = conversation.id, content=response, role="assistant")
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {"response": response, "conversation_id": conversation.id}