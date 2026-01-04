"""
Vector database operations for Qdrant Cloud
Handles content chunking, embedding generation, and similarity search
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
import logging
import hashlib
from typing import List, Dict, Any, Optional, Tuple
import json
from pathlib import Path

from .config import settings

logger = logging.getLogger(__name__)

# Initialize clients
qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ContentChunk:
    """Represents a chunk of textbook content"""
    def __init__(self, text: str, chapter: str, section: str, page_url: str, chunk_index: int):
        self.text = text
        self.chapter = chapter
        self.section = section
        self.page_url = page_url
        self.chunk_index = chunk_index
        self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique ID for the chunk"""
        content = f"{self.chapter}_{self.section}_{self.chunk_index}_{self.text[:100]}"
        return hashlib.md5(content.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "text": self.text,
            "chapter": self.chapter,
            "section": self.section,
            "page_url": self.page_url,
            "chunk_index": self.chunk_index,
        }

async def init_vector_db():
    """Initialize vector database collection"""
    try:
        logger.info("Initializing Qdrant collection...")

        # Check if collection exists
        collections = qdrant_client.get_collections()
        collection_names = [c.name for c in collections.collections]

        if settings.QDRANT_COLLECTION_NAME not in collection_names:
            # Create collection
            qdrant_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=768,  # Gemini embedding dimension
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection: {settings.QDRANT_COLLECTION_NAME}")
        else:
            logger.info(f"Collection {settings.QDRANT_COLLECTION_NAME} already exists")

    except Exception as e:
        logger.error(f"Failed to initialize vector database: {e}")
        raise

def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """Split text into overlapping chunks"""
    if chunk_size is None:
        chunk_size = settings.CHUNK_SIZE
    if overlap is None:
        overlap = settings.CHUNK_OVERLAP

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Find sentence boundary if possible
        if end < len(text):
            # Look for sentence endings within the last 100 characters
            sentence_endings = ['. ', '! ', '? ', '\n\n']
            best_end = end
            for ending in sentence_endings:
                pos = text.rfind(ending, end - 100, end)
                if pos != -1 and pos > best_end - 100:
                    best_end = pos + len(ending)
                    break

            # If no sentence ending found, look for word boundary
            if best_end == end:
                space_pos = text.rfind(' ', end - 50, end)
                if space_pos != -1:
                    best_end = space_pos + 1

            end = best_end

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start position with overlap
        start = end - overlap
        if start >= len(text):
            break

    return chunks

def generate_embedding(text: str) -> List[float]:
    """Generate embedding for text using OpenAI"""
    try:
        response = openai_client.embeddings.create(
            input=text,
            model=settings.OPENAI_EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        raise

def store_chunks(chunks: List[ContentChunk]):
    """Store content chunks in vector database"""
    try:
        points = []

        for chunk in chunks:
            embedding = generate_embedding(chunk.text)

            point = models.PointStruct(
                id=chunk.id,
                vector=embedding,
                payload=chunk.to_dict()
            )
            points.append(point)

        # Upsert in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            qdrant_client.upsert(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                points=batch
            )

        logger.info(f"Stored {len(chunks)} chunks in vector database")

    except Exception as e:
        logger.error(f"Failed to store chunks: {e}")
        raise

def search_similar(query: str, limit: int = 5, score_threshold: float = 0.7) -> List[Dict[str, Any]]:
    """Search for similar content chunks"""
    try:
        query_embedding = generate_embedding(query)

        search_result = qdrant_client.search(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=limit,
            score_threshold=score_threshold
        )

        results = []
        for hit in search_result:
            result = hit.payload.copy()
            result["score"] = hit.score
            results.append(result)

        return results

    except Exception as e:
        logger.error(f"Failed to search similar content: {e}")
        raise

def get_chunk_by_id(chunk_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a specific chunk by ID"""
    try:
        result = qdrant_client.retrieve(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            ids=[chunk_id]
        )

        if result:
            return result[0].payload
        return None

    except Exception as e:
        logger.error(f"Failed to retrieve chunk {chunk_id}: {e}")
        return None

def delete_chunks_by_chapter(chapter: str):
    """Delete all chunks for a specific chapter"""
    try:
        # This is a simplified implementation
        # In production, you'd want to use filters or scroll through all points
        qdrant_client.delete(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points_selector=models.Filter(
                must=[
                    models.FieldCondition(
                        key="chapter",
                        match=models.MatchValue(value=chapter)
                    )
                ]
            )
        )
        logger.info(f"Deleted chunks for chapter: {chapter}")

    except Exception as e:
        logger.error(f"Failed to delete chunks for chapter {chapter}: {e}")
        raise

def get_collection_stats() -> Dict[str, Any]:
    """Get statistics about the vector collection"""
    try:
        info = qdrant_client.get_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME
        )

        return {
            "collection_name": settings.QDRANT_COLLECTION_NAME,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": "ready"
        }

    except Exception as e:
        logger.error(f"Failed to get collection stats: {e}")
        return {"status": "error", "error": str(e)}
