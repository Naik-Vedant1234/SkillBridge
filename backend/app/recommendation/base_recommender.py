"""Base recommender with shared ranking logic."""

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.student import Student
from app.vector.embedding_service import EmbeddingService
from app.vector.qdrant_client import QdrantService


class BaseRecommender:
    """Base class for all recommenders with hybrid ranking."""
    
    def __init__(self):
        # Don't initialize services in __init__ (causes async issues)
        # Initialize them when needed in methods instead
        
        # Hybrid ranking weights (total = 1.0)
        self.WEIGHT_EMBEDDING = 0.40    # Vector similarity
        self.WEIGHT_SKILL = 0.25        # Skill match
        self.WEIGHT_INTEREST = 0.15     # Interest/domain match
        self.WEIGHT_POPULARITY = 0.10   # Popularity score
        self.WEIGHT_ACTIVITY = 0.10     # Recent activity
    
    async def get_student_with_skills(
        self, db: AsyncSession, student_id: UUID
    ) -> tuple[Student | None, list[str]]:
        """
        Get student and their skill names.
        
        Returns tuple of (student, skill_names_list)
        """
        # Get student
        result = await db.execute(
            select(Student).where(Student.id == student_id)
        )
        student = result.scalar_one_or_none()
        
        if not student:
            return None, []
        
        # Get student's skills separately to avoid async issues
        from app.models.student import student_skills
        from app.models.skill import Skill
        
        skills_result = await db.execute(
            select(Skill.name)
            .join(student_skills, Skill.id == student_skills.c.skill_id)
            .where(student_skills.c.student_id == student_id)
        )
        skill_names = [row[0] for row in skills_result.fetchall()]
        
        return student, skill_names
    
    def calculate_skill_match_score(
        self, 
        student_skills: list[str], 
        required_skills: list[str]
    ) -> float:
        """
        Calculate skill match score (0-1).
        
        Formula: matched_skills / required_skills
        """
        if not required_skills:
            return 0.5  # Neutral score if no requirements
        
        student_set = set(s.lower() for s in student_skills)
        required_set = set(s.lower() for s in required_skills)
        
        matched = len(student_set.intersection(required_set))
        return min(matched / len(required_set), 1.0)
    
    def calculate_hybrid_score(
        self,
        embedding_score: float,
        skill_score: float,
        interest_score: float,
        popularity_score: float,
        activity_score: float,
    ) -> float:
        """
        Calculate weighted hybrid score.
        
        All input scores should be normalized to 0-1 range.
        Returns final score in 0-1 range.
        """
        return (
            self.WEIGHT_EMBEDDING * embedding_score +
            self.WEIGHT_SKILL * skill_score +
            self.WEIGHT_INTEREST * interest_score +
            self.WEIGHT_POPULARITY * popularity_score +
            self.WEIGHT_ACTIVITY * activity_score
        )
    
    def normalize_score(self, score: float, min_val: float = 0, max_val: float = 1) -> float:
        """Normalize score to 0-1 range."""
        if max_val == min_val:
            return 0.5
        return max(0.0, min(1.0, (score - min_val) / (max_val - min_val)))
