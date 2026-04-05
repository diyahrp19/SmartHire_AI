# SmartHire AI

SmartHire AI analyzes PDF resumes, extracts candidate details, and scores job-fit using AI.

## Live Demo

https://smarthireaigit-jdkyeumckzsgggiifngfa3.streamlit.app/

## Features

- Parse PDF resumes into structured candidate data
- Match candidates against a job description
- Score and rank candidates
- Run from CLI or Streamlit web app
- Optional OpenAI and Gemini support

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Add API key (optional but recommended):

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-openai-api-key"
# or
$env:GEMINI_API_KEY="your-gemini-api-key"
```

3. Put resumes in:

```text
data/Resumes/
```

## Run

CLI:

```bash
python utils/analyze_resumes.py
```

Web app:

```bash
streamlit run app.py
```

## Deploy (Render)

- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`
- Set env vars: `OPENAI_API_KEY`, `GEMINI_API_KEY`, `SMARTHIRE_USE_AI_QUESTIONS`

## Main Files

- `app.py` - Streamlit UI
- `utils/analyze_resumes.py` - Batch resume analysis
- `utils/resume_parser.py` - PDF and field extraction
- `utils/ai_analysis.py` - AI scoring logic

## License

MIT
