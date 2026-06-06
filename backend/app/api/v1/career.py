from fastapi import APIRouter

router = APIRouter(prefix="/career", tags=["Career"])


@router.get("/skill-gap")
async def get_skill_gap():
    return {"message": "Skill gap analysis - to be implemented"}


@router.get("/roadmap")
async def get_career_roadmap():
    return {"message": "Career roadmap - to be implemented"}


@router.get("/placement-readiness")
async def get_placement_readiness():
    return {"message": "Placement readiness score - to be implemented"}


@router.get("/roles")
async def list_career_roles():
    return {"message": "List career roles - to be implemented"}
