"""Application schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel

from app.models.application import ApplicationTargetType, ApplicationStatus


class ApplicationCreate(BaseModel):
    target_id: uuid.UUID
    target_type: ApplicationTargetType


class ApplicationUpdateStatus(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    target_id: uuid.UUID
    target_type: ApplicationTargetType
    status: ApplicationStatus
    applied_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationListResponse(BaseModel):
    applications: list[ApplicationResponse]
    total: int
