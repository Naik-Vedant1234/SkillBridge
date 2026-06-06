"""Mentor service — mentor profile management."""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.mentor import Mentor
from app.schemas.mentor import MentorUpdate


class MentorService:
    """Business logic for mentor profile management."""

    async def get_mentor_by_user_id(
        self, db: AsyncSession, user_id: uuid.UUID
    ) -> Mentor | None:
        """Get mentor profile by user ID."""
        result = await db.execute(select(Mentor).where(Mentor.user_id == user_id))
        return result.scalar_one_or_none()

    async def update_mentor_profile(
        self, db: AsyncSession, mentor_id: uuid.UUID, data: MentorUpdate
    ) -> Mentor:
        """Update mentor profile fields."""
        result = await db.execute(select(Mentor).where(Mentor.id == mentor_id))
        mentor = result.scalar_one_or_none()
        if not mentor:
            raise ValueError("Mentor not found")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(mentor, field, value)

        await db.commit()
        await db.refresh(mentor)
        return mentor
