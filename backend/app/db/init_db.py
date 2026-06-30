from app.db.database import Base, engine
from app.models.conversation import Conversation
from app.models.messages import Message

def init_db():
    Base.metadata.create_all(bind=engine)