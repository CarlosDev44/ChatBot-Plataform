from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import ConversationResponse
from app.services.conversation_service import delete_conversations, get_conversation, get_conversations


router = APIRouter()


@router.get(
    "/conversations",
    response_model=list[ConversationResponse]
)
def conversations(
    db: Session = Depends(get_db)
):

    return get_conversations(db)

@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse
)
def conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):

    return get_conversation(db, conversation_id)

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    delete_conversations(db, conversation_id)

    return {"message": "Conversation deleted successfully."}