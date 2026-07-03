from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import ConversationResponse
from app.services.conversation_service import get_conversation, get_conversations


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