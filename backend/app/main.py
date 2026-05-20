from fastapi import FastAPI
from app.api import chat, documents, memories, logs
from app.db.database import init_db

app = FastAPI(
    title = "MemoRAG Agent API",
    description="Local first RAG Agent with Long-Term Memory and Observability",
    version="0.1.0"
)

# Khởi tạo database khi ứng dụng khởi động
@app.on_event("startup")
def on_startup():
    init_db()

# Import các router API
# Thì mỗi router sẽ quản lý một nhóm riêng
# Chat thì chat với AI
# Documents thì upload với xử lý tài liệu
# memories thì quản lý trí nhớ dài hạn
# logs thì xem logs hệ thống
app.include_router(chat.router, prefix="/chat", tag=["Chat"])
app.include_router(documents.router, prefix="/documents", tags =["Documents"])
app.include_router(memories.router, prefix="/memories", tag=["Memories"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])

@app.get("/")
def root():
    return {
        "message": "MemoRAG Agent API is running",
        "version": "0.1.0"
    }