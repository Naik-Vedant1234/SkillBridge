"""Resume service — handles upload, parsing orchestration, and analysis."""

import os
import uuid
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.resume import Resume, ResumeStatus
from app.models.student import Student
from app.models.skill import Skill
from app.ml.resume_parser import ResumeParser
from app.ml.profile_builder import ProfileBuilder
from app.vector.embedding_service import get_embedding_service
from app.vector.qdrant_client import get_qdrant_service
from app.core.config import settings


class ResumeService:
    """Business logic for resume management."""
    
    def __init__(self):
        self.parser = ResumeParser()
        self.profile_builder = ProfileBuilder()
        self.embedding_service = get_embedding_service()
        self.qdrant_service = get_qdrant_service()
    
    async def upload_and_process_resume(
        self,
        db: AsyncSession,
        student_id: uuid.UUID,
        file_content: bytes,
        filename: str
    ) -> Resume:
        """
        Upload resume file, parse it, and create resume record.
        
        Args:
            db: Database session
            student_id: Student UUID
            file_content: PDF file content as bytes
            filename: Original filename
            
        Returns:
            Resume database record
        """
        # Verify student exists
        result = await db.execute(select(Student).where(Student.id == student_id))
        student = result.scalar_one_or_none()
        if not student:
            raise ValueError("Student not found")
        
        # Save file to storage
        storage_dir = Path(settings.STORAGE_PATH) / "resumes"
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        file_id = uuid.uuid4()
        file_extension = Path(filename).suffix or ".pdf"
        stored_filename = f"{file_id}{file_extension}"
        file_path = storage_dir / stored_filename
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Create resume record
        resume = Resume(
            student_id=student_id,
            file_url=f"storage/resumes/{stored_filename}",
            original_filename=filename,
            status=ResumeStatus.UPLOADED
        )
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
    # Process resume - can be async with Celery or synchronous
        # Set USE_CELERY=true in .env to enable async processing
        use_celery = settings.DEBUG == False  # Use Celery in production only
        
        if use_celery:
            # Async processing with Celery
            try:
                from app.jobs.celery_app import process_resume as process_resume_task
                process_resume_task.delay(str(resume.id))
            except Exception as e:
                # Log Celery error but don't fail upload
                print(f"Celery task failed to queue: {str(e)}")
                # Fall back to synchronous processing
                try:
                    await self.process_resume(db, resume.id, str(file_path))
                except Exception as sync_e:
                    resume.status = ResumeStatus.FAILED
                    await db.commit()
                    raise sync_e
        else:
            # Synchronous processing (for development)
            try:
                await self.process_resume(db, resume.id, str(file_path))
            except ValueError as ve:
                # Specific parsing errors
                resume.status = ResumeStatus.FAILED
                await db.commit()
                raise HTTPException(
                    status_code=400,
                    detail=f"Resume parsing failed: {str(ve)}"
                )
            except Exception as e:
                # General errors
                resume.status = ResumeStatus.FAILED
                await db.commit()
                import traceback
                error_details = traceback.format_exc()
                print(f"Resume processing error: {error_details}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to process resume: {str(e)}"
                )
        
        return resume
    
    async def process_resume(
        self,
        db: AsyncSession,
        resume_id: uuid.UUID,
        file_path: str
    ):
        """
        Parse resume, extract skills, update profile, and generate embeddings.
        
        Args:
            db: Database session
            resume_id: Resume UUID
            file_path: Path to PDF file
        """
        # Get resume record
        result = await db.execute(select(Resume).where(Resume.id == resume_id))
        resume = result.scalar_one_or_none()
        if not resume:
            raise ValueError("Resume not found")
        
        # Update status
        resume.status = ResumeStatus.PROCESSING
        await db.commit()
        
        try:
            # Parse resume
            parsed_data = self.parser.parse_resume(file_path)
            
            # Build profile updates
            profile_updates = self.profile_builder.build_profile(parsed_data)
            
            # Calculate score
            score = self.profile_builder.calculate_resume_score(parsed_data)
            
            # Update resume record
            resume.parsed_data = parsed_data
            resume.skills_extracted = parsed_data.get("skills", [])
            resume.score = score
            resume.status = ResumeStatus.PARSED
            
            # Update student profile
            result = await db.execute(
                select(Student).where(Student.id == resume.student_id)
            )
            student = result.scalar_one()
            
            for key, value in profile_updates.items():
                setattr(student, key, value)
            
            # Add extracted skills to student
            await self._add_skills_to_student(db, student.id, parsed_data.get("skills", []))
            
            await db.commit()
            
            # Generate and store embedding
            embedding = self.embedding_service.generate_resume_embedding(parsed_data)
            self.qdrant_service.upsert_student_profile(
                student_id=str(resume.student_id),
                embedding=embedding,
                payload={
                    "skills": parsed_data.get("skills", []),
                    "experience_years": parsed_data.get("experience_years", 0),
                    "education": parsed_data.get("education", []),
                }
            )
            
        except Exception as e:
            resume.status = ResumeStatus.FAILED
            await db.commit()
            raise
    
    async def _add_skills_to_student(
        self,
        db: AsyncSession,
        student_id: uuid.UUID,
        skill_names: list[str]
    ):
        """Add extracted skills to student profile."""
        from app.models.student import student_skills, Proficiency
        
        for skill_name in skill_names:
            # Find or create skill
            result = await db.execute(
                select(Skill).where(Skill.name == skill_name)
            )
            skill = result.scalar_one_or_none()
            
            if not skill:
                skill = Skill(name=skill_name, category="Technical")
                db.add(skill)
                await db.flush()
            
            # Check if already added
            check = await db.execute(
                select(student_skills).where(
                    student_skills.c.student_id == student_id,
                    student_skills.c.skill_id == skill.id,
                )
            )
            
            if not check.first():
                # Add skill to student
                await db.execute(
                    student_skills.insert().values(
                        student_id=student_id,
                        skill_id=skill.id,
                        proficiency=Proficiency.INTERMEDIATE  # Default from resume
                    )
                )
    
    async def get_resume_by_id(
        self,
        db: AsyncSession,
        resume_id: uuid.UUID
    ) -> Resume | None:
        """Get resume by ID."""
        result = await db.execute(select(Resume).where(Resume.id == resume_id))
        return result.scalar_one_or_none()
    
    async def get_student_resumes(
        self,
        db: AsyncSession,
        student_id: uuid.UUID
    ) -> list[Resume]:
        """Get all resumes for a student."""
        result = await db.execute(
            select(Resume)
            .where(Resume.student_id == student_id)
            .order_by(Resume.uploaded_at.desc())
        )
        return list(result.scalars().all())
