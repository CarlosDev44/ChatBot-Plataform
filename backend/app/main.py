from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.db.init_db import init_db
from app.api import conversations

# Crea la aplicación principal de FastAPI.
app = FastAPI()

# Se utiliza para inicializar la base de datos creando todas las tablas definidas en los modelos.
init_db()

# Registra los routers de la aplicación.
app.include_router(conversations.router)
app.include_router(chat_router)
