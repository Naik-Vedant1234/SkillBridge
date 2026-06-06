"""Job schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    requirements: list[str] | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    location: str | None = None
    is_remote: bool = False


class JobCreate(JobBase):
    company_id: uuid.UUID


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    requirements: list[str] | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    location: str | None = None
    is_remote: bool | None = None
    is_active: bool | None = None


class JobResponse(JobBase):
    id: uuid.UUID
    company_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    jobs: list[JobResponse]
    total: int
