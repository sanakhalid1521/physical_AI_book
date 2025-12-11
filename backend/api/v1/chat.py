from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

from services.rag import RAGService
from models.query import QueryRequest, QueryResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize RAG service
rag_service = RAGService()

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""
    conversation_id: Optional[str] = None
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[Dict[str, Any]]
    timestamp: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that processes user queries using RAG
    """
    try:
        logger.info(f"Processing chat request: {request.message[:50]}...")

        # Process the query using RAG service
        result = await rag_service.process_query(
            query=request.message,
            context=request.context,
            history=request.history
        )

        response = ChatResponse(
            response=result.get("response", "I couldn't find relevant information to answer your question."),
            conversation_id=result.get("conversation_id", "default"),
            sources=result.get("sources", []),
            timestamp=result.get("timestamp", "")
        )

        return response
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Direct query endpoint for RAG functionality
    """
    try:
        logger.info(f"Processing query: {request.query[:50]}...")

        result = await rag_service.process_query(
            query=request.query,
            context=request.context,
            history=request.history
        )

        return QueryResponse(
            answer=result.get("response", ""),
            sources=result.get("sources", []),
            context_used=result.get("context", ""),
            timestamp=result.get("timestamp", "")
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/health")
async def chat_health():
    """Health check for chat service"""
    return {"status": "healthy", "service": "Chat API"}