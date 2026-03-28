"""AI analysis module for SmartHire candidate evaluation."""

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()


SKILL_NORMALIZATION_MAP = {
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


@dataclass
class CandidateAnalysis:
    """Structured analysis output."""

    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    summary: str


class CandidateAnalyzer:
    """Gemini-powered analyzer with heuristic fallback scoring."""

    def __init__(self, model: str = "gemini-1.5-flash", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    @staticmethod
    def normalize_skill(skill: str) -> str:
        key = re.sub(r"[^a-z0-9+./# ]", "", (skill or "").lower()).strip()
        if key in SKILL_NORMALIZATION_MAP:
            return SKILL_NORMALIZATION_MAP[key]
        return skill.strip().title() if skill else ""

    @classmethod
    def normalize_skills(cls, skills: List[str]) -> List[str]:
        normalized: List[str] = []
        seen = set()
        for skill in skills or []:
            canonical = cls.normalize_skill(str(skill))
            if canonical and canonical.lower() not in seen:
                normalized.append(canonical)
                seen.add(canonical.lower())
        return normalized

    @classmethod
    def extract_required_skills(cls, job_description: str) -> List[str]:
        jd = (job_description or "").lower()
        found = []
        found_set = set()
        for raw, canonical in SKILL_NORMALIZATION_MAP.items():
            pattern = r"(?<![a-z0-9])" + re.escape(raw) + r"(?![a-z0-9])"
            if re.search(pattern, jd) and canonical.lower() not in found_set:
                found.append(canonical)
                found_set.add(canonical.lower())
        return found

    @staticmethod
    def _extract_years(experience_text: Optional[str]) -> float:
        if not experience_text:
            return 0.0
        match = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*(years?|yrs?)", experience_text.lower())
        if match:
            return float(match.group(1))
        return 0.0

    @staticmethod
    def _education_score(education: Optional[str]) -> int:
        if not education:
            return 6
        edu = education.lower()
        if any(x in edu for x in ["phd", "doctorate"]):
            return 12
        if any(x in edu for x in ["master", "m.tech", "mtech", "ms", "m.sc", "msc", "mba"]):
            return 10
        if any(x in edu for x in ["bachelor", "b.tech", "btech", "bs", "b.sc", "bsc"]):
            return 8
        return 6

    @staticmethod
    def _role_score(role: Optional[str], job_description: str) -> int:
        if not role:
            return 4
        role_l = role.lower()
        jd_l = (job_description or "").lower()
        if role_l in jd_l:
            return 10
        if any(term in role_l for term in ["full stack", "backend", "frontend", "developer", "engineer"]):
            return 7
        return 5

    def _heuristic_analysis(self, job_description: str, candidate_data: Dict[str, Any]) -> CandidateAnalysis:
        candidate_skills = self.normalize_skills(candidate_data.get("skills", []) or [])
        required_skills = self.extract_required_skills(job_description)

        candidate_set = {s.lower() for s in candidate_skills}
        required_set = {s.lower() for s in required_skills}

        matched = [s for s in required_skills if s.lower() in candidate_set]
        missing = [s for s in required_skills if s.lower() not in candidate_set]

        ratio = 0.0
        if required_skills:
            ratio = len(matched) / max(1, len(required_skills))

        transferable_skills = {
            "Python",
            "Java",
            "C#",
            "C++",
            "SQL",
            "NoSQL",
            "Docker",
            "Kubernetes",
            "AWS",
            "Azure",
            "GCP",
        }
        transferable_bonus = min(8, sum(1 for s in candidate_skills if s in transferable_skills) * 2)

        skill_component = int(52 + ratio * 28 + transferable_bonus)

        years = self._extract_years(candidate_data.get("experience"))
        if years >= 8:
            exp_component = 20
        elif years >= 5:
            exp_component = 17
        elif years >= 3:
            exp_component = 14
        elif years > 0:
            exp_component = 10
        else:
            exp_component = 6

        edu_component = self._education_score(candidate_data.get("education"))
        role_component = self._role_score(candidate_data.get("role"), job_description)

        missing_penalty = int((1.0 - ratio) * 8) if required_skills else 2
        score = skill_component + exp_component + edu_component + role_component - missing_penalty
        score = max(55, min(96, score))

        strengths = []
        if matched:
            strengths.append(f"Matches {len(matched)} core required skills")
        if years >= 5:
            strengths.append("Strong relevant professional experience")
        elif years > 0:
            strengths.append("Relevant hands-on development experience")
        if candidate_data.get("education"):
            strengths.append("Education aligns with technical role")
        if candidate_data.get("role"):
            strengths.append("Role background is relevant to the position")
        if not strengths:
            strengths = ["Candidate profile has partial data but remains evaluable"]

        summary = "Candidate shows good alignment with core job requirements and is suitable for further evaluation."
        if score >= 85:
            summary = "Candidate demonstrates strong alignment with the role and appears highly suitable."
        elif score >= 70:
            summary = "Candidate demonstrates solid alignment with the role and should be considered for interview."
        elif score >= 55:
            summary = "Candidate has partial alignment and may fit depending on team priorities."

        return CandidateAnalysis(
            match_score=score,
            matched_skills=matched,
            missing_skills=missing,
            strengths=strengths,
            summary=summary,
        )

    def _build_prompt(self, job_description: str, candidate_data: Dict[str, Any], baseline: CandidateAnalysis) -> str:
        normalized_candidate = {
            "name": candidate_data.get("name"),
            "role": candidate_data.get("role"),
            "skills": self.normalize_skills(candidate_data.get("skills", []) or []),
            "experience": candidate_data.get("experience"),
            "education": candidate_data.get("education"),
            "email": candidate_data.get("email"),
            "phone": candidate_data.get("phone"),
        }

        return f"""
You are a senior technical hiring evaluator.

Evaluate the candidate holistically using these criteria:
1) Skill match
2) Relevant experience
3) Education relevance
4) Overall suitability

Important scoring guidance:
- Do NOT be overly strict.
- Missing one field should reduce score moderately, not drastically.
- Realistic score range for partially matching candidates is usually 60-85.
- Use 0-100 integer score.

Job Description:
{job_description}

Candidate Data:
{json.dumps(normalized_candidate, indent=2)}

Baseline heuristic (for realism reference):
{json.dumps(baseline.__dict__, indent=2)}

Return JSON only:
{{
  "match_score": <int 0-100>,
  "matched_skills": ["..."],
  "missing_skills": ["..."],
  "strengths": ["..."],
  "summary": "short summary"
}}
""".strip()

    def _call_gemini(self, prompt: str) -> Dict[str, Any]:
        from google import genai

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing")

        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(model=self.model, contents=prompt)
        text = (response.text or "").strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end <= start:
            raise ValueError("Gemini response did not contain valid JSON")
        return json.loads(text[start:end])

    def _coerce_analysis(self, raw: Dict[str, Any], baseline: CandidateAnalysis, required_skills: List[str]) -> CandidateAnalysis:
        ai_score = int(raw.get("match_score", baseline.match_score) or baseline.match_score)
        ai_score = max(0, min(100, ai_score))

        blended_score = int(round((0.65 * ai_score) + (0.35 * baseline.match_score)))

        ai_matched = self.normalize_skills(raw.get("matched_skills", []) or baseline.matched_skills)
        ai_missing = self.normalize_skills(raw.get("missing_skills", []) or baseline.missing_skills)

        required_set = {s.lower() for s in required_skills}
        matched_set = {s.lower() for s in ai_matched}
        missing_set = {s.lower() for s in ai_missing}

        # Keep matched/missing consistent with job requirements.
        for skill in required_skills:
            s = skill.lower()
            if s in matched_set and s in missing_set:
                missing_set.remove(s)
            if s not in matched_set and s not in missing_set:
                missing_set.add(s)

        matched = [s for s in required_skills if s.lower() in matched_set]
        missing = [s for s in required_skills if s.lower() in missing_set]

        strengths = [str(x).strip() for x in raw.get("strengths", []) if str(x).strip()]
        if not strengths:
            strengths = baseline.strengths

        summary = str(raw.get("summary", "")).strip() or baseline.summary

        return CandidateAnalysis(
            match_score=max(45, min(97, blended_score)),
            matched_skills=matched,
            missing_skills=missing,
            strengths=strengths[:5],
            summary=summary,
        )

    def analyze_candidate(self, job_description: str, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        if not job_description or not candidate_data:
            result = CandidateAnalysis(
                match_score=50,
                matched_skills=[],
                missing_skills=[],
                strengths=["Insufficient input data"],
                summary="Candidate evaluation completed with limited information.",
            )
            return result.__dict__

        # Ensure candidate fields are present.
        safe_candidate = {
            "name": candidate_data.get("name") or "Unknown Candidate",
            "skills": candidate_data.get("skills") or [],
            "experience": candidate_data.get("experience") or "Not specified",
            "education": candidate_data.get("education") or "Not specified",
            "role": candidate_data.get("role") or "Not specified",
            "email": candidate_data.get("email"),
            "phone": candidate_data.get("phone"),
        }

        baseline = self._heuristic_analysis(job_description, safe_candidate)
        required_skills = self.extract_required_skills(job_description)

        try:
            prompt = self._build_prompt(job_description, safe_candidate, baseline)
            ai_raw = self._call_gemini(prompt)
            final = self._coerce_analysis(ai_raw, baseline, required_skills)
            return final.__dict__
        except Exception:
            # Fallback still returns realistic, structured evaluation.
            return baseline.__dict__


def analyze_candidate(job_description: str, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze one candidate using Gemini with resilient fallback behavior."""

    analyzer = CandidateAnalyzer()
    return analyzer.analyze_candidate(job_description, candidate_data)
