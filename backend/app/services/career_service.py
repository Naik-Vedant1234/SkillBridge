"""Career service — skill gap, placement readiness, roadmap generation."""


class CareerService:
    """Orchestrates career intelligence features."""

    async def get_skill_gap(self, student_id: str, role_id: str) -> dict:
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_placement_readiness(self, student_id: str) -> dict:
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_career_roadmap(self, student_id: str, goal_id: str) -> dict:
        raise NotImplementedError("To be implemented in Phase 4")
