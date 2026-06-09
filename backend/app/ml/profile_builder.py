"""
Profile Builder - Builds structured student profile from parsed resume data.
Enhanced to use proficiency levels and skill categories.
"""

from typing import Dict, Any


class ProfileBuilder:
    """Build student profile from parsed resume with advanced features."""
    
    def build_profile(self, parsed_data: dict) -> dict:
        """
        Build structured profile from parsed resume data.
        
        Args:
            parsed_data: Dictionary from ResumeParser with enhanced fields
            
        Returns:
            Profile data that can update student record
        """
        profile = {}
        
        # Name
        if parsed_data.get("name"):
            # Note: Can't update user.name directly, but store in bio or elsewhere
            profile["candidate_name"] = parsed_data["name"]
        
        # Education - extract highest degree and institution
        if parsed_data.get("education"):
            latest_education = parsed_data["education"][0]
            profile["college"] = self._clean_institution_name(
                latest_education.get("institution", "")
            )
            
            # Try to extract graduation year
            if latest_education.get("year"):
                try:
                    profile["graduation_year"] = int(latest_education["year"])
                except (ValueError, TypeError):
                    pass
        
        # Build enhanced bio with primary domain
        experience_years = parsed_data.get("experience_years", 0)
        skills_count = len(parsed_data.get("skills", []))
        primary_domain = parsed_data.get("primary_domain", "")
        
        bio_parts = []
        if primary_domain:
            bio_parts.append(f"{primary_domain} Developer")
        if experience_years > 0:
            bio_parts.append(f"{experience_years}+ years of experience")
        if skills_count > 0:
            bio_parts.append(f"{skills_count}+ skills")
        
        if bio_parts:
            profile["bio"] = " | ".join(bio_parts)
        
        # Add skill categories summary
        skill_categories = parsed_data.get("skill_categories", {})
        if skill_categories:
            profile["skill_domains"] = list(skill_categories.keys())
        
        return profile
    
    def _clean_institution_name(self, text: str) -> str:
        """Clean and extract institution name from education text."""
        # Remove degree info, years, etc.
        text = text.split('\n')[0]  # Take first line
        text = text.split(',')[0]   # Take before comma
        
        # Remove common prefixes
        prefixes = ["Bachelor", "Master", "B.Tech", "M.Tech", "PhD", "Ph.D"]
        for prefix in prefixes:
            text = text.replace(prefix, "")
        
        return text.strip()
    
    def calculate_resume_score(self, parsed_data: dict) -> float:
        """
        Calculate resume completeness and quality score (0-100).
        
        Enhanced scoring criteria:
        - Has name: 5 points
        - Has email: 10 points
        - Has phone: 10 points
        - Has education: 15 points
        - Has experience: 15 points
        - Number of skills: up to 30 points (0.75 points per skill, max 30)
        - Skill proficiencies detected: 10 points
        - Has projects: 5 points
        """
        score = 0.0
        
        # Contact information
        if parsed_data.get("name"):
            score += 5
        if parsed_data.get("email"):
            score += 10
        if parsed_data.get("phone"):
            score += 10
        
        # Education
        if parsed_data.get("education"):
            score += 15
        
        # Experience
        experience_years = parsed_data.get("experience_years", 0)
        if experience_years > 0:
            score += 15
        
        # Skills (up to 30 points)
        skills = parsed_data.get("skills", [])
        skill_points = min(len(skills) * 0.75, 30)
        score += skill_points
        
        # Proficiency detection bonus
        proficiencies = parsed_data.get("skill_proficiencies", {})
        if proficiencies:
            # Check if any proficiencies have high confidence
            high_confidence = sum(1 for p in proficiencies.values() if p.get("confidence", 0) > 0.7)
            if high_confidence > 0:
                score += 10
        
        # Projects bonus
        projects = parsed_data.get("projects", [])
        if projects:
            score += 5
        
        return round(min(score, 100), 2)
