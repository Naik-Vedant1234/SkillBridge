"""Study group schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.study_group import StudyGroupLevel


class StudyGroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    domain: str | None = None
    skill_level: StudyGroupLevel | None = None
    max_members: int = Field(20, ge=2, le=100)


class StudyGroupCreate(StudyGroupBase):
    pass


class StudyGroupUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    domain: str | None = None
    skill_level: StudyGroupLevel | None = None
    max_members: int | None = None
    is_active: bool | None = None


class StudyGroupResponse(StudyGroupBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StudyGroupListResponse(BaseModel):
    study_groups: list[StudyGroupResponse]
    total: int
