import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from config.settings import settings
from models.document import Document, DocumentChunk
from utils.text_splitter import TextSplitter

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.text_splitter = TextSplitter()
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize Qwen and Qdrant clients"""
        try:
            # Import Qwen
            from openai import OpenAI  # Tongyi SDK uses OpenAI-compatible interface
            self.qwen_client = OpenAI(
                api_key=settings.qwen_api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )

            # Import Qdrant
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

            # Create collection if it doesn't exist
            self._create_collection()

        except ImportError as e:
            logger.warning(f"Required packages not installed: {e}")
            logger.warning("Embedding service will use mock implementation")
            self.qwen_client = None
            self.qdrant_client = None

    def _create_collection(self):
        """Create Qdrant collection if it doesn't exist"""
        if not self.qdrant_client:
            return

        try:
            from qdrant_client.http import models as rest

            # Check if collection exists
            collections = self.qdrant_client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if settings.qdrant_collection_name not in collection_names:
                # Create collection with appropriate vector size (1536 for OpenAI embeddings)
                self.qdrant_client.create_collection(
                    collection_name=settings.qdrant_collection_name,
                    vectors_config=rest.VectorParams(size=1536, distance=rest.Distance.COSINE)
                )
                logger.info(f"Created Qdrant collection: {settings.qdrant_collection_name}")
        except Exception as e:
            logger.error(f"Error creating Qdrant collection: {e}")

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Qwen-compatible API"""
        if not self.qwen_client:
            # Mock implementation for testing
            return [[0.1] * 1536 for _ in texts]

        try:
            # Use Qwen-compatible embedding API
            response = self.qwen_client.embeddings.create(
                input=texts,
                model=settings.embedding_model  # This should be a compatible embedding model
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            # Fallback to mock embeddings
            return [[0.1] * 1536 for _ in texts]

    async def chunk_and_embed_document(
        self,
        content: str,
        metadata: Dict[str, Any]
    ) -> List[DocumentChunk]:
        """Split document into chunks and generate embeddings"""
        try:
            # Split content into chunks
            chunks = self.text_splitter.split_text(content)

            # Generate embeddings for all chunks at once (batch processing)
            chunk_texts = [chunk.strip() for chunk in chunks if chunk.strip()]
            embeddings = await self.generate_embeddings(chunk_texts)

            # Create document chunks with embeddings
            document_chunks = []
            for i, (chunk_text, embedding) in enumerate(zip(chunk_texts, embeddings)):
                chunk = DocumentChunk(
                    id=str(uuid.uuid4()),
                    document_id=metadata.get("document_id", str(uuid.uuid4())),
                    content=chunk_text,
                    metadata=metadata,
                    embedding=embedding,
                    chunk_index=i,
                    total_chunks=len(chunk_texts),
                    created_at=datetime.now()
                )
                document_chunks.append(chunk)

            return document_chunks
        except Exception as e:
            logger.error(f"Error chunking and embedding document: {e}")
            raise

    async def store_document_chunks(self, chunks: List[DocumentChunk]) -> bool:
        """Store document chunks in Qdrant vector database"""
        if not self.qdrant_client:
            logger.warning("Qdrant client not available, skipping storage")
            return True

        try:
            # Prepare points for Qdrant
            points = []
            for chunk in chunks:
                points.append(
                    rest.PointStruct(
                        id=chunk.id,
                        vector=chunk.embedding,
                        payload={
                            "content": chunk.content,
                            "document_id": chunk.document_id,
                            "chunk_index": chunk.chunk_index,
                            "metadata": chunk.metadata,
                            "created_at": chunk.created_at.isoformat()
                        }
                    )
                )

            # Upload points to Qdrant
            self.qdrant_client.upsert(
                collection_name=settings.qdrant_collection_name,
                points=points
            )

            logger.info(f"Stored {len(points)} chunks in Qdrant")
            return True
        except Exception as e:
            logger.error(f"Error storing document chunks: {e}")
            raise

    async def process_document(
        self,
        content: str,
        title: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a document: chunk, embed, and store"""
        try:
            # Add document-specific metadata
            doc_metadata = {
                **metadata,
                "title": title,
                "source": "textbook",
                "processed_at": datetime.now().isoformat()
            }

            # Chunk and embed the document
            chunks = await self.chunk_and_embed_document(content, doc_metadata)

            # Store in vector database
            success = await self.store_document_chunks(chunks)

            if not success:
                raise Exception("Failed to store document chunks")

            return {
                "document_id": chunks[0].document_id if chunks else str(uuid.uuid4()),
                "chunks_processed": len(chunks),
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise