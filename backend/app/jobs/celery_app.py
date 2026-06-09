"""
Celery application — background task processing with Redis broker.

Workers:
- Resume Processing: PDF → text → skills → profile JSON
- Embedding Generation: profile → 384-dim vector → Qdrant
- Recommendation Refresh: nightly / on profile change
- Email Notifications: application status changes
"""

from celery import Celery

celery_app = Celery(
    "skillbridge",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_routes={
        "app.jobs.celery_app.process_resume": {"queue": "resume"},
        "app.jobs.celery_app.generate_embeddings": {"queue": "ml"},
        "app.jobs.celery_app.refresh_recommendations": {"queue": "ml"},
        "app.jobs.celery_app.send_notification": {"queue": "notifications"},
    },
)


@celery_app.task(name="process_resume")
def process_resume(resume_id: str):
    """
    Async resume processing: extract text, parse skills, build profile.
    
    This task runs in background to avoid blocking API requests.
    """
    import asyncio
    from app.db.session import async_session_factory
    from uuid import UUID
    
    async def _process():
        from app.services.resume_service import ResumeService
        
        async with async_session_factory() as db:
            service = ResumeService()
            # Get resume to find file path
            from sqlalchemy import select
            from app.models.resume import Resume
            
            result = await db.execute(select(Resume).where(Resume.id == UUID(resume_id)))
            resume = result.scalar_one_or_none()
            
            if not resume:
                raise ValueError(f"Resume {resume_id} not found")
            
            # Get file path from file_url
            file_path = resume.file_url  # e.g., "storage/resumes/filename.pdf"
            
            # Process resume
            await service.process_resume(db, UUID(resume_id), file_path)
    
    # Run async function in event loop
    asyncio.run(_process())


@celery_app.task(name="generate_embeddings")
def generate_embeddings(entity_type: str, entity_id: str):
    """
    Generate embedding vector and store in Qdrant.
    
    Supports: resume, job, internship, course
    """
    from app.vector.embedding_service import get_embedding_service
    from app.vector.qdrant_client import get_qdrant_service
    
    embedding_service = get_embedding_service()
    qdrant_service = get_qdrant_service()
    
    # Implementation depends on entity type
    # For now, this is a placeholder for future entities
    # Resume embeddings are handled in process_resume task
    pass


@celery_app.task(name="refresh_recommendations")
def refresh_recommendations(student_id: str):
    """Re-compute recommendations for a student."""
    # To be implemented in Phase 4
    pass


@celery_app.task(name="send_notification")
def send_notification(user_id: str, notification_type: str, data: dict):
    """Send email/push notification."""
    # To be implemented in Phase 5
    pass
