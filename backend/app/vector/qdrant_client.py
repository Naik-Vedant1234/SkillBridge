"""
Qdrant Client - Manage vector storage in Qdrant.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any
import uuid

from app.core.config import settings


class QdrantService:
    """Manage vector operations in Qdrant."""
    
    def __init__(self):
        """Initialize Qdrant client."""
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
        self.vector_size = 384  # all-MiniLM-L6-v2 dimension
    
    def create_collection(self, collection_name: str):
        """
        Create a new collection if it doesn't exist.
        
        Args:
            collection_name: Name of the collection
        """
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if collection_name not in collection_names:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
    
    def upsert_student_profile(
        self,
        student_id: str,
        embedding: List[float],
        payload: Dict[str, Any]
    ):
        """
        Insert or update student profile vector.
        
        Args:
            student_id: Student UUID
            embedding: Embedding vector
            payload: Metadata (skills, education, etc.)
        """
        self.create_collection("student_profiles")
        
        point = PointStruct(
            id=str(student_id),
            vector=embedding,
            payload=payload
        )
        
        self.client.upsert(
            collection_name="student_profiles",
            points=[point]
        )
    
    def search_similar_students(
        self,
        query_vector: List[float],
        limit: int = 10
    ) -> List[Dict]:
        """
        Search for similar student profiles.
        
        Args:
            query_vector: Query embedding vector
            limit: Number of results to return
            
        Returns:
            List of similar student profiles with scores
        """
        self.create_collection("student_profiles")
        
        results = self.client.search(
            collection_name="student_profiles",
            query_vector=query_vector,
            limit=limit
        )
        
        return [
            {
                "student_id": result.id,
                "score": result.score,
                "payload": result.payload
            }
            for result in results
        ]
    
    def delete_student_profile(self, student_id: str):
        """
        Delete student profile from vector store.
        
        Args:
            student_id: Student UUID
        """
        try:
            self.client.delete(
                collection_name="student_profiles",
                points_selector=[str(student_id)]
            )
        except Exception:
            pass  # Ignore if doesn't exist


# Singleton instance
_qdrant_service = None

def get_qdrant_service() -> QdrantService:
    """Get or create singleton Qdrant service instance."""
    global _qdrant_service
    if _qdrant_service is None:
        _qdrant_service = QdrantService()
    return _qdrant_service
