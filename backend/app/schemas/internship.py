"""Internship schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class InternshipBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    requirements: list[str] | None = None
    duration: str | None = None
    stipend: float | None = None
    location: str | None = None
    is_remote: bool = False


class InternshipCreate(InternshipBase):
    company_id: uuid.UUID


class InternshipUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    requirements: list[str] | None = None
    duration: str | None = None
    stipend: float | None = None
    location: str | None = None
    is_remote: bool | None = None
    is_active: bool | None = None


class InternshipResponse(InternshipBase):
    id: uuid.UUID
    company_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class InternshipListResponse(BaseModel):
    internships: list[InternshipResponse]
    total: int
