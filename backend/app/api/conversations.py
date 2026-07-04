from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import ConversationResponse
from app.services import conversation_service
from fastapi import HTTPException

#Router encargado de gestionar las peticiones relacionadas con las conversaciones.

router = APIRouter()

#Obtiene todas las conversaciones almacenadas en la base de datos y las devuelve como una lista de objetos de respuesta de conversación.
@router.get(
    "/conversations",
    response_model=list[ConversationResponse]
)
def get_conversations(
    db: Session = Depends(get_db)
):

    return conversation_service.get_conversations(db)

#Obtiene una conversación específica por su ID. Si la conversación no se encuentra, lanza una excepción HTTP con un código de estado 404 (No encontrado).
@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse
)
def get_conversation_by_id(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    #Busca la conversacion en la base de datos utilizando el servicio de conversación.
    conversation = conversation_service.get_conversation(db, conversation_id)

    #Si no existe se lanza una excepción HTTP con un código de estado 404 (No encontrado) y un mensaje de error.
    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    #Devuelve la conversación encontrada si todo ha ido bien.
    return conversation

#Elimina una conversación específica por su ID. Si la conversación no se encuentra, lanza una excepción HTTP con un código de estado 404 (No encontrado).
@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    
    #Busca la conversación antes de borrarla.
    conversation = conversation_service.get_conversation(db, conversation_id)

    #Si no se encuentra lanza una excepción HTTP con un código de estado 404 (No encontrado) y un mensaje de error.
    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    conversation_service.delete_conversation(db, conversation)

    #Devuelve un mensaje de éxito si la conversación se ha eliminado correctamente.
    return {"message": "Conversation deleted successfully."}
