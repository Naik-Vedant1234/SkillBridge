from fastapi import APIRouter

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/")
async def create_application():
    return {"message": "Create application - to be implemented"}


@router.get("/")
async def list_my_applications():
    return {"message": "List applications - to be implemented"}


@router.get("/{application_id}")
async def get_application(application_id: str):
    return {"message": "Get application - to be implemented"}


@router.put("/{application_id}/status")
async def update_application_status(application_id: str):
    return {"message": "Update application status - to be implemented"}
