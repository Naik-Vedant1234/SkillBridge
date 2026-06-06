import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin


class RecommendationTargetType(str, enum.Enum):
    JOB = "job"
    INTERNSHIP = "internship"
    MENTOR = "mentor"
    COURSE = "course"
    STUDYGROUP = "studygroup"


class RecommendationAction(str, enum.Enum):
    VIEWED = "viewed"
    CLICKED = "clicked"
    SAVED = "saved"
    APPLIED = "applied"
    DISMISSED = "dismissed"


class Recommendation(Base, UUIDMixin):
    __tablename__ = "recommendations"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    target_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    target_type: Mapped[RecommendationTargetType] = mapped_column(
        Enum(RecommendationTargetType), nullable=False
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="recommendations")
    events: Mapped[list["RecommendationEvent"]] = relationship(
        "RecommendationEvent", back_populates="recommendation"
    )


class RecommendationEvent(Base, UUIDMixin):
    """Tracks user interactions with recommendations for collaborative filtering."""
    __tablename__ = "recommendation_events"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    recommendation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("recommendations.id", ondelete="CASCADE"), nullable=False
    )
    action: Mapped[RecommendationAction] = mapped_column(
        Enum(RecommendationAction), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    recommendation: Mapped["Recommendation"] = relationship(
        "Recommendation", back_populates="events"
    )
