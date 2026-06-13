import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin


class SkillImportance(str, enum.Enum):
    ESSENTIAL = "essential"
    IMPORTANT = "important"
    NICE_TO_HAVE = "nice_to_have"


class ProjectDifficulty(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class CareerRole(Base, UUIDMixin):
    """Career roles that define required skills, projects, courses, and certifications."""
    __tablename__ = "career_roles"

    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    domain: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    role_skills: Mapped[list["RoleSkill"]] = relationship("RoleSkill", back_populates="role", cascade="all, delete-orphan")
    role_projects: Mapped[list["RoleProject"]] = relationship("RoleProject", back_populates="role", cascade="all, delete-orphan")
    role_courses: Mapped[list["RoleCourse"]] = relationship("RoleCourse", back_populates="role", cascade="all, delete-orphan")
    role_certifications: Mapped[list["RoleCertification"]] = relationship("RoleCertification", back_populates="role", cascade="all, delete-orphan")


class RoleSkill(Base, UUIDMixin):
    __tablename__ = "role_skills"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_roles.id", ondelete="CASCADE"), nullable=False
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )
    importance: Mapped[SkillImportance] = mapped_column(
        Enum(SkillImportance, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        default=SkillImportance.IMPORTANT
    )

    role: Mapped["CareerRole"] = relationship("CareerRole", back_populates="role_skills")
    skill: Mapped["Skill"] = relationship("Skill")


class RoleProject(Base, UUIDMixin):
    __tablename__ = "role_projects"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_roles.id", ondelete="CASCADE"), nullable=False
    )
    project_title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[ProjectDifficulty] = mapped_column(
        Enum(ProjectDifficulty, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        default=ProjectDifficulty.INTERMEDIATE
    )

    role: Mapped["CareerRole"] = relationship("CareerRole", back_populates="role_projects")


class RoleCourse(Base, UUIDMixin):
    __tablename__ = "role_courses"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_roles.id", ondelete="CASCADE"), nullable=False
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    priority: Mapped[int] = mapped_column(Integer, default=1)

    role: Mapped["CareerRole"] = relationship("CareerRole", back_populates="role_courses")
    course: Mapped["Course"] = relationship("Course")


class RoleCertification(Base, UUIDMixin):
    __tablename__ = "role_certifications"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("career_roles.id", ondelete="CASCADE"), nullable=False
    )
    certification_name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str | None] = mapped_column(String(255), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=1)

    role: Mapped["CareerRole"] = relationship("CareerRole", back_populates="role_certifications")
