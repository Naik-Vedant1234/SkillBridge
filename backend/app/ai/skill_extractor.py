"""Skill extractor — uses SpaCy NER + Skill Ontology for accurate extraction."""


class SkillExtractor:
    """Extract skills from resume text using NLP + ontology matching."""

    def extract_skills(self, text: str) -> list[str]:
        """Extract skills from resume text."""
        raise NotImplementedError("To be implemented in Phase 3")

    def match_with_ontology(self, raw_skills: list[str]) -> list[dict]:
        """Match extracted terms against the skill ontology for normalization."""
        raise NotImplementedError("To be implemented in Phase 3")
