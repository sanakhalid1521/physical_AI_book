import re
from typing import List
from config.settings import settings

class TextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks of specified size with overlap
        """
        if len(text) <= self.chunk_size:
            return [text]

        # Split by paragraphs first
        paragraphs = text.split('\n\n')

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > self.chunk_size:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # If the paragraph itself is larger than chunk size, split it
                if len(paragraph) > self.chunk_size:
                    sub_chunks = self._split_large_paragraph(paragraph)
                    chunks.extend(sub_chunks)
                    current_chunk = ""
                else:
                    current_chunk = paragraph
            else:
                current_chunk += f"\n\n{paragraph}"

        # Add the last chunk if it exists
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Further split any chunks that are still too large
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > self.chunk_size:
                final_chunks.extend(self._split_large_chunk(chunk))
            else:
                final_chunks.append(chunk)

        return final_chunks

    def _split_large_paragraph(self, paragraph: str) -> List[str]:
        """
        Split a large paragraph into smaller chunks
        """
        sentences = re.split(r'[.!?]+', paragraph)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += f" {sentence}"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _split_large_chunk(self, chunk: str) -> List[str]:
        """
        Further split a chunk that's still too large
        """
        if len(chunk) <= self.chunk_size:
            return [chunk]

        # Split by sentences
        sentences = re.split(r'[.!?]+', chunk)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += f" {sentence}"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def split_markdown(self, markdown: str) -> List[str]:
        """
        Split markdown content while preserving structure
        """
        # This is a simplified version - in a real implementation you'd want
        # to use a proper markdown parser to respect headers, lists, etc.

        # Split by markdown headers
        sections = re.split(r'\n#{1,6}\s', markdown)

        chunks = []
        for i, section in enumerate(sections):
            if section.strip():
                # Add back the header if this isn't the first section
                if i > 0:
                    header_match = re.search(r'(#{1,6}\s[^\n]+)\n', markdown.split(f'#{1,6} ')[i])
                    if header_match:
                        section = f"{header_match.group(1)}\n{section}"

                # Split the section if it's too large
                sub_chunks = self.split_text(section)
                chunks.extend(sub_chunks)

        return chunks