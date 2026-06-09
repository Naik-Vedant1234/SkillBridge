"""Embedding pipeline — wraps sentence-transformers for vector generation."""


class EmbeddingService:
    """
    Uses all-MiniLM-L6-v2 to generate 384-dimensional embeddings.
    Encodes student profiles, jobs, internships, mentors, courses into vectors.
    """

    def __init__(self):
        self.model = None  # Lazy-loaded
        self.model_name = "all-MiniLM-L6-v2"
        self.dimension = 384

    def load_model(self):
        raise NotImplementedError("To be implemented in Phase 3")

    def encode(self, text: str) -> list[float]:
        raise NotImplementedError("To be implemented in Phase 3")

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("To be implemented in Phase 3")
