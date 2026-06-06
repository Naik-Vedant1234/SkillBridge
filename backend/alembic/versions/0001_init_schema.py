"""init schema — all Phase 1 tables

Revision ID: 0001_init_schema
Revises:
Create Date: 2026-06-05

Uses explicit op.create_table() DDL so that:
  - Alembic tracks every column/index properly.
  - Future `alembic revision --autogenerate` produces clean diffs (no false positives).
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001_init_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Enum types are created automatically by SQLAlchemy when tables are created ──
    
    # ── users ─────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=True),
        sa.Column("role", sa.Enum("student", "mentor", "company", "admin", name="userrole"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("google_id", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("google_id", name="uq_users_google_id"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    # ── skills ────────────────────────────────────────────────────────────────
    op.create_table(
        "skills",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("category", sa.String(100), nullable=True),
        sa.UniqueConstraint("name", name="uq_skills_name"),
    )
    op.create_index("ix_skills_name", "skills", ["name"])

    # ── career_goals ──────────────────────────────────────────────────────────
    op.create_table(
        "career_goals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )

    # ── courses ───────────────────────────────────────────────────────────────
    op.create_table(
        "courses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("provider", sa.String(255), nullable=True),
        sa.Column("url", sa.String(500), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("skills_covered", postgresql.JSON(), nullable=True),
        sa.Column(
            "difficulty",
            sa.Enum("beginner", "intermediate", "advanced", name="coursedifficulty"),
            nullable=True,
        ),
        sa.Column("duration", sa.String(100), nullable=True),
        sa.Column("is_free", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    # ── career_roles ──────────────────────────────────────────────────────────
    op.create_table(
        "career_roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("domain", sa.String(100), nullable=True),
        sa.UniqueConstraint("title", name="uq_career_roles_title"),
    )

    # ── role_skills ───────────────────────────────────────────────────────────
    op.create_table(
        "role_skills",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "importance",
            sa.Enum("essential", "important", "nice_to_have", name="skillimportance"),
            nullable=False,
            server_default="important",
        ),
        sa.ForeignKeyConstraint(["role_id"], ["career_roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
    )

    # ── role_projects ─────────────────────────────────────────────────────────
    op.create_table(
        "role_projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "difficulty",
            sa.Enum("beginner", "intermediate", "advanced", name="projectdifficulty"),
            nullable=False,
            server_default="intermediate",
        ),
        sa.ForeignKeyConstraint(["role_id"], ["career_roles.id"], ondelete="CASCADE"),
    )

    # ── role_courses ──────────────────────────────────────────────────────────
    op.create_table(
        "role_courses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(["role_id"], ["career_roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
    )

    # ── role_certifications ───────────────────────────────────────────────────
    op.create_table(
        "role_certifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("certification_name", sa.String(255), nullable=False),
        sa.Column("provider", sa.String(255), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(["role_id"], ["career_roles.id"], ondelete="CASCADE"),
    )

    # ── companies ─────────────────────────────────────────────────────────────
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("website", sa.String(500), nullable=True),
        sa.Column("logo_url", sa.String(500), nullable=True),
        sa.Column("industry", sa.String(100), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", name="uq_companies_user_id"),
    )

    # ── students ──────────────────────────────────────────────────────────────
    op.create_table(
        "students",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("cgpa", sa.Float(), nullable=True),
        sa.Column("college", sa.String(255), nullable=True),
        sa.Column("graduation_year", sa.Integer(), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", name="uq_students_user_id"),
    )

    # ── mentors ───────────────────────────────────────────────────────────────
    op.create_table(
        "mentors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("experience", sa.Integer(), nullable=True),
        sa.Column("domain", sa.String(255), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("max_mentees", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", name="uq_mentors_user_id"),
    )

    # ── study_groups ──────────────────────────────────────────────────────────
    op.create_table(
        "study_groups",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("domain", sa.String(100), nullable=True),
        sa.Column(
            "skill_level",
            sa.Enum("beginner", "intermediate", "advanced", name="studygrouplevel"),
            nullable=True,
        ),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("max_members", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
    )

    # ── student_skills (association) ──────────────────────────────────────────
    op.create_table(
        "student_skills",
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "proficiency",
            sa.Enum("beginner", "intermediate", "advanced", "expert", name="proficiency"),
            nullable=True,
            server_default="beginner",
        ),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("student_id", "skill_id"),
    )

    # ── student_goals (association) ───────────────────────────────────────────
    op.create_table(
        "student_goals",
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("goal_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["goal_id"], ["career_goals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("student_id", "goal_id"),
    )

    # ── resumes ───────────────────────────────────────────────────────────────
    op.create_table(
        "resumes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("file_url", sa.String(500), nullable=False),
        sa.Column("original_filename", sa.String(255), nullable=False),
        sa.Column("parsed_data", postgresql.JSON(), nullable=True),
        sa.Column("skills_extracted", postgresql.JSON(), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("uploaded", "processing", "parsed", "failed", name="resumestatus"),
            nullable=False,
            server_default="uploaded",
        ),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
    )

    # ── jobs ──────────────────────────────────────────────────────────────────
    op.create_table(
        "jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requirements", postgresql.JSON(), nullable=True),
        sa.Column("salary_min", sa.Float(), nullable=True),
        sa.Column("salary_max", sa.Float(), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("is_remote", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
    )

    # ── internships ───────────────────────────────────────────────────────────
    op.create_table(
        "internships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requirements", postgresql.JSON(), nullable=True),
        sa.Column("duration", sa.String(100), nullable=True),
        sa.Column("stipend", sa.Float(), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("is_remote", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
    )

    # ── applications ──────────────────────────────────────────────────────────
    op.create_table(
        "applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "target_type",
            sa.Enum("job", "internship", name="applicationtargettype"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("pending", "reviewed", "shortlisted", "accepted", "rejected", name="applicationstatus"),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("applied_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
    )

    # ── recommendations ───────────────────────────────────────────────────────
    op.create_table(
        "recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "target_type",
            sa.Enum(
                "job", "internship", "mentor", "course", "studygroup",
                name="recommendationtargettype",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
    )

    # ── recommendation_events ─────────────────────────────────────────────────
    op.create_table(
        "recommendation_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("recommendation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "action",
            sa.Enum("viewed", "clicked", "saved", "applied", "dismissed", name="recommendationaction"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["recommendation_id"], ["recommendations.id"], ondelete="CASCADE"
        ),
    )

    # ── mentor_requests ───────────────────────────────────────────────────────
    op.create_table(
        "mentor_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mentor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("pending", "accepted", "rejected", name="mentorrequeststatus"),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["mentor_id"], ["mentors.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    # Drop tables in reverse dependency order
    op.drop_table("mentor_requests")
    op.drop_table("recommendation_events")
    op.drop_table("recommendations")
    op.drop_table("applications")
    op.drop_table("internships")
    op.drop_table("jobs")
    op.drop_table("resumes")
    op.drop_table("student_goals")
    op.drop_table("student_skills")
    op.drop_table("study_groups")
    op.drop_table("mentors")
    op.drop_table("students")
    op.drop_table("companies")
    op.drop_table("role_certifications")
    op.drop_table("role_courses")
    op.drop_table("role_projects")
    op.drop_table("role_skills")
    op.drop_table("career_roles")
    op.drop_table("courses")
    op.drop_table("career_goals")
    op.drop_table("skills")
    op.drop_table("users")

    # Drop enum types
    for enum_name in [
        "mentorrequeststatus", "studygrouplevel", "projectdifficulty",
        "skillimportance", "recommendationaction", "recommendationtargettype",
        "applicationstatus", "applicationtargettype", "coursedifficulty",
        "proficiency", "resumestatus", "userrole",
    ]:
        op.execute(f"DROP TYPE IF EXISTS {enum_name}")
