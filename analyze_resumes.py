"""
Resume Analysis Script for SmartHire AI

This script automatically processes all PDF resumes from the "Resumes" folder,
extracts structured information, and generates AI evaluation results for each candidate.
"""

import os
import glob
from typing import List, Dict, Any
from resume_parser import extract_resume_text, extract_resume_fields
from ai_analysis import analyze_candidate


class ResumeAnalyzer:
    """Main class for analyzing resumes from a folder."""
    
    def __init__(self, resumes_folder: str = "Resumes", job_description: str = ""):
        """
        Initialize the resume analyzer.
        
        Args:
            resumes_folder (str): Path to the folder containing resume PDFs
            job_description (str): Job description for candidate evaluation
        """
        self.resumes_folder = resumes_folder
        self.job_description = job_description
        self.candidates_results = []
    
    def set_job_description(self, job_description: str):
        """Set the job description for analysis."""
        self.job_description = job_description
    
    def find_resume_files(self) -> List[str]:
        """
        Find all PDF files in the resumes folder.
        
        Returns:
            List[str]: List of PDF file paths
        """
        if not os.path.exists(self.resumes_folder):
            print(f"Error: Folder '{self.resumes_folder}' not found.")
            return []
        
        # Find all PDF files in the folder
        pdf_pattern = os.path.join(self.resumes_folder, "*.pdf")
        pdf_files = glob.glob(pdf_pattern)
        
        if not pdf_files:
            print(f"No PDF files found in '{self.resumes_folder}' folder.")
            return []
        
        print(f"Found {len(pdf_files)} resume(s) in '{self.resumes_folder}' folder:")
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"  {i}. {os.path.basename(pdf_file)}")
        
        return pdf_files
    
    def process_single_resume(self, pdf_file_path: str) -> Dict[str, Any]:
        """
        Process a single resume file through the complete pipeline.
        
        Args:
            pdf_file_path (str): Path to the PDF resume file
            
        Returns:
            Dict[str, Any]: Complete analysis results for the candidate
        """
        candidate_name = os.path.splitext(os.path.basename(pdf_file_path))[0]
        print(f"\nProcessing resume: {candidate_name}")
        print("-" * 50)
        
        try:
            # Step 1: Extract text from PDF
            print("Step 1: Extracting text from PDF...")
            raw_text = extract_resume_text(pdf_file_path)
            
            if not raw_text:
                print(f"❌ Failed to extract text from {candidate_name}")
                return {
                    "name": candidate_name,
                    "success": False,
                    "error": "Failed to extract text from PDF",
                    "raw_text": None,
                    "structured_data": None,
                    "ai_analysis": None
                }
            
            print(f"✅ Successfully extracted {len(raw_text)} characters")
            
            # Step 2: Extract structured fields
            print("Step 2: Extracting structured fields...")
            structured_data = extract_resume_fields(raw_text)
            
            if not structured_data:
                print(f"❌ Failed to extract structured data from {candidate_name}")
                return {
                    "name": candidate_name,
                    "success": False,
                    "error": "Failed to extract structured fields",
                    "raw_text": raw_text,
                    "structured_data": None,
                    "ai_analysis": None
                }
            
            print(f"✅ Successfully extracted structured data")
            
            # Step 3: AI analysis
            print("Step 3: Performing AI analysis...")
            ai_analysis = analyze_candidate(self.job_description, structured_data)
            
            print(f"✅ AI analysis completed")
            
            # Combine all results
            result = {
                "name": candidate_name,
                "success": True,
                "error": None,
                "raw_text": raw_text,
                "structured_data": structured_data,
                "ai_analysis": ai_analysis
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error processing {candidate_name}: {str(e)}")
            return {
                "name": candidate_name,
                "success": False,
                "error": str(e),
                "raw_text": None,
                "structured_data": None,
                "ai_analysis": None
            }
    
    def process_all_resumes(self) -> List[Dict[str, Any]]:
        """
        Process all resumes in the folder.
        
        Returns:
            List[Dict[str, Any]]: List of analysis results for all candidates
        """
        if not self.job_description:
            print("Error: Job description not set. Please set a job description first.")
            return []
        
        # Find all resume files
        pdf_files = self.find_resume_files()
        
        if not pdf_files:
            return []
        
        print(f"\nStarting analysis of {len(pdf_files)} resume(s)...")
        print("=" * 60)
        
        # Process each resume
        results = []
        successful_count = 0
        
        for pdf_file in pdf_files:
            result = self.process_single_resume(pdf_file)
            results.append(result)
            
            if result["success"]:
                successful_count += 1
        
        print(f"\n" + "=" * 60)
        print(f"Analysis completed!")
        print(f"Successfully processed: {successful_count}/{len(pdf_files)} resumes")
        print("=" * 60)
        
        self.candidates_results = results
        return results
    
    def display_candidate_results(self, result: Dict[str, Any]):
        """
        Display the analysis results for a single candidate.
        
        Args:
            result (Dict[str, Any]): Analysis result for a candidate
        """
        if not result["success"]:
            print(f"❌ {result['name']}: {result['error']}")
            return
        
        ai_analysis = result["ai_analysis"]
        structured_data = result["structured_data"]
        candidate_name = structured_data.get("name") or result["name"]

        print(f"\nCandidate: {candidate_name}")
        print(f"Match Score: {ai_analysis['match_score']}/100")
        print()
        print(
            f"Matched Skills: {', '.join(ai_analysis['matched_skills']) if ai_analysis['matched_skills'] else 'None'}"
        )
        print(
            f"Missing Skills: {', '.join(ai_analysis['missing_skills']) if ai_analysis['missing_skills'] else 'None'}"
        )
        print()
        print("Strengths:")
        if ai_analysis['strengths']:
            for strength in ai_analysis['strengths']:
                print(f"* {strength}")
        else:
            print("* None")
        print()
        print("Summary:")
        print(ai_analysis['summary'])
    
    def display_all_results(self):
        """Display results for all processed candidates."""
        if not self.candidates_results:
            print("No results to display. Please process resumes first.")
            return
        
        print(f"\n{'='*80}")
        print(f"ALL CANDIDATE RESULTS")
        print(f"{'='*80}")
        
        # Sort by match score (descending)
        successful_results = [r for r in self.candidates_results if r["success"]]
        successful_results.sort(
            key=lambda x: (
                x["ai_analysis"]["match_score"],
                len(x["ai_analysis"].get("matched_skills", [])),
                (x.get("structured_data", {}).get("name") or x["name"]).lower(),
            ),
            reverse=True,
        )
        
        # Display successful results first
        for result in successful_results:
            self.display_candidate_results(result)
        
        # Display failed results
        failed_results = [r for r in self.candidates_results if not r["success"]]
        if failed_results:
            print(f"\n{'='*80}")
            print(f"FAILED RESUMES")
            print(f"{'='*80}")
            for result in failed_results:
                print(f"❌ {result['name']}: {result['error']}")
    
    def get_ranked_candidates(self) -> List[Dict[str, Any]]:
        """
        Get candidates ranked by match score.
        
        Returns:
            List[Dict[str, Any]]: Ranked list of successful candidates
        """
        successful_results = [r for r in self.candidates_results if r["success"]]
        ranked_results = sorted(
            successful_results,
            key=lambda x: (
                x["ai_analysis"]["match_score"],
                len(x["ai_analysis"].get("matched_skills", [])),
                (x.get("structured_data", {}).get("name") or x["name"]).lower(),
            ),
            reverse=True,
        )
        return ranked_results
    
    def print_summary_report(self):
        """Print a summary report of all candidates."""
        if not self.candidates_results:
            print("No results to summarize. Please process resumes first.")
            return
        
        successful_results = [r for r in self.candidates_results if r["success"]]
        failed_results = [r for r in self.candidates_results if not r["success"]]
        
        print(f"\n{'='*60}")
        print(f"SUMMARY REPORT")
        print(f"{'='*60}")
        print(f"Total Resumes Processed: {len(self.candidates_results)}")
        print(f"Successful Analyses: {len(successful_results)}")
        print(f"Failed Analyses: {len(failed_results)}")
        
        if successful_results:
            ranked = self.get_ranked_candidates()
            print(f"\nTop 3 Candidates:")
            for i, result in enumerate(ranked[:3], 1):
                ai_analysis = result["ai_analysis"]
                candidate_name = result.get("structured_data", {}).get("name") or result["name"]
                print(f"  {i}. {candidate_name} - {ai_analysis['match_score']}/100")
            
            avg_score = sum(r["ai_analysis"]["match_score"] for r in successful_results) / len(successful_results)
            print(f"\nAverage Match Score: {avg_score:.1f}/100")
        
        if failed_results:
            print(f"\nFailed Resumes:")
            for result in failed_results:
                print(f"  ❌ {result['name']}: {result['error']}")
        
        print(f"{'='*60}")


def main():
    """Main function to demonstrate the resume analysis functionality."""
    print("SmartHire AI - Resume Analysis System")
    print("=" * 50)
    
    # Sample job description (can be customized)
    sample_job_description = """
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
    
    # Initialize analyzer
    analyzer = ResumeAnalyzer(resumes_folder="Resumes")
    analyzer.set_job_description(sample_job_description)
    
    print("Job Description:")
    print("-" * 17)
    print(sample_job_description[:150] + "...")
    
    # Process all resumes
    results = analyzer.process_all_resumes()
    
    if results:
        # Display detailed results
        analyzer.display_all_results()
        
        # Print summary report
        analyzer.print_summary_report()
        
        # Get ranked candidates
        ranked_candidates = analyzer.get_ranked_candidates()
        if ranked_candidates:
            print(f"\n{'='*60}")
            print(f"FINAL RANKING")
            print(f"{'='*60}")
            for i, candidate in enumerate(ranked_candidates, 1):
                ai_analysis = candidate["ai_analysis"]
                candidate_name = candidate.get("structured_data", {}).get("name") or candidate["name"]
                print(f"{i}. {candidate_name} - {ai_analysis['match_score']}/100")
    else:
        print("\nNo resumes were successfully processed.")
        print("Please ensure:")
        print("1. The 'Resumes' folder exists")
        print("2. It contains PDF files")
        print("3. You have set a job description")
        print("4. Required dependencies are installed")


if __name__ == "__main__":
    main()