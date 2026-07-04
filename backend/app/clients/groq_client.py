from groq import Groq
from app.config.config import GROQ_API_KEY


#Crea y retorna un cliente de Groq utilizando la clave de API configurada.
#Si la clave de API no está configurada, se lanza un error en tiempo de ejecución.    
def get_client():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    return Groq(api_key=GROQ_API_KEY)
