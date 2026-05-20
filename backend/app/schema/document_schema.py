from pydantic import BaseModel
from typing import List

class DocumentUploadResponse(BaseModel):
    document_id: int
    file_name: str
    file_type: str
    total_characters: int
    total_chunks: int
    message: str

class DocumentInfo(BaseModel):
    id: int
    user_id: str
    file_name: str
    file_type: str
    total_characters: int
    total_chunk: int

    class Config:
        from_attributes = True

class ChunkInfo(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    content: str
    char_count: int
    source_file: str
    
    class Config:
        from_attributes = True