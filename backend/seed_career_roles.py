"""
Seed career roles with skills, projects, courses, and certifications.

Usage:
    docker exec -it skillbridge-backend python seed_career_roles.py
"""

import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.career_role import (
    CareerRole, RoleSkill, RoleProject, RoleCourse, RoleCertification,
    SkillImportance, ProjectDifficulty
)
from app.models.skill import Skill
from app.models.course import Course


async def seed_career_roles():
    print("\n" + "="*70)
    print("SEEDING CAREER ROLES DATA")
    print("="*70 + "\n")
    
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Get all skills
        result = await db.execute(select(Skill))
        all_skills = {skill.name: skill for skill in result.scalars().all()}
        
        # Get all courses
        result = await db.execute(select(Course))
        all_courses = list(result.scalars().all())
        
        print(f"Found {len(all_skills)} skills and {len(all_courses)} courses")
        
        # Define career roles
        roles_data = [
            {
                "title": "Full Stack Developer",
                "description": "Build complete web applications from frontend to backend",
                "domain": "Web Development",
                "skills": {
                    "Python": SkillImportance.ESSENTIAL,
                    "JavaScript": SkillImportance.ESSENTIAL,
                    "React": SkillImportance.ESSENTIAL,
                    "Node.js": SkillImportance.IMPORTANT,
                    "PostgreSQL": SkillImportance.IMPORTANT,
                    "Docker": SkillImportance.NICE_TO_HAVE,
                    "REST API": SkillImportance.IMPORTANT,
                    "Git": SkillImportance.ESSENTIAL,
                },
                "projects": [
                    ("E-commerce Platform", "Build a full-featured online store with cart, payments, and admin panel", ProjectDifficulty.ADVANCED),
                    ("Social Media App", "Create a social network with posts, likes, comments, and real-time updates", ProjectDifficulty.INTERMEDIATE),
                    ("Task Management System", "Develop a Trello-like kanban board with drag-drop", ProjectDifficulty.INTERMEDIATE),
                ],
                "certifications": [
                    ("AWS Certified Developer", "Amazon Web Services"),
                    ("Meta Front-End Developer", "Meta"),
                ]
            },
            {
                "title": "Data Scientist",
                "description": "Extract insights from data using ML and statistical analysis",
                "domain": "Data Science",
                "skills": {
                    "Python": SkillImportance.ESSENTIAL,
                    "Machine Learning": SkillImportance.ESSENTIAL,
                    "TensorFlow": SkillImportance.IMPORTANT,
                    "PyTorch": SkillImportance.IMPORTANT,
                    "PostgreSQL": SkillImportance.IMPORTANT,
                },
                "projects": [
                    ("Customer Churn Prediction", "Build ML model to predict customer churn with 85%+ accuracy", ProjectDifficulty.ADVANCED),
                    ("Sales Forecasting Dashboard", "Time series analysis with interactive visualizations", ProjectDifficulty.INTERMEDIATE),
                    ("Recommendation System", "Build collaborative filtering system", ProjectDifficulty.ADVANCED),
                ],
                "certifications": [
                    ("Google Data Analytics Certificate", "Google"),
                    ("IBM Data Science Professional", "IBM"),
                ]
            },
            {
                "title": "DevOps Engineer",
                "description": "Automate deployment, scaling, and management of applications",
                "domain": "DevOps",
                "skills": {
                    "Docker": SkillImportance.ESSENTIAL,
                    "Kubernetes": SkillImportance.ESSENTIAL,
                    "AWS": SkillImportance.ESSENTIAL,
                    "Linux": SkillImportance.ESSENTIAL,
                    "CI/CD": SkillImportance.IMPORTANT,
                    "Python": SkillImportance.IMPORTANT,
                },
                "projects": [
                    ("CI/CD Pipeline", "Automated deployment pipeline with Docker and Kubernetes", ProjectDifficulty.ADVANCED),
                    ("Infrastructure as Code", "Terraform setup for multi-tier application", ProjectDifficulty.INTERMEDIATE),
                    ("Monitoring System", "Setup Prometheus and Grafana for app monitoring", ProjectDifficulty.INTERMEDIATE),
                ],
                "certifications": [
                    ("AWS Certified Solutions Architect", "Amazon Web Services"),
                    ("Certified Kubernetes Administrator", "CNCF"),
                ]
            },
            {
                "title": "Backend Developer",
                "description": "Build scalable APIs and server-side applications",
                "domain": "Backend Development",
                "skills": {
                    "Python": SkillImportance.ESSENTIAL,
                    "FastAPI": SkillImportance.ESSENTIAL,
                    "PostgreSQL": SkillImportance.ESSENTIAL,
                    "REST API": SkillImportance.ESSENTIAL,
                    "Docker": SkillImportance.IMPORTANT,
                    "Redis": SkillImportance.NICE_TO_HAVE,
                    "Microservices": SkillImportance.IMPORTANT,
                },
                "projects": [
                    ("RESTful API Platform", "Build scalable API with auth, rate limiting, caching", ProjectDifficulty.ADVANCED),
                    ("Microservices Architecture", "Build distributed system with message queues", ProjectDifficulty.ADVANCED),
                    ("Real-time Chat API", "WebSocket-based chat with Redis pub/sub", ProjectDifficulty.INTERMEDIATE),
                ],
                "certifications": [
                    ("Python Institute PCAP", "Python Institute"),
                ]
            },
            {
                "title": "Machine Learning Engineer",
                "description": "Deploy ML models to production and build ML infrastructure",
                "domain": "Machine Learning",
                "skills": {
                    "Python": SkillImportance.ESSENTIAL,
                    "Machine Learning": SkillImportance.ESSENTIAL,
                    "Deep Learning": SkillImportance.ESSENTIAL,
                    "TensorFlow": SkillImportance.IMPORTANT,
                    "PyTorch": SkillImportance.IMPORTANT,
                    "Docker": SkillImportance.IMPORTANT,
                    "Kubernetes": SkillImportance.NICE_TO_HAVE,
                },
                "projects": [
                    ("Image Classification API", "Deploy CNN model as REST API", ProjectDifficulty.ADVANCED),
                    ("NLP Sentiment Analyzer", "Build and deploy text classification model", ProjectDifficulty.INTERMEDIATE),
                    ("ML Pipeline", "End-to-end pipeline with training, evaluation, deployment", ProjectDifficulty.ADVANCED),
                ],
                "certifications": [
                    ("TensorFlow Developer Certificate", "Google"),
                    ("AWS Machine Learning Specialty", "Amazon Web Services"),
                ]
            },
        ]
        
        print("\nCreating career roles...")
        
        for role_data in roles_data:
            # Create role
            role = CareerRole(
                title=role_data["title"],
                description=role_data["description"],
                domain=role_data["domain"]
            )
            db.add(role)
            await db.flush()
            
            print(f"\n✅ {role.title}")
            
            # Add skills
            for skill_name, importance in role_data["skills"].items():
                if skill_name in all_skills:
                    role_skill = RoleSkill(
                        role_id=role.id,
                        skill_id=all_skills[skill_name].id,
                        importance=importance
                    )
                    db.add(role_skill)
                    print(f"   - Skill: {skill_name} ({importance.value})")
            
            # Add projects
            for proj_title, proj_desc, difficulty in role_data["projects"]:
                role_project = RoleProject(
                    role_id=role.id,
                    project_title=proj_title,
                    description=proj_desc,
                    difficulty=difficulty
                )
                db.add(role_project)
                print(f"   - Project: {proj_title}")
            
            # Add certifications
            for cert_name, provider in role_data["certifications"]:
                role_cert = RoleCertification(
                    role_id=role.id,
                    certification_name=cert_name,
                    provider=provider,
                    priority=1
                )
                db.add(role_cert)
                print(f"   - Cert: {cert_name}")
        
        await db.commit()
    
    await engine.dispose()
    
    print("\n" + "="*70)
    print("✅ CAREER ROLES SEEDED SUCCESSFULLY")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(seed_career_roles())
