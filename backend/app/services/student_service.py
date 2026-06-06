"""Student service — student profile management."""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.models.student import Student, student_skills, Proficiency
from app.models.skill import Skill
from app.schemas.student import StudentUpdate


class StudentService:
    """Business logic for student profile management."""

    async def get_student_by_user_id(
        self, db: AsyncSession, user_id: uuid.UUID
    ) -> Student | None:
        """Get student profile by user ID with skills and goals."""
        result = await db.execute(
            select(Student)
            .where(Student.user_id == user_id)
            .options(selectinload(Student.skills), selectinload(Student.goals))
        )
        return result.scalar_one_or_none()

    async def update_student_profile(
        self, db: AsyncSession, student_id: uuid.UUID, data: StudentUpdate
    ) -> Student:
        """Update student profile fields."""
        result = await db.execute(select(Student).where(Student.id == student_id))
        student = result.scalar_one_or_none()
        if not student:
            raise ValueError("Student not found")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student, field, value)

        await db.commit()
        await db.refresh(student)
        return student

    async def add_skill_to_student(
        self,
        db: AsyncSession,
        student_id: uuid.UUID,
        skill_id: uuid.UUID,
        proficiency: Proficiency = Proficiency.BEGINNER,
    ) -> None:
        """Add a skill to student profile with proficiency level."""
        # Verify skill exists
        skill_result = await db.execute(select(Skill).where(Skill.id == skill_id))
        skill = skill_result.scalar_one_or_none()
        if not skill:
            raise ValueError("Skill not found")

        # Check if already exists
        check = await db.execute(
            select(student_skills).where(
                student_skills.c.student_id == student_id,
                student_skills.c.skill_id == skill_id,
            )
        )
        if check.first():
            raise ValueError("Skill already added to student")

        # Insert into association table
        await db.execute(
            student_skills.insert().values(
                student_id=student_id, skill_id=skill_id, proficiency=proficiency
            )
        )
        await db.commit()

    async def remove_skill_from_student(
        self, db: AsyncSession, student_id: uuid.UUID, skill_id: uuid.UUID
    ) -> None:
        """Remove a skill from student profile."""
        await db.execute(
            delete(student_skills).where(
                student_skills.c.student_id == student_id,
                student_skills.c.skill_id == skill_id,
            )
        )
        await db.commit()
