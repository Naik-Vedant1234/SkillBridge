import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class UserRole(str, enum.Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    COMPANY = "company"
    ADMIN = "admin"


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)  # nullable for OAuth users
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, native_enum=False, values_callable=lambda x: [e.value for e in x]), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    google_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)

    # Relationships
    student: Mapped["Student | None"] = relationship("Student", back_populates="user", uselist=False)
    mentor: Mapped["Mentor | None"] = relationship("Mentor", back_populates="user", uselist=False)
    company: Mapped["Company | None"] = relationship("Company", back_populates="user", uselist=False)
    owned_study_groups: Mapped[list["StudyGroup"]] = relationship("StudyGroup", back_populates="owner")
