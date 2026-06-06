import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Mentor(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "mentors"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    max_mentees: Mapped[int] = mapped_column(Integer, default=5)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="mentor")
    mentor_requests: Mapped[list["MentorRequest"]] = relationship(
        "MentorRequest", back_populates="mentor", foreign_keys="MentorRequest.mentor_id"
    )
