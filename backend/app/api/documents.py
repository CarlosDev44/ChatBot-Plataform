from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services import document_service


router = APIRouter()


@router.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await document_service.upload_document(db, file)
