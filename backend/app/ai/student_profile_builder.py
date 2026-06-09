"""Student Profile Builder — creates structured profile JSON from parsed resume data."""


class StudentProfileBuilder:
    """
    Builds a unified student profile from multiple data sources:
    - Parsed resume data (skills, experience, projects)
    - Database profile (goals, CGPA, college)
    - Activity history (applications, interactions)

    Output is used for embedding generation.
    """

    def build_profile(self, parsed_resume: dict, student_data: dict) -> dict:
        """Build a comprehensive profile for embedding generation."""
        raise NotImplementedError("To be implemented in Phase 3")

    def profile_to_text(self, profile: dict) -> str:
        """Convert structured profile to text for embedding."""
        raise NotImplementedError("To be implemented in Phase 3")
