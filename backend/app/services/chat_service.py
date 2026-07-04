from backend.app.clients.groq_client import get_client
from app.config.config import MODEL

# Esta función se utiliza para enviar un mensaje al modelo de lenguaje y obtener una respuesta.
def send_message(history):

    # Client es una instancia del cliente de Groq que se utiliza para interactuar con el modelo de lenguaje.
    client = get_client()

    # Response es la respuesta que se obtiene del modelo de lenguaje después de enviar el mensaje.
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ] + history # Se utiliza para enviar el historial de mensajes al modelo de lenguaje para que pueda generar una respuesta coherente basada en el contexto de la conversación.
    )


    # Devuelve el contenido del primer mensaje de la respuesta del modelo de lenguaje.
    return response.choices[0].message.content
