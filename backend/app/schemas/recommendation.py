"""Recommendation schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel

from app.models.recommendation import RecommendationTargetType, RecommendationAction


class RecommendationResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    target_id: uuid.UUID
    target_type: RecommendationTargetType
    score: float
    reason: str | None = None
    generated_at: datetime

    model_config = {"from_attributes": True}


class RecommendationListResponse(BaseModel):
    recommendations: list[RecommendationResponse]
    total: int


class RecommendationEventCreate(BaseModel):
    recommendation_id: uuid.UUID
    action: RecommendationAction


class RecommendationEventResponse(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    recommendation_id: uuid.UUID
    action: RecommendationAction
    created_at: datetime

    model_config = {"from_attributes": True}
