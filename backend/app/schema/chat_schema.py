from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    user_id : str = "default_user"
    message : str

class RetrievedContext(BaseModel):
    source: str
    content: str
    score: Optional[float] = None

class ChatResponse(BaseModel):
    answer: str
    retrieved_contexts: List[RetrievedContext] = []
    memories_used: List[str] = []
    latency_ms: float