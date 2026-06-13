"""
Roadmap Engine — generates month-by-month career plans.
Pipeline: Career Goal → Career Knowledge Service → Skill Gap → Gemini refinement → Roadmap
"""

from uuid import UUID
import google.generativeai as genai
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.career_role import CareerRole, RoleProject, RoleCertification
from app.career.skill_gap_engine import SkillGapEngine


class RoadmapEngine:
    """
    Generates personalized career roadmaps using:
    1. Career Knowledge Base (skills, projects, certs)
    2. Skill Gap Analysis
    3. Gemini AI for timeline and personalization
    """
    
    def __init__(self):
        # Configure Gemini
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')  # Use stable model
        else:
            self.model = None
        
        self.skill_gap_engine = SkillGapEngine()
    
    async def generate(
        self, 
        db: AsyncSession,
        student_id: UUID, 
        role_id: UUID,
        months: int = 4,
        job_description: str | None = None
    ) -> dict:
        """
        Generate a month-by-month career roadmap.
        
        Args:
            db: Database session
            student_id: Student UUID
            role_id: Target career role UUID
            months: Timeline in months (default 4)
            job_description: Optional job description to tailor roadmap
            
        Returns:
            Structured roadmap with monthly milestones
        """
        # Get skill gap analysis
        gap_analysis = await self.skill_gap_engine.analyze_gap(db, student_id, role_id)
        
        if "error" in gap_analysis:
            return gap_analysis
        
        # Get role details with projects and certifications
        role_result = await db.execute(
            select(CareerRole)
            .options(
                selectinload(CareerRole.role_projects),
                selectinload(CareerRole.role_certifications)
            )
            .where(CareerRole.id == role_id)
        )
        role = role_result.scalar_one_or_none()
        
        # Build structured roadmap from knowledge base
        base_roadmap = self._build_base_roadmap(
            role, 
            gap_analysis, 
            months
        )
        
        # Refine with Gemini AI
        if self.model and settings.GEMINI_API_KEY:
            refined_roadmap = await self._refine_with_gemini(
                role,
                gap_analysis,
                base_roadmap,
                months,
                job_description
            )
        else:
            refined_roadmap = base_roadmap
        
        return {
            "role": {
                "id": str(role.id),
                "title": role.title,
                "domain": role.domain
            },
            "timeline_months": months,
            "skill_coverage": gap_analysis["analysis"]["coverage_percentage"],
            "roadmap": refined_roadmap,
            "resources": {
                "projects": [
                    {
                        "title": proj.project_title,
                        "description": proj.description,
                        "difficulty": proj.difficulty.value
                    }
                    for proj in role.role_projects
                ],
                "certifications": [
                    {
                        "name": cert.certification_name,
                        "provider": cert.provider
                    }
                    for cert in role.role_certifications
                ]
            }
        }
    
    def _build_base_roadmap(
        self,
        role: CareerRole,
        gap_analysis: dict,
        months: int
    ) -> list[dict]:
        """Build base roadmap from knowledge base."""
        missing_skills = gap_analysis["missing_skills"]
        
        # Distribute skills across months
        roadmap = []
        skills_per_month = max(1, len(missing_skills) // months)
        
        for month in range(1, months + 1):
            start_idx = (month - 1) * skills_per_month
            end_idx = start_idx + skills_per_month if month < months else len(missing_skills)
            month_skills = missing_skills[start_idx:end_idx]
            
            milestone = {
                "month": month,
                "title": f"Month {month}",
                "focus": self._get_month_focus(month, months),
                "skills_to_learn": [s["name"] for s in month_skills] if month_skills else [],
                "tasks": self._generate_tasks(month, month_skills, role),
                "projects": self._suggest_projects(month, role, months)
            }
            
            roadmap.append(milestone)
        
        return roadmap
    
    def _get_month_focus(self, month: int, total_months: int) -> str:
        """Get focus area for each month."""
        if month == 1:
            return "Foundation & Essential Skills"
        elif month == total_months:
            return "Advanced Topics & Portfolio"
        elif month <= total_months // 2:
            return "Core Skills Development"
        else:
            return "Practical Application"
    
    def _generate_tasks(self, month: int, skills: list[dict], role: CareerRole) -> list[str]:
        """Generate tasks for the month."""
        tasks = []
        
        for skill in skills[:3]:  # Top 3 skills for the month
            if skill["importance"] == "essential":
                tasks.append(f"Master {skill['name']} (essential skill)")
            else:
                tasks.append(f"Learn {skill['name']}")
        
        if month == 1:
            tasks.append("Set up development environment")
            tasks.append("Create GitHub account and portfolio")
        
        return tasks if tasks else ["Continue practicing previous skills"]
    
    def _suggest_projects(self, month: int, role: CareerRole, total_months: int) -> list[str]:
        """Suggest projects based on month."""
        if not role.role_projects:
            return []
        
        projects = []
        
        # Distribute projects across timeline
        if month == total_months // 2:
            # Mid-point: intermediate project
            for proj in role.role_projects:
                if proj.difficulty.value == "intermediate":
                    projects.append(proj.project_title)
                    break
        elif month == total_months:
            # Final month: advanced project
            for proj in role.role_projects:
                if proj.difficulty.value == "advanced":
                    projects.append(proj.project_title)
                    break
        
        return projects
    
    async def _refine_with_gemini(
        self,
        role: CareerRole,
        gap_analysis: dict,
        base_roadmap: list[dict],
        months: int,
        job_description: str | None = None
    ) -> list[dict]:
        """Use Gemini to refine and personalize the roadmap."""
        prompt = self._build_gemini_prompt(role, gap_analysis, base_roadmap, months, job_description)
        
        try:
            response = self.model.generate_content(prompt)
            
            # For now, return base roadmap with AI insights added
            # In production, you'd parse AI response into structured format
            refined = base_roadmap.copy()
            
            # Add AI insights to first milestone
            if refined and response.text:
                refined[0]["ai_insights"] = response.text[:200] + "..."
            
            return refined
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fallback to base roadmap
            return base_roadmap
    
    def _build_gemini_prompt(
        self,
        role: CareerRole,
        gap_analysis: dict,
        base_roadmap: list[dict],
        months: int,
        job_description: str | None = None
    ) -> str:
        """Build prompt for Gemini AI."""
        missing_skills = [s["name"] for s in gap_analysis["missing_skills"][:5]]
        
        job_context = ""
        if job_description:
            job_context = f"\n\nTarget Job Description:\n{job_description[:500]}\n"
        
        prompt = f"""You are a career mentor helping a student become a {role.title}.

The student is missing these key skills: {', '.join(missing_skills)}

Current skill coverage: {gap_analysis['analysis']['coverage_percentage']}%

Timeline: {months} months
{job_context}
Base roadmap structure:
{self._format_roadmap_for_prompt(base_roadmap)}

Please provide:
1. One motivational tip for getting started
2. One warning about common pitfalls
3. One suggestion for accelerating learning
{f"4. How this roadmap aligns with the target job description" if job_description else ""}

Keep your response under 150 words."""
        
        return prompt
    
    def _format_roadmap_for_prompt(self, roadmap: list[dict]) -> str:
        """Format roadmap for prompt."""
        lines = []
        for milestone in roadmap:
            lines.append(f"Month {milestone['month']}: {milestone['focus']}")
            if milestone['skills_to_learn']:
                lines.append(f"  Skills: {', '.join(milestone['skills_to_learn'][:3])}")
        return "\n".join(lines)

