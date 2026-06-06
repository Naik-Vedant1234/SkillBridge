"""Recommendation service — orchestrates all recommender modules."""


class RecommendationService:
    """Orchestrator for the split recommender modules."""

    async def get_job_recommendations(self, student_id: str) -> list:
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_internship_recommendations(self, student_id: str) -> list:
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_mentor_recommendations(self, student_id: str) -> list:
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_course_recommendations(self, student_id: str) -> list:
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_studygroup_recommendations(self, student_id: str) -> list:
        raise NotImplementedError("To be implemented in Phase 4")
