from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


def retrieve_chunks(
    db: Session,
    query_embedding,
    k: int = 10
):
    chunks = (
        db.query(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(query_embedding)
        )
        .limit(k)
        .all()
    )

    return chunks