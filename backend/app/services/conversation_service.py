from app.models.conversation import Conversation
from app.models.messages import Message
from app.services.chat_service import send_message, stream_message
from app.rag.embeddings import generate_query_embedding
from app.rag.retriever import retrieve_chunks

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
def get_ai_response(history, context):

    return send_message(
        history,
        context
    )

# Procesa un mensaje de chat, lo guarda en la conversación correspondiente y devuelve la respuesta generada.
def process_chat(db, message, conversation_id):

    # Obtener la conversación si existe
    if conversation_id is None:
        conversation = None

    else:

        conversation = get_conversation(
            db,
            conversation_id
        )

        if conversation is None:
            return None

    # Construir el historial
    history = build_history(conversation) if conversation else []

    # Generar el embedding de la pregunta
    query_embedding = generate_query_embedding(message)

    # Recuperar los chunks más relevantes
    chunks = retrieve_chunks(
        db,
        query_embedding
    )

    # ===== DEPURACIÓN =====
    print("\n===== CHUNKS RECUPERADOS =====\n")

    for i, chunk in enumerate(chunks, start=1):
        print(f"===== Chunk {i} =====")
        print(chunk.content)
        print("-" * 80)

    # Construir el contexto
    context = "\n\n".join(
        chunk.content
        for chunk in chunks
    )

    # ===== DEPURACIÓN =====
    print("\n===== CONTEXTO ENVIADO AL LLM =====\n")
    print(context)
    print("\n===============================\n")

    # Agregar el mensaje del usuario al historial
    history.append({
        "role": "user",
        "content": message
    })

    # Obtener la respuesta del modelo
    response = get_ai_response(
        history,
        context
    )

    # Si la conversación no existía, crearla
    if conversation is None:

        conversation = create_conversation(
            db,
            message
        )

    # Guardar el mensaje del usuario
    save_message(
        db,
        conversation.id,
        message,
        "user"
    )

    # Guardar la respuesta del asistente
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


def process_chat_stream(db, message, conversation_id):

    if conversation_id is None:
        conversation = create_conversation(
            db,
            message
        )

    else:

        conversation = get_conversation(
            db,
            conversation_id
        )

        if conversation is None:
            return None

    history = build_history(conversation)

    query_embedding = generate_query_embedding(message)

    chunks = retrieve_chunks(
        db,
        query_embedding
    )

    print("\n===== CHUNKS RECUPERADOS =====\n")

    for i, chunk in enumerate(chunks, start=1):
        print(f"===== Chunk {i} =====")
        print(chunk.content)
        print("-" * 80)

    context = "\n\n".join(
        chunk.content
        for chunk in chunks
    )

    print("\n===== CONTEXTO ENVIADO AL LLM =====\n")
    print(context)
    print("\n===============================\n")

    history.append({
        "role": "user",
        "content": message
    })

    save_message(
        db,
        conversation.id,
        message,
        "user"
    )

    def generator():
        response_parts = []

        for token in stream_message(history, context):
            response_parts.append(token)
            yield token

        save_message(
            db,
            conversation.id,
            "".join(response_parts),
            "assistant"
        )

    return {
        "conversation_id": conversation.id,
        "stream": generator()
    }
# Obtiene todas las conversaciones almacenadas en la base de datos.
def get_conversations(db):

    conversations = db.query(Conversation).all()

    return conversations

# Elimina una conversación de la base de datos.
def delete_conversation(db, conversation):

    db.delete(conversation)
    db.commit()
