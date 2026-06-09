import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillResponse

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("/", response_model=list[SkillResponse])
async def list_skills(
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """List all available skills."""
    result = await db.execute(
        select(Skill).order_by(Skill.name).limit(limit)
    )
    skills = result.scalars().all()
    return [SkillResponse.model_validate(skill) for skill in skills]


@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(
    skill_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get skill by ID."""
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return SkillResponse.model_validate(skill)