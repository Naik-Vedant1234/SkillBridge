"""Bookmark API endpoints."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DBSession, require_role
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.bookmark import Bookmark, BookmarkTargetType


router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])


# Request models
class CreateBookmarkRequest(BaseModel):
    target_type: BookmarkTargetType
    target_id: UUID


@router.post("/")
async def create_bookmark(
    request: CreateBookmarkRequest,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """
    Save/bookmark an item (job, internship, mentor, course, study group).
    """
    # Get student
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Check if already bookmarked
    existing = await db.execute(
        select(Bookmark).where(
            and_(
                Bookmark.student_id == student.id,
                Bookmark.target_type == request.target_type,
                Bookmark.target_id == request.target_id
            )
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Item already bookmarked")
    
    # Create bookmark
    bookmark = Bookmark(
        student_id=student.id,
        target_type=request.target_type,
        target_id=request.target_id
    )
    
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    
    return {
        "id": str(bookmark.id),
        "target_type": bookmark.target_type.value,
        "target_id": str(bookmark.target_id),
        "created_at": bookmark.created_at.isoformat(),
        "message": "Item bookmarked successfully"
    }


@router.get("/me")
async def get_my_bookmarks(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    target_type: str | None = None,
):
    """
    Get all bookmarks for the current student with full item details.
    
    Optional filter by target_type (job, internship, mentor, course, study_group).
    """
    from app.models.job import Job
    from app.models.internship import Internship
    from app.models.mentor import Mentor
    from app.models.course import Course
    from app.models.study_group import StudyGroup
    
    # Get student
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Build query
    query = select(Bookmark).where(Bookmark.student_id == student.id)
    
    if target_type:
        query = query.where(Bookmark.target_type == target_type)
    
    query = query.order_by(Bookmark.created_at.desc())
    
    result = await db.execute(query)
    bookmarks = result.scalars().all()
    
    # Fetch full details for each bookmark
    bookmarks_data = []
    for bm in bookmarks:
        item_data = {
            "id": str(bm.id),
            "target_type": bm.target_type.value,
            "target_id": str(bm.target_id),
            "created_at": bm.created_at.isoformat(),
            "item": None
        }
        
        # Fetch the actual item based on type
        try:
            if bm.target_type == BookmarkTargetType.JOB:
                job_result = await db.execute(select(Job).where(Job.id == bm.target_id))
                job = job_result.scalar_one_or_none()
                if job:
                    item_data["item"] = {
                        "title": job.title,
                        "company_id": str(job.company_id),
                        "location": job.location,
                        "salary_range": job.salary_range,
                        "is_remote": job.is_remote
                    }
            
            elif bm.target_type == BookmarkTargetType.INTERNSHIP:
                intern_result = await db.execute(select(Internship).where(Internship.id == bm.target_id))
                internship = intern_result.scalar_one_or_none()
                if internship:
                    item_data["item"] = {
                        "title": internship.title,
                        "company_id": str(internship.company_id),
                        "location": internship.location,
                        "stipend": internship.stipend,
                        "duration": internship.duration
                    }
            
            elif bm.target_type == BookmarkTargetType.MENTOR:
                mentor_result = await db.execute(select(Mentor).where(Mentor.id == bm.target_id))
                mentor = mentor_result.scalar_one_or_none()
                if mentor:
                    item_data["item"] = {
                        "name": mentor.name,
                        "domain": mentor.domain,
                        "experience": mentor.experience_years,
                        "bio": mentor.bio[:100] + "..." if len(mentor.bio) > 100 else mentor.bio
                    }
            
            elif bm.target_type == BookmarkTargetType.COURSE:
                course_result = await db.execute(select(Course).where(Course.id == bm.target_id))
                course = course_result.scalar_one_or_none()
                if course:
                    item_data["item"] = {
                        "title": course.title,
                        "provider": course.provider,
                        "difficulty": course.difficulty,
                        "duration": course.duration,
                        "is_free": course.is_free
                    }
            
            elif bm.target_type == BookmarkTargetType.STUDY_GROUP:
                group_result = await db.execute(select(StudyGroup).where(StudyGroup.id == bm.target_id))
                group = group_result.scalar_one_or_none()
                if group:
                    item_data["item"] = {
                        "name": group.name,
                        "domain": group.domain,
                        "skill_level": group.skill_level,
                        "current_members": group.current_members,
                        "max_members": group.max_members
                    }
        except Exception as e:
            print(f"Error fetching item details: {e}")
            # Continue with None item data
        
        bookmarks_data.append(item_data)
    
    return {
        "bookmarks": bookmarks_data,
        "total": len(bookmarks_data)
    }


@router.delete("/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: UUID,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """
    Remove a bookmark.
    """
    # Get student
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Get bookmark
    bm_result = await db.execute(
        select(Bookmark).where(
            and_(
                Bookmark.id == bookmark_id,
                Bookmark.student_id == student.id
            )
        )
    )
    bookmark = bm_result.scalar_one_or_none()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    await db.delete(bookmark)
    await db.commit()
    
    return {"message": "Bookmark removed successfully"}


@router.delete("/by-target/{target_type}/{target_id}")
async def delete_bookmark_by_target(
    target_type: BookmarkTargetType,
    target_id: UUID,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """
    Remove a bookmark by target type and ID.
    
    Useful for toggle functionality in UI.
    """
    # Get student
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Get bookmark
    bm_result = await db.execute(
        select(Bookmark).where(
            and_(
                Bookmark.student_id == student.id,
                Bookmark.target_type == target_type,
                Bookmark.target_id == target_id
            )
        )
    )
    bookmark = bm_result.scalar_one_or_none()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    await db.delete(bookmark)
    await db.commit()
    
    return {"message": "Bookmark removed successfully"}


@router.get("/check/{target_type}/{target_id}")
async def check_bookmark(
    target_type: BookmarkTargetType,
    target_id: UUID,
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
):
    """
    Check if an item is bookmarked.
    
    Returns bookmarked: true/false and bookmark_id if exists.
    """
    # Get student
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Check bookmark
    bm_result = await db.execute(
        select(Bookmark).where(
            and_(
                Bookmark.student_id == student.id,
                Bookmark.target_type == target_type,
                Bookmark.target_id == target_id
            )
        )
    )
    bookmark = bm_result.scalar_one_or_none()
    
    if bookmark:
        return {
            "bookmarked": True,
            "bookmark_id": str(bookmark.id)
        }
    
    return {"bookmarked": False}
