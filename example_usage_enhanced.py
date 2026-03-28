"""
Enhanced Example Usage of the Resume Parser Module

This script demonstrates the complete pipeline from PDF parsing to structured field extraction
for a Resume Screening AI project.
"""

from resume_parser import extract_resume_text, clean_resume_text, validate_pdf_file, extract_resume_fields


def main():
    """Demonstrate the complete resume parsing pipeline."""
    
    print("Enhanced Resume Parser Example Usage")
    print("=" * 40)
    
    # Example 1: Complete pipeline demonstration
    print("\n1. Complete Pipeline Example:")
    print("-" * 30)
    
    # Sample resume text (simulating what would come from extract_resume_text)
    sample_resume_content = """
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
    
    # Step 1: Clean the resume text
    cleaned_text = clean_resume_text(sample_resume_content)
    print("✓ Step 1: Text cleaning completed")
    
    # Step 2: Extract structured fields
    extracted_fields = extract_resume_fields(cleaned_text)
    print("✓ Step 2: Structured field extraction completed")
    
    # Display the complete results
    print("\nComplete Extraction Results:")
    print("=" * 35)
    for key, value in extracted_fields.items():
        if isinstance(value, list):
            print(f"{key.title()}: {', '.join(value) if value else 'Not found'}")
        else:
            print(f"{key.title()}: {value if value else 'Not found'}")
    
    # Example 2: Integration with AI analysis workflow
    print("\n2. AI Analysis Integration:")
    print("-" * 30)
    
    print("The extracted structured data can now be used for:")
    print("• Skill-based candidate matching")
    print("• Experience level filtering")
    print("• Education verification")
    print("• Automated resume scoring")
    print("• Job description compatibility analysis")
    
    # Example of how this would integrate with an AI model
    if extracted_fields.get("skills"):
        skills_string = ", ".join(extracted_fields["skills"])
        print(f"\nExample: Sending skills '{skills_string}' to AI matching algorithm...")
        # In a real implementation:
        # match_score = ai_model.match_skills(extracted_fields["skills"], job_requirements)
        # print(f"Match Score: {match_score}")
    
    # Example 3: Error handling demonstration
    print("\n3. Error Handling Examples:")
    print("-" * 28)
    
    # Test with empty text
    empty_fields = extract_resume_fields("")
    print("Empty text handling:", empty_fields)
    
    # Test with minimal text
    minimal_text = "Jane Doe\nEmail: jane@example.com"
    minimal_fields = extract_resume_fields(minimal_text)
    print("Minimal text extraction:", minimal_fields)


def process_complete_resume_pipeline(pdf_file_path: str):
    """
    Complete pipeline function for processing uploaded resume files.
    
    Args:
        pdf_file_path (str): Path to the uploaded PDF resume file
        
    Returns:
        dict: Complete processing result with both raw text and structured fields
    """
    result = {
        'success': False,
        'raw_text': None,
        'cleaned_text': None,
        'structured_fields': None,
        'error': None,
        'metadata': {}
    }
    
    try:
        # Step 1: Validate the uploaded file
        if not validate_pdf_file(pdf_file_path):
            result['error'] = "Invalid PDF file or file not found"
            return result
        
        # Step 2: Extract raw text from the PDF
        raw_text = extract_resume_text(pdf_file_path)
        
        if not raw_text:
            result['error'] = "Could not extract text from the resume"
            return result
        
        # Step 3: Clean the extracted text
        cleaned_text = clean_resume_text(raw_text)
        
        # Step 4: Extract structured fields
        structured_fields = extract_resume_fields(cleaned_text)
        
        # Step 5: Calculate metadata
        word_count = len(cleaned_text.split()) if cleaned_text else 0
        char_count = len(cleaned_text) if cleaned_text else 0
        skill_count = len(structured_fields.get('skills', []))
        
        result.update({
            'success': True,
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'structured_fields': structured_fields,
            'metadata': {
                'word_count': word_count,
                'character_count': char_count,
                'skill_count': skill_count,
                'file_path': pdf_file_path
            }
        })
        
        return result
        
    except Exception as e:
        result['error'] = f"Error processing resume: {str(e)}"
        return result


def demonstrate_pipeline_integration():
    """
    Demonstrate how the resume parser integrates into a larger AI screening system.
    """
    print("\n4. Pipeline Integration Example:")
    print("-" * 35)
    
    # Simulate processing multiple resumes
    sample_resumes = [
        {
            'name': 'John Smith',
            'content': """
            John Smith
            Software Engineer
            Email: john.smith@company.com
            Phone: +91-9876543210
            Skills: Python, Django, React, AWS
            Experience: 3 years in web development
            Education: B.Tech Computer Science
            """
        },
        {
            'name': 'Jane Doe',
            'content': """
            Jane Doe
            Data Scientist
            Email: jane.doe@analytics.com
            Phone: +91-8765432109
            Skills: Python, Machine Learning, SQL, TensorFlow
            Experience: 4 years in data analysis
            Education: M.Sc Data Science
            """
        }
    ]
    
    candidates = []
    
    for resume_data in sample_resumes:
        # Process each resume
        cleaned_text = clean_resume_text(resume_data['content'])
        fields = extract_resume_fields(cleaned_text)
        
        # Create candidate profile
        candidate = {
            'name': fields.get('name', 'Unknown'),
            'email': fields.get('email'),
            'role': fields.get('role', 'Unknown'),
            'skills': fields.get('skills', []),
            'experience': fields.get('experience'),
            'education': fields.get('education')
        }
        
        candidates.append(candidate)
    
    # Display processed candidates
    print("Processed Candidate Profiles:")
    print("-" * 32)
    for i, candidate in enumerate(candidates, 1):
        print(f"\nCandidate {i}: {candidate['name']}")
        print(f"  Role: {candidate['role']}")
        print(f"  Skills: {', '.join(candidate['skills'])}")
        print(f"  Experience: {candidate['experience']}")
        print(f"  Education: {candidate['education']}")
    
    # Example of AI-based filtering
    print(f"\nExample: Filtering candidates with Python skills...")
    python_candidates = [c for c in candidates if 'Python' in c['skills']]
    print(f"Found {len(python_candidates)} candidates with Python skills:")
    for candidate in python_candidates:
        print(f"  - {candidate['name']}")


if __name__ == "__main__":
    main()
    demonstrate_pipeline_integration()
    
    print("\n" + "=" * 60)
    print("Enhanced Resume Parser Pipeline Ready!")
    print("✓ PDF text extraction")
    print("✓ Text cleaning and normalization") 
    print("✓ Structured field extraction")
    print("✓ Ready for AI analysis integration")
    print("=" * 60)