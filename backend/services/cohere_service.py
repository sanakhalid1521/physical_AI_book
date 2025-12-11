import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from config.settings import settings

logger = logging.getLogger(__name__)

class CohereService:
    def __init__(self):
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Cohere client"""
        try:
            import cohere
            self.client = cohere.Client(settings.cohere_api_key)
        except ImportError:
            logger.warning("Cohere package not installed, using mock implementation")
            self.client = None
        except Exception as e:
            logger.warning(f"Cohere client initialization failed: {e}")
            self.client = None

    async def summarize_text(self, text: str, length: str = "medium") -> str:
        """Summarize text using Cohere"""
        if not self.client:
            # Return original text if Cohere is not available
            return text

        try:
            response = self.client.summarize(
                text=text,
                length=length,
                format="paragraph",
                model="summarize-xlarge"
            )
            return response.summary
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            # Return original text if summarization fails
            return text

    async def rerank_results(
        self,
        query: str,
        documents: List[str],
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """Rerank search results using Cohere"""
        if not self.client:
            # Return documents in original order with mock scores
            return [
                {"document": doc, "index": i, "relevance_score": 1.0 - (i * 0.1)}
                for i, doc in enumerate(documents[:top_n])
            ]

        try:
            response = self.client.rerank(
                query=query,
                documents=documents,
                top_n=top_n
            )

            results = []
            for idx, result in enumerate(response.results):
                results.append({
                    "document": result.document,
                    "index": result.index,
                    "relevance_score": result.relevance_score
                })

            return results
        except Exception as e:
            logger.error(f"Error reranking results: {e}")
            # Return original order if reranking fails
            return [
                {"document": doc, "index": i, "relevance_score": 1.0}
                for i, doc in enumerate(documents[:top_n])
            ]

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Cohere (alternative to OpenAI)"""
        if not self.client:
            # Mock implementation
            return [[0.1] * 1024 for _ in texts]  # Cohere typically uses 1024-dim embeddings

        try:
            response = self.client.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type="search_document"
            )
            return response.embeddings
        except Exception as e:
            logger.error(f"Error generating Cohere embeddings: {e}")
            raise

    async def classify_text(
        self,
        text: str,
        examples: List[Dict[str, str]]
    ) -> str:
        """Classify text using Cohere"""
        if not self.client:
            return "unknown"

        try:
            response = self.client.classify(
                inputs=[text],
                examples=examples
            )
            return response.classifications[0].prediction
        except Exception as e:
            logger.error(f"Error classifying text: {e}")
            return "unknown"