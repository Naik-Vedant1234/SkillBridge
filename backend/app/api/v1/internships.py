from fastapi import APIRouter

router = APIRouter(prefix="/internships", tags=["Internships"])


@router.get("/")
async def list_internships():
    return {"message": "List internships - to be implemented"}


@router.post("/")
async def create_internship():
    return {"message": "Create internship - to be implemented"}


@router.get("/{internship_id}")
async def get_internship(internship_id: str):
    return {"message": "Get internship - to be implemented"}
