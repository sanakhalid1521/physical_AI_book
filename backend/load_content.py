import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from services.embedding import EmbeddingService
from utils.text_splitter import TextSplitter

async def load_textbook_content():
    """Load textbook MDX content into the vector database"""
    print("Starting textbook content loading process...")

    embedding_service = EmbeddingService()
    text_splitter = TextSplitter()

    # Path to the textbook content
    docs_path = Path("../docs")  # Relative to backend directory

    if not docs_path.exists():
        print(f"Docs directory not found at {docs_path}")
        return

    # Find all MDX files in the textbook
    mdx_files = list(docs_path.rglob("*.mdx"))
    print(f"Found {len(mdx_files)} MDX files to process")

    total_chunks = 0

    for mdx_file in mdx_files:
        print(f"Processing: {mdx_file}")

        try:
            # Read the MDX file
            content = mdx_file.read_text(encoding='utf-8')

            # Extract metadata from the file path
            relative_path = mdx_file.relative_to(docs_path)
            path_parts = relative_path.parts

            metadata = {
                "source": str(relative_path),
                "title": path_parts[-1].replace('.mdx', '').replace('-', ' ').title(),
                "chapter": path_parts[0] if len(path_parts) > 0 else "unknown",
                "lesson": path_parts[1] if len(path_parts) > 1 else "unknown",
                "file_path": str(relative_path),
                "processed_at": "now"
            }

            # Process the document (chunk, embed, and store)
            result = await embedding_service.process_document(
                content=content,
                title=metadata["title"],
                metadata=metadata
            )

            print(f"  - Processed {result['chunks_processed']} chunks")
            total_chunks += result['chunks_processed']

        except Exception as e:
            print(f"  - Error processing {mdx_file}: {e}")
            continue

    print(f"\nCompleted! Processed a total of {total_chunks} content chunks.")

if __name__ == "__main__":
    asyncio.run(load_textbook_content())