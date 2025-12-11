from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class DocumentMetadata(BaseModel):
    source: str
    title: str
    author: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    page_number: Optional[int] = None
    section: Optional[str] = None
    chapter: Optional[str] = None
    tags: Optional[List[str]] = []

class Document(BaseModel):
    id: str
    content: str
    metadata: DocumentMetadata
    embedding: Optional[List[float]] = None
    created_at: datetime
    updated_at: datetime

class DocumentChunk(BaseModel):
    id: str
    document_id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    chunk_index: int
    total_chunks: int
    created_at: datetime