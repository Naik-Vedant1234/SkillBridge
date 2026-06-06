from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users")
async def list_users():
    return {"message": "List users - to be implemented"}


@router.post("/verify/mentor/{mentor_id}")
async def verify_mentor(mentor_id: str):
    return {"message": "Verify mentor - to be implemented"}


@router.post("/verify/company/{company_id}")
async def verify_company(company_id: str):
    return {"message": "Verify company - to be implemented"}


@router.get("/analytics")
async def get_analytics():
    return {"message": "Get analytics - to be implemented"}
