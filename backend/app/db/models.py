from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Định nghĩa model Conversation để lưu trữ thông tin về các cuộc trò chuyện
class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default_user", index=True)
    role = Column(String, nullable=False)  # "user" hoặc "assistant"
    # Message sẽ được tạo dưới dạng text và không thể nào là null được, 
    # vì mỗi message sẽ là một phần quan trọng của cuộc trò chuyện
    message = Column(Text, nullable=False)
    # Sẽ được tạo tự động khi một cuộc trò chuyện mới được tạo ra, 
    # và sẽ lưu lại thời gian của cuộc trò chuyện đó
    created_at = Column(DateTime, default=datetime.utcnow)

# Lớp này sẽ lưu trữ thông tin về trí nhớ dài hạn của người dùng,
# bao gồm cả nội dung trí nhớ và thời gian tạo ra nó
class UserMemory(Base):
    __tablename__ = "user_memories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default_user", index=True)
    memory_type = Column(String, default="general")  # Loại trí nhớ, ví dụ: "general", "important", "temporary"
    content = Column(Text, nullable=False)  # Nội dung trí nhớ
    importance_score = Column(Integer, default= 3 ) # Điểm đánh giá mức độ quan trọng của trí nhớ, từ 1 đến 5
    confidence_score = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)  # Trạng thái hoạt động của trí nhớ
    created_at = Column(DateTime, default=datetime.utcnow)  # Thời gian tạo trí nhớ
    updated_at = Column(DateTime, default=datetime.utcnow)  # Thời gian cập nhật trí nhớ

# Lớp logs dùng để lưu trữ mỗi lần user chat
class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default_user", index=True)
    query = Column(Text, nullable=False)  # Câu hỏi của user
    response = Column(Text, nullable=False)  # Câu trả lời của AI
    retrieved_memories = Column(Integer, default=0)  # Trí nhớ được truy xuất (nếu có)
    memories_used_count = Column(Integer, default=0) # Sau này dùng bao nhiêu memories thì lưu ở đây
    latency_ms = Column(Float, default=0.0)  # Thời gian phản hồi của hệ thống
    llm_model = Column(String) # Model LLM được sử dụng để trả lời câu hỏi
    status = Column(String, default="success")  # Trạng thái của yêu cầu, ví dụ: "success", "error"
    error_message = Column(Text, nullable=True)  # Nếu có lỗi, lưu thông tin lỗi ở đây
    created_at = Column(DateTime, default=datetime.utcnow)  # Thời gian tạo log yêu cầu
