"""Bookmark model for saved items."""

from datetime import datetime
from enum import Enum as PyEnum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BookmarkTargetType(str, PyEnum):
    """Type of bookmarked item."""
    JOB = "job"
    INTERNSHIP = "internship"
    MENTOR = "mentor"
    COURSE = "course"
    STUDY_GROUP = "study_group"


class Bookmark(Base):
    """Student bookmarks for jobs, internships, mentors, courses, and study groups."""
    
    __tablename__ = "bookmarks"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey("students.id"))
    target_type: Mapped[BookmarkTargetType] = mapped_column(
        Enum(BookmarkTargetType, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False
    )
    target_id: Mapped[UUID] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="bookmarks")
    
    def __repr__(self):
        return f"<Bookmark {self.id} - {self.target_type.value}>"
