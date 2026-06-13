"""Recommendation API endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DBSession, require_role
from app.models.user import User, UserRole
from app.models.student import Student
from app.recommendation.job_recommender import JobRecommender
from app.recommendation.internship_recommender import InternshipRecommender
from app.recommendation.mentor_recommender import MentorRecommender
from app.recommendation.course_recommender import CourseRecommender
from app.recommendation.studygroup_recommender import StudyGroupRecommender

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/jobs")
async def get_job_recommendations(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
):
    """
    Get personalized job recommendations for student.
    
    Returns jobs ranked by:
    - Skill match
    - Interest alignment  
    - Popularity
    - Recency
    """
    # Get student profile from database (avoid lazy loading)
    from app.models.student import Student
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        return {"recommendations": [], "total": 0}
    
    recommender = JobRecommender()
    recommendations = await recommender.recommend(
        db=db,
        student_id=student.id,
        limit=limit
    )
    
    return {
        "recommendations": recommendations,
        "total": len(recommendations)
    }


@router.get("/internships")
async def get_internship_recommendations(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Get personalized internship recommendations for student.
    
    Considers timeline and learning opportunities.
    """
    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        return {"recommendations": [], "total": 0}
    
    recommender = InternshipRecommender()
    recommendations = await recommender.recommend(
        db=db,
        student_id=student.id,
        limit=limit
    )
    
    return {
        "recommendations": recommendations,
        "total": len(recommendations)
    }


@router.get("/mentors")
async def get_mentor_recommendations(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Get personalized mentor recommendations for student.
    
    Matches based on:
    - Domain expertise
    - Availability
    - Experience level
    """
    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        return {"recommendations": [], "total": 0}
    
    recommender = MentorRecommender()
    recommendations = await recommender.recommend(
        db=db,
        student_id=student.id,
        limit=limit
    )
    
    return {
        "recommendations": recommendations,
        "total": len(recommendations)
    }


@router.get("/courses")
async def get_course_recommendations(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    limit: int = Query(10, ge=1, le=50),
    target_skills: list[str] = Query(None, description="Specific skills to learn"),
):
    """
    Get personalized course recommendations for student.
    
    Suggests courses based on:
    - Skill gaps
    - Learning goals
    - Difficulty level
    - Ratings
    """
    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        return {"recommendations": [], "total": 0}
    
    recommender = CourseRecommender()
    recommendations = await recommender.recommend(
        db=db,
        student_id=student.id,
        limit=limit,
        target_skills=target_skills
    )
    
    return {
        "recommendations": recommendations,
        "total": len(recommendations)
    }


@router.get("/study-groups")
async def get_study_group_recommendations(
    db: DBSession,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Get personalized study group recommendations for student.
    
    Matches based on:
    - Topic alignment
    - Group capacity
    - Activity level
    """
    # Get student profile
    result = await db.execute(
        select(Student).where(Student.user_id == current_user.id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        return {"recommendations": [], "total": 0}
    
    recommender = StudyGroupRecommender()
    recommendations = await recommender.recommend(
        db=db,
        student_id=student.id,
        limit=limit
    )
    
    return {
        "recommendations": recommendations,
        "total": len(recommendations)
    }
