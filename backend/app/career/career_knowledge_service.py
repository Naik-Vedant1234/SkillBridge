"""
Career Knowledge Service — the heart of the knowledge base.
Owns: career_roles → role_skills → role_projects → role_courses → role_certifications

The whole system depends on this for skill gap, roadmap, and placement readiness.
"""


class CareerKnowledgeService:
    """Queries the career knowledge base for role requirements."""

    async def get_role_requirements(self, role_id: str) -> dict:
        """Get all requirements (skills, projects, courses, certs) for a career role."""
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_required_skills(self, role_id: str) -> list[dict]:
        """Get required skills with importance levels for a role."""
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_suggested_projects(self, role_id: str) -> list[dict]:
        """Get suggested projects for a role."""
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_recommended_courses(self, role_id: str) -> list[dict]:
        """Get recommended courses for a role, ordered by priority."""
        raise NotImplementedError("To be implemented in Phase 4")

    async def get_certifications(self, role_id: str) -> list[dict]:
        """Get recommended certifications for a role."""
        raise NotImplementedError("To be implemented in Phase 4")

    async def list_roles(self, domain: str | None = None) -> list[dict]:
        """List available career roles, optionally filtered by domain."""
        raise NotImplementedError("To be implemented in Phase 4")
