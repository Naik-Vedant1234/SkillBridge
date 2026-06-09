"""Skill Gap Engine — computes gap between student skills and role requirements."""


class SkillGapEngine:
    """
    Input: Student skills + Career Role requirements (from Career Knowledge Service)
    Output: Gap report with missing skills ranked by importance
    """

    async def analyze_gap(self, student_id: str, role_id: str) -> dict:
        raise NotImplementedError("To be implemented in Phase 4")
