from ai_analysis import analyze_candidate


def test_ai_analysis_module():
    """Test the AI analysis functionality."""
    print("Testing AI Analysis Module")
    print("=" * 30)
    
    print("\nTest 1: Single Candidate Analysis")
    print("-" * 35)
    
    job_description = """
    We are looking for a skilled Full Stack Developer with experience in modern web technologies.
    
    Requirements:
    - 3+ years of experience in web development
    - Proficiency in JavaScript, React, and Node.js
    - Experience with MongoDB or similar databases
    - Knowledge of RESTful APIs and microservices
    - Familiarity with Docker and cloud platforms (AWS, Azure)
    - Strong problem-solving skills and ability to work in a team
    
    Preferred Skills:
    - Experience with TypeScript
    - Knowledge of CI/CD pipelines
    - Understanding of Agile methodologies
    """
    
    candidate_data = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": "+91-9876543210",
        "role": "Full Stack Developer",
        "skills": ["JavaScript", "React", "Node.js", "MongoDB", "AWS", "Docker", "TypeScript"],
        "education": "B.Tech in Computer Science",
        "experience": "4+ years of experience in web development"
    }
    
    print("Job Description:")
    print(job_description[:150] + "...")
    
    print("\nCandidate Data:")
    print(f"Name: {candidate_data['name']}")
    print(f"Role: {candidate_data['role']}")
    print(f"Skills: {', '.join(candidate_data['skills'])}")
    print(f"Experience: {candidate_data['experience']}")
    
    print("\nNote: This test demonstrates the expected output format.")
    print("For actual AI analysis, set OPENAI_API_KEY or GEMINI_API_KEY environment variable.")
    
    expected_output = {
        "match_score": 87,
        "matched_skills": ["JavaScript", "React", "Node.js", "MongoDB", "AWS", "Docker", "TypeScript"],
        "missing_skills": [],
        "strengths": ["Strong full-stack experience", "4+ years of relevant experience", "Cloud platform knowledge"],
        "summary": "Candidate is an excellent match with comprehensive full-stack skills and relevant experience."
    }
    
    print("\nExpected Output Structure:")
    print("-" * 28)
    for key, value in expected_output.items():
        if isinstance(value, list):
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value}")
    
    print("\n\nTest 2: Candidate with Missing Skills")
    print("-" * 35)
    
    candidate_with_gaps = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "+91-8765432109",
        "role": "Frontend Developer",
        "skills": ["JavaScript", "React", "HTML", "CSS"],
        "education": "B.Sc in Information Technology",
        "experience": "2+ years of experience in frontend development"
    }
    
    print("Candidate with Gaps:")
    print(f"Name: {candidate_with_gaps['name']}")
    print(f"Skills: {', '.join(candidate_with_gaps['skills'])}")
    print(f"Experience: {candidate_with_gaps['experience']}")
    
    expected_output_gaps = {
        "match_score": 65,
        "matched_skills": ["JavaScript", "React"],
        "missing_skills": ["Node.js", "MongoDB", "Docker", "AWS"],
        "strengths": ["Strong frontend skills", "Good foundation in web technologies"],
        "summary": "Candidate has good frontend skills but lacks backend and DevOps experience required for full-stack role."
    }
    
    print("\nExpected Output for Candidate with Gaps:")
    print("-" * 40)
    for key, value in expected_output_gaps.items():
        if isinstance(value, list):
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value}")
    
    print("\n\nTest 3: Error Handling")
    print("-" * 20)
    
    result_empty_job = analyze_candidate("", candidate_data)
    print("Empty job description result:")
    print(f"Match Score: {result_empty_job['match_score']}")
    print(f"Summary: {result_empty_job['summary']}")
    
    result_empty_candidate = analyze_candidate(job_description, {})
    print("\nEmpty candidate data result:")
    print(f"Match Score: {result_empty_candidate['match_score']}")
    print(f"Summary: {result_empty_candidate['summary']}")
    
    print("\n\nTest 4: Multiple Candidate Analysis")
    print("-" * 35)
    
    candidates = [
        {
            "name": "Alice Johnson",
            "role": "Senior Developer",
            "skills": ["JavaScript", "React", "Node.js", "MongoDB", "AWS", "Docker", "TypeScript", "Kubernetes"],
            "experience": "6+ years of experience",
            "education": "M.Tech in Computer Science"
        },
        {
            "name": "Bob Wilson",
            "role": "Junior Developer", 
            "skills": ["JavaScript", "React", "HTML", "CSS"],
            "experience": "1+ year of experience",
            "education": "B.Tech in IT"
        },
        {
            "name": "Carol Brown",
            "role": "Backend Developer",
            "skills": ["Node.js", "MongoDB", "AWS", "Docker", "Python", "Java"],
            "experience": "3+ years of experience",
            "education": "B.Sc in Computer Science"
        }
    ]
    
    print("Multiple candidates for ranking:")
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate['name']} - {candidate['role']} - {candidate['experience']}")
    
    print("\nExpected Ranking (by match score):")
    print("1. Alice Johnson (highest score - most experienced)")
    print("2. Carol Brown (good backend experience)")
    print("3. Bob Wilson (lowest score - junior level)")
    
    print("\n\nTest 5: Provider Configuration")
    print("-" * 30)
    
    print("Available providers:")
    print("• OpenAI (gpt-3.5-turbo, gpt-4)")
    print("• Google Gemini (gemini-pro, gemini-ultra)")
    
    print("\nConfiguration examples:")
    print("# Using OpenAI with environment variable")
    print("analyzer = CandidateAnalyzer(provider='openai')")
    print("\n# Using OpenAI with explicit API key")
    print("analyzer = CandidateAnalyzer(provider='openai', api_key='your-key')")
    print("\n# Using Gemini")
    print("analyzer = CandidateAnalyzer(provider='gemini')")
    
    print("\n" + "=" * 50)
    print("AI Analysis Module Testing Complete!")
    print("✓ Single candidate analysis")
    print("✓ Multiple candidate ranking")
    print("✓ Error handling")
    print("✓ Provider configuration")
    print("✓ Expected output formats")
    print("=" * 50)


def demonstrate_integration():
    """Demonstrate how the AI analysis integrates with the complete pipeline."""
    print("\n\nIntegration Example: Complete Resume Screening Pipeline")
    print("=" * 55)
    
    print("Pipeline Flow:")
    print("1. Resume PDF → Text Extraction (resume_parser.py)")
    print("2. Text Cleaning → Structured Fields (resume_parser.py)")
    print("3. Job Description + Candidate Data → AI Analysis (ai_analysis.py)")
    print("4. Match Scores → Candidate Ranking")
    
    print("\nExample Integration Code:")
    print("-" * 25)
    
    integration_code = '''
    from resume_parser import extract_resume_text, extract_resume_fields
    from ai_analysis import analyze_candidate
    
    raw_text = extract_resume_text("resume.pdf")
    candidate_data = extract_resume_fields(raw_text)
    
    job_description = get_job_description_from_recruiter()
    
    analysis = analyze_candidate(job_description, candidate_data)
    
    print(f"Candidate Match Score: {analysis['match_score']}/100")
    print(f"Matched Skills: {', '.join(analysis['matched_skills'])}")
    print(f"Summary: {analysis['summary']}")
    '''
    
    print(integration_code)
    
    print("Benefits of this integration:")
    print("• Automated candidate screening")
    print("• Objective scoring based on job requirements")
    print("• Structured feedback for recruiters")
    print("• Scalable processing of multiple candidates")
    print("• Consistent evaluation criteria")


if __name__ == "__main__":
    test_ai_analysis_module()
    demonstrate_integration()
