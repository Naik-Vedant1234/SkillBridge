"""Pydantic schemas — explicit re-exports for the entire API surface."""

# Auth
from app.schemas.auth import (  # noqa: F401
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    GoogleOAuthRequest,
    MessageResponse,
)

# User
from app.schemas.user import (  # noqa: F401
    UserBase,
    UserResponse,
    UserUpdate,
)

# Student
from app.schemas.student import (  # noqa: F401
    StudentBase,
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentWithSkills,
    StudentListResponse,
)

# Skill
from app.schemas.skill import (  # noqa: F401
    SkillBase,
    SkillCreate,
    SkillResponse,
)

# Resume
from app.schemas.resume import (  # noqa: F401
    ResumeUploadResponse,
    ResumeResponse,
    ResumeListResponse,
)

# Job
from app.schemas.job import (  # noqa: F401
    JobBase,
    JobCreate,
    JobUpdate,
    JobResponse,
    JobListResponse,
)

# Internship
from app.schemas.internship import (  # noqa: F401
    InternshipBase,
    InternshipCreate,
    InternshipUpdate,
    InternshipResponse,
    InternshipListResponse,
)

# Company
from app.schemas.company import (  # noqa: F401
    CompanyBase,
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
)

# Mentor
from app.schemas.mentor import (  # noqa: F401
    MentorBase,
    MentorCreate,
    MentorUpdate,
    MentorResponse,
    MentorListResponse,
)

# Course
from app.schemas.course import (  # noqa: F401
    CourseBase,
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseListResponse,
)

# Application
from app.schemas.application import (  # noqa: F401
    ApplicationCreate,
    ApplicationUpdateStatus,
    ApplicationResponse,
    ApplicationListResponse,
)

# Recommendation
from app.schemas.recommendation import (  # noqa: F401
    RecommendationResponse,
    RecommendationListResponse,
    RecommendationEventCreate,
    RecommendationEventResponse,
)

# Career
from app.schemas.career import (  # noqa: F401
    CareerGoalBase,
    CareerGoalCreate,
    CareerGoalResponse,
    CareerRoleResponse,
    CareerRoleDetailResponse,
    SkillGapResponse,
    PlacementReadinessResponse,
    RoadmapResponse,
)

# Study Group
from app.schemas.study_group import (  # noqa: F401
    StudyGroupBase,
    StudyGroupCreate,
    StudyGroupUpdate,
    StudyGroupResponse,
    StudyGroupListResponse,
)

# Mentor Request
from app.schemas.mentor_request import (  # noqa: F401
    MentorRequestCreate,
    MentorRequestUpdateStatus,
    MentorRequestResponse,
    MentorRequestListResponse,
)
