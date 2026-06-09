"""
Hybrid Ranker — combines embedding similarity with business rules.

Final Score = 0.40 × Embedding Similarity
            + 0.25 × Skill Match
            + 0.15 × User Interest
            + 0.10 × Popularity
            + 0.10 × Activity History
"""


class HybridRanker:
    """Rank candidates/opportunities using the hybrid scoring formula."""

    WEIGHT_EMBEDDING = 0.40
    WEIGHT_SKILL_MATCH = 0.25
    WEIGHT_USER_INTEREST = 0.15
    WEIGHT_POPULARITY = 0.10
    WEIGHT_ACTIVITY = 0.10

    def rank(self, candidates: list[dict], student_profile: dict) -> list[dict]:
        """Rank a list of candidates using the hybrid scoring formula."""
        raise NotImplementedError("To be implemented in Phase 4")

    def compute_skill_match(self, student_skills: list, required_skills: list) -> float:
        """Compute Jaccard-like skill overlap score."""
        raise NotImplementedError("To be implemented in Phase 4")

    def compute_final_score(self, scores: dict) -> float:
        """Apply weighted formula to component scores."""
        return (
            self.WEIGHT_EMBEDDING * scores.get("embedding", 0)
            + self.WEIGHT_SKILL_MATCH * scores.get("skill_match", 0)
            + self.WEIGHT_USER_INTEREST * scores.get("user_interest", 0)
            + self.WEIGHT_POPULARITY * scores.get("popularity", 0)
            + self.WEIGHT_ACTIVITY * scores.get("activity", 0)
        )
