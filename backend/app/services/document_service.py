import os
import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.rag.loader import load_pdf
from app.rag.text_splitter import split_documents
from app.models.document_chunk import DocumentChunk
from app.rag.embeddings import generate_embeddings


async def upload_document(
    db: Session,
    file: UploadFile
):

    # Carpeta donde se guardarán los PDFs
    upload_dir = "app/uploads"

    # Crea la carpeta si no existe
    os.makedirs(upload_dir, exist_ok=True)

    # Ruta completa del archivo
    file_path = os.path.join(upload_dir, file.filename)

    # Guarda el PDF en el disco
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Guarda la información del documento en la base de datos
    document = Document(
        filename=file.filename,
        filepath=file_path
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Lee el PDF
    langchain_documents = load_pdf(file_path)

    # Divide el documento en chunks
    chunks = split_documents(langchain_documents)

    embeddings = generate_embeddings(chunks)

    for chunk, embedding in zip(chunks, embeddings):

        document_chunk = DocumentChunk(
        content=chunk.page_content,
        embedding=embedding,
        document_id=document.id
    )
        db.add(document_chunk)
        
    db.commit()

    return {
        "message": "Document uploaded successfully.",
        "document_id": document.id,
        "filename": document.filename
    }