"""
Embedding Service - Generate embeddings using sentence-transformers.
"""

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingService:
    """Generate text embeddings for semantic search."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model.
        
        Args:
            model_name: HuggingFace model name (default: all-MiniLM-L6-v2, 384-dim)
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # all-MiniLM-L6-v2 produces 384-dim vectors
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list of floats
        """
        if not text or not text.strip():
            # Return zero vector for empty text
            return [0.0] * self.dimension
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (more efficient).
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def generate_resume_embedding(self, parsed_data: dict) -> List[float]:
        """
        Generate embedding for resume/student profile.
        Combines skills, education, and experience into one embedding.
        
        Args:
            parsed_data: Parsed resume data
            
        Returns:
            Embedding vector
        """
        # Build a rich text representation
        text_parts = []
        
        # Add skills
        skills = parsed_data.get("skills", [])
        if skills:
            text_parts.append(f"Skills: {', '.join(skills)}")
        
        # Add education
        education = parsed_data.get("education", [])
        for edu in education:
            edu_text = f"{edu.get('degree', '')} {edu.get('field', '')}"
            text_parts.append(edu_text.strip())
        
        # Add experience indicator
        exp_years = parsed_data.get("experience_years", 0)
        if exp_years > 0:
            text_parts.append(f"{exp_years} years of experience")
        
        # Combine all parts
        combined_text = ". ".join(filter(None, text_parts))
        
        return self.generate_embedding(combined_text)


# Singleton instance
_embedding_service = None

def get_embedding_service() -> EmbeddingService:
    """Get or create singleton embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
