"""Resume schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel

from app.models.resume import ResumeStatus


class ResumeUploadResponse(BaseModel):
    id: uuid.UUID
    status: ResumeStatus
    original_filename: str
    message: str = "Resume uploaded successfully"

    model_config = {"from_attributes": True}


class ResumeResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    file_url: str
    original_filename: str
    parsed_data: dict | None = None
    skills_extracted: list | None = None
    score: float | None = None
    status: ResumeStatus
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class ResumeListResponse(BaseModel):
    resumes: list[ResumeResponse]
    total: int
