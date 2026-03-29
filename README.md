# SmartHire AI - Resume Analysis System

An automated resume screening and analysis system that processes PDF resumes, extracts structured information, and provides AI-powered candidate evaluation.

## 🚀 Features

### Core Functionality

- **PDF Resume Processing**: Automatically extracts text from PDF resumes
- **Structured Data Extraction**: Converts resume text into structured fields (name, skills, experience, education, etc.)
- **AI-Powered Evaluation**: Uses Large Language Models (LLMs) to evaluate candidates against job descriptions
- **Batch Processing**: Processes multiple resumes automatically from a folder
- **Candidate Ranking**: Ranks candidates by match score for easy comparison

### Web Interface

- **Modern Streamlit UI**: Beautiful, professional web interface for recruiters
- **Drag & Drop Upload**: Easy file upload with visual feedback
- **Real-time Processing**: Live progress indicators and results
- **Interactive Results**: Detailed candidate cards with match visualization
- **Responsive Design**: Works on desktop and tablet devices

### Technical Features

- **Multiple LLM Providers**: Support for OpenAI (GPT) and Google Gemini
- **Error Handling**: Graceful handling of parsing errors and missing data
- **Modular Architecture**: Clean separation of concerns for easy maintenance
- **Comprehensive Logging**: Detailed processing information and error reporting

## 📁 Project Structure

```
SmartHire_AI/
├── app.py                          # Streamlit app entrypoint
├── Procfile                        # Start command for PaaS platforms
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render Blueprint deployment config
├── utils/resume_parser.py          # PDF text extraction and field parsing
├── utils/ai_analysis.py            # AI evaluation using LLMs
├── utils/analyze_resumes.py        # Main script for batch processing
├── utils/test_analyze_resumes.py   # Test suite
├── utils/example_usage.py          # Basic usage examples
├── utils/example_usage_enhanced.py # Enhanced pipeline examples
├── data/Resumes/                  # Folder for resume PDFs (create this)
└── README.md                       # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- PDF resume files to analyze

### Setup

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up API Keys**

   For OpenAI:

   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

   For Google Gemini:

   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```

3. **Create Resumes Folder**

   ```bash
   mkdir data/Resumes
   ```

4. **Add Resume PDFs**
   Place your PDF resume files in the `data/Resumes/` folder.

## 📖 Usage

### Option 1: Command Line Interface

Run the main analysis script:

```bash
python utils/analyze_resumes.py
```

This will:

1. Scan the `data/Resumes/` folder for PDF files
2. Process each resume through the complete pipeline
3. Display detailed results for each candidate
4. Provide a summary report with rankings

### Option 2: Web Interface (Recommended)

Launch the modern Streamlit web application:

```bash
# Install project requirements
pip install -r requirements.txt

# Set API keys
export OPENAI_API_KEY="your-openai-api-key"

# Run the web app
streamlit run app.py
```

## 🌐 Deploy On Render

This project is ready for Render Web Service deployment.

### Option 1: Blueprint (recommended)

1. Push this repository to GitHub.
2. In Render, click **New +** → **Blueprint**.
3. Select your repository.
4. Render will auto-detect `render.yaml` and create the service.
5. Add environment variables in Render:
   - `OPENAI_API_KEY` (optional)
   - `GEMINI_API_KEY` (optional)
   - `SMARTHIRE_USE_AI_QUESTIONS` (`false` by default)

### Option 2: Manual Web Service

Use these values while creating a Python Web Service:

- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`

### Notes

- `Procfile` and `render.yaml` are both included for compatibility.
- Uploaded files are processed from memory and temporary files only, so no persistent disk is required.

Open your browser to `http://localhost:8501` to access the beautiful recruiter dashboard.

#### Web Interface Features:

- **Drag & Drop Upload**: Upload multiple PDF resumes easily
- **Real-time Processing**: Watch as resumes are analyzed in real-time
- **Interactive Results**: Beautiful candidate cards with match visualization
- **Professional Dashboard**: Clean, modern interface designed for recruiters
- **Detailed Analytics**: Comprehensive match scores and skill analysis

### Example Output

```
SmartHire AI - Resume Analysis System
==================================================

Found 3 resume(s) in 'data/Resumes' folder:
  1. John_Doe_Resume.pdf
  2. Jane_Smith_Developer.pdf
  3. Bob_Wilson_Tech.pdf

Starting analysis of 3 resume(s)...
============================================================

Processing resume: John_Doe_Resume
--------------------------------------------------
Step 1: Extracting text from PDF...
✅ Successfully extracted 8500 characters
Step 2: Extracting structured fields...
✅ Successfully extracted structured data
Step 3: Performing AI analysis...
✅ AI analysis completed

============================================================
CANDIDATE: JOHN_DOE_RESUME
============================================================
Name: John Doe
Email: john.doe@example.com
Phone: +91-8765432109
Role: Full Stack Developer
Education: M.Tech in Software Engineering
Experience: 4+ years of experience

----------------------------------------
AI EVALUATION RESULTS
----------------------------------------
Match Score: 78/100

Matched Skills (9):
  1. JavaScript
  2. React
  3. Node.js
  4. MongoDB
  5. AWS
  6. Git
  7. RESTful APIs
  8. TypeScript
  9. Express

Missing Skills (3):
  1. Docker
  2. Microservices
  3. CI/CD

Strengths (3):
  1. Strong full-stack foundation
  2. Good cloud platform knowledge
  3. Relevant educational background

AI Summary:
  Strong candidate with solid full-stack skills and good experience. Could benefit from additional DevOps and containerization experience.
============================================================

============================================================
SUMMARY REPORT
============================================================
Total Resumes Processed: 3
Successful Analyses: 3
Failed Analyses: 0

Top 3 Candidates:
  1. Jane_Smith_Developer - 92/100
  2. John_Doe_Resume - 78/100
  3. Bob_Wilson_Tech - 65/100

Average Match Score: 78.3/100
============================================================

============================================================
FINAL RANKING
============================================================
1. Jane_Smith_Developer - 92/100
2. John_Doe_Resume - 78/100
3. Bob_Wilson_Tech - 65/100
```

## 🔧 Customization

### Setting a Custom Job Description

Edit the `main()` function in `utils/analyze_resumes.py`:

```python
# Replace with your job description
sample_job_description = """
Your custom job description here...
"""
```

### Using Different LLM Providers

```python
# For OpenAI (default)
analyzer = ResumeAnalyzer(resumes_folder="data/Resumes")
analyzer.set_job_description(job_description)

# For Google Gemini
analyzer = ResumeAnalyzer(resumes_folder="data/Resumes")
analyzer.set_job_description(job_description)
# Set GEMINI_API_KEY environment variable
```

### Custom Folder Location

```python
# Use a different folder
analyzer = ResumeAnalyzer(resumes_folder="path/to/your/resumes")
```

## 📊 Pipeline Flow

```
Resumes Folder → Resume Parser → Field Extraction → AI Analysis → Candidate Results
     ↓              ↓              ↓              ↓              ↓
  PDF Files → Text Extraction → Structured Data → LLM Evaluation → Ranked Candidates
```

### Step-by-Step Processing

1. **Resume Discovery**: Scans the specified folder for PDF files
2. **Text Extraction**: Uses `pdfplumber` to extract text from each PDF
3. **Field Extraction**: Parses the text to extract structured information:
   - Name
   - Email
   - Phone
   - Role/Job Title
   - Skills
   - Education
   - Work Experience
4. **AI Analysis**: Sends structured data + job description to LLM for evaluation
5. **Results Generation**: Creates detailed analysis with match scores and recommendations

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_utils/analyze_resumes.py
```

This will:

- Test the ResumeAnalyzer class
- Demonstrate expected output format
- Verify folder structure

## 📋 Requirements

### Core Dependencies

- `pdfplumber>=0.8.0` - PDF text extraction
- `openai>=1.0.0` - OpenAI API integration
- `google-generativeai>=0.3.0` - Google Gemini API integration

### Optional Dependencies

- `fpdf>=1.7.2` - For creating sample PDFs in tests

## 🔑 API Keys

### OpenAI Setup

1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

### Google Gemini Setup

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

## 🚨 Error Handling

The system handles various error scenarios:

- **Missing Folder**: Creates the Resumes folder if it doesn't exist
- **No PDF Files**: Gracefully handles empty folders
- **Parsing Errors**: Skips files that can't be processed
- **API Errors**: Provides fallback responses when LLM APIs fail
- **Missing Data**: Handles incomplete resume information

## 🎯 Output Format

Each candidate analysis includes:

- **Basic Information**: Name, contact details, role, education, experience
- **Match Score**: 0-100 score indicating job description alignment
- **Matched Skills**: List of skills that match job requirements
- **Missing Skills**: Important skills that are missing
- **Strengths**: Key candidate advantages
- **AI Summary**: Natural language explanation of the match

## 🔍 Integration

### With Existing HR Systems

The system can be integrated into existing HR workflows:

```python
from utils.analyze_resumes import ResumeAnalyzer

# Initialize analyzer
analyzer = ResumeAnalyzer(resumes_folder="path/to/resumes")
analyzer.set_job_description(job_description)

# Process resumes
results = analyzer.process_all_resumes()

# Get ranked candidates
ranked_candidates = analyzer.get_ranked_candidates()

# Export results
for candidate in ranked_candidates:
    # Send to your HR system
    send_to_hr_system(candidate)
```

### Batch Processing

For high-volume recruitment:

```python
# Process multiple job descriptions
job_descriptions = [
    "Senior Developer",
    "Frontend Developer",
    "Backend Developer"
]

for job_desc in job_descriptions:
    analyzer = ResumeAnalyzer(resumes_folder="data/Resumes")
    analyzer.set_job_description(job_desc)
    results = analyzer.process_all_resumes()
    # Store results for each job description
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:

1. Check the [Issues](../../issues) section
2. Review the documentation
3. Create a new issue with detailed information

## 🙏 Acknowledgments

- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF text extraction
- [OpenAI](https://openai.com/) for GPT models
- [Google AI](https://ai.google/) for Gemini models

---

**SmartHire AI** - Making resume screening faster, smarter, and more accurate.
