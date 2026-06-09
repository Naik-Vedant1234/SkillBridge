"""
Placement Readiness Engine — computes a 0-100 readiness score.

Inputs: Skills + Projects + Internships + Resume Score
Output: Score with breakdown by category
"""


class PlacementReadinessEngine:
    async def compute_score(self, student_id: str) -> dict:
        raise NotImplementedError("To be implemented in Phase 4")
