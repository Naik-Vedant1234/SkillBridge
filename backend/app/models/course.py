import enum

from sqlalchemy import Boolean, Enum, Float, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, UUIDMixin


class CourseDifficulty(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Course(Base, UUIDMixin):
    __tablename__ = "courses"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str | None] = mapped_column(String(255), nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills_covered: Mapped[list | None] = mapped_column(JSON, nullable=True)
    difficulty: Mapped[CourseDifficulty | None] = mapped_column(Enum(CourseDifficulty), nullable=True)
    duration: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_free: Mapped[bool] = mapped_column(Boolean, default=False)
