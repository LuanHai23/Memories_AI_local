import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "MemoRAG Agent"
    # database memorag.db sẽ được tạo trong folder backend
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./memorag.db")
    # OLLAMA sẽ chạy ở localhost với port 11434, và model mặc định là qwen3:8b
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    # Model embedding local sẽ sử dụng sentence-transformers/all-MiniLM-L6-v2, 
    # có thể thay đổi model này nếu muốn
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    # Đường dẫn để lưu vector embedding của ChromaDB
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "./chroma_db")

settings = Settings()