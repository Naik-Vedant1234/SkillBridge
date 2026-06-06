from fastapi import APIRouter

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/")
async def list_courses():
    return {"message": "List courses - to be implemented"}


@router.get("/{course_id}")
async def get_course(course_id: str):
    return {"message": "Get course - to be implemented"}
