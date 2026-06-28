import os
from dotenv import load_dotenv

# carga el archivo .env
load_dotenv()

# variables del proyecto
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
MODEL = os.getenv("MODEL")