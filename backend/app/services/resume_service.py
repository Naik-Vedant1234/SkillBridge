"""Resume service — handles upload, parsing orchestration, and analysis."""


class ResumeService:
    """Business logic for resume management."""

    async def upload_resume(self, student_id: str, file) -> dict:
        raise NotImplementedError("To be implemented in Phase 3")

    async def get_analysis(self, resume_id: str) -> dict:
        raise NotImplementedError("To be implemented in Phase 3")

    async def get_score(self, resume_id: str) -> dict:
        raise NotImplementedError("To be implemented in Phase 3")
