from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin


class CareerGoal(Base, UUIDMixin):
    __tablename__ = "career_goals"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    students: Mapped[list["Student"]] = relationship(
        "Student", secondary="student_goals", back_populates="goals"
    )
