from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import ChatRequest

from app.services.conversation_service import process_chat

router = APIRouter()


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    try:
        result = process_chat(
            db,
            request.message,
            request.conversation_id
        )
    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    
    return result
