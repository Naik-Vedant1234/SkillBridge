from fastapi import APIRouter

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/jobs")
async def get_job_recommendations():
    return {"message": "Job recommendations - to be implemented"}


@router.get("/internships")
async def get_internship_recommendations():
    return {"message": "Internship recommendations - to be implemented"}


@router.get("/mentors")
async def get_mentor_recommendations():
    return {"message": "Mentor recommendations - to be implemented"}


@router.get("/courses")
async def get_course_recommendations():
    return {"message": "Course recommendations - to be implemented"}


@router.get("/study-groups")
async def get_study_group_recommendations():
    return {"message": "Study group recommendations - to be implemented"}
