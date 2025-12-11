import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from config.settings import settings
from services.embedding import EmbeddingService

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize Qdrant client for retrieval"""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models as rest

            if settings.qdrant_api_key:
                self.qdrant_client = QdrantClient(
                    url=settings.qdrant_host,
                    port=settings.qdrant_port,
                    api_key=settings.qdrant_api_key
                )
            else:
                self.qdrant_client = QdrantClient(
                    host=settings.qdrant_host,
                    port=settings.qdrant_port
                )
        except ImportError as e:
            logger.warning(f"Qdrant client not installed: {e}")
            self.qdrant_client = None

    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for relevant documents based on query"""
        if not self.qdrant_client:
            # Mock implementation for testing
            return [
                {
                    "id": f"mock-{i}",
                    "content": f"Mock result for query: {query}",
                    "metadata": {"source": "mock", "similarity": 0.8},
                    "similarity": 0.8
                }
                for i in range(top_k)
            ]

        try:
            # Generate embedding for the query
            query_embedding = await self.embedding_service.generate_embeddings([query])
            query_vector = query_embedding[0]

            # Prepare filters if provided
            qdrant_filters = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    if isinstance(value, str):
                        conditions.append(
                            {"key": f"metadata.{key}", "match": {"value": value}}
                        )
                    elif isinstance(value, (int, float)):
                        conditions.append(
                            {"key": f"metadata.{key}", "range": {"gte": value, "lte": value}}
                        )

                if conditions:
                    qdrant_filters = {"must": conditions}

            # Perform search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=settings.qdrant_collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=qdrant_filters,
                score_threshold=settings.similarity_threshold
            )

            # Format results
            results = []
            for hit in search_results:
                result = {
                    "id": hit.id,
                    "content": hit.payload.get("content", ""),
                    "metadata": hit.payload.get("metadata", {}),
                    "similarity": hit.score,
                    "document_id": hit.payload.get("document_id", ""),
                    "chunk_index": hit.payload.get("chunk_index", 0)
                }
                results.append(result)

            logger.info(f"Found {len(results)} results for query: {query[:50]}...")
            return results

        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise

    async def get_relevant_context(
        self,
        query: str,
        top_k: int = 3
    ) -> str:
        """Get relevant context for a query to use in RAG"""
        try:
            results = await self.search(query, top_k)

            # Combine content from relevant results
            context_parts = []
            for result in results:
                content = result["content"]
                if content.strip():
                    context_parts.append(f"Source: {result.get('metadata', {}).get('title', 'Unknown')}\n{content}")

            context = "\n\n".join(context_parts)
            return context
        except Exception as e:
            logger.error(f"Error getting relevant context: {e}")
            return ""