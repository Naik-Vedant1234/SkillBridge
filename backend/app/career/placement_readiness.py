"""
Placement Readiness Engine — computes a 0-100 readiness score.

Inputs: Skills + Projects + Internships + Resume Score
Output: Score with breakdown by category
"""

from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student, student_skills
from app.models.application import Application, ApplicationTargetType, ApplicationStatus
from app.models.resume import Resume


class PlacementReadinessEngine:
    """
    Calculates placement readiness score based on multiple factors.
    
    Scoring breakdown:
    - Skills: 30 points (number and quality of skills)
    - Projects: 25 points (GitHub projects)
    - Experience: 25 points (internships, work experience)
    - Resume: 20 points (resume quality and completeness)
    """
    
    # Scoring weights
    WEIGHT_SKILLS = 30
    WEIGHT_PROJECTS = 25
    WEIGHT_EXPERIENCE = 25
    WEIGHT_RESUME = 20
    
    async def compute_score(self, db: AsyncSession, student_id: UUID) -> dict:
        """
        Compute placement readiness score for a student.
        
        Args:
            db: Database session
            student_id: Student UUID
            
        Returns:
            Dict with overall score and breakdown by category
        """
        # Get student
        student_result = await db.execute(
            select(Student).where(Student.id == student_id)
        )
        student = student_result.scalar_one_or_none()
        
        if not student:
            return {"error": "Student not found"}
        
        # Calculate individual scores
        skills_score = await self._calculate_skills_score(db, student_id)
        projects_score = await self._calculate_projects_score(db, student)
        experience_score = await self._calculate_experience_score(db, student_id)
        resume_score = await self._calculate_resume_score(db, student_id)
        
        # Calculate total
        total_score = (
            skills_score * (self.WEIGHT_SKILLS / 100) +
            projects_score * (self.WEIGHT_PROJECTS / 100) +
            experience_score * (self.WEIGHT_EXPERIENCE / 100) +
            resume_score * (self.WEIGHT_RESUME / 100)
        )
        
        # Determine readiness level
        if total_score >= 80:
            readiness_level = "Excellent"
            message = "You're well-prepared for placements!"
        elif total_score >= 60:
            readiness_level = "Good"
            message = "You're on track. Focus on improving weaker areas."
        elif total_score >= 40:
            readiness_level = "Fair"
            message = "Build more skills and projects to improve readiness."
        else:
            readiness_level = "Needs Improvement"
            message = "Focus on building foundational skills and experience."
        
        return {
            "overall_score": int(total_score),
            "readiness_level": readiness_level,
            "message": message,
            "breakdown": {
                "skills": {
                    "score": int(skills_score),
                    "max_score": self.WEIGHT_SKILLS,
                    "percentage": int((skills_score / 100) * 100)
                },
                "projects": {
                    "score": int(projects_score),
                    "max_score": self.WEIGHT_PROJECTS,
                    "percentage": int((projects_score / 100) * 100)
                },
                "experience": {
                    "score": int(experience_score),
                    "max_score": self.WEIGHT_EXPERIENCE,
                    "percentage": int((experience_score / 100) * 100)
                },
                "resume": {
                    "score": int(resume_score),
                    "max_score": self.WEIGHT_RESUME,
                    "percentage": int((resume_score / 100) * 100)
                }
            },
            "recommendations": self._generate_recommendations(
                skills_score, projects_score, experience_score, resume_score
            )
        }
    
    async def _calculate_skills_score(self, db: AsyncSession, student_id: UUID) -> float:
        """Calculate score based on number and diversity of skills (0-100)."""
        # Count student's skills
        result = await db.execute(
            select(func.count())
            .select_from(student_skills)
            .where(student_skills.c.student_id == student_id)
        )
        skill_count = result.scalar() or 0
        
        # Scoring: 0-2 skills = 20%, 3-5 = 50%, 6-9 = 75%, 10+ = 100%
        if skill_count >= 10:
            return 100
        elif skill_count >= 6:
            return 75
        elif skill_count >= 3:
            return 50
        elif skill_count >= 1:
            return 30
        else:
            return 0
    
    async def _calculate_projects_score(self, db: AsyncSession, student: Student) -> float:
        """Calculate score based on projects (0-100)."""
        # For Phase 4, we'll use a simple check
        # In future, parse GitHub or project count from resume
        # For now, give default score based on profile completeness
        if student.bio and len(student.bio) > 50:
            return 60  # Has detailed bio, likely has projects
        elif student.bio:
            return 40
        else:
            return 20
    
    async def _calculate_experience_score(self, db: AsyncSession, student_id: UUID) -> float:
        """Calculate score based on internships and applications (0-100)."""
        # Count accepted internship applications
        result = await db.execute(
            select(func.count())
            .select_from(Application)
            .where(
                Application.student_id == student_id,
                Application.target_type == ApplicationTargetType.INTERNSHIP,
                Application.status == ApplicationStatus.ACCEPTED
            )
        )
        accepted_internships = result.scalar() or 0
        
        # Count total applications (shows effort)
        result = await db.execute(
            select(func.count())
            .select_from(Application)
            .where(Application.student_id == student_id)
        )
        total_applications = result.scalar() or 0
        
        # Scoring
        experience_score = 0
        if accepted_internships >= 2:
            experience_score += 70
        elif accepted_internships == 1:
            experience_score += 50
        
        # Bonus for application activity
        if total_applications >= 10:
            experience_score += 30
        elif total_applications >= 5:
            experience_score += 20
        elif total_applications >= 1:
            experience_score += 10
        
        return min(experience_score, 100)
    
    async def _calculate_resume_score(self, db: AsyncSession, student_id: UUID) -> float:
        """Calculate score based on resume quality (0-100)."""
        # Check if resume exists
        result = await db.execute(
            select(Resume)
            .where(Resume.student_id == student_id)
            .order_by(Resume.uploaded_at.desc())
            .limit(1)
        )
        resume = result.scalar_one_or_none()
        
        if not resume:
            return 0
        
        # Resume exists: 40 points
        score = 40
        
        # Resume has analysis: 30 points
        if resume.parsed_data:
            score += 30
        
        # Resume score (if we have it): 30 points
        if resume.score:
            score += min(resume.score / 100 * 30, 30)
        
        return min(score, 100)
    
    def _generate_recommendations(
        self, 
        skills: float, 
        projects: float, 
        experience: float, 
        resume: float
    ) -> list[str]:
        """Generate recommendations based on weak areas."""
        recommendations = []
        
        if skills < 60:
            recommendations.append("Learn 3-5 more in-demand technical skills")
        if projects < 60:
            recommendations.append("Build 2-3 portfolio projects showcasing your skills")
        if experience < 60:
            recommendations.append("Apply to internships to gain practical experience")
        if resume < 60:
            recommendations.append("Upload and optimize your resume")
        
        if not recommendations:
            recommendations.append("Keep updating your skills and applying to opportunities")
        
        return recommendations

