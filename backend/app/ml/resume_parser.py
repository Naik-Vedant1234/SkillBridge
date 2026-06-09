"""
Resume Parser - Extract text and structure from PDF resumes using PyMuPDF.
Enhanced with SpaCy NER, proficiency detection, and skill categorization.
"""

import re
from pathlib import Path
import pymupdf  # PyMuPDF

from app.ml.skill_ontology import extract_skills_from_text
from app.ml.skill_categories import categorize_skills, get_primary_domain
from app.ml.proficiency_detector import ProficiencyDetector
from app.ml.spacy_extractor import SpacyExtractor


class ResumeParser:
    """Parse resume PDFs and extract structured information with advanced AI features."""
    
    def __init__(self):
        self.proficiency_detector = ProficiencyDetector()
        self.spacy_extractor = SpacyExtractor()
        self.use_spacy = self.spacy_extractor.is_available()
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all text from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        try:
            doc = pymupdf.open(pdf_path)
            text = ""
            
            for page in doc:
                text += page.get_text()
            
            doc.close()
            return text

        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_email(self, text: str) -> str | None:
        """Extract email address from text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def extract_phone(self, text: str) -> str | None:
        """Extract phone number from text."""
        # Match various phone formats
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{10}',
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        
        return None
    
    def extract_name(self, text: str) -> str | None:
        """
        Extract candidate's name from resume.
        Uses SpaCy if available, falls back to heuristics.
        """
        if self.use_spacy:
            name = self.spacy_extractor.extract_name(text)
            if name:
                return name
        
        # Fallback: first line heuristic
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            first_line = lines[0]
            if len(first_line) < 50 and not re.search(r'\d', first_line):
                return first_line
        
        return None
    
    def extract_education(self, text: str) -> list[dict]:
        """
        Extract education information from text.
        Uses SpaCy for better extraction if available.
        Returns list of education entries.
        """
        if self.use_spacy:
            education = self.spacy_extractor.extract_education_entries(text)
            if education:
                return education
        
        # Fallback to original pattern-based extraction
        education = []
        text_lower = text.lower()
        
        # Common degree patterns
        degrees = [
            "bachelor", "b.tech", "btech", "b.e.", "b.sc", "bsc",
            "master", "m.tech", "mtech", "m.e.", "m.sc", "msc",
            "phd", "ph.d", "doctorate",
            "diploma", "associate"
        ]
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for degree in degrees:
                if degree in line_lower:
                    # Try to extract year
                    year_match = re.search(r'(19|20)\d{2}', line)
                    year = year_match.group(0) if year_match else None
                    
                    education.append({
                        "degree": degree.title(),
                        "institution": line.strip(),
                        "year": year
                    })
                    break
        
        return education
    
    def extract_experience(self, text: str) -> list[dict]:
        """
        Extract work experience entries.
        Uses SpaCy for better extraction if available.
        """
        if self.use_spacy:
            experience = self.spacy_extractor.extract_experience_entries(text)
            if experience:
                return experience
        
        # Fallback: basic extraction
        return []
    
    def extract_projects(self, text: str) -> list[dict]:
        """
        Extract project information.
        Uses SpaCy for better extraction if available.
        """
        if self.use_spacy:
            projects = self.spacy_extractor.extract_projects(text)
            return projects
        
        return []
    
    def calculate_experience_years(self, text: str) -> int:
        """
        Estimate years of experience from resume text.
        Simple heuristic: count year ranges mentioned.
        """
        # Match patterns like "2020-2023", "2020 - Present", etc.
        year_ranges = re.findall(r'(19|20)\d{2}\s*[-–]\s*(?:(19|20)\d{2}|present|current)', text, re.IGNORECASE)
        
        total_years = 0
        current_year = 2026  # From system date
        
        for start, end in year_ranges:
            start_year = int(start) if start else 0
            if end and end.lower() not in ['present', 'current']:
                end_year = int(end)
            else:
                end_year = current_year
            
            if start_year > 0:
                years = end_year - start_year
                if 0 <= years <= 50:  # Sanity check
                    total_years += years
        
        return min(total_years, 50)  # Cap at 50 years
    
    def parse_resume(self, pdf_path: str) -> dict:
        """
        Parse resume PDF and extract structured data with advanced AI features.
        
        Args:
            pdf_path: Path to resume PDF file
            
        Returns:
            Dictionary with parsed resume data including:
            - Basic info (name, email, phone)
            - Education and experience
            - Skills with proficiency levels and categories
            - Projects (if SpaCy available)
        """
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        # Extract skills first
        skills = extract_skills_from_text(text)
        
        # Detect proficiency levels for each skill
        proficiencies = self.proficiency_detector.detect_all_proficiencies(skills, text)
        
        # Categorize skills
        skill_categories = categorize_skills(skills)
        primary_domain = get_primary_domain(skills)
        
        # Extract structured information
        parsed_data = {
            "raw_text": text,
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "education": self.extract_education(text),
            "experience": self.extract_experience(text),
            "experience_years": self.calculate_experience_years(text),
            "projects": self.extract_projects(text),
            "skills": skills,
            "skill_proficiencies": proficiencies,
            "skill_categories": skill_categories,
            "primary_domain": primary_domain,
            "spacy_used": self.use_spacy
        }
        
        return parsed_data
