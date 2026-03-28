# SmartHire AI - Streamlit Application Guide

## 🚀 Quick Start

### 1. Install Streamlit Requirements
```bash
pip install -r streamlit_requirements.txt
```

### 2. Set Up API Keys
For AI analysis functionality, you need to set up API keys:

**OpenAI Setup:**
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

**Google Gemini Setup:**
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Open in Browser
The application will automatically open in your default browser at `http://localhost:8501`

## 🎨 UI Features

### Header Section
- **SmartHire AI Logo**: Modern gradient header with robot emoji
- **Subtitle**: "AI-powered resume screening and candidate ranking"
- **Professional Design**: Clean, modern layout with wide screen support

### Job Description Input
- **Large Text Area**: For pasting complete job descriptions
- **Placeholder Text**: Helpful guidance for users
- **Validation**: Warns if no job description is provided

### Resume Upload
- **Drag & Drop**: Modern file upload interface
- **Multiple Files**: Support for uploading multiple PDFs at once
- **File Type Validation**: Only accepts PDF files
- **Visual Feedback**: Hover effects and clear styling

### Analyze Button
- **Gradient Design**: Attractive button with hover effects
- **Loading State**: Shows processing animation
- **Validation**: Disabled until both job description and resumes are provided

### Results Display

#### Top Candidates Ranking
- **Leaderboard Style**: Clean ranking display
- **Match Scores**: Prominently displayed scores
- **Match Quality Indicators**: Color-coded match quality (Excellent/Good/Needs Review)

#### Detailed Candidate Cards
- **Modern Card Layout**: Clean, shadowed cards for each candidate
- **Score Visualization**: Circular score display with progress bar
- **Matched Skills**: Tag-style display of matching skills
- **Missing Skills**: Highlighted areas for improvement
- **Strengths**: Positive reinforcement of candidate strengths
- **AI Summary**: Natural language explanation of the match

#### Summary Statistics
- **Key Metrics**: Total candidates, average score, match quality breakdown
- **Visual Metrics**: Clean metric cards with icons
- **Data Insights**: Quick overview of the candidate pool

## 🎯 User Workflow

### Step 1: Enter Job Description
1. Paste the complete job description in the text area
2. The system will use this to evaluate all candidates

### Step 2: Upload Resumes
1. Click "Browse files" or drag & drop PDF files
2. Select multiple PDF resumes to analyze
3. Files are processed individually

### Step 3: Analyze Candidates
1. Click the "🚀 Analyze Candidates" button
2. System processes each resume through the complete pipeline:
   - PDF → Text Extraction → Field Extraction → AI Analysis
3. Results appear automatically

### Step 4: Review Results
1. **Top Candidates**: See ranked list by match score
2. **Detailed Analysis**: Click through individual candidate cards
3. **Summary Statistics**: View overall metrics and insights

## 🎨 Visual Design Features

### Color Scheme
- **Primary Colors**: Purple gradient (#667eea to #764ba2)
- **Success Colors**: Green (#10b981, #059669)
- **Warning Colors**: Orange (#f59e0b, #d97706)
- **Error Colors**: Red (#ef4444, #dc2626)
- **Neutral Colors**: Gray scale for backgrounds and text

### Typography
- **Headers**: Bold, modern fonts with gradient effects
- **Body Text**: Clean, readable typography
- **Metrics**: Large, prominent display for key numbers

### Layout
- **Wide Layout**: Optimized for desktop screens
- **Responsive Design**: Adapts to different screen sizes
- **Card-Based**: Modular design for easy scanning
- **Clear Hierarchy**: Logical information flow

### Interactive Elements
- **Hover Effects**: Subtle animations on buttons and cards
- **Loading States**: Clear feedback during processing
- **Progress Indicators**: Visual progress bars for match scores
- **Error States**: Clear error messages with helpful guidance

## 🔧 Technical Features

### Error Handling
- **File Upload Errors**: Clear messages for invalid files
- **Processing Errors**: Graceful handling of parsing failures
- **API Errors**: Fallback responses when LLM APIs fail
- **Validation**: Real-time validation of required fields

### Performance
- **Async Processing**: Non-blocking analysis
- **Progress Feedback**: Real-time processing status
- **Memory Management**: Temporary file cleanup
- **Error Recovery**: Continues processing even if individual files fail

### Security
- **File Validation**: Only accepts PDF files
- **Temporary Files**: Secure temporary file handling
- **Input Sanitization**: Safe handling of user input

## 📊 Data Flow

```
User Input → Streamlit Frontend → Backend Processing → AI Analysis → Results Display
     ↓              ↓                    ↓                ↓              ↓
Job Description → Text Processing → Resume Parsing → LLM Evaluation → Visual Results
Resume Files → File Upload → PDF Extraction → Field Analysis → Ranked Output
```

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. **Streamlit Cloud**: Upload to Streamlit Community Cloud
2. **Docker**: Containerize with Docker
3. **Heroku**: Deploy to Heroku with Streamlit buildpack
4. **AWS/GCP/Azure**: Deploy to cloud platforms

### Environment Variables for Production
```bash
# Required
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key

# Optional
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

## 🐛 Troubleshooting

### Common Issues

**Streamlit not found:**
```bash
pip install streamlit
```

**PDF files not processing:**
- Ensure pdfplumber is installed
- Check file permissions
- Verify PDF files are not corrupted

**AI analysis failing:**
- Check API keys are set correctly
- Verify internet connection
- Check API rate limits

**Style not loading:**
- Clear browser cache
- Check CSS in app.py
- Ensure Streamlit version supports custom CSS

### Debug Mode
Run with debug mode for detailed error messages:
```bash
streamlit run app.py --logger.level=debug
```

## 📈 Performance Optimization

### For Large Numbers of Resumes
- **Batch Processing**: Process resumes in smaller batches
- **Caching**: Implement result caching for repeated analyses
- **Async Processing**: Use async/await for better performance
- **Progress Tracking**: Show detailed progress for long operations

### For Production Use
- **Load Balancing**: Distribute processing across multiple instances
- **Database Integration**: Store results in a database
- **API Endpoints**: Create REST API for programmatic access
- **Monitoring**: Add performance monitoring and logging

## 🎉 Customization

### Branding
- Modify the header gradient colors
- Add company logo
- Customize the favicon
- Update the footer text

### Functionality
- Add new analysis metrics
- Implement custom scoring algorithms
- Add candidate comparison tools
- Integrate with HR systems

### Styling
- Customize the color scheme
- Modify card layouts
- Add animations and transitions
- Create dark mode support

---

**SmartHire AI** - Transforming resume screening with beautiful, intuitive interfaces.