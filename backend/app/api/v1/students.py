import uuid
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import CurrentUser, DBSession, require_role
from app.models.user import UserRole, User
from app.models.student import Proficiency
from app.schemas.student import StudentResponse, StudentUpdate
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/me", response_model=StudentResponse)
async def get_student_profile(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """Get current student profile (students only)."""
    service = StudentService()
    student = await service.get_student_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student


@router.patch("/me", response_model=StudentResponse)
async def update_student_profile(
    data: StudentUpdate,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """Update current student profile (students only)."""
    service = StudentService()
    student = await service.get_student_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    updated = await service.update_student_profile(db, student.id, data)
    return updated


@router.post("/me/skills/{skill_id}", status_code=201)
async def add_skill_to_student(
    skill_id: uuid.UUID,
    db: DBSession,
    proficiency: Proficiency = Proficiency.BEGINNER,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """Add a skill to current student profile with proficiency level."""
    service = StudentService()
    student = await service.get_student_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    try:
        await service.add_skill_to_student(db, student.id, skill_id, proficiency)
        return {"message": "Skill added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/me/skills/{skill_id}", status_code=204)
async def remove_skill_from_student(
    skill_id: uuid.UUID,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """Remove a skill from current student profile."""
    service = StudentService()
    student = await service.get_student_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    await service.remove_skill_from_student(db, student.id, skill_id)
    return None
