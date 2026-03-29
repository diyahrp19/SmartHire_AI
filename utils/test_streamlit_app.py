import os
import sys
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import process_resume_file, get_score_color_class, get_progress_class


def test_score_color_classes():
    """Test the score color class functions."""
    print("Testing Score Color Classes...")
    
    assert get_score_color_class(90) == "match-score-high"
    assert get_score_color_class(80) == "match-score-high"
    
    assert get_score_color_class(75) == "match-score-medium"
    assert get_score_color_class(60) == "match-score-medium"
    
    assert get_score_color_class(50) == "match-score-low"
    assert get_score_color_class(0) == "match-score-low"
    
    print("✅ Score color classes working correctly")


def test_progress_classes():
    """Test the progress bar color class functions."""
    print("Testing Progress Bar Classes...")
    
    assert get_progress_class(90) == "progress-high"
    assert get_progress_class(80) == "progress-high"
    
    assert get_progress_class(75) == "progress-medium"
    assert get_progress_class(60) == "progress-medium"
    
    assert get_progress_class(50) == "progress-low"
    assert get_progress_class(0) == "progress-low"
    
    print("✅ Progress bar classes working correctly")


def test_process_resume_file():
    """Test the resume file processing function."""
    print("Testing Resume File Processing...")
    
    mock_file = Mock()
    mock_file.name = "test_resume.pdf"
    mock_file.getvalue.return_value = b"Mock PDF content"
    
    with patch('app.extract_resume_text') as mock_extract_text, \
         patch('app.extract_resume_fields') as mock_extract_fields, \
         patch('app.analyze_candidate') as mock_analyze:
        
        mock_extract_text.return_value = "Extracted resume text"
        mock_extract_fields.return_value = {
            "name": "John Doe",
            "skills": ["Python", "JavaScript"],
            "experience": "5 years"
        }
        mock_analyze.return_value = {
            "match_score": 85,
            "matched_skills": ["Python"],
            "missing_skills": ["React"],
            "strengths": ["Strong experience"],
            "summary": "Good candidate"
        }
        
        job_description = "We need a Python developer"
        result = process_resume_file(mock_file, job_description)
        
        assert result["success"] == True
        assert result["name"] == "test_resume.pdf"
        assert result["structured_data"]["name"] == "John Doe"
        assert result["ai_analysis"]["match_score"] == 85
        
        print("✅ Resume file processing working correctly")


def test_error_handling():
    """Test error handling in resume processing."""
    print("Testing Error Handling...")
    
    mock_file = Mock()
    mock_file.name = "test_resume.pdf"
    mock_file.getvalue.return_value = b"Mock PDF content"
    
    with patch('app.extract_resume_text') as mock_extract_text:
        mock_extract_text.return_value = None
        
        job_description = "Job description"
        result = process_resume_file(mock_file, job_description)
        
        assert result["success"] == False
        assert "Failed to extract text" in result["error"]
    
    with patch('app.extract_resume_text') as mock_extract_text, \
         patch('app.extract_resume_fields') as mock_extract_fields:
        
        mock_extract_text.return_value = "Text content"
        mock_extract_fields.return_value = None
        
        result = process_resume_file(mock_file, job_description)
        
        assert result["success"] == False
        assert "Failed to extract structured fields" in result["error"]
    
    print("✅ Error handling working correctly")


def test_app_imports():
    """Test that the app imports correctly."""
    print("Testing App Imports...")
    
    try:
        import app
        print("✅ App imports successfully")
        
        assert hasattr(app, 'main')
        assert hasattr(app, 'process_resume_file')
        assert hasattr(app, 'get_score_color_class')
        assert hasattr(app, 'get_progress_class')
        
        print("✅ All required functions exist")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("SmartHire AI - Streamlit App Test Suite")
    print("=" * 50)
    
    try:
        if not test_app_imports():
            return
        
        test_score_color_classes()
        test_progress_classes()
        
        test_process_resume_file()
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed!")
        print("✅ Streamlit application is ready to run")
        print("\nTo start the application:")
        print("1. Install requirements: pip install -r data/requirements.txt")
        print("2. Set API keys: export OPENAI_API_KEY=your-key")
        print("3. Run: streamlit run app.py")
        print("4. Open browser: http://localhost:8501")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Please check the application code and dependencies.")


if __name__ == "__main__":
    main()
