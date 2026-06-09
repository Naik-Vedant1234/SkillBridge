"""Job recommender — finds best job matches for students."""


class JobRecommender:
    async def recommend(self, student_id: str, limit: int = 10) -> list[dict]:
        raise NotImplementedError("To be implemented in Phase 4")
