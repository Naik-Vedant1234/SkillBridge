"""Mentor schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class MentorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    experience: int | None = None
    domain: str | None = None
    bio: str | None = None
    max_mentees: int = 5


class MentorCreate(MentorBase):
    pass


class MentorUpdate(BaseModel):
    name: str | None = None
    experience: int | None = None
    domain: str | None = None
    bio: str | None = None
    max_mentees: int | None = None


class MentorResponse(MentorBase):
    id: uuid.UUID
    user_id: uuid.UUID
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MentorListResponse(BaseModel):
    mentors: list[MentorResponse]
    total: int
