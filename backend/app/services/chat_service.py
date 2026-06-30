from app.services.groq_client import client
from app.config.config import MODEL


def send_message(history):

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