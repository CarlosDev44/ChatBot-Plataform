from app.models.chat import ChatRequest
from fastapi import APIRouter
from app.services.chat_service import send_message

router = APIRouter()

@router.post("/chat")
def chat(request: ChatRequest):
    response = send_message(request.message)
    return {"response": response}