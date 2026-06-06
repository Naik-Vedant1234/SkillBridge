"""Student schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    cgpa: float | None = Field(None, ge=0, le=10)
    college: str | None = None
    graduation_year: int | None = None
    bio: str | None = None
    avatar_url: str | None = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    cgpa: float | None = Field(None, ge=0, le=10)
    college: str | None = None
    graduation_year: int | None = None
    bio: str | None = None
    avatar_url: str | None = None


class StudentResponse(StudentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StudentWithSkills(StudentResponse):
    """Extended profile with skills and career goals — resolved after all schemas load."""
    skills: list[dict] = []   # [{id, name, category}]
    goals: list[dict] = []    # [{id, title}]


class StudentListResponse(BaseModel):
    students: list[StudentResponse]
    total: int
