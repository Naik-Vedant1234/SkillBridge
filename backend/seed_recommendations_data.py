"""
Seed script to populate test data for recommendation testing.

Usage:
    docker exec -it skillbridge-backend python seed_recommendations_data.py
    docker exec -it skillbridge-backend python seed_recommendations_data.py --clear
"""

import asyncio
import sys
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.mentor import Mentor
from app.models.job import Job
from app.models.internship import Internship
from app.models.course import Course, CourseDifficulty
from app.models.study_group import StudyGroup, StudyGroupLevel
from app.models.student import Student
from app.models.skill import Skill


# Extended test data with more realistic variety
TECH_DOMAINS = [
    "Web Development", "Mobile Development", "Data Science", "Machine Learning",
    "DevOps", "Cloud Computing", "Cybersecurity", "Backend Development",
    "Frontend Development", "Full Stack", "AI/ML", "Blockchain", "Game Development",
    "IoT", "Embedded Systems", "Network Engineering"
]

SKILLS_DATA = [
    # Programming Languages
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust",
    "Ruby", "PHP", "Swift", "Kotlin", "Dart", "Scala", "R",
    
    # Frontend
    "React", "Vue.js", "Angular", "Next.js", "Svelte", "HTML", "CSS", "Tailwind CSS",
    "Material-UI", "Redux", "React Native", "Flutter",
    
    # Backend
    "Node.js", "Express.js", "FastAPI", "Django", "Flask", "Spring Boot", 
    "ASP.NET", "Laravel", "Ruby on Rails", "Nest.js",
    
    # Databases
    "PostgreSQL", "MongoDB", "MySQL", "Redis", "Elasticsearch", "Cassandra",
    "DynamoDB", "SQLite", "Oracle", "Neo4j",
    
    # DevOps & Cloud
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Jenkins", "GitLab CI",
    "GitHub Actions", "Terraform", "Ansible", "Linux", "Bash",
    
    # Data Science & ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn",
    "Pandas", "NumPy", "Matplotlib", "Jupyter", "Keras", "OpenCV",
    
    # Tools & Practices
    "Git", "CI/CD", "REST API", "GraphQL", "Microservices", "Agile", "Scrum",
    "Testing", "Jest", "Pytest", "Selenium", "Postman"
]

JOB_TITLES = [
    # Entry Level
    "Junior Full Stack Developer", "Junior Frontend Developer", "Junior Backend Developer",
    "Associate Software Engineer", "Graduate Software Developer", "Entry Level Data Analyst",
    
    # Mid Level
    "Full Stack Developer", "Frontend Developer", "Backend Developer",
    "Software Engineer", "Data Scientist", "ML Engineer", "DevOps Engineer",
    "Python Developer", "React Developer", "Node.js Developer",
    "Cloud Engineer", "Mobile Developer", "QA Engineer",
    
    # Specialized
    "API Developer", "Database Administrator", "Security Engineer",
    "Systems Architect", "Data Engineer", "AI Research Engineer",
    "Site Reliability Engineer", "Platform Engineer", "Integration Engineer"
]

INTERNSHIP_TITLES = [
    "Software Engineering Intern", "Data Science Intern", "ML Research Intern",
    "Frontend Development Intern", "Backend Development Intern", "DevOps Intern",
    "Full Stack Intern", "Mobile App Development Intern", "Cloud Engineering Intern",
    "AI/ML Intern", "Data Analytics Intern", "QA Testing Intern",
    "Cybersecurity Intern", "UI/UX Development Intern", "Web Development Intern"
]

COMPANY_NAMES = [
    "TechCorp", "DataSoft", "CloudNine Systems", "InnovateLabs", "ByteWorks",
    "CodeCraft Solutions", "DevSolutions Inc", "AI Dynamics", "WebMasters Pro", "AppForge",
    "NextGen Tech", "Digital Horizons", "Quantum Labs", "Pixel Perfect", "Binary Solutions",
    "Cyber Shield", "Data Nexus", "Cloud Architects", "Smart Systems", "Future Tech"
]

COURSE_PROVIDERS = [
    "Coursera", "Udemy", "edX", "Pluralsight", "LinkedIn Learning",
    "FreeCodeCamp", "Codecademy", "Khan Academy", "Udacity", "Skillshare"
]

# Job descriptions templates
JOB_DESCRIPTIONS = [
    "Join our dynamic team to build cutting-edge web applications using modern technologies.",
    "We're looking for passionate developers to work on innovative projects with global impact.",
    "Exciting opportunity to work with cloud-native technologies in a fast-paced environment.",
    "Build scalable solutions that serve millions of users worldwide.",
    "Join us in revolutionizing the industry with AI and machine learning solutions.",
    "Work on challenging problems with a team of talented engineers.",
    "Help us build the next generation of mobile applications.",
    "Contribute to open-source projects while working on enterprise solutions.",
]

# Indian cities for realistic locations
INDIAN_CITIES = [
    "Bangalore", "Mumbai", "Delhi NCR", "Pune", "Hyderabad",
    "Chennai", "Kolkata", "Ahmedabad", "Gurugram", "Noida",
    "Remote", "Hybrid - Bangalore", "Hybrid - Mumbai"
]


async def create_skills(session: AsyncSession) -> dict[str, Skill]:
    """Get or create skill records."""
    print("Getting/creating skills...")
    skills_map = {}
    
    for skill_name in SKILLS_DATA:
        # Check if skill already exists
        result = await session.execute(
            select(Skill).where(Skill.name == skill_name)
        )
        skill = result.scalar_one_or_none()
        
        if not skill:
            skill = Skill(name=skill_name)
            session.add(skill)
        
        skills_map[skill_name] = skill
    
    await session.commit()
    print(f"✓ Ensured {len(skills_map)} skills exist")
    return skills_map


async def create_companies(session: AsyncSession) -> list[Company]:
    """Create company accounts with realistic profiles."""
    print("Creating companies...")
    companies = []
    
    company_data = [
        ("TechCorp Solutions", "Enterprise software solutions provider", "Software Development", "Bangalore"),
        ("DataSoft Analytics", "Big data and analytics platform", "Data Science", "Mumbai"),
        ("CloudNine Systems", "Cloud infrastructure and services", "Cloud Computing", "Pune"),
        ("InnovateLabs", "Innovation and R&D laboratory", "AI/ML", "Hyderabad"),
        ("ByteWorks", "Custom software development", "Web Development", "Delhi NCR"),
        ("CodeCraft Solutions", "Digital transformation consultancy", "Full Stack", "Chennai"),
        ("DevSolutions Inc", "DevOps and automation experts", "DevOps", "Bangalore"),
        ("AI Dynamics", "Artificial intelligence solutions", "Machine Learning", "Bangalore"),
        ("WebMasters Pro", "Web and mobile development", "Web Development", "Mumbai"),
        ("AppForge", "Mobile-first application development", "Mobile Development", "Pune"),
        ("NextGen Tech", "Next-generation technology solutions", "Cloud Computing", "Gurugram"),
        ("Digital Horizons", "Digital product development", "Full Stack", "Noida"),
        ("Quantum Labs", "Quantum computing research", "AI/ML", "Bangalore"),
        ("Pixel Perfect", "UI/UX focused development", "Frontend Development", "Mumbai"),
        ("Binary Solutions", "Enterprise IT solutions", "Backend Development", "Hyderabad"),
        ("Cyber Shield", "Cybersecurity services", "Cybersecurity", "Delhi NCR"),
        ("Data Nexus", "Data engineering and pipelines", "Data Science", "Pune"),
        ("Cloud Architects", "Cloud migration specialists", "Cloud Computing", "Chennai"),
        ("Smart Systems", "IoT and embedded systems", "IoT", "Bangalore"),
        ("Future Tech", "Emerging technology solutions", "Blockchain", "Mumbai"),
    ]
    
    for i, (name, description, industry, location) in enumerate(company_data):
        # Create user account
        user = User(
            email=f"company{i}@test.com",
            password_hash="$2b$12$dummy_hash_for_testing",
            role=UserRole.COMPANY,
            is_active=True
        )
        session.add(user)
        await session.flush()
        
        # Create company profile
        company = Company(
            user_id=user.id,
            name=name,
            description=description,
            website=f"https://{name.lower().replace(' ', '')}.com",
            industry=industry,
            location=location,
            is_verified=True
        )
        session.add(company)
        companies.append(company)
    
    await session.commit()
    print(f"✓ Created {len(companies)} companies")
    return companies


async def create_jobs(
    session: AsyncSession, 
    companies: list[Company],
    skills_map: dict[str, Skill]
) -> list[Job]:
    """Create job postings with realistic variety."""
    print("Creating jobs...")
    jobs = []
    
    # Skill requirement templates based on roles
    skill_templates = {
        "full_stack": ["JavaScript", "React", "Node.js", "PostgreSQL", "Git"],
        "frontend": ["React", "TypeScript", "HTML", "CSS", "Redux"],
        "backend": ["Python", "FastAPI", "PostgreSQL", "Docker", "REST API"],
        "data_science": ["Python", "Pandas", "Machine Learning", "NumPy", "Jupyter"],
        "devops": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD"],
        "mobile": ["React Native", "JavaScript", "Redux", "REST API"],
        "ml": ["Python", "TensorFlow", "Machine Learning", "Deep Learning", "PyTorch"],
        "cloud": ["AWS", "Docker", "Kubernetes", "Terraform", "Linux"],
    }
    
    for i in range(50):  # 50 jobs for better variety
        company = companies[i % len(companies)]
        title = JOB_TITLES[i % len(JOB_TITLES)]
        
        # Choose skill template based on job title
        if "Full Stack" in title:
            required_skills = skill_templates["full_stack"]
        elif "Frontend" in title or "React" in title:
            required_skills = skill_templates["frontend"]
        elif "Backend" in title or "Python" in title or "Node" in title:
            required_skills = skill_templates["backend"]
        elif "Data" in title:
            required_skills = skill_templates["data_science"]
        elif "DevOps" in title or "Cloud" in title or "SRE" in title:
            required_skills = skill_templates["devops"]
        elif "Mobile" in title:
            required_skills = skill_templates["mobile"]
        elif "ML" in title or "AI" in title:
            required_skills = skill_templates["ml"]
        else:
            required_skills = SKILLS_DATA[i % 5:(i % 5) + 4]
        
        # Determine if entry level
        is_entry_level = any(word in title for word in ["Junior", "Entry", "Associate", "Graduate"])
        
        # Salary based on level
        if is_entry_level:
            salary_min = 300000 + (i * 10000)  # 3-5 LPA
            salary_max = 500000 + (i * 10000)
        else:
            salary_min = 600000 + (i * 20000)  # 6-12 LPA
            salary_max = 1200000 + (i * 20000)
        
        location = INDIAN_CITIES[i % len(INDIAN_CITIES)]
        is_remote = "Remote" in location or "Hybrid" in location
        
        job = Job(
            company_id=company.id,
            title=title,
            description=JOB_DESCRIPTIONS[i % len(JOB_DESCRIPTIONS)] + f" {title} role with growth opportunities.",
            requirements=required_skills[:5],  # Max 5 skills
            salary_min=salary_min,
            salary_max=salary_max,
            location=location,
            is_remote=is_remote,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=i % 30)  # Vary posting dates
        )
        session.add(job)
        jobs.append(job)
    
    await session.commit()
    print(f"✓ Created {len(jobs)} jobs")
    return jobs


async def create_internships(
    session: AsyncSession,
    companies: list[Company]
) -> list[Internship]:
    """Create internship postings with realistic variety."""
    print("Creating internships...")
    internships = []
    
    stipend_ranges = [15000, 20000, 25000, 30000, 40000, 50000]  # Monthly stipends
    
    for i in range(40):  # 40 internships
        company = companies[i % len(companies)]
        title = INTERNSHIP_TITLES[i % len(INTERNSHIP_TITLES)]
        
        # Skill requirements (2-4 skills for interns)
        required_skills = SKILLS_DATA[i % 8:(i % 8) + 3]
        
        duration_options = ["2 months", "3 months", "6 months", "Summer (2 months)", "Winter (3 months)"]
        
        location = INDIAN_CITIES[i % len(INDIAN_CITIES)]
        is_remote = "Remote" in location
        
        internship = Internship(
            company_id=company.id,
            title=title,
            description=f"Hands-on {title} opportunity. Learn from industry experts and work on real projects.",
            requirements=required_skills,
            duration=duration_options[i % len(duration_options)],
            stipend=stipend_ranges[i % len(stipend_ranges)],
            location=location,
            is_remote=is_remote,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=i % 25)
        )
        session.add(internship)
        internships.append(internship)
    
    await session.commit()
    print(f"✓ Created {len(internships)} internships")
    return internships


async def create_mentors(session: AsyncSession) -> list[Mentor]:
    """Create mentor accounts with realistic profiles."""
    print("Creating mentors...")
    mentors = []
    
    mentor_names = [
        "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sneha Reddy", "Vikram Singh",
        "Ananya Desai", "Karthik Iyer", "Divya Menon", "Rohan Gupta", "Meera Krishnan",
        "Aditya Verma", "Kavya Nair", "Sanjay Mehta", "Pooja Agarwal", "Arjun Rao",
        "Ishita Joshi", "Manish Malhotra", "Neha Chopra", "Rahul Bansal", "Shruti Kapoor"
    ]
    
    specializations = [
        "Full Stack Development", "Frontend Architecture", "Backend Systems", 
        "Data Science & Analytics", "Machine Learning Engineering", "DevOps & Cloud",
        "Mobile App Development", "Cybersecurity", "System Design", "API Development",
        "Microservices Architecture", "AI/ML Research", "Cloud Solutions", "Database Design",
        "Web Performance", "Security Best Practices"
    ]
    
    for i in range(20):  # 20 mentors
        # Create user account
        user = User(
            email=f"mentor{i}@test.com",
            password_hash="$2b$12$dummy_hash_for_testing",
            role=UserRole.MENTOR,
            is_active=True
        )
        session.add(user)
        await session.flush()
        
        # Create mentor profile
        mentor = Mentor(
            user_id=user.id,
            name=mentor_names[i % len(mentor_names)],
            experience=3 + (i % 15),  # 3-18 years experience
            domain=TECH_DOMAINS[i % len(TECH_DOMAINS)],
            bio=f"Experienced {specializations[i % len(specializations)]} professional with {3 + (i % 15)} years of industry experience. Passionate about mentoring and helping students achieve their career goals.",
            is_verified=True,
            max_mentees=3 + (i % 8)  # 3-10 mentees
        )
        session.add(mentor)
        mentors.append(mentor)
    
    await session.commit()
    print(f"✓ Created {len(mentors)} mentors")
    return mentors


async def create_courses(session: AsyncSession) -> list[Course]:
    """Create course records with comprehensive curriculum."""
    print("Creating courses...")
    courses = []
    
    course_data = [
        # Programming Fundamentals
        ("Complete Python Bootcamp 2024", "Python,Programming,Git", CourseDifficulty.BEGINNER, "40 hours", True),
        ("JavaScript Masterclass", "JavaScript,HTML,CSS,DOM", CourseDifficulty.BEGINNER, "35 hours", True),
        ("Java Programming Complete", "Java,OOP,Spring Boot", CourseDifficulty.BEGINNER, "50 hours", False),
        
        # Web Development
        ("Modern React with Hooks & Context", "React,JavaScript,Redux,Hooks", CourseDifficulty.INTERMEDIATE, "30 hours", False),
        ("Advanced React with TypeScript", "React,TypeScript,JavaScript", CourseDifficulty.ADVANCED, "30 hours", False),
        ("Full Stack Web Development", "JavaScript,Node.js,React,MongoDB", CourseDifficulty.BEGINNER, "80 hours", True),
        ("Vue.js Complete Guide", "Vue.js,JavaScript,Vuex", CourseDifficulty.INTERMEDIATE, "25 hours", False),
        ("Next.js & React for Production", "Next.js,React,TypeScript", CourseDifficulty.ADVANCED, "28 hours", False),
        
        # Backend Development
        ("Node.js API Development", "Node.js,Express.js,REST API", CourseDifficulty.INTERMEDIATE, "35 hours", False),
        ("FastAPI Modern Python", "Python,FastAPI,REST API", CourseDifficulty.INTERMEDIATE, "20 hours", True),
        ("Django for Beginners", "Python,Django,PostgreSQL", CourseDifficulty.BEGINNER, "45 hours", False),
        ("Microservices Architecture", "Microservices,Docker,Kubernetes", CourseDifficulty.ADVANCED, "45 hours", False),
        
        # Data Science & ML
        ("Machine Learning A-Z", "Machine Learning,Python,Scikit-learn", CourseDifficulty.INTERMEDIATE, "50 hours", False),
        ("Deep Learning Specialization", "Deep Learning,TensorFlow,Python", CourseDifficulty.ADVANCED, "70 hours", False),
        ("Data Science with Python", "Python,Pandas,NumPy,Matplotlib", CourseDifficulty.BEGINNER, "40 hours", True),
        ("Neural Networks & PyTorch", "PyTorch,Deep Learning,Python", CourseDifficulty.ADVANCED, "55 hours", False),
        
        # DevOps & Cloud
        ("Docker & Kubernetes Complete", "Docker,Kubernetes,DevOps", CourseDifficulty.INTERMEDIATE, "25 hours", True),
        ("AWS Solutions Architect", "AWS,Cloud Computing,DevOps", CourseDifficulty.ADVANCED, "60 hours", False),
        ("Azure Cloud Fundamentals", "Azure,Cloud Computing", CourseDifficulty.BEGINNER, "30 hours", True),
        ("CI/CD with Jenkins & GitLab", "CI/CD,Jenkins,GitLab CI", CourseDifficulty.INTERMEDIATE, "22 hours", False),
        
        # Databases
        ("PostgreSQL Complete Guide", "PostgreSQL,SQL", CourseDifficulty.BEGINNER, "20 hours", True),
        ("MongoDB for Developers", "MongoDB,NoSQL", CourseDifficulty.INTERMEDIATE, "18 hours", False),
        ("Redis & Caching Strategies", "Redis,Caching", CourseDifficulty.ADVANCED, "15 hours", False),
        
        # API & Architecture
        ("REST API Design Best Practices", "REST API,Node.js,FastAPI", CourseDifficulty.INTERMEDIATE, "15 hours", True),
        ("GraphQL Complete Course", "GraphQL,JavaScript,Apollo", CourseDifficulty.ADVANCED, "25 hours", False),
        ("System Design Fundamentals", "System Design,Architecture", CourseDifficulty.ADVANCED, "35 hours", False),
        
        # Mobile Development
        ("React Native for Mobile", "React Native,JavaScript,Redux", CourseDifficulty.INTERMEDIATE, "42 hours", False),
        ("Flutter & Dart Complete", "Flutter,Dart,Mobile Development", CourseDifficulty.BEGINNER, "48 hours", False),
        
        # Testing & Quality
        ("Testing JavaScript Applications", "Jest,Testing,JavaScript", CourseDifficulty.INTERMEDIATE, "20 hours", True),
        ("Python Testing with Pytest", "Pytest,Testing,Python", CourseDifficulty.INTERMEDIATE, "18 hours", False),
    ]
    
    for i, (title, skills, difficulty, duration, is_free) in enumerate(course_data):
        course = Course(
            title=title,
            provider=COURSE_PROVIDERS[i % len(COURSE_PROVIDERS)],
            url=f"https://example.com/course/{i}",
            description=f"Comprehensive course covering {skills.replace(',', ', ')}. Hands-on projects and real-world examples included.",
            skills_covered=skills.split(","),
            difficulty=difficulty,
            duration=duration,
            is_free=is_free
        )
        session.add(course)
        courses.append(course)
    
    await session.commit()
    print(f"✓ Created {len(courses)} courses")
    return courses


async def create_study_groups(session: AsyncSession) -> list[StudyGroup]:
    """Create study groups with diverse topics."""
    print("Creating study groups...")
    study_groups = []
    
    # Get a student user to be owner
    result = await session.execute(
        select(User).where(User.role == UserRole.STUDENT).limit(1)
    )
    owner = result.scalar_one_or_none()
    
    if not owner:
        # Create a dummy student if none exists
        owner = User(
            email="studygroup_owner@test.com",
            password_hash="$2b$12$dummy_hash_for_testing",
            role=UserRole.STUDENT,
            is_active=True
        )
        session.add(owner)
        await session.flush()
    
    group_data = [
        # Beginner Groups
        ("Python Learners Group", "Web Development", StudyGroupLevel.BEGINNER, 
         "Learn Python from scratch with hands-on projects"),
        ("JavaScript Fundamentals", "Web Development", StudyGroupLevel.BEGINNER,
         "Master JavaScript basics and build interactive websites"),
        ("Data Science Explorers", "Data Science", StudyGroupLevel.BEGINNER,
         "Introduction to data analysis with Python and Pandas"),
        ("Git & GitHub Basics", "DevOps", StudyGroupLevel.BEGINNER,
         "Version control fundamentals for beginners"),
        
        # Intermediate Groups
        ("React Developers Circle", "Web Development", StudyGroupLevel.INTERMEDIATE,
         "Build modern web apps with React hooks and state management"),
        ("ML/AI Study Circle", "Machine Learning", StudyGroupLevel.INTERMEDIATE,
         "Explore machine learning algorithms and real-world applications"),
        ("Backend with Node.js", "Backend Development", StudyGroupLevel.INTERMEDIATE,
         "Master Node.js, Express, and REST API development"),
        ("Cloud Computing Study", "Cloud Computing", StudyGroupLevel.INTERMEDIATE,
         "AWS and Azure cloud services hands-on practice"),
        ("Database Design Masters", "Backend Development", StudyGroupLevel.INTERMEDIATE,
         "PostgreSQL, MongoDB and database optimization"),
        
        # Advanced Groups
        ("DevOps Masters", "DevOps", StudyGroupLevel.ADVANCED,
         "Docker, Kubernetes, CI/CD and infrastructure as code"),
        ("Cybersecurity Elite", "Cybersecurity", StudyGroupLevel.ADVANCED,
         "Advanced security practices, penetration testing and ethical hacking"),
        ("System Design Study", "Backend Development", StudyGroupLevel.ADVANCED,
         "Design scalable distributed systems and microservices"),
        ("Deep Learning Research", "Machine Learning", StudyGroupLevel.ADVANCED,
         "Neural networks, transformers and cutting-edge AI research"),
        ("Full Stack Architects", "Full Stack", StudyGroupLevel.ADVANCED,
         "End-to-end application development with modern tech stacks"),
    ]
    
    for name, domain, level, description in group_data:
        group = StudyGroup(
            name=name,
            description=description,
            domain=domain,
            skill_level=level,
            owner_id=owner.id,
            max_members=15 + (len(study_groups) % 10),  # 15-25 members
            is_active=True
        )
        session.add(group)
        study_groups.append(group)
    
    await session.commit()
    print(f"✓ Created {len(study_groups)} study groups")
    return study_groups


async def clear_seed_data(session: AsyncSession):
    """Clear all seed data (keeps real user accounts)."""
    print("\n" + "="*60)
    print("CLEARING SEED DATA")
    print("="*60 + "\n")
    
    # Delete in reverse dependency order
    print("Deleting study groups...")
    await session.execute(delete(StudyGroup))
    
    print("Deleting courses...")
    await session.execute(delete(Course))
    
    print("Deleting mentors...")
    await session.execute(delete(Mentor))
    
    print("Deleting internships...")
    await session.execute(delete(Internship))
    
    print("Deleting jobs...")
    await session.execute(delete(Job))
    
    print("Deleting companies...")
    await session.execute(delete(Company))
    
    # Delete only test user accounts
    print("Deleting test users...")
    await session.execute(
        delete(User).where(
            User.email.like("%@test.com")
        )
    )
    
    await session.commit()
    print("✓ Seed data cleared!\n")


async def main():
    """Main seeding function."""
    # Check for --clear flag
    clear_first = "--clear" in sys.argv
    
    print("\n" + "="*60)
    print("SEEDING RECOMMENDATION TEST DATA")
    print("="*60 + "\n")
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        if clear_first:
            await clear_seed_data(session)
        
        # Create all data
        skills_map = await create_skills(session)
        companies = await create_companies(session)
        jobs = await create_jobs(session, companies, skills_map)
        internships = await create_internships(session, companies)
        mentors = await create_mentors(session)
        courses = await create_courses(session)
        study_groups = await create_study_groups(session)
    
    await engine.dispose()
    
    print("\n" + "="*60)
    print("✓ SEEDING COMPLETE!")
    print("="*60)
    print(f"\nSummary:")
    print(f"  - {len(skills_map)} Skills")
    print(f"  - {len(companies)} Companies")
    print(f"  - {len(jobs)} Jobs")
    print(f"  - {len(internships)} Internships")
    print(f"  - {len(mentors)} Mentors")
    print(f"  - {len(courses)} Courses")
    print(f"  - {len(study_groups)} Study Groups")
    print("\nYou can now test the recommendation endpoints!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
