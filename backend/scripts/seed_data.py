"""Seed the SkillBridge database with development data.

Usage (from backend/):
  python scripts/seed_data.py
  python scripts/seed_data.py --students 1000 --jobs 500 --internships 500 --mentors 100 --courses 300
  python scripts/seed_data.py --truncate-first   # wipe and re-seed

Notes:
- Intended for local/dev only.
- Assumes migrations have been applied: alembic upgrade head
- Default counts match the implementation plan targets.
"""

from __future__ import annotations

import argparse
import asyncio
import random
import sys
import uuid
from pathlib import Path
from typing import Iterable

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from faker import Faker
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password
from app.db.session import async_session_factory
from app.models.career_role import (
    CareerRole,
    RoleCertification,
    RoleCourse,
    RoleProject,
    RoleSkill,
    SkillImportance,
    ProjectDifficulty,
)
from app.models.company import Company
from app.models.course import Course, CourseDifficulty
from app.models.internship import Internship
from app.models.job import Job
from app.models.mentor import Mentor
from app.models.mentor_request import MentorRequest
from app.models.recommendation import Recommendation, RecommendationEvent
from app.models.application import Application
from app.models.resume import Resume
from app.models.skill import Skill
from app.models.student import Student, student_goals, student_skills
from app.models.study_group import StudyGroup, StudyGroupLevel
from app.models.user import User, UserRole


#  Static seed data 

SKILLS_SEED: list[tuple[str, str]] = [
    ("Python", "programming"),
    ("JavaScript", "programming"),
    ("TypeScript", "programming"),
    ("Java", "programming"),
    ("C++", "programming"),
    ("SQL", "database"),
    ("PostgreSQL", "database"),
    ("MongoDB", "database"),
    ("Redis", "database"),
    ("FastAPI", "backend"),
    ("Django", "backend"),
    ("Flask", "backend"),
    ("Node.js", "backend"),
    ("Spring Boot", "backend"),
    ("React", "frontend"),
    ("Next.js", "frontend"),
    ("Vue.js", "frontend"),
    ("Docker", "devops"),
    ("Kubernetes", "devops"),
    ("AWS", "cloud"),
    ("Google Cloud", "cloud"),
    ("Azure", "cloud"),
    ("Git", "tools"),
    ("Linux", "os"),
    ("Machine Learning", "ai"),
    ("Deep Learning", "ai"),
    ("TensorFlow", "ai"),
    ("PyTorch", "ai"),
    ("Scikit-learn", "ai"),
    ("Pandas", "data"),
    ("NumPy", "data"),
    ("Data Analysis", "data"),
    ("REST API", "architecture"),
    ("GraphQL", "architecture"),
    ("CI/CD", "devops"),
    ("Agile", "methodology"),
    ("DSA", "cs"),
    ("System Design", "cs"),
    ("NLP", "ai"),
    ("Computer Vision", "ai"),
]

# Career Knowledge Base: roles  required skills + projects + certifications
CAREER_KB: list[dict] = [
    {
        "title": "Backend Engineer",
        "domain": "backend",
        "description": "Designs and builds server-side APIs, databases and microservices.",
        "essential_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Git", "REST API"],
        "important_skills": ["Redis", "AWS", "CI/CD", "Linux", "System Design"],
        "nice_to_have": ["Kubernetes", "GraphQL"],
        "projects": [
            ("REST API with Auth", "Build a JWT-secured CRUD API", ProjectDifficulty.BEGINNER),
            ("Microservices with Docker", "Split a monolith into services with Docker Compose", ProjectDifficulty.INTERMEDIATE),
            ("Distributed Task Queue", "Celery + Redis async job processing system", ProjectDifficulty.ADVANCED),
        ],
        "certifications": [
            ("AWS Certified Developer  Associate", "Amazon"),
            ("Docker Certified Associate", "Docker"),
        ],
    },
    {
        "title": "Frontend Engineer",
        "domain": "frontend",
        "description": "Builds responsive, accessible user interfaces with modern JS frameworks.",
        "essential_skills": ["JavaScript", "TypeScript", "React", "Git", "REST API"],
        "important_skills": ["Next.js", "Vue.js", "CI/CD"],
        "nice_to_have": ["GraphQL", "Docker"],
        "projects": [
            ("Portfolio Website", "Personal site with responsive design", ProjectDifficulty.BEGINNER),
            ("E-Commerce UI", "Product listing, cart, checkout with React", ProjectDifficulty.INTERMEDIATE),
            ("Real-time Dashboard", "WebSocket-powered live data dashboard", ProjectDifficulty.ADVANCED),
        ],
        "certifications": [
            ("Meta Front-End Developer Certificate", "Meta"),
            ("Google UX Design Certificate", "Google"),
        ],
    },
    {
        "title": "Data Scientist",
        "domain": "data",
        "description": "Extracts insights from data using statistics, ML, and visualisation.",
        "essential_skills": ["Python", "Machine Learning", "Pandas", "NumPy", "SQL", "Data Analysis"],
        "important_skills": ["Scikit-learn", "TensorFlow", "NLP", "Deep Learning"],
        "nice_to_have": ["Apache Spark", "Tableau"],
        "projects": [
            ("EDA Notebook", "Exploratory analysis on a public dataset", ProjectDifficulty.BEGINNER),
            ("ML Classification Pipeline", "End-to-end scikit-learn pipeline with hyperparameter tuning", ProjectDifficulty.INTERMEDIATE),
            ("NLP Sentiment Analyser", "Fine-tuned transformer for product reviews", ProjectDifficulty.ADVANCED),
        ],
        "certifications": [
            ("Google Professional Data Engineer", "Google"),
            ("IBM Data Science Professional Certificate", "IBM"),
        ],
    },
    {
        "title": "ML Engineer",
        "domain": "ai",
        "description": "Productionises ML models with robust pipelines and serving infrastructure.",
        "essential_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Docker", "Git"],
        "important_skills": ["AWS", "Kubernetes", "NLP", "Computer Vision", "CI/CD"],
        "nice_to_have": ["Scikit-learn", "Deep Learning"],
        "projects": [
            ("Model Training Script", "Train a CNN on CIFAR-10", ProjectDifficulty.BEGINNER),
            ("ML REST API", "Serve a model with FastAPI + Docker", ProjectDifficulty.INTERMEDIATE),
            ("MLOps Pipeline", "Automated retraining + drift detection on AWS", ProjectDifficulty.ADVANCED),
        ],
        "certifications": [
            ("TensorFlow Developer Certificate", "Google"),
            ("AWS Certified Machine Learning  Specialty", "Amazon"),
        ],
    },
    {
        "title": "DevOps Engineer",
        "domain": "devops",
        "description": "Automates infrastructure, deployments and reliability for software systems.",
        "essential_skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "AWS", "Git"],
        "important_skills": ["Python", "Terraform", "Nginx", "Azure", "Google Cloud"],
        "nice_to_have": ["Agile", "System Design"],
        "projects": [
            ("CI/CD Pipeline", "GitHub Actions pipeline for a Node.js app", ProjectDifficulty.BEGINNER),
            ("K8s Deployment", "Deploy a microservices app on Kubernetes with Helm", ProjectDifficulty.INTERMEDIATE),
            ("Infrastructure as Code", "Full AWS infrastructure using Terraform modules", ProjectDifficulty.ADVANCED),
        ],
        "certifications": [
            ("Certified Kubernetes Administrator (CKA)", "CNCF"),
            ("AWS Certified DevOps Engineer", "Amazon"),
        ],
    },
    {
        "title": "Full Stack Engineer",
        "domain": "fullstack",
        "description": "Builds end-to-end web applications across frontend, backend and databases.",
        "essential_skills": ["JavaScript", "TypeScript", "React", "Node.js", "PostgreSQL", "Git", "REST API"],
        "important_skills": ["Docker", "Next.js", "AWS", "CI/CD", "System Design"],
        "nice_to_have": ["GraphQL", "Redis"],
        "projects": [
            ("Todo App", "Full-stack CRUD app with auth", ProjectDifficulty.BEGINNER),
            ("SaaS Dashboard", "Multi-tenant app with billing and roles", ProjectDifficulty.INTERMEDIATE),
            ("Real-time Collaboration Tool", "Notion-like editor with WebSocket sync", ProjectDifficulty.ADVANCED),
        ],
        "certifications": [
            ("Meta Full-Stack Developer Certificate", "Meta"),
            ("AWS Certified Developer  Associate", "Amazon"),
        ],
    },
]

STUDY_GROUP_DOMAINS = [
    ("Python Backend", "backend", StudyGroupLevel.INTERMEDIATE),
    ("React Developers", "frontend", StudyGroupLevel.BEGINNER),
    ("ML Paper Reading Club", "ai", StudyGroupLevel.ADVANCED),
    ("DSA Interview Prep", "cs", StudyGroupLevel.INTERMEDIATE),
    ("DevOps & Cloud", "devops", StudyGroupLevel.INTERMEDIATE),
    ("Data Science Bootcamp", "data", StudyGroupLevel.BEGINNER),
    ("System Design Study Group", "cs", StudyGroupLevel.ADVANCED),
    ("Open Source Contributors", "fullstack", StudyGroupLevel.INTERMEDIATE),
]


#  Helpers 

def _chunks(items: list, size: int) -> Iterable[list]:
    for idx in range(0, len(items), size):
        yield items[idx: idx + size]


#  Truncate 

async def _truncate_all() -> None:
    """Delete all rows in FK-safe order for dev reseeding."""
    print("    Truncating existing data...")
    async with async_session_factory() as session:
        await session.execute(delete(student_skills))
        await session.execute(delete(student_goals))
        for model in (
            RecommendationEvent,
            Recommendation,
            Application,
            Resume,
            MentorRequest,
            StudyGroup,
            Job,
            Internship,
            RoleCertification,
            RoleCourse,
            RoleProject,
            RoleSkill,
            CareerRole,
            Mentor,
            Student,
            Company,
            Course,
            Skill,
            User,
        ):
            await session.execute(delete(model))
        await session.commit()
    print("   Truncation complete.")


#  Skills 

async def _seed_skills() -> dict[str, Skill]:
    """Seed canonical skills. Returns {name: Skill} lookup."""
    print("   Seeding skills...")
    async with async_session_factory() as session:
        existing = {s.name: s for s in (await session.execute(select(Skill))).scalars().all()}
        if existing:
            return existing

        skills = [Skill(name=name, category=cat) for name, cat in SKILLS_SEED]
        session.add_all(skills)
        await session.commit()
        for s in skills:
            await session.refresh(s)
        result = {s.name: s for s in skills}
    print(f"   {len(result)} skills seeded.")
    return result


#  Career Knowledge Base 

async def _seed_career_kb(skills_map: dict[str, Skill], courses: list[Course]) -> None:
    """Seed career_roles + role_skills + role_projects + role_courses + role_certifications."""
    print("   Seeding career knowledge base...")
    async with async_session_factory() as session:
        for entry in CAREER_KB:
            role = CareerRole(
                title=entry["title"],
                domain=entry["domain"],
                description=entry["description"],
            )
            session.add(role)
            await session.flush()  # get role.id

            # role_skills
            def _add_role_skills(skill_names: list[str], importance: SkillImportance) -> None:
                for name in skill_names:
                    skill = skills_map.get(name)
                    if skill:
                        session.add(RoleSkill(
                            role_id=role.id,
                            skill_id=skill.id,
                            importance=importance,
                        ))

            _add_role_skills(entry["essential_skills"], SkillImportance.ESSENTIAL)
            _add_role_skills(entry["important_skills"], SkillImportance.IMPORTANT)
            _add_role_skills(entry["nice_to_have"], SkillImportance.NICE_TO_HAVE)

            # role_projects
            for proj_title, proj_desc, difficulty in entry["projects"]:
                session.add(RoleProject(
                    role_id=role.id,
                    project_title=proj_title,
                    description=proj_desc,
                    difficulty=difficulty,
                ))

            # role_courses  link 3 random courses per role
            for priority, course in enumerate(random.sample(courses, min(3, len(courses))), start=1):
                session.add(RoleCourse(
                    role_id=role.id,
                    course_id=course.id,
                    priority=priority,
                ))

            # role_certifications
            for priority, (cert_name, provider) in enumerate(entry["certifications"], start=1):
                session.add(RoleCertification(
                    role_id=role.id,
                    certification_name=cert_name,
                    provider=provider,
                    priority=priority,
                ))

        await session.commit()
    print(f"   {len(CAREER_KB)} career roles seeded with full KB data.")


#  Companies 

async def _seed_companies(fake: Faker, count: int) -> list[Company]:
    print(f"   Seeding {count} companies...")
    companies: list[Company] = []
    async with async_session_factory() as session:
        for _ in range(count):
            user = User(
                email=fake.unique.company_email(),
                password_hash=hash_password("password123"),
                role=UserRole.COMPANY,
                is_active=True,
            )
            company = Company(
                user=user,
                name=fake.company(),
                description=fake.catch_phrase(),
                website=fake.url(),
                industry=fake.bs(),
                location=f"{fake.city()}, {fake.country_code()}",
                is_verified=bool(random.getrandbits(1)),
            )
            session.add(company)
            companies.append(company)
        await session.commit()
        for c in companies:
            await session.refresh(c)
    print(f"   {len(companies)} companies created.")
    return companies


#  Students 

async def _seed_students(fake: Faker, count: int, skills: list[Skill]) -> list[Student]:
    print(f"   Seeding {count} students...")
    students: list[Student] = []
    async with async_session_factory() as session:
        for _ in range(count):
            user = User(
                email=fake.unique.email(),
                password_hash=hash_password("password123"),
                role=UserRole.STUDENT,
                is_active=True,
            )
            student = Student(
                user=user,
                name=fake.name(),
                cgpa=round(random.uniform(6.0, 10.0), 2),
                college=fake.company() + " Institute of Technology",
                graduation_year=random.choice([2025, 2026, 2027, 2028]),
                bio=fake.sentence(nb_words=14),
            )
            # Assign 37 random skills
            for skill in random.sample(skills, min(random.randint(3, 7), len(skills))):
                student.skills.append(skill)
            session.add(student)
            students.append(student)
        await session.commit()
        for s in students:
            await session.refresh(s)
    print(f"   {len(students)} students created.")
    return students


#  Mentors 

async def _seed_mentors(fake: Faker, count: int) -> list[Mentor]:
    print(f"   Seeding {count} mentors...")
    domains = ["backend", "frontend", "data", "ai", "devops", "fullstack", "product"]
    mentors: list[Mentor] = []
    async with async_session_factory() as session:
        for _ in range(count):
            user = User(
                email=fake.unique.email(),
                password_hash=hash_password("password123"),
                role=UserRole.MENTOR,
                is_active=True,
            )
            mentor = Mentor(
                user=user,
                name=fake.name(),
                experience=random.randint(1, 15),
                domain=random.choice(domains),
                bio=fake.paragraph(nb_sentences=2),
                is_verified=bool(random.getrandbits(1)),
                max_mentees=random.choice([3, 5, 8, 10]),
            )
            session.add(mentor)
            mentors.append(mentor)
        await session.commit()
        for m in mentors:
            await session.refresh(m)
    print(f"   {len(mentors)} mentors created.")
    return mentors


#  Courses 

async def _seed_courses(fake: Faker, count: int) -> list[Course]:
    print(f"   Seeding {count} courses...")
    providers = ["Coursera", "Udemy", "edX", "YouTube", "freeCodeCamp", "Pluralsight", "LinkedIn Learning"]
    # Use the string values, not the enum members
    difficulties = ["beginner", "intermediate", "advanced"]
    courses: list[Course] = []
    async with async_session_factory() as session:
        for _ in range(count):
            course = Course(
                title=fake.sentence(nb_words=5).rstrip("."),
                provider=random.choice(providers),
                url=fake.url(),
                description=fake.sentence(nb_words=16),
                skills_covered=[fake.word() for _ in range(random.randint(3, 7))],
                difficulty=random.choice(difficulties),  # Pass string directly
                duration=f"{random.randint(2, 40)}h",
                is_free=bool(random.getrandbits(1)),
            )
            session.add(course)
            courses.append(course)
        await session.commit()
        for c in courses:
            await session.refresh(c)
    print(f"   {len(courses)} courses created.")
    return courses


#  Jobs 

async def _seed_jobs(fake: Faker, companies: list[Company], count: int) -> None:
    print(f"   Seeding {count} jobs...")
    titles = [
        "Software Engineer", "Backend Engineer", "Frontend Engineer",
        "Full Stack Engineer", "Data Analyst", "ML Engineer",
        "DevOps Engineer", "Cloud Architect", "Site Reliability Engineer",
    ]
    async with async_session_factory() as session:
        created = 0
        while created < count:
            batch = []
            for _ in range(min(200, count - created)):
                sal_min = random.choice([None, 300000, 500000, 800000, 1200000])
                sal_max = (sal_min * random.uniform(1.2, 1.8)) if sal_min else None
                batch.append(Job(
                    company_id=random.choice(companies).id,
                    title=random.choice(titles),
                    description=fake.paragraph(nb_sentences=5),
                    requirements=[fake.word() for _ in range(random.randint(4, 10))],
                    salary_min=round(sal_min, 2) if sal_min else None,
                    salary_max=round(sal_max, 2) if sal_max else None,
                    location=f"{fake.city()}, {fake.country_code()}",
                    is_remote=bool(random.getrandbits(1)),
                    is_active=True,
                ))
            session.add_all(batch)
            await session.commit()
            created += len(batch)
    print(f"   {count} jobs created.")


#  Internships 

async def _seed_internships(fake: Faker, companies: list[Company], count: int) -> None:
    print(f"   Seeding {count} internships...")
    titles = [
        "Software Intern", "Backend Intern", "Frontend Intern",
        "Data Science Intern", "ML Intern", "DevOps Intern", "Research Intern",
    ]
    async with async_session_factory() as session:
        created = 0
        while created < count:
            batch = []
            for _ in range(min(200, count - created)):
                batch.append(Internship(
                    company_id=random.choice(companies).id,
                    title=random.choice(titles),
                    description=fake.paragraph(nb_sentences=4),
                    requirements=[fake.word() for _ in range(random.randint(4, 10))],
                    duration=random.choice(["8 weeks", "12 weeks", "16 weeks", "6 months", None]),
                    stipend=random.choice([None, 5000.0, 10000.0, 15000.0, 20000.0, 25000.0]),
                    location=f"{fake.city()}, {fake.country_code()}",
                    is_remote=bool(random.getrandbits(1)),
                    is_active=True,
                ))
            session.add_all(batch)
            await session.commit()
            created += len(batch)
    print(f"   {count} internships created.")


#  Study Groups 

async def _seed_study_groups(mentors: list[Mentor]) -> None:
    """Seed fixed study groups owned by mentor users."""
    print(f"   Seeding {len(STUDY_GROUP_DOMAINS)} study groups...")
    async with async_session_factory() as session:
        # Load mentor user_ids
        mentor_user_ids = [m.user_id for m in mentors]

        for name, domain, level in STUDY_GROUP_DOMAINS:
            session.add(StudyGroup(
                name=name,
                description=f"A peer group focused on {domain} skills.",
                domain=domain,
                skill_level=level,
                owner_id=random.choice(mentor_user_ids),
                max_members=random.choice([15, 20, 25, 30]),
                is_active=True,
            ))
        await session.commit()
    print(f"   {len(STUDY_GROUP_DOMAINS)} study groups created.")


#  Orchestrator 

async def seed(
    *,
    students: int,
    jobs: int,
    internships: int,
    mentors: int,
    courses: int,
    companies: int,
    truncate_first: bool,
    random_seed: int,
) -> None:
    fake = Faker()
    Faker.seed(random_seed)
    random.seed(random_seed)

    print("\n SkillBridge seed starting...\n".encode('utf-8', errors='replace').decode('utf-8'))

    if truncate_first:
        await _truncate_all()

    skills_map = await _seed_skills()
    skill_list = list(skills_map.values())

    course_list = await _seed_courses(fake, courses)
    await _seed_career_kb(skills_map, course_list)

    company_list = await _seed_companies(fake, companies)
    await _seed_students(fake, students, skill_list)
    mentor_list = await _seed_mentors(fake, mentors)

    await _seed_jobs(fake, company_list, jobs)
    await _seed_internships(fake, company_list, internships)
    await _seed_study_groups(mentor_list)

    print("\n Seeding complete!\n")
    print(f"   Skills       : {len(skill_list)}")
    print(f"   Career roles : {len(CAREER_KB)}")
    print(f"   Courses      : {courses}")
    print(f"   Companies    : {companies}")
    print(f"   Students     : {students}")
    print(f"   Mentors      : {mentors}")
    print(f"   Jobs         : {jobs}")
    print(f"   Internships  : {internships}")
    print(f"   Study groups : {len(STUDY_GROUP_DOMAINS)}\n")


#  CLI 

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seed dev data for SkillBridge")
    p.add_argument("--students", type=int, default=1000)
    p.add_argument("--jobs", type=int, default=500)
    p.add_argument("--internships", type=int, default=500)
    p.add_argument("--mentors", type=int, default=100)
    p.add_argument("--courses", type=int, default=300)
    p.add_argument("--companies", type=int, default=80)
    p.add_argument(
        "--truncate-first", action="store_true",
        help="Delete all existing rows before seeding (safe re-seed)",
    )
    p.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    try:
        asyncio.run(seed(
            students=args.students,
            jobs=args.jobs,
            internships=args.internships,
            mentors=args.mentors,
            courses=args.courses,
            companies=args.companies,
            truncate_first=args.truncate_first,
            random_seed=args.seed,
        ))
    except IntegrityError as exc:
        raise SystemExit(
            "\n Seeding failed due to integrity constraint.\n"
            "   Try running with --truncate-first to wipe existing data first.\n"
            f"   Details: {exc}\n"
        ) from exc


if __name__ == "__main__":
    main()
