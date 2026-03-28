"""
Test script for resume_parser.py module

This script tests the resume parser functionality with sample data
and demonstrates how to use the module.
"""

import os
import tempfile
from resume_parser import extract_resume_text, clean_resume_text, validate_pdf_file, extract_resume_fields


def create_sample_pdf():
    """Create a sample PDF file for testing purposes."""
    try:
        from fpdf import FPDF
        
        # Create a simple PDF with sample resume content
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        sample_content = """
        John Doe
        Software Engineer
        Email: john.doe@example.com | Phone: (555) 123-4567
        
        PROFESSIONAL SUMMARY
        Experienced software engineer with 5 years of experience in web development
        and cloud technologies. Skilled in Python, JavaScript, and modern frameworks.
        
        TECHNICAL SKILLS
        Programming Languages: Python, JavaScript, Java
        Frameworks: Django, React, Node.js
        Databases: PostgreSQL, MongoDB, MySQL
        Tools: Git, Docker, AWS
        
        EXPERIENCE
        Senior Software Engineer
        Tech Corp, San Francisco, CA
        January 2020 - Present
        
        - Developed and maintained web applications using Python and Django
        - Collaborated with cross-functional teams to deliver high-quality software
        - Implemented RESTful APIs and database schemas
        
        EDUCATION
        Bachelor of Science in Computer Science
        University of California, Berkeley
        Graduated: May 2018
        """
        
        # Write content to PDF
        for line in sample_content.split('\n'):
            if line.strip():
                pdf.cell(0, 10, txt=line.strip(), ln=True)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        pdf.output(temp_file.name)
        return temp_file.name
        
    except ImportError:
        print("Warning: fpdf not available. Cannot create sample PDF for testing.")
        return None


def test_resume_parser():
    """Test the resume parser functionality."""
    print("Testing Resume Parser Module")
    print("=" * 40)
    
    # Test 1: Test with a sample PDF (if fpdf is available)
    sample_pdf_path = create_sample_pdf()
    
    if sample_pdf_path:
        print("Test 1: Extracting text from sample PDF")
        try:
            extracted_text = extract_resume_text(sample_pdf_path)
            if extracted_text:
                print("✓ Successfully extracted text from PDF")
                print(f"Extracted text length: {len(extracted_text)} characters")
                print("First 200 characters:")
                print(extracted_text[:200] + "...")
            else:
                print("✗ Failed to extract text from PDF")
        except Exception as e:
            print(f"✗ Error during PDF extraction: {e}")
        finally:
            # Clean up temporary file
            if os.path.exists(sample_pdf_path):
                os.unlink(sample_pdf_path)
    else:
        print("Skipping PDF test (fpdf not available)")
    
    print()
    
    # Test 2: Test text cleaning functionality
    print("Test 2: Testing text cleaning functionality")
    dirty_text = """
    John Doe
    
    Software Engineer
    
    
    Email: john.doe@example.com
    
    Phone: (555) 123-4567
    
    
    """
    
    cleaned_text = clean_resume_text(dirty_text)
    print(f"Original text length: {len(dirty_text)}")
    print(f"Cleaned text length: {len(cleaned_text)}")
    print("Cleaned text:")
    print(repr(cleaned_text))
    
    # Verify cleaning worked
    if '\n\n\n' not in cleaned_text and '  ' not in cleaned_text.strip():
        print("✓ Text cleaning successful")
    else:
        print("✗ Text cleaning may have issues")
    
    print()
    
    # Test 3: Test file validation
    print("Test 3: Testing file validation")
    
    # Test with non-existent file
    result = validate_pdf_file("nonexistent.pdf")
    print(f"Non-existent file validation: {result} (should be False)")
    
    # Test with invalid extension
    result = validate_pdf_file("test.txt")
    print(f"Invalid extension validation: {result} (should be False)")
    
    # Test with sample PDF if available
    if sample_pdf_path and os.path.exists(sample_pdf_path):
        result = validate_pdf_file(sample_pdf_path)
        print(f"Valid PDF validation: {result} (should be True)")
    
    print()
    
    # Test 4: Test structured field extraction
    print("Test 4: Testing structured field extraction")
    print("-" * 40)
    
    # Sample cleaned resume text for testing
    sample_resume_text = """
    John Smith
    Senior Software Developer
    Email: john.smith@techcompany.com
    Phone: +91-9876543210
    
    SUMMARY
    Experienced developer with expertise in Python, JavaScript, and cloud technologies.
    5 years of experience in web application development and system architecture.
    
    TECHNICAL SKILLS
    Programming Languages: Python, JavaScript, Java, C++
    Frameworks: Django, React, Node.js, Spring Boot
    Databases: PostgreSQL, MongoDB, MySQL
    Tools: Git, Docker, AWS, Kubernetes
    
    EXPERIENCE
    Senior Software Engineer
    Tech Solutions Inc., Mumbai
    March 2019 - Present
    
    - Led development of scalable web applications using Python and Django
    - Implemented RESTful APIs and microservices architecture
    - Mentored junior developers and conducted code reviews
    
    EDUCATION
    Bachelor of Technology in Computer Science
    Indian Institute of Technology, Bombay
    Graduated: June 2018
    """
    
    # Clean the sample text
    cleaned_sample = clean_resume_text(sample_resume_text)
    
    # Extract structured fields
    extracted_fields = extract_resume_fields(cleaned_sample)
    
    print("Extracted Fields:")
    print("-" * 20)
    for key, value in extracted_fields.items():
        if isinstance(value, list):
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value}")
    
    # Verify extraction results
    print("\nVerification:")
    print("-" * 12)
    
    # Check name extraction
    if extracted_fields.get("name") and "John Smith" in extracted_fields["name"]:
        print("✓ Name extraction successful")
    else:
        print("✗ Name extraction failed")
    
    # Check email extraction
    if extracted_fields.get("email") == "john.smith@techcompany.com":
        print("✓ Email extraction successful")
    else:
        print("✗ Email extraction failed")
    
    # Check phone extraction
    if extracted_fields.get("phone") and "+91" in extracted_fields["phone"]:
        print("✓ Phone extraction successful")
    else:
        print("✗ Phone extraction failed")
    
    # Check role extraction
    if extracted_fields.get("role") and "software" in extracted_fields["role"].lower():
        print("✓ Role extraction successful")
    else:
        print("✗ Role extraction failed")
    
    # Check skills extraction
    skills = extracted_fields.get("skills", [])
    expected_skills = ["Python", "JavaScript", "Django", "React"]
    found_skills = [skill for skill in skills if skill in expected_skills]
    if found_skills:
        print(f"✓ Skills extraction successful: {found_skills}")
    else:
        print("✗ Skills extraction failed")
    
    # Check education extraction
    education = extracted_fields.get("education")
    if education and ("b.tech" in education.lower() or "bachelor" in education.lower() or "bsc" in education.lower() or "ba" in education.lower()):
        print("✓ Education extraction successful")
    else:
        print("✗ Education extraction failed")
    
    # Check experience extraction
    if extracted_fields.get("experience") and "5" in extracted_fields["experience"]:
        print("✓ Experience extraction successful")
    else:
        print("✗ Experience extraction failed")
    
    print()
    print("Testing completed!")


if __name__ == "__main__":
    test_resume_parser()