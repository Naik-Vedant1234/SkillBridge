"""Company schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    website: str | None = None
    logo_url: str | None = None
    industry: str | None = None
    location: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    website: str | None = None
    logo_url: str | None = None
    industry: str | None = None
    location: str | None = None


class CompanyResponse(CompanyBase):
    id: uuid.UUID
    user_id: uuid.UUID
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
