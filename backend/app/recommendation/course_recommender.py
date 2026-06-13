"""Course recommender — suggests learning resources for skill gaps."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course, CourseDifficulty
from app.models.student import Student
from app.recommendation.base_recommender import BaseRecommender


class CourseRecommender(BaseRecommender):
    """Recommends courses based on skill gaps and learning path."""
    
    async def recommend(
        self, 
        db: AsyncSession,
        student_id: UUID, 
        limit: int = 10,
        target_skills: list[str] | None = None
    ) -> list[dict]:
        """
        Get personalized course recommendations.
        
        Args:
            db: Database session
            student_id: Student UUID
            limit: Max recommendations
            target_skills: Optional list of skills to focus on
            
        Returns:
            List of course recommendations with relevance scores
        """
        # Get student profile and skills
        student, student_skills = await self.get_student_with_skills(db, student_id)
        if not student:
            return []
        
        # Get all courses
        result = await db.execute(
            select(Course)
            .limit(200)  # Pre-filter to reasonable set
        )
        courses = result.scalars().all()
        
        if not courses:
            return []
        
        # Determine target skills (gaps or specified)
        if target_skills:
            skills_to_learn = target_skills
        else:
            # Recommend courses for skills student doesn't have
            # (In Phase 4.2, we'll use skill gap analysis)
            skills_to_learn = self._identify_popular_skills_to_learn(student_skills)
        
        # Score each course
        scored_courses = []
        for course in courses:
            relevance_score = self._calculate_relevance_score(
                course, student_skills, skills_to_learn
            )
            difficulty_score = self._calculate_difficulty_score(course, student, student_skills)
            popularity_score = self._calculate_course_popularity(course)
            rating_score = self._calculate_rating_score(course)
            
            embedding_score = 0.5  # TODO: Add vector similarity
            
            # Course-specific weights
            final_score = (
                0.35 * embedding_score +
                0.30 * relevance_score +
                0.20 * difficulty_score +
                0.10 * popularity_score +
                0.05 * rating_score
            )
            
            scored_courses.append({
                "course": course,
                "score": final_score,
                "relevance": int(relevance_score * 100),
            })
        
        scored_courses.sort(key=lambda x: x["score"], reverse=True)
        
        recommendations = []
        for item in scored_courses[:limit]:
            course = item["course"]
            recommendations.append({
                "id": str(course.id),
                "title": course.title,
                "provider": course.provider,
                "url": course.url,
                "difficulty": course.difficulty.value if course.difficulty else "intermediate",
                "duration": course.duration,  # Course has 'duration' field, not 'duration_hours'
                "rating": 4.5,  # Default rating (course model doesn't have this field)
                "description": course.description[:200] + "..." if course.description and len(course.description) > 200 else course.description,
                "skills_covered": course.skills_covered or [],
                "relevance": item["relevance"],
                "score": round(item["score"], 3),
            })
        
        return recommendations
    
    def _identify_popular_skills_to_learn(self, current_skills: list[str]) -> list[str]:
        """
        Identify popular skills student should learn.
        
        Returns skills not in current_skills that are in-demand.
        """
        popular_skills = [
            "Python", "JavaScript", "React", "Node.js", "Docker",
            "Kubernetes", "AWS", "Machine Learning", "System Design",
            "Data Structures", "Algorithms", "SQL", "MongoDB"
        ]
        
        current_lower = {s.lower() for s in current_skills}
        return [s for s in popular_skills if s.lower() not in current_lower]
    
    def _calculate_relevance_score(
        self, 
        course: Course, 
        student_skills: list[str],
        target_skills: list[str]
    ) -> float:
        """
        Calculate how relevant course is to student's learning goals.
        
        Higher score if course teaches target skills student wants.
        """
        if not course.skills_covered:
            return 0.3
        
        course_skills_lower = {s.lower() for s in course.skills_covered}
        target_skills_lower = {s.lower() for s in target_skills}
        
        # How many target skills does this course teach?
        overlap = len(course_skills_lower.intersection(target_skills_lower))
        
        if not target_skills:
            return 0.5
        
        return min(overlap / len(target_skills), 1.0)
    
    def _calculate_difficulty_score(self, course: Course, student: Student, student_skills: list[str]) -> float:
        """
        Calculate difficulty appropriateness.
        
        Match course difficulty to student's level.
        """
        if not course.difficulty:
            return 0.5
        
        # Estimate student level based on skill count
        skill_count = len(student_skills)
        
        if skill_count < 3:
            student_level = "beginner"
        elif skill_count < 8:
            student_level = "intermediate"
        else:
            student_level = "advanced"
        
        # Perfect match = 1.0, one level off = 0.7, two levels off = 0.4
        difficulty_order = ["beginner", "intermediate", "advanced"]
        
        try:
            student_idx = difficulty_order.index(student_level)
            course_idx = difficulty_order.index(course.difficulty.value)
            diff = abs(student_idx - course_idx)
            
            if diff == 0:
                return 1.0
            elif diff == 1:
                return 0.7
            else:
                return 0.4
        except ValueError:
            return 0.5
    
    def _calculate_course_popularity(self, course: Course) -> float:
        """Calculate popularity score (based on enrollment count if available)."""
        # TODO: Track enrollment in Phase 5
        return 0.5
    
    def _calculate_rating_score(self, course: Course) -> float:
        """Calculate score from course rating (Course model doesn't have rating field)."""
        # Return neutral score since we don't track ratings yet
        return 0.7
