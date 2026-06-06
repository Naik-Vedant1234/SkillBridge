from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import CurrentUser, DBSession, require_role
from app.models.user import UserRole, User
from app.schemas.mentor import MentorResponse, MentorUpdate
from app.services.mentor_service import MentorService

router = APIRouter(prefix="/mentors", tags=["Mentors"])


@router.get("/me", response_model=MentorResponse)
async def get_mentor_profile(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.MENTOR)),
):
    """Get current mentor profile (mentors only)."""
    service = MentorService()
    mentor = await service.get_mentor_by_user_id(db, current_user.id)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor profile not found")
    return mentor


@router.patch("/me", response_model=MentorResponse)
async def update_mentor_profile(
    data: MentorUpdate,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.MENTOR)),
):
    """Update current mentor profile (mentors only)."""
    service = MentorService()
    mentor = await service.get_mentor_by_user_id(db, current_user.id)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor profile not found")
    
    try:
        updated = await service.update_mentor_profile(db, mentor.id, data)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
