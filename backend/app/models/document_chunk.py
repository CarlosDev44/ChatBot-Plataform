from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from pgvector.sqlalchemy import Vector

from app.db.database import Base


class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)

    embedding = Column(Vector(384))

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )