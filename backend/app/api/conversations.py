from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import ConversationResponse
from app.services import conversation_service
from fastapi import HTTPException

router = APIRouter()


@router.get(
    "/conversations",
    response_model=list[ConversationResponse]
)
def get_conversations(
    db: Session = Depends(get_db)
):

    return conversation_service.get_conversations(db)

@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse
)
def get_conversation_by_id(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    
    conversation = conversation_service.get_conversation(db, conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    return conversation

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    conversation = conversation_service.get_conversation(db, conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    conversation_service.delete_conversation(db, conversation)

    return {"message": "Conversation deleted successfully."}
