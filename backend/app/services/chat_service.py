from app.clients.groq_client import get_client
from app.config.config import MODEL


def send_message(history, context):

    client = get_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"""
You are a helpful assistant.

Answer the user's questions using ONLY the information provided in the context.

If the answer is not contained in the context, say that you don't know.

Context:
{context}
"""
            }
        ] + history
    )

    return response.choices[0].message.content


def stream_message(history, context):

    client = get_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"""
You are a helpful assistant.

Answer the user's questions using ONLY the information provided in the context.

If the answer is not contained in the context, say that you don't know.

Context:
{context}
"""
            }
        ] + history,
        stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content
