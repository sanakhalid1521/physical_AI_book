from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

from services.embedding import EmbeddingService
from services.retrieval import RetrievalService

logger = logging.getLogger(__name__)
router = APIRouter()

embedding_service = EmbeddingService()
retrieval_service = RetrievalService()

class DocumentUploadResponse(BaseModel):
    document_id: str
    chunks_processed: int
    status: str

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    filters: Optional[Dict[str, Any]] = {}

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]

@router.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    metadata: str = Form("{}")  # JSON string of metadata
):
    """
    Upload a document and process it for RAG
    """
    try:
        logger.info(f"Uploading document: {file.filename}")

        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')

        # Process document and store embeddings
        result = await embedding_service.process_document(
            content=content_str,
            title=title,
            metadata=metadata
        )

        return DocumentUploadResponse(
            document_id=result["document_id"],
            chunks_processed=result["chunks_processed"],
            status="success"
        )
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@router.post("/documents/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    Search for relevant documents based on query
    """
    try:
        logger.info(f"Searching for: {request.query[:50]}...")

        results = await retrieval_service.search(
            query=request.query,
            top_k=request.top_k,
            filters=request.filters
        )

        return SearchResponse(results=results)
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")

@router.get("/documents/health")
async def documents_health():
    """Health check for documents service"""
    return {"status": "healthy", "service": "Documents API"}