from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, DBSession
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: CurrentUser):
    """Get current authenticated user profile."""
    return current_user
