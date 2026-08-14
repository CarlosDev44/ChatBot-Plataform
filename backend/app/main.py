from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.db.init_db import init_db
from app.api import conversations
from app.api.documents import router as document_router

# Crea la aplicación principal de FastAPI.
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Se utiliza para inicializar la base de datos creando todas las tablas definidas en los modelos.
init_db()

# Registra los routers de la aplicación.
app.include_router(conversations.router)
app.include_router(chat_router)
app.include_router(document_router)
