import os
import shutil
from pathlib import Path
from typing import Tuple, List

from fastapi import UploadFile

from app.utils.file_loader import load_document_text
from app.services.chunking_service import ChunkingService

# Lớp này dùng để xử lý tài liệu sau khi đã upload, đọc text từ file và chunk text
class DocumentService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir

        # Tạo 1 folder uploads nếu nó chưa được tạo
        os.makedirs(self.upload_dir, exist_ok=True)

        # Tạo chunking service
        self.chunking_service = ChunkingService(
            chunk_size=1000,
            overlap= 200
        )

    # Check xem file có được hỗ trợ không
    # Vì trước đó chỉ hỗ trợ những file .txt hoặc .pdf
    def validate_file_type(self, filename: str) -> str:
        suffix = Path(filename).suffix.lower()

        if suffix == ".txt":
            return ".txt"
        
        if suffix == ".pdf":
            return ".pdf"
        
        raise ValueError("Only pdf and txt files are supported.")
    
    # Lưu file upload vào folder uploads
    def save_upload_file(self, file: UploadFile) -> str:
        file_path = os.path.join(
            self.upload_dir,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path
    
    def process_upload_file(self, file: UploadFile) -> Tuple[str, str, List[str]]:
        file_type = self.validate_file_type(file.filename)

        file_path = self.save_upload_file(file)

        raw_text = load_document_text(file_path)

        chunks = self.chunking_service.split_text(raw_text)

        return file_path, file_type, raw_text, chunks
    
