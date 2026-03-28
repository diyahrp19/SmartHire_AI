"""
SmartHire AI - Modern Resume Screening Platform
Streamlit Web Application

Professional AI-powered resume screening with modern UI, candidate ranking,
skill analysis, and comprehensive data visualization.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import tempfile
import json
import re
from typing import List, Dict, Any

# ─── PDF text extraction (pure Python, no external binary) ───────────────────

try:
    import pdfplumber
    def extract_resume_text(path: str) -> str:
        with pdfplumber.open(path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
except ImportError:
    try:
        import PyPDF2
        def extract_resume_text(path: str) -> str:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "\n".join(page.extract_text() or "" for page in reader.pages)
    except ImportError:
        def extract_resume_text(path: str) -> str:
            return ""

# ─── Simple resume field extraction ─────────────────────────────────────────

def extract_resume_fields(text: str) -> Dict[str, Any]:
    """Extract basic fields from resume text."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    name = lines[0] if lines else "Unknown Candidate"

    email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    email = email_match.group(0) if email_match else "N/A"

    phone_match = re.search(r'[\+]?[\d\s\-\(\)]{7,15}', text)
    phone = phone_match.group(0).strip() if phone_match else "N/A"

    common_skills = [
        "Python", "JavaScript", "TypeScript", "React", "Angular", "Vue",
        "Node.js", "Django", "Flask", "FastAPI", "AWS", "Azure", "GCP",
        "Docker", "Kubernetes", "SQL", "PostgreSQL", "MongoDB", "Redis",
        "Git", "CI/CD", "REST", "GraphQL", "HTML", "CSS", "Tailwind",
        "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin",
        "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch",
        "Pandas", "NumPy", "Scikit-learn", "Data Analysis", "Agile", "Scrum",
        "Linux", "Terraform", "Jenkins", "GitHub Actions",
    ]
    found_skills = [s for s in common_skills if s.lower() in text.lower()]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": found_skills,
        "raw_text": text,
    }


# ─── AI-like candidate analysis (rule-based, no API needed) ─────────────────

def analyze_candidate(job_desc: str, structured: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze how well a candidate matches the job description."""
    job_lower = job_desc.lower()
    candidate_skills = structured.get("skills", [])

    # Extract required skills from job description
    all_skills = [
        "Python", "JavaScript", "TypeScript", "React", "Angular", "Vue",
        "Node.js", "Django", "Flask", "FastAPI", "AWS", "Azure", "GCP",
        "Docker", "Kubernetes", "SQL", "PostgreSQL", "MongoDB", "Redis",
        "Git", "CI/CD", "REST", "GraphQL", "HTML", "CSS", "Tailwind",
        "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin",
        "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch",
        "Pandas", "NumPy", "Scikit-learn", "Data Analysis", "Agile", "Scrum",
        "Linux", "Terraform", "Jenkins", "GitHub Actions",
    ]
    required = [s for s in all_skills if s.lower() in job_lower]
    if not required:
        required = all_skills[:5]

    matched = [s for s in required if s.lower() in [c.lower() for c in candidate_skills]]
    missing = [s for s in required if s.lower() not in [c.lower() for c in candidate_skills]]

    if required:
        score = int((len(matched) / len(required)) * 100)
    else:
        score = 50

    # Bonus for extra skills
    extra = [s for s in candidate_skills if s.lower() not in [r.lower() for r in required]]
    score = min(100, score + len(extra) * 2)

    # Generate summary
    if score >= 80:
        summary = f"Excellent match with {len(matched)} key skills aligned. Strong candidate recommended for interview. Additional strengths in {', '.join(extra[:3]) if extra else 'relevant areas'}."
    elif score >= 60:
        summary = f"Candidate has partial alignment with {len(matched)} matched skills and may fit depending on team priorities. Consider for second round with focus on {', '.join(missing[:3]) if missing else 'growth areas'}."
    else:
        summary = f"Limited alignment with only {len(matched)} matched skills. Significant gaps in {', '.join(missing[:3]) if missing else 'core requirements'}. May need extensive training."

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "summary": summary,
    }


# ─── Configure Streamlit ────────────────────────────────────────────────────

st.set_page_config(
    page_title="SmartHire AI – Resume Screening Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Modern CSS ──────────────────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink-900: #1e293b;
        --ink-700: #334155;
        --ink-500: #64748b;
        --paper: #f8fbff;
        --panel: #f1f7ff;
        --line: #dbe7f5;
        --brand: #2563eb;
        --brand-strong: #1d4ed8;
        --brand-soft: #bfdbfe;
        --teal: #0ea5e9;
        --danger: #dc2626;
        --ok: #16a34a;
    }

    @keyframes riseIn {
        from { opacity: 0; transform: translateY(18px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes floatBlob {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-10px, 10px) scale(1.05); }
        100% { transform: translate(0, 0) scale(1); }
    }

    body, [data-testid="stAppViewContainer"] {
        font-family: 'Manrope', system-ui, -apple-system, sans-serif !important;
        background:
            radial-gradient(1200px 500px at 10% -15%, rgba(59, 130, 246, 0.18), transparent 55%),
            radial-gradient(900px 480px at 95% 0%, rgba(125, 211, 252, 0.2), transparent 50%),
            linear-gradient(180deg, #f4f9ff 0%, #ecf5ff 45%, #f8fbff 100%) !important;
        color: var(--ink-900);
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1150px !important;
    }

    .hero-shell {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 2.6rem 2.3rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(130deg, #f0f9ff 0%, #dbeafe 50%, #e0e7ff 100%);
        box-shadow: 0 20px 44px rgba(59, 130, 246, 0.18);
        animation: riseIn 0.55s ease-out;
    }

    .hero-shell::before,
    .hero-shell::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        border-radius: 50%;
        filter: blur(4px);
        animation: floatBlob 7s ease-in-out infinite;
    }

    .hero-shell::before {
        top: -110px;
        right: -60px;
        background: radial-gradient(circle, rgba(96, 165, 250, 0.28), transparent 68%);
    }

    .hero-shell::after {
        bottom: -120px;
        left: -80px;
        background: radial-gradient(circle, rgba(129, 140, 248, 0.25), transparent 68%);
    }

    .hero-title {
        position: relative;
        margin: 0;
        font-size: 2.55rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #1e293b;
    }

    .hero-subtitle {
        position: relative;
        margin: 0.7rem 0 0;
        max-width: 760px;
        color: #334155;
        line-height: 1.65;
        font-size: 1.02rem;
    }

    .hero-pills {
        position: relative;
        margin-top: 1.2rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
    }

    .hero-pill {
        background: rgba(255, 255, 255, 0.78);
        color: #1d4ed8;
        border: 1px solid rgba(147, 197, 253, 0.45);
        border-radius: 999px;
        padding: 0.35rem 0.8rem;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    .panel-card {
        border: 1px solid var(--line);
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(241, 247, 255, 0.9));
        border-radius: 22px;
        padding: 1.25rem 1.35rem;
        margin: 0 0 1.1rem;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.12);
        backdrop-filter: blur(6px);
        animation: riseIn 0.5s ease-out;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--line) !important;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(241, 247, 255, 0.9)) !important;
        border-radius: 22px !important;
        padding: 0.7rem 0.85rem !important;
        margin-bottom: 1.1rem !important;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.12) !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(.section-title) {
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(.section-title):hover {
        transform: translateY(-3px);
        border-color: #93c5fd !important;
        box-shadow: 0 16px 28px rgba(37, 99, 235, 0.18) !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-name) {
        border: 1px solid var(--line) !important;
        background: linear-gradient(180deg, #f8fbff, #edf4ff) !important;
        border-radius: 20px !important;
        padding: 0.8rem 0.9rem !important;
        box-shadow: 0 12px 25px rgba(37, 99, 235, 0.12) !important;
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-name):hover {
        transform: translateY(-3px);
        border-color: #93c5fd !important;
        box-shadow: 0 16px 30px rgba(37, 99, 235, 0.18) !important;
    }

    .stTextArea [data-baseweb="textarea"] {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }

    .stTextArea [data-baseweb="textarea"]:focus-within {
        border: none !important;
        box-shadow: none !important;
    }

    .section-title {
        margin: 0;
        color: var(--ink-900);
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .section-note {
        margin: 0.38rem 0 0.85rem;
        color: var(--ink-500);
        font-size: 0.87rem;
    }

    .stTextArea textarea {
        border-radius: 14px !important;
        border: 1.7px solid var(--line) !important;
        background: #f8fbff !important;
        color: var(--ink-900) !important;
        font-size: 0.95rem !important;
        line-height: 1.55 !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: var(--brand) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.18) !important;
        outline: none !important;
    }

    .stTextArea textarea:focus-visible {
        outline: none !important;
    }

    [data-testid="stFileUploader"] > div {
        border: 2px dashed rgba(37, 99, 235, 0.45) !important;
        border-radius: 16px !important;
        background: linear-gradient(180deg, #eef5ff, #f8fbff) !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stFileUploader"] > div:hover {
        border-color: var(--brand) !important;
        box-shadow: 0 10px 24px rgba(37, 99, 235, 0.2) !important;
        transform: translateY(-1px);
    }

    .selected-file {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        margin: 0.25rem 0.32rem 0 0;
        border-radius: 999px;
        border: 1px solid #bfdbfe;
        background: #eaf2ff;
        color: #1e40af;
        padding: 0.35rem 0.75rem;
        font-size: 0.79rem;
        font-weight: 700;
    }

    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        border-radius: 14px !important;
        border: none !important;
        padding: 0.86rem 1rem !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        background: linear-gradient(135deg, #2563eb 0%, #38bdf8 100%) !important;
        color: #fff !important;
        box-shadow: 0 14px 26px rgba(37, 99, 235, 0.28) !important;
        transition: all 0.22s ease !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 18px 30px rgba(37, 99, 235, 0.35) !important;
        background: linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 100%) !important;
    }

    .results-heading {
        margin: 1rem 0 0.55rem;
        font-size: 1.45rem;
        color: var(--ink-900);
        letter-spacing: -0.025em;
        font-weight: 800;
    }

    .kpi-card {
        border-radius: 16px;
        border: 1px solid var(--line);
        background: #f8fbff;
        padding: 1.05rem;
        text-align: center;
        box-shadow: 0 6px 14px rgba(37, 99, 235, 0.08);
    }

    .kpi-label {
        color: var(--ink-500);
        font-size: 0.74rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 800;
    }

    .kpi-value {
        margin-top: 0.25rem;
        color: var(--brand-strong);
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.15;
    }

    .candidate-card {
        border-radius: 20px;
        border: 1px solid var(--line);
        background: linear-gradient(180deg, #f8fbff, #edf4ff);
        padding: 1.2rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 12px 25px rgba(37, 99, 235, 0.12);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }

    .candidate-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 30px rgba(37, 99, 235, 0.18);
    }

    .candidate-name {
        margin: 0;
        font-size: 1.02rem;
        font-weight: 800;
        color: var(--ink-900);
        letter-spacing: -0.01em;
    }

    .candidate-email {
        margin: 0.2rem 0 0;
        color: var(--ink-700);
        font-size: 0.82rem;
    }

    .score-badge {
        width: 66px;
        height: 66px;
        border-radius: 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        font-weight: 800;
        color: #fff;
    }

    .score-high { background: linear-gradient(135deg, #1e40af, #1d4ed8); }
    .score-medium { background: linear-gradient(135deg, #2563eb, #3b82f6); }
    .score-low { background: linear-gradient(135deg, #60a5fa, #93c5fd); }

    .rank-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 56px;
        border-radius: 999px;
        font-size: 0.9rem;
        font-weight: 800;
        padding: 0.45rem 0.75rem;
    }

    .rank-1 { background: #dbeafe; color: #1d4ed8; }
    .rank-2 { background: #e0e7ff; color: #4338ca; }
    .rank-3 { background: #e0f2fe; color: #0369a1; }
    .rank-other { background: #eff6ff; color: #334155; }

    .meter-track {
        width: 100%;
        height: 8px;
        background: #dbe7f5;
        border-radius: 999px;
        margin: 0.9rem 0 0.55rem;
        overflow: hidden;
    }

    .meter-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #2563eb, #38bdf8);
    }

    .skill-badge {
        display: inline-block;
        padding: 0.32rem 0.65rem;
        border-radius: 999px;
        margin: 0.14rem;
        font-size: 0.76rem;
        font-weight: 700;
    }

    .skill-matched { background: #dbeafe; color: #1e3a8a; border: 1px solid #93c5fd; }
    .skill-missing { background: #e0e7ff; color: #3730a3; border: 1px solid #a5b4fc; }
    .skill-extra { background: #e0f2fe; color: #0c4a6e; border: 1px solid #7dd3fc; }

    .summary-box {
        margin-top: 0.85rem;
        border-left: 4px solid var(--brand);
        border-radius: 11px;
        background: #eff6ff;
        padding: 0.9rem 1rem;
    }

    .summary-title {
        margin: 0;
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #1d4ed8;
        letter-spacing: 0.08em;
        font-weight: 800;
    }

    .summary-text {
        margin: 0.35rem 0 0;
        font-size: 0.85rem;
        line-height: 1.56;
        color: var(--ink-700);
    }

    .stProgress > div > div > div {
        border-radius: 999px !important;
        background: linear-gradient(90deg, #2563eb, #38bdf8) !important;
    }

    div[data-testid="stExpander"] {
        border-radius: 14px !important;
        border: 1px solid var(--line) !important;
        background: #f8fbff !important;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #c7d9f0, transparent);
        margin: 1.3rem 0;
    }

    @media (max-width: 900px) {
        .hero-title {
            font-size: 2rem;
        }

        .hero-shell {
            padding: 2rem 1.25rem;
        }

        .kpi-value {
            font-size: 1.65rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_rank_badge(rank: int) -> str:
    badges = {1: "🥇", 2: "🥈", 3: "🥉"}
    return badges.get(rank, f"#{rank}")

def get_rank_class(rank: int) -> str:
    return f"rank-{rank}" if rank <= 3 else "rank-other"

def get_score_class(score: int) -> str:
    if score >= 80: return "score-high"
    if score >= 60: return "score-medium"
    return "score-low"

def get_score_color(score: int) -> str:
    if score >= 80: return "#1d4ed8"
    if score >= 60: return "#3b82f6"
    return "#93c5fd"


# ─── Charts ──────────────────────────────────────────────────────────────────

def create_score_chart(results):
    names = [r["structured_data"].get("name", f"C{i}").split()[0] for i, r in enumerate(results[:10])]
    scores = [r["ai_analysis"]["match_score"] for r in results[:10]]
    colors = [get_score_color(s) for s in scores]

    fig = go.Figure(go.Bar(
        x=names, y=scores,
        marker=dict(color=colors, cornerradius=8),
        text=scores, textposition="outside", textfont=dict(size=13, weight=700),
    ))
    fig.update_layout(
        title=dict(text="📊 Match Scores", font=dict(size=18, family="Plus Jakarta Sans", weight=800)),
        xaxis=dict(title="Candidate", tickangle=-30),
        yaxis=dict(title="Score", range=[0, 110]),
        height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", size=12),
        margin=dict(t=60, b=60),
    )
    return fig

def create_skill_chart(results):
    names = [r["structured_data"].get("name", f"C{i}").split()[0] for i, r in enumerate(results[:10])]
    matched = [len(r["ai_analysis"]["matched_skills"]) for r in results[:10]]
    missing = [len(r["ai_analysis"]["missing_skills"]) for r in results[:10]]

    fig = go.Figure()
    fig.add_trace(go.Bar(y=names, x=matched, name="✅ Matched", orientation="h",
                         marker=dict(color="#1d4ed8", cornerradius=4)))
    fig.add_trace(go.Bar(y=names, x=missing, name="❌ Missing", orientation="h",
                         marker=dict(color="#93c5fd", cornerradius=4)))
    fig.update_layout(
        title=dict(text="🎯 Skill Analysis", font=dict(size=18, family="Plus Jakarta Sans", weight=800)),
        barmode="group", height=max(300, len(names) * 50),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", size=12),
        margin=dict(l=100, t=60),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


# ─── Process Resume ──────────────────────────────────────────────────────────

def process_resume(uploaded_file, job_desc: str) -> Dict[str, Any]:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        raw_text = extract_resume_text(tmp_path)
        if not raw_text.strip():
            os.unlink(tmp_path)
            return {"success": False, "error": "Could not extract text from PDF. Ensure pdfplumber or PyPDF2 is installed.", "name": uploaded_file.name}

        structured = extract_resume_fields(raw_text)
        analysis = analyze_candidate(job_desc, structured)
        os.unlink(tmp_path)

        return {
            "success": True,
            "structured_data": structured,
            "ai_analysis": analysis,
            "name": uploaded_file.name,
        }
    except Exception as e:
        try: os.unlink(tmp_path)
        except: pass
        return {"success": False, "error": str(e), "name": uploaded_file.name}


# ─── Main App ────────────────────────────────────────────────────────────────

def main():
    st.markdown("""
    <div class="hero-shell">
        <h1 class="hero-title">SmartHire AI</h1>
        <p class="hero-subtitle">
            Screen resumes with confidence, rank candidates intelligently, and uncover skill-fit insights in a clean recruiter dashboard.
        </p>
        <div class="hero-pills">
            <span class="hero-pill">Resume Intelligence</span>
            <span class="hero-pill">Skill Match Scoring</span>
            <span class="hero-pill">Visual Candidate Ranking</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<p class="section-title">Job Description</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-note">Describe the role requirements, skills, and experience expectations.</p>', unsafe_allow_html=True)
        job_desc = st.text_area(
            "Job Description",
            height=150,
            placeholder="Example: Hiring a full-stack engineer with React, Node.js, PostgreSQL, AWS, and CI/CD experience. 3+ years preferred.",
            label_visibility="collapsed",
        )

    with st.container(border=True):
        st.markdown('<p class="section-title">Upload Resume PDFs</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-note">Drop one or more PDF files to evaluate candidates against your role.</p>', unsafe_allow_html=True)
        files = st.file_uploader("Resume Files", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")

        if files:
            selected_tags = "".join([f'<span class="selected-file">PDF {f.name}</span>' for f in files])
            st.markdown(selected_tags, unsafe_allow_html=True)

    with st.container(border=True):
        cta_col_l, cta_col_c, cta_col_r = st.columns([1, 1.3, 1])
        with cta_col_c:
            st.markdown('<div class="cta-wrap">', unsafe_allow_html=True)
            analyze_btn = st.button("Analyze Candidates", use_container_width=True, type="primary")
            st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        if not job_desc.strip():
            st.error("⚠️ Please enter a job description before analyzing.")
            return
        if not files:
            st.error("⚠️ Please upload at least one resume PDF.")
            return

        st.markdown("---")
        st.markdown('<h2 class="results-heading">Screening Results</h2>', unsafe_allow_html=True)

        progress = st.progress(0)
        status = st.empty()
        results = []

        for idx, f in enumerate(files):
            status.text(f"⏳ Processing {idx+1}/{len(files)}: {f.name}")
            result = process_resume(f, job_desc)
            results.append(result)
            progress.progress((idx + 1) / len(files))

        status.empty()
        progress.empty()

        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        if failed:
            with st.expander(f"⚠️ {len(failed)} file(s) could not be processed", expanded=False):
                for r in failed:
                    st.warning(f"**{r['name']}**: {r['error']}")

        if not successful:
            st.error("❌ No resumes were processed successfully. Please check your PDF files.")
            return

        successful.sort(key=lambda x: x["ai_analysis"]["match_score"], reverse=True)

        # ── Summary Metrics ──
        st.markdown('<p class="section-title">Summary</p>', unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        avg = sum(r["ai_analysis"]["match_score"] for r in successful) / len(successful)
        high = sum(1 for r in successful if r["ai_analysis"]["match_score"] >= 80)
        low = sum(1 for r in successful if r["ai_analysis"]["match_score"] < 60)

        for col, label, value in [
            (m1, "Total Candidates", len(successful)),
            (m2, "Avg Score", f"{avg:.0f}"),
            (m3, "High Match", high),
            (m4, "Needs Dev", low),
        ]:
            with col:
                st.markdown(f'''
                <div class="kpi-card">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")

        # ── Candidate Rankings ──
        st.markdown('<p class="section-title">Candidate Rankings</p>', unsafe_allow_html=True)

        for idx, r in enumerate(successful):
            rank = idx + 1
            analysis = r["ai_analysis"]
            score = analysis["match_score"]
            name = r["structured_data"].get("name", "Unknown")
            email = r["structured_data"].get("email", "N/A")

            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 4, 1])
                with c1:
                    st.markdown(f'<div class="score-badge {get_score_class(score)}">{score}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="candidate-name">{name}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="candidate-email">{email}</div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="rank-badge {get_rank_class(rank)}">{get_rank_badge(rank)}</div>', unsafe_allow_html=True)

                # Progress bar
                st.markdown(f'''
                <div class="meter-track">
                    <div class="meter-fill" style="width: {score}%;"></div>
                </div>
                ''', unsafe_allow_html=True)

                # Skills
                if analysis["matched_skills"]:
                    st.markdown("**Matched Skills:**")
                    skills_html = " ".join([f'<span class="skill-badge skill-matched">{s}</span>' for s in analysis["matched_skills"]])
                    st.markdown(skills_html, unsafe_allow_html=True)

                if analysis["missing_skills"]:
                    st.markdown("**Missing Skills:**")
                    skills_html = " ".join([f'<span class="skill-badge skill-missing">{s}</span>' for s in analysis["missing_skills"]])
                    st.markdown(skills_html, unsafe_allow_html=True)

                if analysis.get("extra_skills"):
                    st.markdown("**Extra Skills:**")
                    skills_html = " ".join([f'<span class="skill-badge skill-extra">{s}</span>' for s in analysis["extra_skills"]])
                    st.markdown(skills_html, unsafe_allow_html=True)

                # AI Summary
                st.markdown(f'''
                <div class="summary-box">
                    <div class="summary-title">🤖 AI Summary</div>
                    <div class="summary-text">{analysis["summary"]}</div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")

        # ── Data Visualization ──
        st.markdown('<p class="section-title">Data Visualization</p>', unsafe_allow_html=True)

        ch1, ch2 = st.columns(2)
        with ch1:
            st.plotly_chart(create_score_chart(successful), use_container_width=True)
        with ch2:
            st.plotly_chart(create_skill_chart(successful), use_container_width=True)


if __name__ == "__main__":
    main()