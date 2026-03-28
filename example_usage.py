"""
Example usage of the resume_parser.py module

This script demonstrates how to use the resume parser in a real-world scenario
for a Resume Screening AI project.
"""

from resume_parser import extract_resume_text, clean_resume_text, validate_pdf_file


def main():
    """Demonstrate how to use the resume parser module."""
    
    print("Resume Parser Example Usage")
    print("=" * 30)
    
    # Example 1: Basic usage
    print("\n1. Basic Usage Example:")
    print("-" * 20)
    
    # Note: This would normally be a real PDF file path
    sample_resume_path = "sample_resume.pdf"
    
    # Check if file exists and is valid
    if validate_pdf_file(sample_resume_path):
        print(f"✓ Valid PDF file: {sample_resume_path}")
        
        # Extract text from the resume
        resume_text = extract_resume_text(sample_resume_path)
        
        if resume_text:
            print("✓ Successfully extracted resume text")
            print(f"Resume text length: {len(resume_text)} characters")
            print("\nFirst 300 characters of extracted text:")
            print("-" * 40)
            print(resume_text[:300] + ("..." if len(resume_text) > 300 else ""))
        else:
            print("✗ Failed to extract text from resume")
    else:
        print(f"✗ Invalid or missing PDF file: {sample_resume_path}")
        print("Note: In a real scenario, this would be an uploaded resume file")
    
    # Example 2: Text cleaning demonstration
    print("\n2. Text Cleaning Example:")
    print("-" * 20)
    
    dirty_resume_text = """
    John Smith
    Senior Software Developer
    
    
    Email: john.smith@techcompany.com
    
    Phone: (555) 987-6543
    
    
    SUMMARY
    Experienced developer with expertise in Python, JavaScript, and cloud technologies.
    
    
    """
    
    print("Original (dirty) text:")
    print(repr(dirty_resume_text))
    
    cleaned_text = clean_resume_text(dirty_resume_text)
    
    print("\nCleaned text:")
    print(repr(cleaned_text))
    
    print(f"\nText cleaning reduced size from {len(dirty_resume_text)} to {len(cleaned_text)} characters")
    
    # Example 3: Integration with AI analysis (conceptual)
    print("\n3. Integration with AI Analysis:")
    print("-" * 30)
    
    print("The cleaned resume text can now be used for:")
    print("• Skill extraction using NLP models")
    print("• Candidate experience analysis")
    print("• Job description matching")
    print("• Resume scoring and ranking")
    
    # Example of how you might send this to an AI model
    if cleaned_text:
        print(f"\nExample: Sending {len(cleaned_text)} characters of resume data to AI model...")
        # In a real implementation, this would be:
        # ai_response = ai_model.analyze_resume(cleaned_text)
        # print(f"AI Analysis Result: {ai_response}")


def process_uploaded_resume(file_path: str):
    """
    Example function showing how to process an uploaded resume file.
    
    Args:
        file_path (str): Path to the uploaded PDF resume file
        
    Returns:
        dict: Processing result with extracted text and metadata
    """
    result = {
        'success': False,
        'text': None,
        'error': None,
        'metadata': {}
    }
    
    try:
        # Validate the uploaded file
        if not validate_pdf_file(file_path):
            result['error'] = "Invalid PDF file or file not found"
            return result
        
        # Extract text from the resume
        extracted_text = extract_resume_text(file_path)
        
        if not extracted_text:
            result['error'] = "Could not extract text from the resume"
            return result
        
        # Calculate some basic metadata
        word_count = len(extracted_text.split())
        char_count = len(extracted_text)
        
        result.update({
            'success': True,
            'text': extracted_text,
            'metadata': {
                'word_count': word_count,
                'character_count': char_count,
                'file_path': file_path
            }
        })
        
        return result
        
    except Exception as e:
        result['error'] = f"Error processing resume: {str(e)}"
        return result


if __name__ == "__main__":
    main()
    
    print("\n" + "=" * 50)
    print("Resume Parser Module Ready for Integration!")
    print("The module is clean, well-structured, and ready to be")
    print("integrated with your main AI agent for resume screening.")