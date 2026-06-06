"""Course schemas."""

import uuid
from pydantic import BaseModel, Field

from app.models.course import CourseDifficulty


class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    provider: str | None = None
    url: str | None = None
    description: str | None = None
    skills_covered: list[str] | None = None
    difficulty: CourseDifficulty | None = None
    duration: str | None = None
    is_free: bool = False


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: str | None = None
    provider: str | None = None
    url: str | None = None
    description: str | None = None
    skills_covered: list[str] | None = None
    difficulty: CourseDifficulty | None = None
    duration: str | None = None
    is_free: bool | None = None


class CourseResponse(CourseBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}


class CourseListResponse(BaseModel):
    courses: list[CourseResponse]
    total: int
