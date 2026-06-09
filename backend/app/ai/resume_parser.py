"""Resume parser — extracts text and structured data from PDF/DOCX resumes."""


class ResumeParser:
    """Pipeline: PDF → text extraction → cleaning → structured output."""

    def parse_pdf(self, file_path: str) -> dict:
        """Extract text from PDF using PyMuPDF, then structure it."""
        raise NotImplementedError("To be implemented in Phase 3")

    def clean_text(self, raw_text: str) -> str:
        """Clean extracted text — remove noise, normalize whitespace."""
        raise NotImplementedError("To be implemented in Phase 3")

    def extract_sections(self, text: str) -> dict:
        """Split resume text into sections: education, experience, projects, skills."""
        raise NotImplementedError("To be implemented in Phase 3")
