"""
SpaCy NER Extractor - Use SpaCy for enhanced entity extraction and context understanding.
"""

import re
from typing import Dict, List, Tuple

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False


class SpacyExtractor:
    """Enhanced extraction using SpaCy NER and linguistic features."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize SpaCy extractor.
        
        Args:
            model_name: SpaCy model to load (default: en_core_web_sm)
        """
        self.nlp = None
        self.model_name = model_name
        
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load(model_name)
            except OSError:
                # Model not installed, will use fallback methods
                print(f"SpaCy model '{model_name}' not found. Using fallback extraction.")
                self.nlp = None
        else:
            print("SpaCy not available. Using fallback extraction.")
    
    def is_available(self) -> bool:
        """Check if SpaCy is available and loaded."""
        return self.nlp is not None
    
    def extract_name(self, text: str) -> str | None:
        """
        Extract candidate's name from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Extracted name or None
        """
        if self.nlp:
            # Use SpaCy NER to find PERSON entities
            doc = self.nlp(text[:500])  # Check first 500 chars
            
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    return ent.text
        
        # Fallback: assume first line is name
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            first_line = lines[0]
            # Basic validation - name shouldn't be too long or contain numbers
            if len(first_line) < 50 and not re.search(r'\d', first_line):
                return first_line
        
        return None
    
    def extract_organizations(self, text: str) -> List[str]:
        """
        Extract organization/company names from text.
        
        Args:
            text: Resume text
            
        Returns:
            List of organization names
        """
        orgs = []
        
        if self.nlp:
            doc = self.nlp(text)
            
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    orgs.append(ent.text)
        else:
            # Fallback: look for common company indicators
            company_patterns = [
                r'(?:worked at|employed at|position at)\s+([A-Z][A-Za-z\s&]+(?:Inc|LLC|Ltd|Corp|Corporation)?)',
                r'([A-Z][A-Za-z\s&]+(?:Inc|LLC|Ltd|Corp|Corporation))'
            ]
            
            for pattern in company_patterns:
                matches = re.findall(pattern, text)
                orgs.extend(matches)
        
        return list(set(orgs))[:10]  # Return unique, limit to 10
    
    def extract_experience_entries(self, text: str) -> List[Dict]:
        """
        Extract work experience entries with better context understanding.
        
        Args:
            text: Resume text
            
        Returns:
            List of experience entries
        """
        experiences = []
        
        # Look for common experience section headers
        experience_section = self._extract_section(text, [
            "experience", "work experience", "professional experience",
            "employment", "work history"
        ])
        
        if not experience_section:
            return experiences
        
        # Extract organizations from experience section
        orgs = self.extract_organizations(experience_section)
        
        # Extract job titles using common patterns
        title_patterns = [
            r'(Software Engineer|Developer|Programmer|Architect|Manager|Lead|Senior|Junior|Intern)',
            r'(Full[- ]?Stack|Front[- ]?End|Back[- ]?End|Data Scientist|ML Engineer)',
        ]
        
        titles = []
        for pattern in title_patterns:
            matches = re.findall(pattern, experience_section, re.IGNORECASE)
            titles.extend(matches)
        
        # Extract date ranges
        date_ranges = re.findall(
            r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4})\s*[-–]\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|Present|Current)',
            experience_section,
            re.IGNORECASE
        )
        
        # Combine extracted info
        max_entries = max(len(orgs), len(titles), len(date_ranges))
        
        for i in range(min(max_entries, 5)):  # Limit to 5 entries
            experience = {
                "title": titles[i] if i < len(titles) else "Position",
                "company": orgs[i] if i < len(orgs) else "Company",
                "duration": f"{date_ranges[i][0]} - {date_ranges[i][1]}" if i < len(date_ranges) else None
            }
            experiences.append(experience)
        
        return experiences
    
    def extract_education_entries(self, text: str) -> List[Dict]:
        """
        Extract education entries with better structure.
        
        Args:
            text: Resume text
            
        Returns:
            List of education entries
        """
        education = []
        
        # Look for education section
        education_section = self._extract_section(text, [
            "education", "academic", "qualification", "university", "college"
        ])
        
        if not education_section:
            return education
        
        # Extract degrees
        degree_patterns = [
            r"(Bachelor(?:'s)?|B\.?Tech|B\.?E\.?|B\.?Sc\.?|B\.?A\.?)",
            r"(Master(?:'s)?|M\.?Tech|M\.?E\.?|M\.?Sc\.?|M\.?A\.?|MBA)",
            r"(Ph\.?D\.?|Doctorate)",
        ]
        
        degrees = []
        for pattern in degree_patterns:
            matches = re.findall(pattern, education_section, re.IGNORECASE)
            degrees.extend([m if isinstance(m, str) else m[0] for m in matches])
        
        # Extract institutions (organizations in education section)
        institutions = self.extract_organizations(education_section)
        
        # Extract years
        years = re.findall(r'\b(19|20)\d{2}\b', education_section)
        
        # Combine
        max_entries = max(len(degrees), len(institutions))
        
        for i in range(min(max_entries, 3)):  # Limit to 3 entries
            edu = {
                "degree": degrees[i] if i < len(degrees) else "Degree",
                "institution": institutions[i] if i < len(institutions) else "Institution",
                "year": years[i] if i < len(years) else None
            }
            education.append(edu)
        
        return education
    
    def extract_projects(self, text: str) -> List[Dict]:
        """
        Extract project information from resume.
        
        Args:
            text: Resume text
            
        Returns:
            List of projects
        """
        projects = []
        
        # Look for projects section
        project_section = self._extract_section(text, [
            "projects", "personal projects", "portfolio", "work samples"
        ])
        
        if not project_section:
            return projects
        
        # Split by common delimiters
        lines = project_section.split('\n')
        
        current_project = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line looks like a project title (short, starts with capital or bullet)
            if (len(line) < 100 and 
                (line[0].isupper() or line.startswith('•') or line.startswith('-'))):
                
                if current_project:
                    projects.append(current_project)
                
                current_project = {
                    "title": line.lstrip('•-').strip(),
                    "description": ""
                }
            elif current_project:
                # Add to description
                current_project["description"] += " " + line
        
        if current_project:
            projects.append(current_project)
        
        return projects[:5]  # Limit to 5 projects
    
    def _extract_section(self, text: str, section_headers: List[str]) -> str:
        """
        Extract a specific section from resume text.
        
        Args:
            text: Full resume text
            section_headers: List of possible section header names
            
        Returns:
            Extracted section text
        """
        text_lower = text.lower()
        
        for header in section_headers:
            # Look for section header
            pattern = r'\n\s*' + re.escape(header) + r'\s*\n'
            matches = list(re.finditer(pattern, text_lower))
            
            if matches:
                start = matches[0].end()
                
                # Find next section (next all-caps line or double newline)
                next_section = re.search(r'\n\s*[A-Z\s]{3,}\s*\n', text[start:])
                
                if next_section:
                    end = start + next_section.start()
                else:
                    end = min(start + 1000, len(text))  # Take next 1000 chars
                
                return text[start:end]
        
        return ""
    
    def get_text_chunks(self, text: str, chunk_size: int = 200) -> List[str]:
        """
        Split text into chunks for better processing.
        
        Args:
            text: Text to split
            chunk_size: Number of characters per chunk
            
        Returns:
            List of text chunks
        """
        if self.nlp:
            doc = self.nlp(text)
            
            # Split by sentences for better context
            chunks = []
            current_chunk = ""
            
            for sent in doc.sents:
                if len(current_chunk) + len(sent.text) > chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = sent.text
                else:
                    current_chunk += " " + sent.text
            
            if current_chunk:
                chunks.append(current_chunk)
            
            return chunks
        else:
            # Fallback: simple character-based chunking
            return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
