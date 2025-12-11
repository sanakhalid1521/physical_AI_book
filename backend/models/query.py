from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None

class QueryRequest(BaseModel):
    query: str
    context: Optional[str] = ""
    history: Optional[List[ChatMessage]] = []
    top_k: Optional[int] = 5
    temperature: Optional[float] = 0.7

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    context_used: str
    timestamp: str

class DocumentChunk(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    similarity_score: Optional[float] = None

class SearchResult(BaseModel):
    chunks: List[DocumentChunk]
    query: str
    timestamp: str