"""Mentor recommender — matches students with mentors."""

from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mentor import Mentor
from app.models.student import Student
from app.models.mentor_request import MentorRequest
from app.recommendation.base_recommender import BaseRecommender


class MentorRecommender(BaseRecommender):
    """Recommends mentors based on expertise and availability."""
    
    async def recommend(
        self, 
        db: AsyncSession,
        student_id: UUID, 
        limit: int = 10
    ) -> list[dict]:
        """
        Get personalized mentor recommendations.
        
        Matching criteria:
        - Domain/expertise alignment
        - Availability (max_mentees not reached)
        - Experience level
        - Verified status
        """
        # Get student profile and skills
        student, student_skills = await self.get_student_with_skills(db, student_id)
        if not student:
            return []
        
        # Get verified, available mentors
        result = await db.execute(
            select(Mentor)
            .where(Mentor.is_verified == True)
            .limit(50)
        )
        mentors = result.scalars().all()
        
        if not mentors:
            return []
        
        # Get existing mentor requests from this student
        requested_result = await db.execute(
            select(MentorRequest.mentor_id)
            .where(MentorRequest.student_id == student_id)
        )
        requested_mentor_ids = {row[0] for row in requested_result.fetchall()}
        
        # Score each mentor
        scored_mentors = []
        for mentor in mentors:
            # Skip if already requested
            if mentor.id in requested_mentor_ids:
                continue
            
            # Check availability
            availability_score = self._calculate_availability_score(mentor)
            if availability_score == 0:
                continue  # Skip mentors at capacity
            
            domain_score = self._calculate_domain_score(student, mentor)
            experience_score = self._calculate_experience_score(mentor)
            verification_score = 1.0 if mentor.is_verified else 0.3
            
            embedding_score = 0.5  # TODO: Add vector similarity
            
            # Mentor-specific weights
            final_score = (
                0.30 * embedding_score +
                0.30 * domain_score +
                0.20 * experience_score +
                0.10 * verification_score +
                0.10 * availability_score
            )
            
            scored_mentors.append({
                "mentor": mentor,
                "score": final_score,
                "match_percentage": int(final_score * 100),
                "domain_match": int(domain_score * 100),
            })
        
        scored_mentors.sort(key=lambda x: x["score"], reverse=True)
        
        recommendations = []
        for item in scored_mentors[:limit]:
            mentor = item["mentor"]
            recommendations.append({
                "id": str(mentor.id),
                "name": mentor.name,
                "domain": mentor.domain,
                "experience": mentor.experience,
                "bio": mentor.bio[:150] + "..." if mentor.bio and len(mentor.bio) > 150 else mentor.bio,
                "max_mentees": mentor.max_mentees,
                "is_verified": mentor.is_verified,
                "match_percentage": item["match_percentage"],
                "domain_match": item["domain_match"],
                "score": round(item["score"], 3),
            })
        
        return recommendations
    
    def _calculate_availability_score(self, mentor: Mentor) -> float:
        """
        Calculate availability score.
        
        Returns 0 if at capacity, 1 if fully available.
        """
        # TODO: Count current mentees from relationships
        # For now, assume available if max_mentees > 0
        if not mentor.max_mentees or mentor.max_mentees <= 0:
            return 0.0
        
        # Assume some current mentees (will be accurate in Phase 5)
        assumed_current = 2
        remaining = mentor.max_mentees - assumed_current
        
        if remaining <= 0:
            return 0.0
        elif remaining >= 3:
            return 1.0
        else:
            return remaining / 3.0
    
    def _calculate_domain_score(self, student: Student, mentor: Mentor) -> float:
        """
        Calculate domain alignment score.
        
        Match mentor's domain with student's interests/goals.
        """
        if not mentor.domain:
            return 0.5
        
        # TODO: Match against student career goals
        # For now, simple keyword matching
        mentor_domain_lower = mentor.domain.lower()
        
        # Check if any student skills relate to mentor domain
        relevant_keywords = ["backend", "frontend", "fullstack", "ml", "ai", "data"]
        if any(kw in mentor_domain_lower for kw in relevant_keywords):
            return 0.8
        
        return 0.6
    
    def _calculate_experience_score(self, mentor: Mentor) -> float:
        """
        Calculate experience score.
        
        More experience = better mentor (with diminishing returns).
        """
        if not mentor.experience:
            return 0.5
        
        years = mentor.experience
        
        # 0-2 years: 0.5
        # 3-5 years: 0.7
        # 6-10 years: 0.9
        # 10+ years: 1.0
        if years <= 2:
            return 0.5
        elif years <= 5:
            return 0.7
        elif years <= 10:
            return 0.9
        else:
            return 1.0
