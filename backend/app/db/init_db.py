from app.db.database import Base, engine
from app.models.conversation import Conversation
from app.models.messages import Message

# Esta función se utiliza para inicializar la base de datos creando todas las tablas definidas en los modelos. vc
def init_db():
    Base.metadata.create_all(bind=engine)