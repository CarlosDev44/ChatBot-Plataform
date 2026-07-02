from fastapi import APIRouter, Depends
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

    return process_chat(
        db,
        request.message,
        request.conversation_id
    )