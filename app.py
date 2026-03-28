"""
SmartHire AI - Resume Screening Agent
Streamlit Web Application

A modern, visually attractive UI for AI-powered resume screening and candidate ranking.
"""

import streamlit as st
import os
import tempfile
from typing import List, Dict, Any
from resume_parser import extract_resume_text, extract_resume_fields
from ai_analysis import analyze_candidate


# Configure Streamlit page
st.set_page_config(
    page_title="SmartHire AI – Resume Screening Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Modern SaaS Dashboard Theme - Deep Blue to Cyan Gradients */
    :root {
        --primary-gradient: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        --secondary-gradient: linear-gradient(135deg, #1e40af 0%, #0ea5e9 100%);
        --success-gradient: linear-gradient(135deg, #10b981, #059669);
        --warning-gradient: linear-gradient(135deg, #f59e0b, #d97706);
        --error-gradient: linear-gradient(135deg, #ef4444, #dc2626);
        --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --hover-lift: translateY(-4px) scale(1.02);
    }
    
    /* Hero Header with Gradient Background */
    .hero-section {
        background: var(--primary-gradient);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: var(--card-shadow);
        animation: fadeInDown 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.3rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Enhanced Cards */
    .card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 2rem;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--secondary-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: var(--hover-lift);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }
    .card:hover::before {
        transform: scaleX(1);
    }
    .card.animate-card {
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
        transform: translateY(30px);
    }
    .card.animate-card:nth-child(1) { animation-delay: 0.1s; }
    .card.animate-card:nth-child(2) { animation-delay: 0.2s; }
    .card.animate-card:nth-child(3) { animation-delay: 0.3s; }
    
    /* Score Circle with Pulse */
    .score-circle {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        font-weight: 800;
        color: white;
        margin: 0 auto 1rem auto;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        position: relative;
        animation: pulse 2s infinite;
    }
    .score-circle::after {
        content: '';
        position: absolute;
        inset: -4px;
        border-radius: 50%;
        background: inherit;
        opacity: 0.3;
        animation: pulse-ring 2s infinite;
    }
    .match-score-high { background: var(--success-gradient); }
    .match-score-medium { background: var(--warning-gradient); }
    .match-score-low { background: var(--error-gradient); }
    
    /* Skill Tags - Color Coded */
    .skill-tag {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.3rem 0.3rem 0 0;
        border: 1px solid transparent;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .skill-tag.matched {
        background: var(--success-gradient);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    .skill-tag.missing {
        background: var(--error-gradient);
        color: white;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
    }
    .skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    /* Strengths & Missing */
    .strength-badge {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        color: #166534;
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        border-left: 5px solid #22c55e;
        margin: 0.75rem 0;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
        transition: all 0.3s ease;
    }
    .strength-badge:hover {
        transform: translateX(8px);
    }
    
    .missing-skill {
        background: linear-gradient(135deg, #fef2f2, #fecaca);
        color: #991b1b;
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        border-left: 5px solid #ef4444;
        margin: 0.75rem 0;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
        transition: all 0.3s ease;
    }
    .missing-skill:hover {
        transform: translateX(8px);
    }
    
    /* Enhanced Candidate Header */
    .candidate-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 3px solid transparent;
        background: linear-gradient(90deg, transparent 0%, rgba(30, 58, 138, 0.05) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    .rank-badge {
        background: var(--secondary-gradient);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 1.2rem;
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4);
        animation: bounceIn 0.6s ease-out;
    }
    
    /* Progress Bar with Shine */
    .progress-container {
        background: linear-gradient(90deg, #f1f5f9, #e2e8f0);
        border-radius: 25px;
        height: 14px;
        margin: 1.5rem 0;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    .progress-bar {
        height: 100%;
        border-radius: 25px;
        transition: width 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shine 2s infinite;
    }
    .progress-high { background: var(--success-gradient); }
    .progress-medium { background: var(--warning-gradient); }
    .progress-low { background: var(--error-gradient); }
    
    /* Summary Box */
    .summary-box {
        background: linear-gradient(135deg, rgba(248, 250, 252, 0.8), rgba(241, 245, 249, 0.8));
        border: 1px solid rgba(226, 232, 240, 0.5);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1.5rem;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    }
    
    .summary-title {
        font-weight: 700;
        background: var(--secondary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.2rem;
    }
    
    /* Upload Area */
    .upload-area {
        border: 3px dashed rgba(59, 130, 246, 0.5);
        border-radius: 20px;
        padding: 4rem 2rem;
        text-align: center;
        transition: all 0.4s ease;
        background: linear-gradient(135deg, rgba(255,255,255,0.7), rgba(248, 250, 252, 0.7));
        backdrop-filter: blur(20px);
        cursor: pointer;
    }
    .upload-area:hover {
        border-color: #0ea5e9;
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(241, 245, 249, 0.9));
        transform: scale(1.02);
        box-shadow: 0 20px 40px rgba(14, 165, 233, 0.2);
    }
    
    .job-desc-area {
        border: 2px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        background: linear-gradient(135deg, white, #f8fafc);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    
    /* Glassmorphism Analyze Button */
    .analyze-btn {
        background: linear-gradient(145deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 1.25rem 3rem;
        border-radius: 20px;
        font-size: 1.2rem;
        font-weight: 700;
        width: 100%;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .analyze-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    .analyze-btn:hover {
        transform: var(--hover-lift);
        box-shadow: 0 25px 50px rgba(30, 58, 138, 0.4);
        border-color: rgba(255,255,255,0.5);
    }
    .analyze-btn:hover::before {
        left: 100%;
    }
    .analyze-btn:disabled {
        background: rgba(156, 163, 175, 0.3);
        backdrop-filter: blur(10px);
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    /* Section Backgrounds */
    .section-bg {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.03), rgba(6, 182, 212, 0.03));
        border-radius: 20px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Keyframe Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    @keyframes pulse-ring {
        0% { transform: scale(0.95); opacity: 1; }
        100% { transform: scale(1.1); opacity: 0; }
    }
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header { font-size: 2.5rem; }
        .card { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)


def get_score_color_class(score: int) -> str:
    """Get CSS class based on match score."""
    if score >= 80:
        return "match-score-high"
    elif score >= 60:
        return "match-score-medium"
    else:
        return "match-score-low"


def get_progress_class(score: int) -> str:
    """Get progress bar CSS class based on score."""
    if score >= 80:
        return "progress-high"
    elif score >= 60:
        return "progress-medium"
    else:
        return "progress-low"


def display_candidate_card(candidate_data: Dict[str, Any], rank: int):
    """Display a candidate's analysis results in a styled card."""
    ai_analysis = candidate_data["ai_analysis"]
    structured_data = candidate_data["structured_data"]
    
    score = ai_analysis["match_score"]
    score_color_class = get_score_color_class(score)
    progress_class = get_progress_class(score)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f"""
        <div class="score-circle {score_color_class}">
            {score}/100
        </div>
        <div style="text-align: center; font-weight: bold; color: #374151;">
            Match Score
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar {progress_class}" style="width: {score}%"></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="candidate-header">
            <div>
                <h3 style="margin: 0; color: #111827;">{structured_data.get('name', 'Unknown Candidate')}</h3>
                <p style="margin: 0; color: #6b7280;">{structured_data.get('role', 'No role specified')}</p>
            </div>
            <div class="rank-badge">
                #{rank}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Matched Skills
        if ai_analysis["matched_skills"]:
            st.markdown("**✅ Matched Skills:**")
            skills_html = ""
            for skill in ai_analysis["matched_skills"]:
                skills_html += f'<span class="skill-tag matched">{skill}</span>'
            st.markdown(f'<div>{skills_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #6b7280;">No matched skills found.</p>', unsafe_allow_html=True)
        
        # Missing Skills
        if ai_analysis["missing_skills"]:
            st.markdown("**❌ Missing Skills:**")
            for skill in ai_analysis["missing_skills"]:
                st.markdown(f'<div class="missing-skill">• {skill}</div>', unsafe_allow_html=True)
        
        # Strengths
        if ai_analysis["strengths"]:
            st.markdown("**💪 Strengths:**")
            for strength in ai_analysis["strengths"]:
                st.markdown(f'<div class="strength-badge">• {strength}</div>', unsafe_allow_html=True)
        
        # AI Summary
        st.markdown('<div class="summary-box animate-card">', unsafe_allow_html=True)
        st.markdown('<div class="summary-title">🤖 AI Analysis Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="line-height: 1.6; color: #374151;">{ai_analysis["summary"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def process_resume_file(uploaded_file, job_description: str) -> Dict[str, Any]:
    """Process a single uploaded resume file."""
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Extract text from PDF
        raw_text = extract_resume_text(tmp_file_path)
        
        if not raw_text:
            return {
                "name": uploaded_file.name,
                "success": False,
                "error": "Failed to extract text from PDF",
                "structured_data": None,
                "ai_analysis": None
            }
        
        # Extract structured fields
        structured_data = extract_resume_fields(raw_text)
        
        if not structured_data:
            return {
                "name": uploaded_file.name,
                "success": False,
                "error": "Failed to extract structured fields",
                "structured_data": None,
                "ai_analysis": None
            }
        
        # Perform AI analysis
        ai_analysis = analyze_candidate(job_description, structured_data)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return {
            "name": uploaded_file.name,
            "success": True,
            "error": None,
            "structured_data": structured_data,
            "ai_analysis": ai_analysis
        }
        
    except Exception as e:
        # Clean up temporary file if it exists
        try:
            os.unlink(tmp_file_path)
        except:
            pass
        
        return {
            "name": uploaded_file.name,
            "success": False,
            "error": str(e),
            "structured_data": None,
            "ai_analysis": None
        }


def main():
    """Main Streamlit application."""
    
    # Header Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-header">🤖 SmartHire AI</h1>
        <p class="sub-header">AI-powered resume screening and candidate ranking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Content
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Job Description Input
    st.markdown('<div class="section-bg">', unsafe_allow_html=True)
    st.markdown("### 📋 Job Description")
    job_description = st.text_area(
        "Enter Job Description",
        height=150,
        placeholder="Paste the job description here... The AI will analyze candidates against these requirements.",
        help="Enter the complete job description. The AI will evaluate candidates based on this description."
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Resume Upload
    st.markdown('<div class="upload-area" style="margin-bottom: 1rem;">Drop your PDF resumes here or click to browse</div>', unsafe_allow_html=True)
    st.markdown("### 📄 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload Candidate Resumes",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload PDF resume files. You can select multiple files at once."
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Analyze Button
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        analyze_clicked = st.button(
            "🚀 Analyze Candidates",
            key="analyze",
            help="Click to start AI-powered analysis",
            use_container_width=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Results Section
    if analyze_clicked:
        st.markdown("### 🎯 Analysis Results")
        
        # Validation
        if not job_description.strip():
            st.warning("⚠️ Please enter a job description before analyzing candidates.")
            return
        
        if not uploaded_files:
            st.warning("⚠️ Please upload at least one resume file.")
            return
        
        # Process resumes
        with st.spinner("🤖 Analyzing candidates... This may take a moment."):
            results = []
            
            # Process each uploaded file
            for uploaded_file in uploaded_files:
                result = process_resume_file(uploaded_file, job_description)
                results.append(result)
            
            # Separate successful and failed results
            successful_results = [r for r in results if r["success"]]
            failed_results = [r for r in results if not r["success"]]
            
            if successful_results:
                # Sort by match score (descending)
                successful_results.sort(key=lambda x: x["ai_analysis"]["match_score"], reverse=True)
                
                # Display Top Candidates Ranking
                st.markdown("### 🏆 Top Candidates")
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                for i, result in enumerate(successful_results, 1):
                    ai_analysis = result["ai_analysis"]
                    candidate_name = result["structured_data"].get("name", f"Candidate {i}")
                    
                    col1, col2, col3 = st.columns([6, 2, 2])
                    
                    with col1:
                        st.markdown(f"**{i}. {candidate_name}**")
                    
                    with col2:
                        score = ai_analysis["match_score"]
                        st.markdown(f"**{score}/100**")
                    
                    with col3:
                        if score >= 80:
                            st.markdown('<span style="color: #10b981; font-weight: bold;">Excellent Match</span>', unsafe_allow_html=True)
                        elif score >= 60:
                            st.markdown('<span style="color: #f59e0b; font-weight: bold;">Good Match</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span style="color: #ef4444; font-weight: bold;">Needs Review</span>', unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Display Detailed Results
                st.markdown("### 📊 Detailed Analysis")
                
                for i, result in enumerate(successful_results, 1):
                    st.markdown(f'<div class="card animate-card">', unsafe_allow_html=True)
                    display_candidate_card(result, i)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Summary Statistics
                st.markdown("### 📈 Summary Statistics")
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Candidates", len(successful_results))
                
                with col2:
                    avg_score = sum(r["ai_analysis"]["match_score"] for r in successful_results) / len(successful_results)
                    st.metric("Average Score", f"{avg_score:.1f}/100")
                
                with col3:
                    high_matches = sum(1 for r in successful_results if r["ai_analysis"]["match_score"] >= 80)
                    st.metric("Excellent Matches", high_matches)
                
                with col4:
                    medium_matches = sum(1 for r in successful_results if 60 <= r["ai_analysis"]["match_score"] < 80)
                    st.metric("Good Matches", medium_matches)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            if failed_results:
                st.markdown("### ❌ Failed Analyses")
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                for result in failed_results:
                    st.error(f"**{result['name']}**: {result['error']}")
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
        SmartHire AI – Making resume screening faster, smarter, and more accurate.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()