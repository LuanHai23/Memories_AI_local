import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schema.chat_schema import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from app.db.database import get_db
from app.db.models import Conversation, RequestLog

# Tạo router cho API chat
router = APIRouter()

llm_service = LLMService()

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    start_time = time.time()

    # Lưu câu hỏi của user vào database
    user_message = Conversation(
        user_id=request.user_id,
        role="user",
        message=request.message
    )
    db.add(user_message)
    db.commit()
    # Tạo prompt cho LLM
    prompt = f"""
            You are MemoryRAG Agent, a helpfull local-first AI assistant.

            Your current capabilities:
            - You can answer general questions.
            - In future versions, you will use RAG and long-term memory.
            - Answer clearly and concisely.
            User question: {request.message}
            Assistant answer:
            Please answer in a helpful and concise way
            """
    
    # Gọi LLM để tạo câu trả lời
    try:
        answer = llm_service.generate(prompt)

        status = "success"
        error_message = None
    except Exception as e:
        answer = "Sorry, I could not generate an answer"
        status = "faild"
        error_message = str(e)
    
    # Lưu message của assistant
    assistant_message = Conversation(
        user_id = request.user_id,
        role = "assistant",
        message = answer,
    )
    db.add(assistant_message)

    # Tính latency
    latency_ms = round((time.time() - start_time) * 1000, 2)

    # Lưu request log
    log = RequestLog(
        user_id=request.user_id,
        query=request.message,
        response=answer,

        # Hiện tại chưa có RAG nên = 0
        retrieved_chunks_count=0,

        # Hiện tại chưa có memory retrieval nên = 0
        memories_used_count=0,

        latency_ms=latency_ms,
        llm_model=llm_service.model,
        status=status,
        error_message=error_message
    )

    db.add(log)

    # Commit 1 lần để lưu assistant message và log
    db.commit()

    # Trả về response cho frontend
    return ChatResponse(
        answer = answer,
        # Hiện tại chưa có RAG nên để rỗng
        retrieved_contexts = [],
        # Cái này cũng dị chưa có mẻmory retrieval nên để rỗng
        memories_used = [],
        latency_ms = latency_ms
    )