from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship

# Esta clase representa la tabla "conversations" en la base de datos
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    messages = relationship("Message", back_populates="conversation", cascade = "all, delete-orphan")

    #Relationship es para establecer una relación entre la tabla "conversations" y la tabla "messages".
    #Cascade es para que cuando se elimine una conversación, se eliminen todos los mensajes asociados a esa conversación.