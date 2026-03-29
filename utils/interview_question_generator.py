import os
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class InterviewQuestion:
    question: str
    category: str
    difficulty: str

class InterviewQuestionGenerator:
    def __init__(self, model: str = "gemini-2.5-flash", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.max_questions = 3
        self.use_ai = str(os.getenv("SMARTHIRE_USE_AI_QUESTIONS", "false")).lower() == "true"
        self._model_fallbacks = [
            self.model,
            "gemini-2.0-flash",
            "gemini-1.5-flash",
        ]
        
        # Define question categories and their weightages
        self.question_categories = {
            "technical": 0.4,      # 40% - Core technical skills
            "scenario": 0.3,       # 30% - Practical scenarios
            "problem_solving": 0.2, # 20% - Problem-solving approach
            "job_specific": 0.1    # 10% - Job description specific
        }

    @staticmethod
    def normalize_skill(skill: str) -> str:
        """Normalize skill names to standard format"""
        skill_map = {
            "nodejs": "Node.js",
            "node.js": "Node.js",
            "reactjs": "React",
            "react.js": "React",
            "react": "React",
            "mongodb": "MongoDB",
            "mongo db": "MongoDB",
            "javascript": "JavaScript",
            "js": "JavaScript",
            "typescript": "TypeScript",
            "ts": "TypeScript",
            "postgres": "PostgreSQL",
            "postgresql": "PostgreSQL",
            "aws": "AWS",
            "docker": "Docker",
            "kubernetes": "Kubernetes",
            "k8s": "Kubernetes",
            "ci/cd": "CI/CD",
            "cicd": "CI/CD",
            "expressjs": "Express",
            "express.js": "Express",
            "express": "Express",
            "python": "Python",
            "java": "Java",
            "sql": "SQL",
            "nosql": "NoSQL",
        }
        
        key = re.sub(r"[^a-z0-9+./# ]", "", (skill or "").lower()).strip()
        if key in skill_map:
            return skill_map[key]
        return skill.strip().title() if skill else ""

    @classmethod
    def normalize_skills(cls, skills: List[str]) -> List[str]:
        """Normalize a list of skills"""
        normalized: List[str] = []
        seen = set()
        for skill in skills or []:
            canonical = cls.normalize_skill(str(skill))
            if canonical and canonical.lower() not in seen:
                normalized.append(canonical)
                seen.add(canonical.lower())
        return normalized

    def _extract_technical_keywords(self, job_description: str) -> List[str]:
        """Extract technical keywords from job description"""
        jd_lower = job_description.lower()
        tech_keywords = [
            "api", "rest", "graphql", "microservices", "architecture", "design patterns",
            "database", "orm", "cache", "security", "authentication", "authorization",
            "performance", "scalability", "testing", "debugging", "deployment",
            "version control", "git", "agile", "scrum", "devops", "monitoring"
        ]
        
        found_keywords = []
        for keyword in tech_keywords:
            if keyword in jd_lower:
                found_keywords.append(keyword.title())
        
        return found_keywords

    def _extract_required_skills(self, job_description: str) -> List[str]:
        """Extract common skill tokens from JD for fast, targeted questions."""
        jd = (job_description or "").lower()
        skill_catalog = [
            "python", "java", "javascript", "typescript", "react", "node.js", "node", "express",
            "django", "flask", "fastapi", "sql", "postgresql", "mysql", "mongodb", "redis",
            "aws", "azure", "gcp", "docker", "kubernetes", "git", "ci/cd", "rest", "graphql",
        ]

        found: List[str] = []
        for token in skill_catalog:
            if token in jd:
                found.append(self.normalize_skill(token))
        return self.normalize_skills(found)

    def _build_question_prompt(self, job_description: str, candidate_data: Dict[str, Any]) -> str:
        """Build the prompt for generating interview questions"""
        
        # Normalize candidate data
        normalized_candidate = {
            "name": candidate_data.get("name", "Candidate"),
            "role": candidate_data.get("role", ""),
            "skills": self.normalize_skills(candidate_data.get("skills", []) or []),
            "experience": candidate_data.get("experience", ""),
            "education": candidate_data.get("education", ""),
        }
        
        # Extract technical keywords from job description
        tech_keywords = self._extract_technical_keywords(job_description)
        
        # Build skills context
        skills_context = ", ".join(normalized_candidate["skills"]) if normalized_candidate["skills"] else "various technologies"
        
        # Build experience context
        exp_context = normalized_candidate["experience"] or "relevant experience"
        
        prompt = f"""
You are a senior technical interviewer preparing questions for a candidate.

Generate 2-3 highly personalized interview questions for this candidate based on their profile and the job requirements.

**Job Description:**
{job_description}

**Candidate Profile:**
- Name: {normalized_candidate["name"]}
- Role: {normalized_candidate["role"]}
- Skills: {skills_context}
- Experience: {exp_context}
- Education: {normalized_candidate["education"]}

**Technical Keywords from Job Description:**
{", ".join(tech_keywords) if tech_keywords else "Standard technical concepts"}

**Requirements:**
1. Generate only 2-3 questions total (prefer 3)
2. Questions MUST be specific to the candidate's skills and experience
3. Avoid generic questions like "Tell me about yourself"
4. Include a mix of:
   - Technical questions about specific skills (40%)
   - Scenario-based practical questions (30%)
   - Problem-solving and debugging questions (20%)
   - Job description specific questions (10%)
5. Questions should be clear, professional, and actionable
6. Keep each question short and direct (one sentence, no long multi-part wording)
7. Return questions as a JSON array with format:
   [
     {{"question": "Question text", "category": "technical|scenario|problem_solving|job_specific", "difficulty": "easy|medium|hard"}},
     ...
   ]

**Important:**
- DO NOT ask about skills the candidate doesn't have
- DO NOT ask generic HR questions
- Focus on hands-on technical knowledge and real-world application
- Make questions specific enough to assess actual competency
"""
        
        return prompt.strip()

    def _call_gemini(self, prompt: str) -> List[Dict[str, Any]]:
        """Call Gemini API to generate questions."""
        try:
            from google import genai
        except ImportError:
            print("Gemini SDK not installed. Falling back to template questions.")
            return []

        if not self.api_key:
            return []

        client = genai.Client(api_key=self.api_key)
        tried_models: List[str] = []
        for model_name in self._model_fallbacks:
            if model_name in tried_models:
                continue
            tried_models.append(model_name)

            try:
                response = client.models.generate_content(model=model_name, contents=prompt)
                text = (response.text or "").strip()

                start = text.find("[")
                end = text.rfind("]") + 1
                if start == -1 or end <= start:
                    raise ValueError("Gemini response did not contain valid JSON")

                questions_data = json.loads(text[start:end])

                validated_questions = []
                for item in questions_data:
                    if isinstance(item, dict) and "question" in item:
                        question = {
                            "question": str(item.get("question", "")).strip(),
                            "category": str(item.get("category", "technical")).lower(),
                            "difficulty": str(item.get("difficulty", "medium")).lower(),
                        }
                        if question["question"] and len(question["question"]) > 10:
                            validated_questions.append(question)

                if validated_questions:
                    return validated_questions[:self.max_questions]
            except Exception as e:
                error_text = str(e).lower()
                if "not_found" in error_text or "not found" in error_text:
                    continue
                print(f"Gemini request failed: {e}")
                break

        print("Gemini model unavailable or returned invalid output. Using fallback questions.")
        return []

    def _generate_fallback_questions(self, candidate_data: Dict[str, Any], job_description: str) -> List[Dict[str, Any]]:
        """Generate fast, relevant local questions without external API calls."""

        questions: List[Dict[str, Any]] = []
        role = str(candidate_data.get("role", "")).strip() or "developer"
        experience = str(candidate_data.get("experience", "")).strip()

        candidate_skills = self.normalize_skills(candidate_data.get("skills", []) or [])
        matched_skills = self.normalize_skills(candidate_data.get("matched_skills", []) or [])
        job_skills = self._extract_required_skills(job_description)

        focus_skills = matched_skills or [s for s in candidate_skills if s in set(job_skills)] or candidate_skills
        focus_skills = focus_skills[:2]

        for skill in focus_skills:
            questions.append({
                "question": f"In one project, how did you use {skill} to solve a real production problem?",
                "category": "technical",
                "difficulty": "medium",
            })

        if len(questions) < self.max_questions:
            if experience:
                questions.append({
                    "question": f"Based on your {experience}, what is one engineering decision you would make first for this {role} role?",
                    "category": "scenario",
                    "difficulty": "medium",
                })
            else:
                questions.append({
                    "question": "How do you debug a production issue when the root cause is unclear?",
                    "category": "problem_solving",
                    "difficulty": "medium",
                })

        return questions[:self.max_questions]

    def generate_questions(self, job_description: str, candidate_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized interview questions for a candidate"""
        
        if not job_description or not candidate_data:
            return []
        
        if self.use_ai and self.api_key:
            try:
                prompt = self._build_question_prompt(job_description, candidate_data)
                questions = self._call_gemini(prompt)
                if questions:
                    return questions
            except Exception as e:
                print(f"AI generation failed, falling back to template: {e}")

        return self._generate_fallback_questions(candidate_data, job_description)


def generate_interview_questions(job_description: str, candidate_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Main function to generate interview questions for a candidate"""
    generator = InterviewQuestionGenerator()
    return generator.generate_questions(job_description, candidate_data)