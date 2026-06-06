"""Skill schemas."""

import uuid
from pydantic import BaseModel


class SkillBase(BaseModel):
    name: str
    category: str | None = None


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}
