from fastapi import APIRouter

router = APIRouter(prefix="/study-groups", tags=["Study Groups"])


@router.get("/")
async def list_study_groups():
    return {"message": "List study groups - to be implemented"}


@router.post("/")
async def create_study_group():
    return {"message": "Create study group - to be implemented"}


@router.get("/{group_id}")
async def get_study_group(group_id: str):
    return {"message": "Get study group - to be implemented"}


@router.post("/{group_id}/join")
async def join_study_group(group_id: str):
    return {"message": "Join study group - to be implemented"}
