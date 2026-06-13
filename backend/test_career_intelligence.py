"""Test script for career intelligence features."""
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.student import Student
from app.models.career_role import CareerRole
from app.career.skill_gap_engine import SkillGapEngine
from app.career.placement_readiness import PlacementReadinessEngine
from app.career.roadmap_engine import RoadmapEngine


async def test_career_features():
    print("\n" + "="*70)
    print("TESTING CAREER INTELLIGENCE ENGINES")
    print("="*70 + "\n")
    
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Get a student
        result = await db.execute(select(Student).limit(1))
        student = result.scalar_one_or_none()
        
        if not student:
            print("❌ No student found!")
            return
        
        # Get a career role
        result = await db.execute(select(CareerRole).limit(1))
        role = result.scalar_one_or_none()
        
        if not role:
            print("❌ No career roles found! Run seed_career_roles.py first.")
            return
        
        print(f"📋 Testing with:")
        print(f"   Student: {student.name} (ID: {student.id})")
        print(f"   Target Role: {role.title}\n")
        
        # Test 1: Skill Gap Analysis
        print("1️⃣  Testing Skill Gap Engine...")
        try:
            gap_engine = SkillGapEngine()
            gap_result = await gap_engine.analyze_gap(db, student.id, role.id)
            
            if "error" not in gap_result:
                print(f"   ✅ Skill gap analyzed successfully")
                print(f"      Coverage: {gap_result['analysis']['coverage_percentage']}%")
                print(f"      Skills matched: {gap_result['analysis']['skills_matched']}")
                print(f"      Skills missing: {gap_result['analysis']['skills_missing']}")
                if gap_result['missing_skills']:
                    print(f"      Top missing skill: {gap_result['missing_skills'][0]['name']}")
            else:
                print(f"   ❌ Error: {gap_result['error']}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Test 2: Placement Readiness Score
        print("\n2️⃣  Testing Placement Readiness Engine...")
        try:
            readiness_engine = PlacementReadinessEngine()
            readiness_result = await readiness_engine.compute_score(db, student.id)
            
            if "error" not in readiness_result:
                print(f"   ✅ Readiness score calculated")
                print(f"      Overall Score: {readiness_result['overall_score']}/100")
                print(f"      Level: {readiness_result['readiness_level']}")
                print(f"      Skills: {readiness_result['breakdown']['skills']['score']}/{readiness_result['breakdown']['skills']['max_score']}")
                print(f"      Projects: {readiness_result['breakdown']['projects']['score']}/{readiness_result['breakdown']['projects']['max_score']}")
                print(f"      Experience: {readiness_result['breakdown']['experience']['score']}/{readiness_result['breakdown']['experience']['max_score']}")
                print(f"      Resume: {readiness_result['breakdown']['resume']['score']}/{readiness_result['breakdown']['resume']['max_score']}")
            else:
                print(f"   ❌ Error: {readiness_result['error']}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Test 3: Career Roadmap Generator
        print("\n3️⃣  Testing Career Roadmap Engine...")
        try:
            roadmap_engine = RoadmapEngine()
            roadmap_result = await roadmap_engine.generate(db, student.id, role.id, months=4)
            
            if "error" not in roadmap_result:
                print(f"   ✅ Roadmap generated successfully")
                print(f"      Timeline: {roadmap_result['timeline_months']} months")
                print(f"      Skill coverage: {roadmap_result['skill_coverage']}%")
                print(f"      Milestones: {len(roadmap_result['roadmap'])}")
                if roadmap_result['roadmap']:
                    first_milestone = roadmap_result['roadmap'][0]
                    print(f"      Month 1 focus: {first_milestone['focus']}")
                    if first_milestone['skills_to_learn']:
                        print(f"      Skills to learn: {', '.join(first_milestone['skills_to_learn'][:3])}")
            else:
                print(f"   ❌ Error: {roadmap_result['error']}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    await engine.dispose()
    
    print("\n" + "="*70)
    print("✅ ALL CAREER INTELLIGENCE TESTS COMPLETED")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(test_career_features())
