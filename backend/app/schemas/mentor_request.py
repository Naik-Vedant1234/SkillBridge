"""Mentor request schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel

from app.models.mentor_request import MentorRequestStatus


class MentorRequestCreate(BaseModel):
    mentor_id: uuid.UUID
    message: str | None = None


class MentorRequestUpdateStatus(BaseModel):
    status: MentorRequestStatus


class MentorRequestResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    mentor_id: uuid.UUID
    message: str | None = None
    status: MentorRequestStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MentorRequestListResponse(BaseModel):
    requests: list[MentorRequestResponse]
    total: int
