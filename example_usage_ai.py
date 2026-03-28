"""
Clean example usage: Resume parsing + AI analysis with exact output format.
"""

from resume_parser import extract_resume_fields, clean_resume_text
from ai_analysis import analyze_candidate

def main():
    # Sample resume text (replace with extract_resume_text(pdf_path) for real PDF)
    sample_resume = """
Alice Johnson
Senior Full Stack Developer
Email: alice.johnson@email.com
Phone: +91-9876543210

SUMMARY
5+ years full-stack development experience. Proficient in modern web technologies.

TECHNICAL SKILLS
JavaScript, React, Node.js, MongoDB, AWS, Docker, TypeScript, CI/CD

EXPERIENCE
TechCorp Inc., Bangalore
Senior Developer, 2020-Present
- Built scalable React/Node.js applications
- Deployed on AWS with Docker containers
- Implemented CI/CD pipelines

EDUCATION
B.Tech Computer Science, IIT Bombay, 2019
"""

    # Job description
    job_desc = """
Senior Full Stack Developer needed.

Requirements: 
- JavaScript, React, Node.js, MongoDB
- AWS/Docker deployment experience
- CI/CD pipelines
- 3+ years experience
"""

    # Parse resume
    cleaned = clean_resume_text(sample_resume)
    candidate_data = extract_resume_fields(cleaned)

    # Analyze
    analysis = analyze_candidate(job_desc, candidate_data)

    # Print exact format
    print(f"Candidate: {candidate_data.get('name', 'Unknown')}")
    print(f"Match Score: {analysis['match_score']}/100")
    print()
    
    if analysis['matched_skills']:
        print(f"Matched Skills: {', '.join(analysis['matched_skills'])}")
    print()
    
    if analysis['missing_skills']:
        print(f"Missing Skills: {', '.join(analysis['missing_skills'])}")
    print()
    
    print("Strengths:")
    for strength in analysis['strengths']:
        print(f"* {strength}")
    print()
    
    print(f"Summary:")
    print(analysis['summary'])

if __name__ == "__main__":
    main()

