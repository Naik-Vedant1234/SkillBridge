from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import CurrentUser, DBSession, require_role
from app.models.user import UserRole, User
from app.schemas.company import CompanyResponse, CompanyUpdate
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/me", response_model=CompanyResponse)
async def get_company_profile(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.COMPANY)),
):
    """Get current company profile (companies only)."""
    service = CompanyService()
    company = await service.get_company_by_user_id(db, current_user.id)
    if not company:
        raise HTTPException(status_code=404, detail="Company profile not found")
    return company


@router.patch("/me", response_model=CompanyResponse)
async def update_company_profile(
    data: CompanyUpdate,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.COMPANY)),
):
    """Update current company profile (companies only)."""
    service = CompanyService()
    company = await service.get_company_by_user_id(db, current_user.id)
    if not company:
        raise HTTPException(status_code=404, detail="Company profile not found")
    
    try:
        updated = await service.update_company_profile(db, company.id, data)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
