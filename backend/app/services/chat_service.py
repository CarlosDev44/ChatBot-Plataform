from backend.app.clients.groq_client import get_client
from app.config.config import MODEL


def send_message(history):

    client = get_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ] + history
    )

    return response.choices[0].message.content
