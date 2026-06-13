"""Study group recommender — matches students with peer learning groups."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.study_group import StudyGroup
from app.models.student import Student
from app.recommendation.base_recommender import BaseRecommender


class StudyGroupRecommender(BaseRecommender):
    """Recommends study groups for collaborative learning."""
    
    async def recommend(
        self, 
        db: AsyncSession,
        student_id: UUID, 
        limit: int = 10
    ) -> list[dict]:
        """
        Get personalized study group recommendations.
        
        Matching criteria:
        - Topic/domain alignment
        - Difficulty level fit
        - Group size (not full)
        - Active groups
        """
        # Get student profile and skills  
        student, student_skills = await self.get_student_with_skills(db, student_id)
        if not student:
            return []
        
        # Get active study groups
        result = await db.execute(
            select(StudyGroup)
            .where(StudyGroup.is_active == True)
            .limit(50)
        )
        groups = result.scalars().all()
        
        if not groups:
            return []
        
        # TODO: Check if student is already member of groups
        
        # Score each study group
        scored_groups = []
        for group in groups:
            topic_score = self._calculate_topic_score(student_skills, group)
            capacity_score = self._calculate_capacity_score(group)
            activity_score = self._calculate_activity_level(group)
            
            embedding_score = 0.5
            
            # Study group weights
            final_score = (
                0.40 * embedding_score +
                0.30 * topic_score +
                0.20 * capacity_score +
                0.10 * activity_score
            )
            
            scored_groups.append({
                "group": group,
                "score": final_score,
                "topic_match": int(topic_score * 100),
            })
        
        scored_groups.sort(key=lambda x: x["score"], reverse=True)
        
        recommendations = []
        for item in scored_groups[:limit]:
            group = item["group"]
            recommendations.append({
                "id": str(group.id),
                "name": group.name,
                "description": group.description[:200] + "..." if group.description and len(group.description) > 200 else group.description,
                "domain": group.domain,
                "skill_level": group.skill_level.value if group.skill_level else "beginner",
                "max_members": group.max_members,
                "owner_id": str(group.owner_id),
                "is_active": group.is_active,
                "created_at": group.created_at.isoformat(),
                "topic_match": item["topic_match"],
                "score": round(item["score"], 3),
            })
        
        return recommendations
    
    def _calculate_topic_score(self, student_skills: list[str], group: StudyGroup) -> float:
        """
        Calculate topic alignment score.
        
        Check if group's topic matches student's skills/interests.
        """
        if not group.domain:
            return 0.5
        
        domain_lower = group.domain.lower()
        student_skills_lower = [s.lower() for s in student_skills]
        
        # Check for keyword matches
        for skill in student_skills_lower:
            if skill in domain_lower or domain_lower in skill:
                return 0.9
        
        # Check for domain matches
        domains = ["backend", "frontend", "ml", "ai", "data", "mobile", "devops"]
        for domain in domains:
            if domain in domain_lower:
                return 0.7
        
        return 0.5
    
    def _calculate_capacity_score(self, group: StudyGroup) -> float:
        """
        Calculate capacity score.
        
        Returns 0 if full, 1 if plenty of space.
        """
        if not group.max_members:
            return 0.8  # Unlimited capacity
        
        # TODO: Count current members from relationships
        # Assume some members for now
        assumed_current = 3
        remaining = group.max_members - assumed_current
        
        if remaining <= 0:
            return 0.0
        elif remaining >= 5:
            return 1.0
        else:
            return remaining / 5.0
    
    def _calculate_activity_level(self, group: StudyGroup) -> float:
        """
        Calculate group activity level.
        
        Active groups are more valuable.
        """
        if not group.is_active:
            return 0.0
        
        # TODO: Track actual activity metrics in Phase 5
        return 0.7
