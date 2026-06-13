"""Career Intelligence API endpoints."""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DBSession, require_role
from app.models.user import User, UserRole
from app.models.student import Student
from app.career.skill_gap_engine import SkillGapEngine
from app.career.placement_readiness import PlacementReadinessEngine
from app.career.roadmap_engine import RoadmapEngine
from sqlalchemy import select


router = APIRouter(prefix="/career", tags=["Career Intelligence"])


# Request models
class SkillGapRequest(BaseModel):
    role_id: UUID4


class RoadmapRequest(BaseModel):
    role_id: UUID4
    months: int = 4
    job_description: str | None = None


@router.post("/skill-gap")
async def analyze_skill_gap(
    request: SkillGapRequest,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """
    Analyze skill gap between student's current skills and target role requirements.
    
    Returns:
    - Missing skills ranked by importance
    - Skills already possessed
    - Coverage percentage
    - Recommendations
    """
    # Get student ID
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        return {"error": "Student profile not found"}
    
    engine = SkillGapEngine()
    analysis = await engine.analyze_gap(db, student.id, request.role_id)
    
    return analysis


@router.get("/readiness")
async def get_placement_readiness(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """
    Calculate placement readiness score (0-100) based on:
    - Skills count and diversity (30%)
    - Projects and portfolio (25%)
    - Internship experience (25%)
    - Resume quality (20%)
    
    Returns overall score with breakdown by category.
    """
    # Get student ID
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        return {"error": "Student profile not found"}
    
    engine = PlacementReadinessEngine()
    score = await engine.compute_score(db, student.id)
    
    return score


@router.post("/roadmap")
async def generate_career_roadmap(
    request: RoadmapRequest,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """
    Generate personalized career roadmap using:
    1. Career Knowledge Base (skills, projects, certifications)
    2. Skill Gap Analysis
    3. Gemini AI for timeline personalization
    
    Returns month-by-month milestones with tasks, skills, and projects.
    """
    # Get student ID
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        return {"error": "Student profile not found"}
    
    engine = RoadmapEngine()
    roadmap = await engine.generate(
        db, 
        student.id, 
        request.role_id,
        request.months,
        job_description=request.job_description
    )
    
    return roadmap


@router.get("/roles")
async def list_career_roles(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """
    List all available career roles for students to explore.
    
    Returns list of roles with title, description, and domain.
    """
    from app.models.career_role import CareerRole
    
    result = await db.execute(select(CareerRole))
    roles = result.scalars().all()
    
    return {
        "roles": [
            {
                "id": str(role.id),
                "title": role.title,
                "description": role.description,
                "domain": role.domain
            }
            for role in roles
        ],
        "total": len(roles)
    }
