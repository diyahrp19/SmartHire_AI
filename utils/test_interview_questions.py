#!/usr/bin/env python3
"""Smoke test for interview question generation."""

from interview_question_generator import generate_interview_questions


def test_interview_question_generator():
    job_description = """
    We are looking for a Full Stack Software Engineer with experience in:
    - React and TypeScript for frontend development
    - Node.js and Express for backend APIs
    - PostgreSQL for database management
    - AWS cloud services for deployment
    - Docker for containerization
    - Experience with CI/CD pipelines
    - Strong problem-solving skills and ability to work in agile teams
    """

    candidate_data = {
        "name": "John Doe",
        "role": "Full Stack Developer",
        "skills": ["React", "Node.js", "PostgreSQL", "AWS", "Docker", "JavaScript", "HTML", "CSS"],
        "experience": "5 years of full-stack development experience",
        "education": "Bachelor's degree in Computer Science",
    }

    print("Testing Interview Question Generator")
    print("=" * 50)
    print(f"Job Description: {job_description[:100]}...")
    print(f"Candidate: {candidate_data['name']}")
    print(f"Skills: {', '.join(candidate_data['skills'])}")
    print(f"Experience: {candidate_data['experience']}")
    print()

    questions = generate_interview_questions(job_description, candidate_data)

    print(f"Generated {len(questions)} interview questions:")
    print("=" * 50)
    for i, q in enumerate(questions, 1):
        question_text = q.get("question", "")
        category = q.get("category", "technical").title()
        difficulty = q.get("difficulty", "medium").title()
        print(f"{i}. [{category} | {difficulty}] {question_text}")
        print()

    minimal_candidate = {
        "name": "Jane Smith",
        "skills": ["Python", "JavaScript"],
        "experience": "2 years",
    }

    minimal_questions = generate_interview_questions(job_description, minimal_candidate)
    print("Testing with minimal candidate data")
    print("=" * 50)
    print(f"Generated {len(minimal_questions)} questions for minimal candidate:")
    for i, q in enumerate(minimal_questions, 1):
        print(f"{i}. {q.get('question', '')}")

    print("\nTest completed successfully!")


if __name__ == "__main__":
    test_interview_question_generator()