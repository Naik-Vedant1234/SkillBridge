from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin


class Skill(Base, UUIDMixin):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    students: Mapped[list["Student"]] = relationship(
        "Student", secondary="student_skills", back_populates="skills"
    )
