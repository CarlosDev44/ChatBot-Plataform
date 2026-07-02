from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.db.init_db import init_db
from app.api import conversations

app = FastAPI()

init_db()

app.include_router(conversations.router)
app.include_router(chat_router)
