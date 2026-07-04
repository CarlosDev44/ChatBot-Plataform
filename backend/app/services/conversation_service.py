from app.models.conversation import Conversation
from app.models.messages import Message
from app.services.chat_service import send_message

# Módulo encargado de gestionar la lógica de conversaciones y mensajes del chat.

# Crea una nueva conversación en la base de datos con el título proporcionado.
def create_conversation(db, title):

    conversation = Conversation(title=title)

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

# Obtiene una conversación específica a partir de su identificador.
def get_conversation(db, conversation_id):

    return db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()

# Guarda un mensaje asociado a una conversación en la base de datos.
def save_message(db, conversation_id, content, role):

    message = Message(
        conversation_id=conversation_id,
        content=content,
        role=role
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message

# Construye el historial de mensajes de una conversación en el formato esperado por el modelo de IA.
def build_history(conversation):

    history = []

    for message in conversation.messages:
        history.append({
            "role": message.role,
            "content": message.content
        })

    return history

# Solicita una respuesta al servicio de IA utilizando el historial de mensajes.
def get_ai_response(history):

    return send_message(history)

# Procesa un mensaje de chat, lo guarda en la conversación correspondiente y devuelve la respuesta generada.
def process_chat(db, message, conversation_id):

    if conversation_id is None:
        conversation = None

    else:

        conversation = get_conversation(
            db,
            conversation_id
        )

        if conversation is None:
            return None

    history = build_history(conversation) if conversation else []
    history.append({
        "role": "user",
        "content": message
    })

    response = get_ai_response(history)

    if conversation is None:
        conversation = create_conversation(
            db,
            message
        )

    save_message(
        db,
        conversation.id,
        message,
        "user"
    )

    save_message(
        db,
        conversation.id,
        response,
        "assistant"
    )

    return {
        "response": response,
        "conversation_id": conversation.id
    }

# Obtiene todas las conversaciones almacenadas en la base de datos.
def get_conversations(db):

    conversations = db.query(Conversation).all()

    return conversations

# Elimina una conversación de la base de datos.
def delete_conversation(db, conversation):

    db.delete(conversation)
    db.commit()
