from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Keys
    qwen_api_key: Optional[str] = os.getenv("QWEN_API_KEY")
    cohere_api_key: Optional[str] = os.getenv("COHERE_API_KEY")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")

    # Qdrant Configuration
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

    # Model Configuration
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")  # Using OpenAI embeddings or compatible
    llm_model: str = os.getenv("LLM_MODEL", "qwen-max")  # Qwen model

    # Application Configuration
    app_title: str = "RAG Chatbot API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Vector search parameters
    default_top_k: int = int(os.getenv("DEFAULT_TOP_K", "5"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Validate required settings
def validate_settings():
    required_keys = ["qwen_api_key"]
    missing_keys = [key for key in required_keys if not getattr(settings, key)]

    if missing_keys:
        raise ValueError(f"Missing required environment variables: {missing_keys}")

# Run validation
validate_settings()