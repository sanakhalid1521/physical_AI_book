import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from config.settings import settings
from services.embedding import EmbeddingService
from services.retrieval import RetrievalService
from services.cohere_service import CohereService
from models.query import QueryRequest, ChatMessage

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.retrieval_service = RetrievalService()
        self.cohere_service = CohereService()
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize Qwen client for response generation"""
        try:
            from openai import OpenAI
            self.qwen_client = OpenAI(
                api_key=settings.qwen_api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
        except ImportError as e:
            logger.warning(f"Qwen client not installed: {e}")
            self.qwen_client = None

    async def process_query(
        self,
        query: str,
        context: Optional[str] = "",
        history: Optional[List[ChatMessage]] = None
    ) -> Dict[str, Any]:
        """Process a query using RAG (Retrieval-Augmented Generation)"""
        try:
            logger.info(f"Processing query: {query[:50]}...")

            # Get relevant context from vector database
            retrieved_context = await self.retrieval_service.get_relevant_context(query)

            # Combine contexts
            final_context = "\n\n".join(filter(None, [context, retrieved_context]))

            # Prepare conversation history for context
            conversation_history = ""
            if history:
                for msg in history[-5:]:  # Use last 5 messages as context
                    conversation_history += f"\n{msg.role.value}: {msg.content}"

            # Generate response using OpenAI
            response_text = await self._generate_response(
                query=query,
                context=final_context,
                history=conversation_history
            )

            # Get sources for attribution
            sources = await self._get_sources(query)

            # Apply Cohere enhancements if available
            if settings.cohere_api_key:
                try:
                    response_text = await self.cohere_service.summarize_text(response_text)
                except Exception as e:
                    logger.warning(f"Cohere enhancement failed: {e}")

            result = {
                "response": response_text,
                "sources": sources,
                "context": final_context,
                "conversation_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"Query processed successfully")
            return result

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

    async def _generate_response(
        self,
        query: str,
        context: str,
        history: str = ""
    ) -> str:
        """Generate response using Qwen with context"""
        if not self.qwen_client:
            # Mock response for testing
            return f"I received your query: '{query}'. This is a mock response since Qwen is not configured."

        try:
            # Prepare the messages for the chat completion
            messages = []

            # Add system message
            messages.append({
                "role": "system",
                "content": (
                    "You are an AI assistant for the Physical AI & Humanoid Robotics Textbook. "
                    "Use the provided context to answer questions accurately. "
                    "If the context doesn't contain enough information, say so. "
                    "Always be helpful and educational."
                )
            })

            # Add conversation history if available
            if history:
                messages.append({
                    "role": "user",
                    "content": f"Previous conversation:\n{history}"
                })

            # Add context
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Context for answering the question:\n{context}"
                })

            # Add the current query
            messages.append({
                "role": "user",
                "content": query
            })

            # Call Qwen API
            response = self.qwen_client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    async def _get_sources(self, query: str) -> List[Dict[str, Any]]:
        """Get sources for the query response"""
        try:
            # Search for relevant documents
            results = await self.retrieval_service.search(
                query=query,
                top_k=settings.default_top_k
            )

            sources = []
            for result in results:
                source = {
                    "id": result.get("id"),
                    "content": result.get("content", "")[:200] + "...",  # Truncate content
                    "similarity": result.get("similarity", 0.0),
                    "metadata": result.get("metadata", {}),
                    "document_id": result.get("document_id", "")
                }
                sources.append(source)

            return sources
        except Exception as e:
            logger.error(f"Error getting sources: {e}")
            return []

    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        history: Optional[List[ChatMessage]] = None
    ) -> Dict[str, Any]:
        """Process a chat message with conversation context"""
        try:
            result = await self.process_query(
                query=message,
                context="",
                history=history
            )

            result["conversation_id"] = conversation_id or str(uuid.uuid4())
            return result
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise