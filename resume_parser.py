"""
Resume Parser Module for Resume Screening AI Project

This module provides functionality to extract text content from uploaded resume files
in PDF format. The extracted text can then be analyzed by an AI model for various
purposes such as skill extraction, candidate analysis, and job description matching.
"""

import os
import re
from typing import Optional, Dict, List
import pdfplumber


def extract_resume_text(file_path: str) -> Optional[str]:
    """
    Extract text content from a PDF resume file.
    
    Args:
        file_path (str): Path to the PDF file to be processed
        
    Returns:
        Optional[str]: Cleaned text content from the resume, or None if extraction fails
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not a PDF
    """
    # Validate file path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Validate file extension
    if not file_path.lower().endswith('.pdf'):
        raise ValueError(f"Unsupported file format. Please provide a PDF file: {file_path}")
    
    try:
        # Open the PDF file using pdfplumber
        with pdfplumber.open(file_path) as pdf:
            extracted_text = []
            
            # Extract text from all pages
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    # Extract text from current page
                    page_text = page.extract_text()
                    
                    if page_text:
                        extracted_text.append(page_text)
                        
                except Exception as page_error:
                    print(f"Warning: Could not extract text from page {page_num}: {page_error}")
                    continue
            
            # Combine all page text into a single string
            full_text = '\n'.join(extracted_text)
            
            # Clean the extracted text
            cleaned_text = clean_resume_text(full_text)
            
            return cleaned_text if cleaned_text else None
            
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None


def clean_resume_text(text: str) -> str:
    """
    Clean and normalize extracted resume text.
    
    Args:
        text (str): Raw text extracted from PDF
        
    Returns:
        str: Cleaned and normalized text suitable for AI analysis
    """
    if not text:
        return ""
    
    # Remove excessive whitespace and normalize line breaks
    cleaned = re.sub(r'\n\s*\n', '\n\n', text)  # Replace multiple newlines with double newlines
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)   # Replace multiple spaces/tabs with single space
    
    # Remove leading/trailing whitespace from each line
    cleaned = '\n'.join(line.strip() for line in cleaned.split('\n'))
    
    # Remove excessive consecutive empty lines (more than 2)
    cleaned = re.sub(r'\n\n\n+', '\n\n', cleaned)
    
    # Remove any non-printable characters except standard whitespace
    cleaned = re.sub(r'[^\x20-\x7E\n\r\t]', '', cleaned)
    
    # Strip leading and trailing whitespace from the entire text
    cleaned = cleaned.strip()
    
    return cleaned


def validate_pdf_file(file_path: str) -> bool:
    """
    Validate if a file is a readable PDF.
    
    Args:
        file_path (str): Path to the file to validate
        
    Returns:
        bool: True if the file is a valid PDF, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            return False
        
        if not file_path.lower().endswith('.pdf'):
            return False
        
        # Try to open the PDF to verify it's valid
        with pdfplumber.open(file_path) as pdf:
            # Check if we can access basic properties
            _ = len(pdf.pages)
            
        return True
        
    except Exception:
        return False


def extract_resume_fields(resume_text: str) -> Dict[str, Optional[str]]:
    """
    Extract structured information from cleaned resume text.
    
    Args:
        resume_text (str): Cleaned resume text from extract_resume_text()
        
    Returns:
        Dict[str, Optional[str]]: Dictionary containing extracted resume fields
    """
    if not resume_text:
        return {
            "name": None,
            "email": None,
            "phone": None,
            "role": None,
            "skills": [],
            "education": None,
            "experience": None
        }
    
    # Convert to lowercase for case-insensitive matching
    text_lower = resume_text.lower()
    
    # Extract email using regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, resume_text)
    email = emails[0] if emails else None
    
    # Extract phone number using regex (Indian format and international)
    phone_patterns = [
        r'\+91[-\s]?\d{5}[-\s]?\d{5}',  # Indian format: +91 98765 43210 or +91-98765-43210
        r'\+?\d{1,3}[-\s]?\d{10}',      # International format
        r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b',  # US format variations
        r'\b\d{10}\b'                   # Simple 10-digit number
    ]
    
    phone = None
    for pattern in phone_patterns:
        phones = re.findall(pattern, resume_text)
        if phones:
            phone = phones[0]
            break
    
    # Extract name (usually at the beginning, first 2-3 capitalized words)
    name = extract_name(resume_text)
    
    # Extract role/job title
    role = extract_role(text_lower)
    
    # Extract skills
    skills = extract_skills(text_lower)
    
    # Extract education
    education = extract_education(text_lower)
    
    # Extract experience
    experience = extract_experience(text_lower)
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "role": role,
        "skills": skills,
        "education": education,
        "experience": experience
    }


def extract_name(resume_text: str) -> Optional[str]:
    """
    Extract name from resume text (usually appears at the beginning).
    
    Args:
        resume_text (str): Cleaned resume text
        
    Returns:
        Optional[str]: Extracted name or None
    """
    lines = resume_text.split('\n')
    
    # Look for name in first few lines
    for i, line in enumerate(lines[:5]):
        # Skip empty lines and common headers
        if not line.strip() or any(keyword in line.lower() for keyword in 
                                   ['email', 'phone', 'address', 'linkedin', 'github']):
            continue
            
        # Look for lines with 2-4 capitalized words (likely a name)
        words = line.strip().split()
        if 2 <= len(words) <= 4:
            # Check if most words are capitalized (indicating a name)
            capitalized_words = sum(1 for word in words if word and word[0].isupper())
            if capitalized_words >= len(words) * 0.7:  # At least 70% of words should be capitalized
                return line.strip()
    
    return None


def extract_role(text_lower: str) -> Optional[str]:
    """
    Extract job role/title from resume text.
    
    Args:
        text_lower (str): Lowercase resume text
        
    Returns:
        Optional[str]: Extracted role or None
    """
    # Look for common job titles in the text
    common_titles = [
        'software engineer', 'software developer', 'frontend developer', 'backend developer',
        'full stack developer', 'data scientist', 'data analyst', 'machine learning engineer',
        'devops engineer', 'system administrator', 'network engineer', 'security analyst',
        'project manager', 'product manager', 'business analyst', 'qa engineer',
        'ui/ux designer', 'graphic designer', 'web developer'
    ]
    
    for title in common_titles:
        if title in text_lower:
            return title.title()
    
    # Look for role indicators followed by text
    role_patterns = [
        r'summary\s*:?\s*([a-zA-Z\s]+)',
        r'objective\s*:?\s*([a-zA-Z\s]+)',
        r'profile\s*:?\s*([a-zA-Z\s]+)',
        r'title\s*:?\s*([a-zA-Z\s]+)',
        r'position\s*:?\s*([a-zA-Z\s]+)',
        r'role\s*:?\s*([a-zA-Z\s]+)'
    ]
    
    for pattern in role_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            role = matches[0].strip()
            if role and len(role) > 2:
                return role
    
    return None


def extract_skills(text_lower: str) -> List[str]:
    """
    Extract skills from resume text.
    
    Args:
        text_lower (str): Lowercase resume text
        
    Returns:
        List[str]: List of extracted skills
    """
    skill_aliases = {
        "JavaScript": ["javascript", " js "],
        "TypeScript": ["typescript", " ts "],
        "Node.js": ["node.js", "nodejs", " node "],
        "React": ["react", "reactjs", "react.js"],
        "MongoDB": ["mongodb", "mongo db"],
        "Express": ["express", "expressjs", "express.js"],
        "PostgreSQL": ["postgresql", "postgres"],
        "MySQL": ["mysql"],
        "Python": ["python"],
        "Java": ["java"],
        "C#": ["c#", "csharp"],
        "C++": ["c++"],
        "HTML": ["html"],
        "CSS": ["css"],
        "Django": ["django"],
        "Flask": ["flask"],
        "FastAPI": ["fastapi"],
        "Angular": ["angular"],
        "Vue": ["vue", "vue.js"],
        "Docker": ["docker"],
        "Kubernetes": ["kubernetes", "k8s"],
        "AWS": ["aws", "amazon web services"],
        "Azure": ["azure"],
        "GCP": ["gcp", "google cloud"],
        "Git": ["git"],
        "Jenkins": ["jenkins"],
        "Terraform": ["terraform"],
        "Linux": ["linux"],
        "Redis": ["redis"],
        "SQL": ["sql"],
        "NoSQL": ["nosql"],
    }

    padded_text = f" {text_lower} "
    extracted: List[str] = []
    seen = set()

    for canonical, aliases in skill_aliases.items():
        for alias in aliases:
            if alias in padded_text:
                key = canonical.lower()
                if key not in seen:
                    extracted.append(canonical)
                    seen.add(key)
                break

    return extracted


def extract_education(text_lower: str) -> Optional[str]:
    """
    Extract education information from resume text.
    
    Args:
        text_lower (str): Lowercase resume text
        
    Returns:
        Optional[str]: Extracted education information or None
    """
    # Look for education section
    education_keywords = ['education', 'academic background', 'qualifications']
    
    for keyword in education_keywords:
        if keyword in text_lower:
            # Find the education section
            pattern = rf'{keyword}.*?(?=\n\n|\n[A-Z][a-z]+\s*:|\Z)'
            matches = re.findall(pattern, text_lower, re.DOTALL)
            if matches:
                education_text = matches[0].strip()
                # Extract degree information
                degree_pattern = r'(b\.?tech|b\.?sc|b\.?com|b\.?a|m\.?tech|m\.?sc|m\.?com|m\.?a|ph\.?d|mba|ms|bs)'
                degrees = re.findall(degree_pattern, education_text, re.IGNORECASE)
                if degrees:
                    return f"{degrees[0].upper()} in {extract_degree_major(education_text)}"
    
    # Look for degree patterns in the entire text
    degree_patterns = [
        r'(b\.?tech|b\.?sc|b\.?com|b\.?a|m\.?tech|m\.?sc|m\.?com|m\.?a|ph\.?d|mba|ms|bs)',
        r'(bachelor|master|phd|mba)\s+(of\s+)?(science|technology|arts|commerce|engineering)',
        r'(bsc|btech|bcom|ba|msc|mtech|mcom|ma|phd|mba)'
    ]
    
    for pattern in degree_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            degree = matches[0][0] if isinstance(matches[0], tuple) else matches[0]
            return f"{degree.upper()} in {extract_degree_major(text_lower)}"
    
    # Look for specific degree mentions in education section
    education_section_pattern = r'education.*?(?=\n\n|\Z)'
    education_matches = re.findall(education_section_pattern, text_lower, re.DOTALL | re.IGNORECASE)
    if education_matches:
        education_text = education_matches[0]
        # Look for specific degree patterns in education section
        specific_degree_patterns = [
            r'bachelor.*?technology.*?computer.*?science',
            r'b\.?tech.*?computer.*?science',
            r'bsc.*?computer.*?science'
        ]
        for pattern in specific_degree_patterns:
            if re.search(pattern, education_text, re.IGNORECASE):
                return f"B.TECH in {extract_degree_major(education_text)}"
    
    return None


def extract_degree_major(text_lower: str) -> str:
    """
    Extract the major/field of study from education text.
    
    Args:
        text_lower (str): Lowercase text to search
        
    Returns:
        str: Extracted major or "Computer Science" as default
    """
    # Common majors
    majors = [
        'computer science', 'information technology', 'software engineering', 'electrical engineering',
        'mechanical engineering', 'civil engineering', 'chemical engineering', 'data science',
        'business administration', 'finance', 'marketing', 'mathematics', 'physics'
    ]
    
    for major in majors:
        if major in text_lower:
            return major.title()
    
    return "Computer Science"


def extract_experience(text_lower: str) -> Optional[str]:
    """
    Extract experience information from resume text.
    
    Args:
        text_lower (str): Lowercase resume text
        
    Returns:
        Optional[str]: Extracted experience information or None
    """
    # Look for experience section
    experience_keywords = ['experience', 'work experience', 'professional experience', 'employment history']
    
    for keyword in experience_keywords:
        if keyword in text_lower:
            # Find the experience section
            pattern = rf'{keyword}.*?(?=\n\n|\n[A-Z][a-z]+\s*:|\Z)'
            matches = re.findall(pattern, text_lower, re.DOTALL)
            if matches:
                experience_text = matches[0].strip()
                # Extract years of experience
                year_pattern = r'(\d+)\s*(years?|yrs?)\s*(of\s*)?(experience|exp)'
                year_matches = re.findall(year_pattern, experience_text, re.IGNORECASE)
                if year_matches:
                    years = year_matches[0][0]
                    return f"{years}+ years of experience"
    
    # Look for experience patterns in the entire text
    exp_patterns = [
        r'(\d+)\s*(years?|yrs?)\s*(of\s*)?(experience|exp)',
        r'experience\s*:\s*(\d+)\s*years?',
        r'(\d+)\s*years?\s*in\s*[a-zA-Z\s]+'
    ]
    
    for pattern in exp_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            if len(matches[0]) > 0 and matches[0][0].isdigit():
                years = matches[0][0]
                return f"{years}+ years of experience"
    
    return None


if __name__ == "__main__":
    # Example usage
    # This section can be used for testing the module
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result = extract_resume_text(file_path)
        
        if result:
            print("Resume text extracted successfully:")
            print("=" * 50)
            print(result[:1000] + ("..." if len(result) > 1000 else ""))
        else:
            print("Failed to extract text from the resume.")
    else:
        print("Usage: python resume_parser.py <path_to_pdf_file>")