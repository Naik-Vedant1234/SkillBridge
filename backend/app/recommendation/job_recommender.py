"""Job recommender — finds best job matches for students."""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.models.student import Student
from app.models.application import Application
from app.recommendation.base_recommender import BaseRecommender


class JobRecommender(BaseRecommender):
    """Recommends jobs using hybrid ranking."""
    
    async def recommend(
        self, 
        db: AsyncSession,
        student_id: UUID, 
        limit: int = 10
    ) -> list[dict]:
        """
        Get personalized job recommendations for student.
        
        Args:
            db: Database session
            student_id: Student UUID
            limit: Max recommendations to return
            
        Returns:
            List of job dicts with scores, sorted by relevance
        """
        # Get student profile and skills
        student, student_skills = await self.get_student_with_skills(db, student_id)
        if not student:
            return []
        
        # Get all active jobs
        result = await db.execute(
            select(Job)
            .where(Job.is_active == True)
            .limit(100)  # Pre-filter to reasonable set
        )
        jobs = result.scalars().all()
        
        if not jobs:
            return []
        
        # Get student's applied jobs (to exclude)
        from app.models.application import ApplicationTargetType
        applied_result = await db.execute(
            select(Application.target_id)
            .where(
                Application.student_id == student_id,
                Application.target_type == ApplicationTargetType.JOB
            )
        )
        applied_job_ids = {row[0] for row in applied_result.fetchall()}
        
        # Score each job
        scored_jobs = []
        for job in jobs:
            # Skip if already applied
            if job.id in applied_job_ids:
                continue
            
            # Calculate individual scores
            skill_score = self._calculate_skill_score(student_skills, job)
            interest_score = self._calculate_interest_score(student, job)
            popularity_score = self._calculate_popularity_score(job)
            activity_score = self._calculate_activity_score(job)
            
            # TODO: Embedding similarity (Phase 4.2)
            # For now, use skill-based proxy for embedding score
            embedding_score = skill_score * 0.8 + 0.1  # Slight variation from skill score
            
            # Calculate hybrid score
            final_score = self.calculate_hybrid_score(
                embedding_score=embedding_score,
                skill_score=skill_score,
                interest_score=interest_score,
                popularity_score=popularity_score,
                activity_score=activity_score,
            )
            
            scored_jobs.append({
                "job": job,
                "score": final_score,
                "match_percentage": int(final_score * 100),
                "skill_match": int(skill_score * 100),
            })
        
        # Sort by score descending
        scored_jobs.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top N with formatted data
        recommendations = []
        for item in scored_jobs[:limit]:
            job = item["job"]
            salary_range = None
            if job.salary_min and job.salary_max:
                salary_range = f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}"
            elif job.salary_min:
                salary_range = f"${job.salary_min:,.0f}+"
            
            recommendations.append({
                "id": str(job.id),
                "title": job.title,
                "company_id": str(job.company_id),
                "location": job.location or "Remote" if job.is_remote else "Not specified",
                "is_remote": job.is_remote,
                "salary_range": salary_range,
                "requirements": job.requirements or [],
                "description": job.description[:200] + "..." if len(job.description) > 200 else job.description,
                "posted_at": job.created_at.isoformat(),
                "match_percentage": item["match_percentage"],
                "skill_match": item["skill_match"],
                "score": round(item["score"], 3),
            })
        
        return recommendations
    
    def _calculate_skill_score(self, student_skills: list[str], job: Job) -> float:
        """Calculate skill match score."""
        if not job.requirements:
            return 0.5
        
        return self.calculate_skill_match_score(
            student_skills, 
            job.requirements
        )
    
    def _calculate_interest_score(self, student: Student, job: Job) -> float:
        """
        Calculate interest/domain match score.
        
        Based on job title and requirements complexity.
        """
        # Score based on seniority level in title
        title_lower = job.title.lower()
        
        # Entry/Junior positions - good for students
        if any(word in title_lower for word in ['junior', 'entry', 'intern', 'associate', 'graduate']):
            return 0.9
        # Mid-level positions
        elif any(word in title_lower for word in ['senior', 'lead', 'principal', 'staff']):
            return 0.4  # Less suitable for students
        # Standard positions
        else:
            return 0.7
    
    def _calculate_popularity_score(self, job: Job) -> float:
        """
        Calculate popularity score based on job attributes.
        
        Popular attributes: remote work, good salary range, clear requirements
        """
        score = 0.5  # Base score
        
        # Remote jobs are popular
        if job.is_remote:
            score += 0.2
        
        # Jobs with salary info are attractive
        if job.salary_min or job.salary_max:
            score += 0.2
        
        # Jobs with clear requirements
        if job.requirements and len(job.requirements) >= 3:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_activity_score(self, job: Job) -> float:
        """
        Calculate activity/freshness score.
        
        Recent jobs get higher scores.
        """
        now = datetime.now(timezone.utc)
        days_old = (now - job.created_at).days
        
        # Fresh jobs (0-7 days): 1.0
        # Week-old (7-14 days): 0.8
        # Month-old (14-30 days): 0.6
        # Older: 0.4
        if days_old <= 7:
            return 1.0
        elif days_old <= 14:
            return 0.8
        elif days_old <= 30:
            return 0.6
        else:
            return 0.4
