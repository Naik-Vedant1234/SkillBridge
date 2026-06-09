"""
Proficiency Detector - Detect skill proficiency levels from resume text context.
"""

import re
from enum import Enum


class ProficiencyLevel(str, Enum):
    """Skill proficiency levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


# Proficiency patterns with their levels
PROFICIENCY_PATTERNS = {
    ProficiencyLevel.EXPERT: [
        r"expert\s+(?:in|with|at)",
        r"mastery\s+(?:of|in)",
        r"deep\s+(?:expertise|knowledge|understanding)\s+(?:in|of|with)",
        r"extensive\s+experience\s+(?:in|with)",
        r"(\d+)\+?\s*years?\s+(?:of\s+)?experience",  # 5+ years
        r"lead\s+developer",
        r"senior\s+developer",
        r"architect",
        r"guru",
        r"ninja",
        r"wizard",
    ],
    ProficiencyLevel.ADVANCED: [
        r"advanced",
        r"proficient\s+(?:in|with|at)",
        r"strong\s+(?:skills|knowledge|experience)\s+(?:in|of|with)",
        r"solid\s+(?:understanding|experience|knowledge)\s+(?:of|in|with)",
        r"experienced\s+(?:in|with)",
        r"(\d+)\s*years?\s+(?:of\s+)?experience",  # 2-4 years
        r"skilled\s+(?:in|with|at)",
        r"competent",
    ],
    ProficiencyLevel.INTERMEDIATE: [
        r"intermediate",
        r"working\s+knowledge\s+(?:of|in)",
        r"good\s+(?:understanding|knowledge)\s+(?:of|in)",
        r"hands-on\s+experience\s+(?:with|in)",
        r"practical\s+experience\s+(?:with|in)",
        r"comfortable\s+(?:with|using)",
        r"moderate",
    ],
    ProficiencyLevel.BEGINNER: [
        r"beginner",
        r"basic\s+(?:knowledge|understanding)\s+(?:of|in)",
        r"familiar\s+with",
        r"exposure\s+to",
        r"introduced\s+to",
        r"learning",
        r"beginner-level",
        r"novice",
        r"foundational",
    ]
}


class ProficiencyDetector:
    """Detect skill proficiency levels from text context."""
    
    def __init__(self):
        self.patterns = PROFICIENCY_PATTERNS
    
    def detect_proficiency(self, skill_name: str, text: str, context_window: int = 100) -> tuple[ProficiencyLevel, float]:
        """
        Detect proficiency level for a skill based on surrounding context.
        
        Args:
            skill_name: Name of the skill to check
            text: Full resume text
            context_window: Number of characters to check before/after skill mention
            
        Returns:
            Tuple of (ProficiencyLevel, confidence_score)
        """
        text_lower = text.lower()
        skill_lower = skill_name.lower()
        
        # Find all occurrences of the skill in text
        skill_positions = [m.start() for m in re.finditer(r'\b' + re.escape(skill_lower) + r'\b', text_lower)]
        
        if not skill_positions:
            return ProficiencyLevel.INTERMEDIATE, 0.3  # Default if skill not found
        
        # Check context around each mention
        proficiency_scores = {level: 0.0 for level in ProficiencyLevel}
        
        for pos in skill_positions:
            # Extract context window
            start = max(0, pos - context_window)
            end = min(len(text_lower), pos + len(skill_lower) + context_window)
            context = text_lower[start:end]
            
            # Check for proficiency patterns
            for level, patterns in self.patterns.items():
                for pattern in patterns:
                    if re.search(pattern, context):
                        # Special handling for years of experience
                        if r"years" in pattern:
                            years_match = re.search(r'(\d+)', pattern)
                            if years_match:
                                years = int(years_match.group(1))
                                # More years = higher proficiency
                                if years >= 5:
                                    proficiency_scores[ProficiencyLevel.EXPERT] += 2.0
                                elif years >= 3:
                                    proficiency_scores[ProficiencyLevel.ADVANCED] += 1.5
                                elif years >= 1:
                                    proficiency_scores[ProficiencyLevel.INTERMEDIATE] += 1.0
                        else:
                            proficiency_scores[level] += 1.0
        
        # If no proficiency indicators found, use heuristics
        if all(score == 0 for score in proficiency_scores.values()):
            # Check if skill is mentioned multiple times
            mention_count = len(skill_positions)
            if mention_count >= 3:
                proficiency_scores[ProficiencyLevel.ADVANCED] = 0.5
            elif mention_count >= 2:
                proficiency_scores[ProficiencyLevel.INTERMEDIATE] = 0.6
            else:
                proficiency_scores[ProficiencyLevel.INTERMEDIATE] = 0.4
        
        # Find highest scoring proficiency
        best_level = max(proficiency_scores.items(), key=lambda x: x[1])
        
        # Calculate confidence (normalize to 0-1)
        total_score = sum(proficiency_scores.values())
        confidence = min(best_level[1] / max(total_score, 1.0), 1.0)
        
        # Boost confidence if we found explicit patterns
        if best_level[1] > 0:
            confidence = max(confidence, 0.7)
        
        return best_level[0], round(confidence, 2)
    
    def detect_all_proficiencies(self, skills: list[str], text: str) -> dict[str, dict]:
        """
        Detect proficiency levels for all skills.
        
        Args:
            skills: List of skill names
            text: Full resume text
            
        Returns:
            Dictionary mapping skill names to proficiency info
        """
        proficiencies = {}
        
        for skill in skills:
            level, confidence = self.detect_proficiency(skill, text)
            proficiencies[skill] = {
                "level": level.value,
                "confidence": confidence
            }
        
        return proficiencies
    
    def get_proficiency_score(self, level: ProficiencyLevel) -> int:
        """
        Convert proficiency level to numeric score (1-4).
        
        Args:
            level: ProficiencyLevel enum
            
        Returns:
            Numeric score (1=beginner, 2=intermediate, 3=advanced, 4=expert)
        """
        score_map = {
            ProficiencyLevel.BEGINNER: 1,
            ProficiencyLevel.INTERMEDIATE: 2,
            ProficiencyLevel.ADVANCED: 3,
            ProficiencyLevel.EXPERT: 4
        }
        return score_map.get(level, 2)
