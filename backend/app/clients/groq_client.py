from groq import Groq
from app.config.config import GROQ_API_KEY


def get_client():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    return Groq(api_key=GROQ_API_KEY)
