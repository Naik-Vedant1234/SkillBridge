"""Career schemas — career goals, career roles, skill gap, roadmap, placement readiness."""

import uuid
from pydantic import BaseModel, Field

from app.models.career_role import SkillImportance, ProjectDifficulty


# ── Career Goal ──────────────────────────────────────────────────────────────

class CareerGoalBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class CareerGoalCreate(CareerGoalBase):
    pass


class CareerGoalResponse(CareerGoalBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}


# ── Career Role (Knowledge Base) ─────────────────────────────────────────────

class RoleSkillResponse(BaseModel):
    skill_id: uuid.UUID
    skill_name: str
    importance: SkillImportance

    model_config = {"from_attributes": True}


class RoleProjectResponse(BaseModel):
    id: uuid.UUID
    project_title: str
    description: str | None = None
    difficulty: ProjectDifficulty

    model_config = {"from_attributes": True}


class RoleCourseResponse(BaseModel):
    course_id: uuid.UUID
    course_title: str
    priority: int

    model_config = {"from_attributes": True}


class RoleCertificationResponse(BaseModel):
    id: uuid.UUID
    certification_name: str
    provider: str | None = None
    priority: int

    model_config = {"from_attributes": True}


class CareerRoleResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    domain: str | None = None

    model_config = {"from_attributes": True}


class CareerRoleDetailResponse(CareerRoleResponse):
    """Full role details with all knowledge-base relationships."""
    role_skills: list[RoleSkillResponse] = []
    role_projects: list[RoleProjectResponse] = []
    role_courses: list[RoleCourseResponse] = []
    role_certifications: list[RoleCertificationResponse] = []


# ── Skill Gap ─────────────────────────────────────────────────────────────────

class SkillGapItem(BaseModel):
    skill: str
    importance: SkillImportance
    status: str  # "missing" | "in_progress" | "acquired"


class SkillGapResponse(BaseModel):
    career_role: str
    total_required: int
    acquired: int
    missing: int
    gap_percentage: float
    items: list[SkillGapItem]


# ── Placement Readiness ───────────────────────────────────────────────────────

class PlacementReadinessResponse(BaseModel):
    score: float = Field(..., ge=0, le=100, description="Overall readiness score 0–100")
    skill_score: float
    project_score: float
    internship_score: float
    resume_score: float
    breakdown: dict[str, float]
    feedback: list[str]


# ── Roadmap ───────────────────────────────────────────────────────────────────

class RoadmapStep(BaseModel):
    week: int
    title: str
    description: str
    resources: list[str] = []
    skills: list[str] = []


class RoadmapResponse(BaseModel):
    career_role: str
    duration_weeks: int
    steps: list[RoadmapStep]
    generated_by: str = "kb+llm"   # "kb" or "kb+llm"
