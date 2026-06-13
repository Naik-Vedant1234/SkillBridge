# Import all models so Alembic can discover them via Base.metadata

from app.db.base import Base  # noqa: F401

from app.models.user import User, UserRole  # noqa: F401
from app.models.student import Student, student_skills, student_goals, Proficiency  # noqa: F401
from app.models.skill import Skill  # noqa: F401
from app.models.career_goal import CareerGoal  # noqa: F401
from app.models.resume import Resume, ResumeStatus  # noqa: F401
from app.models.job import Job  # noqa: F401
from app.models.internship import Internship  # noqa: F401
from app.models.company import Company  # noqa: F401
from app.models.mentor import Mentor  # noqa: F401
from app.models.course import Course, CourseDifficulty  # noqa: F401
from app.models.application import Application, ApplicationTargetType, ApplicationStatus  # noqa: F401
from app.models.bookmark import Bookmark, BookmarkTargetType  # noqa: F401
from app.models.recommendation import (  # noqa: F401
    Recommendation,
    RecommendationEvent,
    RecommendationTargetType,
    RecommendationAction,
)
from app.models.career_role import (  # noqa: F401
    CareerRole,
    RoleSkill,
    RoleProject,
    RoleCourse,
    RoleCertification,
    SkillImportance,
    ProjectDifficulty,
)
from app.models.study_group import StudyGroup, StudyGroupLevel  # noqa: F401
from app.models.mentor_request import MentorRequest, MentorRequestStatus  # noqa: F401
