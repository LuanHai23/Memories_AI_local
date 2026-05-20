from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Document, DocumentChunk
from app.services.document_service import DocumentService
from app.schema.document_schema import (
    DocumentUploadResponse,
    DocumentInfo,
    ChunkInfo
)


# Router cho nhóm API doc
router = APIRouter()

document_service = DocumentService()

# Endpoint này dùng để upload tài liệu
@router.post("/upload", response_model = DocumentUploadResponse)
def upload_document(
    user_id: str = Form("default_user"),
    file: UploadFile = File(),
    db: Session = Depends(get_db)
):
    try:
        file_path, file_type, raw_text, chunks = document_service.process_upload_file(file)

        # Nếu file không parse ra text hoặc text rỗng
        if not raw_text.strip():
            raise HTTPExeption(
                status_code = 400,
                detail="Could not extract text from this document"
            )
        
        # Tạo document record
        document = Document(
            user_id = user_id,
            file_name = file.filename,
            file_type = file_type,
            file_path = file_path,
            total_characters = len(raw_text),
            total_chunks = len(chunks)
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        # Lưu từng chunk vào bảng document_chunks
        for index, chunk_text in enumerate(chunks):
            chunk = DocumentChunk(
                document_id = document.id,
                user_id = user_id,
                chunk_index = index,
                content = chunk_text,
                char_count = len(chunk_text),
                source_file = file.filename
            )

            db.add(chunk)
        db.commit()

        return DocumentUploadResponse(
            document_id=document.id,
            file_name = document.file_name,
            file_type = document.file_type,
            total_characters = document.total_characters,
            total_chunks = document.total_chunks,
            message = "Document uploaded and chunked successfully"
        )
    
    except ValueError as e:
        raise HTTPExeption(
            status_code = 400,
            detail = str(e)
        )
    
    except Exception as e:
        raise HTTPExeption(
            status_code = 500,
            detail = f"Document upploaod failed: {str(e)}"
        )

@router.get("/", response_model  = List[DocumentInfo])
def list_documents(user_id: str = "default_user", db: Session = Depends(get_db)):
    # return {"message": "Documents API is ready"}
    documents = (
        db.query(Document)
        .filter(Document.user_id == user_id)
        .order_by(Document.create_at.desc())
        .all()
    )    

    return documents

@router.get("/{document_id}/chunks", response_model = List[ChunkInfo])
def list_document_chunks(document_id: int, db: Session = Depends(get_db)):
    chunks = (
        db.query(DocumentChunk)
        .filter(Document.document_id == document_id)
        .order_by(DocumentChunk.chunk_index.asc())
        .all()
    )

    return chunks