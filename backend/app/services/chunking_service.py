from typing import List

# Lớp này phụ trách chia text thành nhiều chunk nhỏ
# Sử dụng fixed-size chunking
class ChunkingService:
    # Hàm khỏi tạo chunk size và overlap cho chunking
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

        if self.overlap >= self.chunk_size:
            raise ValueError("overlapp must be smaller than chunk_size")
        
    # Dùng để làm sạch text basic
    def clean_text(slef, text: str) -> str:
        lines = text.splitlines()

        cleanned_lines = []

        for line in lines:
            line = line.strip()

            if line:
                cleanned_lines.append(line)
        return "\n".join(cleanned_lines)
    
    def split_text(self, text: str) -> List[str]:
        text = self.clean_text(text)

        if not text:
            return []
        
        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start - self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end - self.overlap
        
        return chunks