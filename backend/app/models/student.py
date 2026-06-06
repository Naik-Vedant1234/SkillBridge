import enum
import uuid

from sqlalchemy import (
    Boolean, Column, Enum, Float, ForeignKey, Integer, String, Table, Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Proficiency(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


# Association table: student <-> skill
student_skills = Table(
    "student_skills",
    Base.metadata,
    Column("student_id", UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
    Column("proficiency", Enum(Proficiency, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=Proficiency.BEGINNER),
)

# Association table: student <-> career_goal
student_goals = Table(
    "student_goals",
    Base.metadata,
    Column("student_id", UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("goal_id", UUID(as_uuid=True), ForeignKey("career_goals.id", ondelete="CASCADE"), primary_key=True),
)


class Student(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "students"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    cgpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    college: Mapped[str | None] = mapped_column(String(255), nullable=True)
    graduation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="student")
    skills: Mapped[list["Skill"]] = relationship("Skill", secondary=student_skills, back_populates="students")
    goals: Mapped[list["CareerGoal"]] = relationship("CareerGoal", secondary=student_goals, back_populates="students")
    resumes: Mapped[list["Resume"]] = relationship("Resume", back_populates="student")
    applications: Mapped[list["Application"]] = relationship("Application", back_populates="student")
    recommendations: Mapped[list["Recommendation"]] = relationship("Recommendation", back_populates="student")
    mentor_requests: Mapped[list["MentorRequest"]] = relationship(
        "MentorRequest", back_populates="student", foreign_keys="MentorRequest.student_id"
    )
