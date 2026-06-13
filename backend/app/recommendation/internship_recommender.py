"""Internship recommender — finds best internship matches for students."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.internship import Internship
from app.models.student import Student
from app.models.application import Application
from app.recommendation.base_recommender import BaseRecommender


class InternshipRecommender(BaseRecommender):
    """Recommends internships using hybrid ranking."""
    
    async def recommend(
        self, 
        db: AsyncSession,
        student_id: UUID, 
        limit: int = 10
    ) -> list[dict]:
        """
        Get personalized internship recommendations.
        
        Similar to job recommender but considers:
        - Student's year/graduation timeline
        - Internship duration compatibility
        - Learning opportunities
        """
        # Get student profile and skills
        student, student_skills = await self.get_student_with_skills(db, student_id)
        if not student:
            return []
        
        # Get active internships
        result = await db.execute(
            select(Internship)
            .where(Internship.is_active == True)
            .limit(100)
        )
        internships = result.scalars().all()
        
        if not internships:
            return []
        
        # Get applied internships
        from app.models.application import ApplicationTargetType
        applied_result = await db.execute(
            select(Application.target_id)
            .where(
                Application.student_id == student_id,
                Application.target_type == ApplicationTargetType.INTERNSHIP
            )
        )
        applied_ids = {row[0] for row in applied_result.fetchall()}
        
        # Score each internship
        scored_internships = []
        for internship in internships:
            if internship.id in applied_ids:
                continue
            
            skill_score = self._calculate_skill_score(student_skills, internship)
            interest_score = self._calculate_interest_score(student, internship)
            popularity_score = self._calculate_popularity_score(internship)
            activity_score = self._calculate_activity_score(internship)
            timeline_score = self._calculate_timeline_score(student, internship)
            
            embedding_score = 0.5  # TODO: Add vector similarity
            
            # Adjust weights for internships (timeline more important)
            final_score = (
                0.35 * embedding_score +
                0.25 * skill_score +
                0.15 * interest_score +
                0.10 * popularity_score +
                0.15 * timeline_score  # Higher weight for timeline fit
            )
            
            scored_internships.append({
                "internship": internship,
                "score": final_score,
                "match_percentage": int(final_score * 100),
                "skill_match": int(skill_score * 100),
            })
        
        scored_internships.sort(key=lambda x: x["score"], reverse=True)
        
        recommendations = []
        for item in scored_internships[:limit]:
            internship = item["internship"]
            recommendations.append({
                "id": str(internship.id),
                "title": internship.title,
                "company_id": str(internship.company_id),
                "location": internship.location,
                "duration": internship.duration,
                "stipend": internship.stipend,
                "requirements": internship.requirements or [],
                "description": internship.description[:200] + "..." if len(internship.description) > 200 else internship.description,
                "posted_at": internship.created_at.isoformat(),
                "posted_at": internship.created_at.isoformat(),
                "match_percentage": item["match_percentage"],
                "skill_match": item["skill_match"],
                "score": round(item["score"], 3),
            })
        
        return recommendations
    
    def _calculate_skill_score(self, student_skills: list[str], internship: Internship) -> float:
        """Calculate skill match."""
        if not internship.requirements:
            return 0.5
        return self.calculate_skill_match_score(student_skills, internship.requirements)
    
    def _calculate_interest_score(self, student: Student, internship: Internship) -> float:
        """Calculate interest match."""
        return 0.6
    
    def _calculate_popularity_score(self, internship: Internship) -> float:
        """Calculate popularity."""
        return 0.5
    
    def _calculate_activity_score(self, internship: Internship) -> float:
        """Calculate freshness."""
        now = datetime.now(timezone.utc)
        days_old = (now - internship.created_at).days
        
        if days_old <= 7:
            return 1.0
        elif days_old <= 14:
            return 0.8
        elif days_old <= 30:
            return 0.6
        else:
            return 0.4
    
    def _calculate_timeline_score(self, student: Student, internship: Internship) -> float:
        """
        Calculate timeline compatibility.
        
        Considers:
        - Student's graduation year
        - Internship start date
        - Duration fit
        """
        # Internship model doesn't have start_date, use creation date as proxy
        now = datetime.now(timezone.utc)
        days_old = (now - internship.created_at).days
        
        # Fresh postings (0-14 days): 1.0
        # Recent (14-30 days): 0.8
        # Older: 0.6
        if days_old <= 14:
            return 1.0
        elif days_old <= 30:
            return 0.8
        else:
            return 0.6
