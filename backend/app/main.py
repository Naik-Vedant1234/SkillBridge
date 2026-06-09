from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.exceptions import generic_exception_handler

# Import routers
from app.api.v1 import (
    auth, users, students, resumes, recommendations,
    jobs, internships, mentors, companies, courses, applications,
    admin, career, study_groups, skills,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    import os
    os.makedirs(f"{settings.STORAGE_PATH}/resumes", exist_ok=True)
    os.makedirs(f"{settings.STORAGE_PATH}/certificates", exist_ok=True)
    print(f"🚀 {settings.APP_NAME} starting up...")
    yield
    # Shutdown
    print(f"🛑 {settings.APP_NAME} shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Career Intelligence and Recommendation Platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(Exception, generic_exception_handler)

# Mount static files for resume downloads
import os
storage_path = os.path.abspath(settings.STORAGE_PATH)
app.mount("/storage", StaticFiles(directory=storage_path), name="storage")

# Include all v1 routers
api_prefix = settings.API_V1_PREFIX
app.include_router(auth.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(students.router, prefix=api_prefix)
app.include_router(resumes.router, prefix=api_prefix)
app.include_router(recommendations.router, prefix=api_prefix)
app.include_router(jobs.router, prefix=api_prefix)
app.include_router(internships.router, prefix=api_prefix)
app.include_router(mentors.router, prefix=api_prefix)
app.include_router(companies.router, prefix=api_prefix)
app.include_router(courses.router, prefix=api_prefix)
app.include_router(applications.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)
app.include_router(career.router, prefix=api_prefix)
app.include_router(study_groups.router, prefix=api_prefix)
app.include_router(skills.router, prefix=api_prefix)


@app.get("/", tags=["Health"])
async def root():
    return {"name": settings.APP_NAME, "status": "running", "version": "0.1.0"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
