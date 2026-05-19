import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "MemoRAG Agent"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./memorag.db")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "htt[://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "./chroma_db")

settings = Settings()