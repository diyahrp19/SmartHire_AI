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
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    :root {
        --primary: #3b82f6;
        --primary-dark: #1e3a8a;
        --accent: #06b6d4;
        --success: #10b981;
        --success-light: #d1fae5;
        --warning: #f59e0b;
        --danger: #ef4444;
        --danger-light: #fee2e2;
        --light-bg: #f5f6fa;
        --card-bg: #ffffff;
        --text-dark: #0f172a;
        --text-muted: #64748b;
        --border: #e2e8f0;
    }

    /* Page Load Animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Smooth Transitions */
    :root {
        --transition-speed: 0.3s ease-in-out;
    }

    body, [data-testid="stAppViewContainer"] {
        background-color: var(--light-bg) !important;
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
        animation: fadeIn 0.5s ease-in-out;
    }

    [data-testid="stHeader"] { background: transparent !important; }

    /* ─── HERO HEADER: Wide rectangular div with deep blue gradient background ─── */
    .hero-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        background-size: 400% 400%;
        padding: 3.5rem 2.5rem;
        border-radius: 24px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(30, 58, 138, 0.2);
        position: relative;
        overflow: hidden;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        animation: fadeIn 0.5s ease-in-out;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -30%;
        width: 160%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }

    .app-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0 0 0.5rem 0;
        text-shadow: 0 2px 15px rgba(0,0,0,0.15);
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        justify-content: center;
    }

    .app-subtitle {
        font-size: 1.05rem;
        color: rgba(255,255,255,0.9);
        margin: 0;
        font-weight: 500;
        letter-spacing: 0.01em;
    }

    /* ─── MODERN CARD: White background with light gray border ─── */
    .modern-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
        border: 1px solid var(--border);
        transition: all var(--transition-speed);
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.5s ease-in-out;
    }

    .card-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--text-dark);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .card-subtitle {
        font-size: 0.88rem;
        color: var(--text-muted);
        margin-bottom: 1.2rem;
    }

    /* ─── TEXTAREA: Document icon label with focus-within effect ─── */
    .textarea-container {
        margin-bottom: 1.5rem;
    }
    
    .textarea-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid var(--border) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 1rem !important;
        transition: all var(--transition-speed) !important;
        background: #f8fafc !important;
        color: var(--text-dark) !important;
    }
    
    .stTextArea:focus-within textarea {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.25) !important;
    }

    /* ─── FILE UPLOADER: Dashed border with hover effects ─── */
    .file-uploader-container {
        margin-bottom: 1.5rem;
    }
    
    [data-testid="stFileUploader"] > div {
        border-radius: 16px !important;
        border: 2px dashed rgba(59, 130, 246, 0.3) !important;
        padding: 1.5rem !important;
        transition: all var(--transition-speed) !important;
        background: rgba(248, 250, 252, 0.8) !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    
    [data-testid="stFileUploader"] > div:hover {
        border-color: var(--primary) !important;
        background: rgba(59, 130, 246, 0.05) !important;
        transform: scale(1.02);
    }
    
    .upload-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        transition: transform 0.2s ease;
    }
    
    [data-testid="stFileUploader"] > div:hover .upload-icon {
        transform: scale(1.05);
    }

    /* ─── ANALYZE BUTTON: Orange background with rocket icon ─── */
    .analyze-btn-wrapper .stButton > button {
        background: linear-gradient(135deg, #f97316 0%, #f59e0b 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        padding: 0.9rem 3rem !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 8px 30px rgba(249, 115, 22, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
        letter-spacing: 0.02em !important;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        width: 100%;
    }
    
    .analyze-btn-wrapper .stButton > button:hover {
        background: linear-gradient(135deg, #ea580c 0%, #d97706 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(249, 115, 22, 0.4) !important;
    }

    /* ─── SECTION HEADERS ─── */
    .section-header {
        font-size: 1.7rem;
        font-weight: 800;
        color: var(--text-dark);
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid var(--primary);
        display: flex;
        align-items: center;
        gap: 0.6rem;
        animation: fadeIn 0.5s ease-in-out;
    }

    .sub-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-dark);
        margin: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ─── METRICS ─── */
    .metric-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        border: 1px solid var(--border);
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
        transition: all var(--transition-speed);
        animation: fadeIn 0.5s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }

    .metric-value {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }

    .metric-label {
        font-size: 0.78rem;
        color: var(--text-muted);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.3rem;
    }

    /* ─── SCORE BADGE ─── */
    .score-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 72px;
        height: 72px;
        border-radius: 50%;
        font-size: 1.6rem;
        font-weight: 900;
        color: white;
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        transition: all var(--transition-speed);
        flex-shrink: 0;
    }
    .score-high { background: linear-gradient(135deg, #10b981, #059669); }
    .score-medium { background: linear-gradient(135deg, #f59e0b, #d97706); }
    .score-low { background: linear-gradient(135deg, #ef4444, #dc2626); }

    /* ─── RANK BADGE ─── */
    .rank-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.6rem 1.2rem;
        border-radius: 12px;
        font-weight: 800;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all var(--transition-speed);
    }
    .rank-1 { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #78350f; }
    .rank-2 { background: linear-gradient(135deg, #d1d5db, #9ca3af); color: #374151; }
    .rank-3 { background: linear-gradient(135deg, #fb923c, #f97316); color: #ffffff; }
    .rank-other { background: linear-gradient(135deg, #e2e8f0, #cbd5e1); color: #475569; }

    /* ─── SKILL BADGES ─── */
    .skill-badge {
        display: inline-block;
        padding: 0.45rem 0.9rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        margin: 0.25rem;
        transition: all var(--transition-speed);
    }
    .skill-badge:hover { transform: scale(1.05); }
    .skill-matched {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: #065f46;
        border: 1px solid #6ee7b7;
    }
    .skill-missing {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #7f1d1d;
        border: 1px solid #fca5a5;
    }
    .skill-extra {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        color: #1e40af;
        border: 1px solid #93c5fd;
    }

    /* ─── CANDIDATE CARD ─── */
    .candidate-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
        border: 1px solid var(--border);
        transition: all var(--transition-speed);
        animation: fadeIn 0.5s ease-in-out;
    }
    .candidate-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.1);
    }

    .candidate-name {
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--text-dark);
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .candidate-email {
        font-size: 0.85rem;
        color: var(--text-muted);
    }

    /* ─── PROGRESS BAR ─── */
    .progress-container {
        width: 100%;
        height: 8px;
        background: #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.8rem 0;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: 10px;
        transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* ─── SUMMARY BOX ─── */
    .summary-box {
        background: linear-gradient(135deg, rgba(248, 250, 252, 0.9), rgba(241, 245, 249, 0.9));
        border-left: 4px solid var(--primary);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1.2rem;
    }
    .summary-title {
        font-size: 0.85rem;
        font-weight: 800;
        color: var(--text-dark);
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .summary-text {
        font-size: 0.88rem;
        color: var(--text-muted);
        line-height: 1.6;
    }

    /* ─── FILE TAGS ─── */
    .file-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: linear-gradient(135deg, #dbeafe, #bae6fd);
        color: #1e40af;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1px solid #93c5fd;
        transition: all var(--transition-speed);
    }
    .file-tag:hover { transform: scale(1.03); }

    /* ─── STREAMLIT OVERRIDES ─── */
    div[data-testid="stExpander"] {
        border-radius: 16px !important;
        border: 1px solid var(--border) !important;
        overflow: hidden;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
        border-radius: 10px !important;
    }

    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 2rem 0;
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
    if score >= 80: return "#10b981"
    if score >= 60: return "#f59e0b"
    return "#ef4444"


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
                         marker=dict(color="#10b981", cornerradius=4)))
    fig.add_trace(go.Bar(y=names, x=missing, name="❌ Missing", orientation="h",
                         marker=dict(color="#ef4444", cornerradius=4)))
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
    # Hero Header
    st.markdown("""
    <div class="hero-header">
        <div class="app-title">🚀 SmartHire AI</div>
        <div class="app-subtitle">AI-powered resume screening and intelligent candidate ranking</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Job Description ──
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 Job Description</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Enter the job requirements to match against resumes</div>', unsafe_allow_html=True)
    job_desc = st.text_area("Job Description", height=130, placeholder="e.g. Full-stack developer with React, Node.js, AWS experience. 3+ years required...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Upload Resumes ──
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📄 Upload Resumes</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-subtitle">Select PDF resume files to analyze</div>', unsafe_allow_html=True)
    files = st.file_uploader("Resume Files", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")

    if files:
        st.markdown("**Selected Files:**")
        tags = "".join([f'<span class="file-tag">📄 {f.name}</span>' for f in files])
        st.markdown(tags, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Analyze Button ──
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        st.markdown('<div class="analyze-btn-wrapper">', unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Analyze Candidates", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Results ──
    if analyze_btn:
        if not job_desc.strip():
            st.error("⚠️ Please enter a job description before analyzing.")
            return
        if not files:
            st.error("⚠️ Please upload at least one resume PDF.")
            return

        st.markdown("---")
        st.markdown('<div class="section-header">🎯 Screening Results</div>', unsafe_allow_html=True)

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
        st.markdown('<div class="sub-header">📊 Summary</div>', unsafe_allow_html=True)

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
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")

        # ── Candidate Rankings ──
        st.markdown('<div class="sub-header">👥 Candidate Rankings</div>', unsafe_allow_html=True)

        for idx, r in enumerate(successful):
            rank = idx + 1
            analysis = r["ai_analysis"]
            score = analysis["match_score"]
            name = r["structured_data"].get("name", "Unknown")
            email = r["structured_data"].get("email", "N/A")

            st.markdown(f'<div class="candidate-card">', unsafe_allow_html=True)

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
            <div class="progress-container">
                <div class="progress-bar" style="width: {score}%;"></div>
            </div>
            ''', unsafe_allow_html=True)

            # Skills
            if analysis["matched_skills"]:
                st.markdown("**✅ Matched Skills:**")
                skills_html = " ".join([f'<span class="skill-badge skill-matched">{s}</span>' for s in analysis["matched_skills"]])
                st.markdown(skills_html, unsafe_allow_html=True)

            if analysis["missing_skills"]:
                st.markdown("**❌ Missing Skills:**")
                skills_html = " ".join([f'<span class="skill-badge skill-missing">{s}</span>' for s in analysis["missing_skills"]])
                st.markdown(skills_html, unsafe_allow_html=True)

            if analysis.get("extra_skills"):
                st.markdown("**🌟 Extra Skills:**")
                skills_html = " ".join([f'<span class="skill-badge skill-extra">{s}</span>' for s in analysis["extra_skills"]])
                st.markdown(skills_html, unsafe_allow_html=True)

            # AI Summary
            st.markdown(f'''
            <div class="summary-box">
                <div class="summary-title">🤖 AI Summary</div>
                <div class="summary-text">{analysis["summary"]}</div>
            </div>
            ''', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # ── Data Visualization ──
        st.markdown('<div class="sub-header">📈 Data Visualization</div>', unsafe_allow_html=True)

        ch1, ch2 = st.columns(2)
        with ch1:
            st.plotly_chart(create_score_chart(successful), use_container_width=True)
        with ch2:
            st.plotly_chart(create_skill_chart(successful), use_container_width=True)


if __name__ == "__main__":
    main()