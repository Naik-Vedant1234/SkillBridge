from fastapi import APIRouter

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload")
async def upload_resume():
    return {"message": "Upload resume - to be implemented"}


@router.get("/analysis")
async def get_resume_analysis():
    return {"message": "Get resume analysis - to be implemented"}


@router.get("/{resume_id}/score")
async def get_resume_score(resume_id: str):
    return {"message": "Get resume score - to be implemented"}
