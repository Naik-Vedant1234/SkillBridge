from fastapi import APIRouter

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/")
async def list_jobs():
    return {"message": "List jobs - to be implemented"}


@router.post("/")
async def create_job():
    return {"message": "Create job - to be implemented"}


@router.get("/{job_id}")
async def get_job(job_id: str):
    return {"message": "Get job - to be implemented"}
