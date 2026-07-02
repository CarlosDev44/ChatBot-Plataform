from app.models.conversation import Conversation
from app.models.messages import Message
from app.services.chat_service import send_message


def create_conversation(db, title):

    conversation = Conversation(title=title)

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversation(db, conversation_id):

    return db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()


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


def build_history(conversation):

    history = []

    for message in conversation.messages:
        history.append({
            "role": message.role,
            "content": message.content
        })

    return history


def get_ai_response(history):

    return send_message(history)


def process_chat(db, message, conversation_id):

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

    save_message(
        db,
        conversation.id,
        message,
        "user"
    )

    history = build_history(conversation)

    response = get_ai_response(history)

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