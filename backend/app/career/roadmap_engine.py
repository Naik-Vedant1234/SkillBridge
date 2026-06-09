"""
Roadmap Engine — generates month-by-month career plans.
Pipeline: Career Goal → Career Knowledge Service → Skill Gap → Gemini refinement → Roadmap
"""


class RoadmapEngine:
    async def generate(self, student_id: str, goal_id: str, months: int = 4) -> dict:
        raise NotImplementedError("To be implemented in Phase 4")
