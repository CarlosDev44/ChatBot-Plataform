import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import ChatRequest

from app.services.conversation_service import process_chat, process_chat_stream

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


@router.post("/chat/stream")
def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    try:
        result = process_chat_stream(
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

    def event_stream():
        yield f"data: {json.dumps({'type': 'meta', 'conversation_id': result['conversation_id']})}\n\n"

        for token in result["stream"]:
            yield f"data: {json.dumps({'type': 'delta', 'content': token})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
