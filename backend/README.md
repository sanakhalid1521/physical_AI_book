# RAG Chatbot Backend

This is the backend service for the Physical AI & Humanoid Robotics Textbook RAG chatbot. It provides AI-powered search and conversation capabilities using Qwen, Qdrant vector database, and Cohere for enhanced NLP features.

## Features

- **Retrieval-Augmented Generation (RAG)**: Combines vector search with language models for accurate answers
- **Vector Storage**: Uses Qdrant for efficient semantic search
- **AI Integration**: Qwen for response generation, Cohere for summarization and reranking
- **Content Loading**: Scripts to load textbook content into the vector database

## Architecture

- **FastAPI**: Modern Python web framework for building APIs
- **Qwen**: For natural language processing and response generation (via Tongyi SDK)
- **Qdrant**: Vector database for semantic search and retrieval
- **Cohere**: For additional NLP features like summarization and reranking

## API Endpoints

- `POST /api/v1/chat`: Chat conversation endpoint
- `POST /api/v1/query`: Direct query endpoint
- `POST /api/v1/documents/upload`: Upload documents for RAG
- `POST /api/v1/documents/search`: Search documents

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env to add your API keys
   ```

3. Start the Qdrant vector database (if using locally):
   ```bash
   # Using Docker
   docker run -p 6333:6333 -p 6334:6334 \
     -e QDRANT__SERVICE__API_KEY=your-api-key \
     -v $(pwd)/qdrant_data:/qdrant/storage:Z \
     qdrant/qdrant
   ```

4. Start the backend server:
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

## Loading Textbook Content

To load the textbook content into the vector database:

```bash
python load_content.py
```

This will process all MDX files in the `../docs` directory and store them in the vector database.

## Environment Variables

- `QWEN_API_KEY`: Your Qwen API key from Alibaba Cloud (required)
- `COHERE_API_KEY`: Your Cohere API key (optional)
- `QDRANT_API_KEY`: Your Qdrant API key (required for cloud)
- `QDRANT_HOST`: Qdrant host (default: localhost)
- `QDRANT_PORT`: Qdrant port (default: 6333)
- `EMBEDDING_MODEL`: Qwen-compatible embedding model (default: text-embedding-v1)
- `LLM_MODEL`: Qwen language model (default: qwen-max)