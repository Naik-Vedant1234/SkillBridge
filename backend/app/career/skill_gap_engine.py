"""Skill Gap Engine — computes gap between student skills and role requirements."""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.career_role import CareerRole, RoleSkill, SkillImportance
from app.models.student import Student, student_skills
from app.models.skill import Skill


class SkillGapEngine:
    """
    Analyzes the gap between a student's current skills and target role requirements.
    
    Returns:
    - Missing skills ranked by importance
    - Skills the student already has
    - Recommended courses to fill gaps
    """

    async def analyze_gap(self, db: AsyncSession, student_id: UUID, role_id: UUID) -> dict:
        """
        Analyze skill gap for a student targeting a specific career role.
        
        Args:
            db: Database session
            student_id: Student UUID
            role_id: Career role UUID
            
        Returns:
            Dict with gap analysis including missing skills, current skills, coverage %
        """
        # Get student's current skills
        student_skills_result = await db.execute(
            select(Skill.name)
            .join(student_skills, Skill.id == student_skills.c.skill_id)
            .where(student_skills.c.student_id == student_id)
        )
        current_skills = {row[0].lower() for row in student_skills_result.fetchall()}
        
        # Get role requirements
        role_result = await db.execute(
            select(CareerRole)
            .options(selectinload(CareerRole.role_skills).selectinload(RoleSkill.skill))
            .where(CareerRole.id == role_id)
        )
        role = role_result.scalar_one_or_none()
        
        if not role:
            return {"error": "Career role not found"}
        
        # Analyze gaps
        missing_skills = []
        matched_skills = []
        
        for role_skill in role.role_skills:
            skill_name = role_skill.skill.name
            skill_data = {
                "name": skill_name,
                "importance": role_skill.importance.value,
                "weight": self._importance_to_weight(role_skill.importance)
            }
            
            if skill_name.lower() in current_skills:
                matched_skills.append(skill_data)
            else:
                missing_skills.append(skill_data)
        
        # Sort missing skills by importance
        missing_skills.sort(key=lambda x: x["weight"], reverse=True)
        
        # Calculate coverage
        total_skills = len(role.role_skills)
        matched_count = len(matched_skills)
        coverage_percentage = int((matched_count / total_skills * 100)) if total_skills > 0 else 0
        
        return {
            "role": {
                "id": str(role.id),
                "title": role.title,
                "description": role.description,
                "domain": role.domain
            },
            "analysis": {
                "total_required_skills": total_skills,
                "skills_matched": matched_count,
                "skills_missing": len(missing_skills),
                "coverage_percentage": coverage_percentage
            },
            "missing_skills": missing_skills,
            "matched_skills": matched_skills,
            "recommendations": {
                "priority": "essential" if missing_skills and missing_skills[0]["importance"] == "essential" else "important",
                "focus_areas": [s["name"] for s in missing_skills[:3]] if missing_skills else []
            }
        }
    
    def _importance_to_weight(self, importance: SkillImportance) -> int:
        """Convert importance enum to numeric weight for sorting."""
        weights = {
            SkillImportance.ESSENTIAL: 3,
            SkillImportance.IMPORTANT: 2,
            SkillImportance.NICE_TO_HAVE: 1
        }
        return weights.get(importance, 1)

