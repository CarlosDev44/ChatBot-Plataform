from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import ChatRequest

from app.services.conversation_service import process_chat

#Router encargado de gestionar las peticiones relacionadas con el chat.

router = APIRouter()

#Endpoint para procesar un mensaje de chat. Recibe un mensaje y un ID de conversación, y devuelve la respuesta generada por el modelo de lenguaje.
@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    #Delega el procesamiento del chat al servicio de conversación y maneja posibles errores.
    try:
        result = process_chat(
            db,
            request.message,
            request.conversation_id
        )
    #Si ocurre un error de tiempo de ejecución durante el procesamiento del chat, se lanza una excepción HTTP
    #con un código de estado 503 (Servicio no disponible) y el detalle del error.    
    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error

    #Si no se encuentra la conversación correspondiente al ID proporcionado, se lanza una excepción HTTP
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    #Devuelve la respuesta generada por el modelo de lenguaje si todo ha ido bien.
    return result
