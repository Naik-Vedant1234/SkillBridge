"""Roadmap Generator — uses Career Knowledge Base + Skill Gap + Gemini LLM refinement."""


class RoadmapGenerator:
    """
    Pipeline:
    Career Goal → Career Knowledge Service → Skill Gap → Gemini refinement → Roadmap

    The LLM refines, it doesn't invent. The knowledge base provides the structure.
    """

    async def generate_roadmap(
        self, student_id: str, goal_id: str, timeline_months: int = 4
    ) -> dict:
        """Generate a month-by-month career roadmap."""
        raise NotImplementedError("To be implemented in Phase 4")
