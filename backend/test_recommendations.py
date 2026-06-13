"""Test script to verify all recommendation endpoints work."""
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.user import User, UserRole
from app.models.student import Student
from app.recommendation.job_recommender import JobRecommender
from app.recommendation.internship_recommender import InternshipRecommender
from app.recommendation.mentor_recommender import MentorRecommender
from app.recommendation.course_recommender import CourseRecommender
from app.recommendation.studygroup_recommender import StudyGroupRecommender


async def test_all_recommenders():
    print("\n" + "="*70)
    print("TESTING RECOMMENDATION ENGINES")
    print("="*70 + "\n")
    
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Get first student
        result = await db.execute(
            select(Student).limit(1)
        )
        student = result.scalar_one_or_none()
        
        if not student:
            print("❌ No student found in database!")
            return
        
        print(f"📋 Testing with student: {student.name} (ID: {student.id})\n")
        
        # Test Job Recommendations
        print("1️⃣  Testing Job Recommender...")
        try:
            job_rec = JobRecommender()
            jobs = await job_rec.recommend(db, student.id, limit=5)
            print(f"   ✅ Jobs returned: {len(jobs)}")
            if jobs:
                print(f"      Top result: {jobs[0].get('title', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Test Internship Recommendations
        print("\n2️⃣  Testing Internship Recommender...")
        try:
            intern_rec = InternshipRecommender()
            internships = await intern_rec.recommend(db, student.id, limit=5)
            print(f"   ✅ Internships returned: {len(internships)}")
            if internships:
                print(f"      Top result: {internships[0].get('title', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Test Mentor Recommendations
        print("\n3️⃣  Testing Mentor Recommender...")
        try:
            mentor_rec = MentorRecommender()
            mentors = await mentor_rec.recommend(db, student.id, limit=5)
            print(f"   ✅ Mentors returned: {len(mentors)}")
            if mentors:
                print(f"      Top result: {mentors[0].get('name', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Test Course Recommendations
        print("\n4️⃣  Testing Course Recommender...")
        try:
            course_rec = CourseRecommender()
            courses = await course_rec.recommend(db, student.id, limit=5)
            print(f"   ✅ Courses returned: {len(courses)}")
            if courses:
                print(f"      Top result: {courses[0].get('title', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Test Study Group Recommendations
        print("\n5️⃣  Testing Study Group Recommender...")
        try:
            group_rec = StudyGroupRecommender()
            groups = await group_rec.recommend(db, student.id, limit=5)
            print(f"   ✅ Study Groups returned: {len(groups)}")
            if groups:
                print(f"      Top result: {groups[0].get('name', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    await engine.dispose()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(test_all_recommenders())
