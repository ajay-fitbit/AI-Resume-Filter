# AI Resume Filter - Multi-Agent System

## 🤖 What's New: Multi-Agent Architecture

This application has been upgraded to a **Multi-Agent System** where specialized AI agents work together to analyze resumes:

- **Resume Parser Agent**: Extracts structured data from documents
- **Skills Assessment Agent**: Evaluates candidate skills
- **Semantic Matching Agent**: AI-powered similarity analysis (Transformer models)
- **Red Flag Agent**: Detects career issues
- **Ranking Orchestrator**: Coordinates all agents

📖 **See [MULTI_AGENT_ARCHITECTURE.md](MULTI_AGENT_ARCHITECTURE.md) for detailed architecture**  
🚀 **See [RAG_INTEGRATION_GUIDE.md](RAG_INTEGRATION_GUIDE.md) for future RAG pipeline**

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server (5.7 or higher)
- At least 2GB RAM
- Internet connection (for downloading AI models)

## 🚀 Installation Steps

### 1. Clone or Download the Project

Ensure all project files are in: `C:\Users\Ajay\Downloads\AI Resume Filter`

### 2. Set Up MySQL Database

1. **Install MySQL** (if not already installed):
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Run the installer and follow the setup wizard
   - Remember the root password you set

2. **Start MySQL Service**:
   ```powershell
   net start MySQL
   ```

3. **Create Database User** (optional but recommended):
   ```sql
   CREATE USER 'resume_app'@'localhost' IDENTIFIED BY 'your_secure_password';
   GRANT ALL PRIVILEGES ON resume_filter_db.* TO 'resume_app'@'localhost';
   FLUSH PRIVILEGES;
   ```

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` file with your MySQL credentials:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=resume_filter_db
   
   FLASK_SECRET_KEY=your_random_secret_key_here
   FLASK_ENV=development
   ```

### 4. Install Python Dependencies

1. **Create Virtual Environment** (recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Upgrade pip**:
   ```powershell
   python -m pip install --upgrade pip
   ```

3. **Install Required Packages**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Download spaCy Language Model**:
   ```powershell
   python -m spacy download en_core_web_sm
   ```

### 5. Initialize Database

1. **Create database and tables**:
   ```powershell
   # Load the schema into MySQL
   Get-Content database_schema.sql | mysql -u root -p
   ```

2. **Convert tables to InnoDB** (required for foreign keys):
   ```powershell
   python convert_to_innodb.py
   ```

3. **Apply CASCADE DELETE constraints**:
   ```powershell
   python force_cascade_fix.py
   ```

This will:
- Create the database with UTF8MB4 encoding
- Set up all 5 required tables (InnoDB engine)
- Configure CASCADE DELETE relationships for data integrity

### 6. Run the Application

```powershell
python app.py
```

The application will start on: **http://localhost:5000**

## 📖 How to Use

### 1. Access the Dashboard
- Open your browser and go to: `http://localhost:5000`
- You'll see the main dashboard with statistics

### 2. Create Job Description
1. Click **"Create Job"** in the navigation
2. Enter the job title and full job description
3. Click **"Create Job Description"**

### 3. Upload Resumes
1. Click **"Upload Resumes"** in the navigation
2. Select the job description from the dropdown
3. Choose one or multiple resume files (PDF or DOCX)
4. Click **"Process Resumes"**

### 4. View Results
- The system will automatically:
  - Parse all resumes
  - Extract candidate information
  - Calculate match scores
  - Detect red flags
  - Rank candidates
- You'll be redirected to the candidates list

### 5. Review Candidates
- See ranked candidates with scores
- Click **"View Details"** for comprehensive analysis
- Review skills match, experience match, and red flags
- Read AI-generated explanations
- **Download Resume**: Click green download button to get original resume file
- Delete candidates using the red "Delete" button

### 6. Chat with AI Assistant (RAG System) 🆕
- Click **"💬 Resume Q&A"** in the navigation to access the AI chatbot
- Ask questions in natural language:
  - "Who is best for DevOps engineering?"
  - "Find candidates with database skills"
  - "Show me cloud experts"
  - "List all Python developers with 5+ years experience"
- Features:
  - **AI-Powered Semantic Search** using SentenceTransformer model
  - **8 Query Types**: Greetings, Help, Count, Comparison, Profile, Recommendation, Listing, Search
  - **Chat History**: Persists across page refreshes (50 messages)
  - **Markdown Formatting**: Clean, readable responses
  - **Match Scores**: Shows relevance percentage (2 decimal places)

### 7. Monitor Multi-Agent System
- Click **"🤖 Agents"** in the navigation to access the monitoring dashboard
- View status of all 5 agents (Resume Parser, Skills Assessor, Semantic Matcher, Red Flag Detector)
- See recent agent executions with timing information
- Click **"View Logs"** on any execution to see:
  - Agent scoring breakdown (Semantic 30%, Keywords 25%, Skills 30%, Experience 15%)
  - Matched vs missing skills
  - Red flags detected
  - Extracted resume data

### 8. Manage Jobs and Candidates
- Click **"All Jobs"** to view all job postings
- View how many candidates applied for each
- See average match scores
- Delete jobs using the red "Delete" button (removes all associated data)
- Click **"All Candidates"** to view all uploaded resumes across all jobs
- **Download Resumes**: Available on dashboard, candidates page, and chatbot results

## 🎯 Features

### Resume Download 🆕
- ✅ Download original resume files from multiple locations:
  - Dashboard (recent analyses)
  - Candidates page (desktop & mobile views)
  - AI Chatbot results
- ✅ Secure file serving with proper filename format
- ✅ Files served with original extension (.pdf, .docx, .doc)
- ✅ Green download buttons for easy identification

### AI-Powered RAG Chatbot 🆕
- ✅ **Natural Language Queries**: Ask questions conversationally
- ✅ **Semantic Understanding**: AI model understands context and meaning
- ✅ **SentenceTransformer Model**: all-MiniLM-L6-v2 (384-dim embeddings)
- ✅ **8 Query Types**: Greetings, Help, Count, Comparison, Profile, Recommendation, Listing, Search
- ✅ **Chat History**: localStorage persistence (50 messages)
- ✅ **Markdown Formatting**: Headers, bold, lists, code blocks
- ✅ **Hybrid Scoring**: AI semantic (0-30pts) + keyword matching + fuzzy logic
- ✅ **Intelligent Boosting**: Adaptive scoring based on query type
- ✅ **Fallback Mechanism**: Uses fuzzy matching if AI unavailable
- ✅ **Local Execution**: No API calls, fully offline
- ✅ **Download Resumes**: Download candidate resumes directly from chat results

### Resume Parsing
- ✅ Extracts name, email, phone
- ✅ Identifies **160+ technical skills** across categories:
  - Programming: Python, Java, JavaScript, TypeScript, Go, Rust, Scala, R, etc.
  - AI/ML: LLM, RAG, Machine Learning, TensorFlow, PyTorch, OpenAI, GPT, BERT
  - Cloud/DevOps: AWS, Azure, GCP, Docker, Kubernetes, CI/CD, Terraform
  - Data: SQL, PostgreSQL, MongoDB, Snowflake, ETL, Power BI, Tableau
  - And many more (see full list in `app/resume_parser.py`)
- ✅ Calculates years of experience (supports "20 years of IT experience", date ranges, etc.)
- ✅ Extracts education, certifications, projects
- ✅ Recognizes job titles and roles

### Job Matching
- ✅ Semantic similarity analysis (AI-powered)
- ✅ Keyword overlap calculation
- ✅ Skills matching percentage
- ✅ Experience requirement matching
- ✅ Overall match score (0-100%)

### Red Flag Detection
- ⚠️ Job hopping (average tenure < 2.5 years across 4+ jobs)
- ⚠️ Career gaps (2+ year gaps between employment periods)
- ⚠️ Missing required skills (from job description)
- ⚠️ Irrelevant work experience (doesn't align with job)
- ⚠️ Insufficient experience (below required years)

### Ranking System
- 🥇 **Top Tier**: 80-100% match
- 🥈 **Medium Tier**: 60-79% match
- 🥉 **Low Tier**: <60% match

## 🔧 Troubleshooting

### Database Connection Error
```
Error: Can't connect to MySQL server
```
**Solution**:
1. Check MySQL is running: `net start MySQL`
2. Verify credentials in `.env` file
3. Test connection: `mysql -u root -p`

### Import Errors
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**:
1. Activate virtual environment: `.\venv\Scripts\Activate.ps1`
2. Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use
```
Address already in use: Port 5000
```
**Solution**:
1. Stop the conflicting process
2. Or change port in `app.py`: `app.run(port=5001)`

### AI Model Download Issues
```
Error loading sentence transformer model
```
**Solution**:
1. Check internet connection
2. Manually download: `pip install sentence-transformers`
3. The app will still work with reduced accuracy

### File Upload Fails
```
File type not allowed
```
**Solution**:
- Only PDF, DOC, and DOCX files are supported
- Maximum file size: 16MB
- Ensure files are not corrupted

### CASCADE DELETE Not Working
```
Orphaned records in resume_data/analysis_results/red_flags tables
```
**Solution**:
1. Check table engine: `SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'resume_filter_db'`
2. If tables are MyISAM (doesn't support foreign keys), convert to InnoDB:
   ```powershell
   python convert_to_innodb.py
   ```
3. Apply CASCADE constraints:
   ```powershell
   python force_cascade_fix.py
   ```
4. Verify constraints: Check output shows "DELETE: CASCADE" for all foreign keys

## 📂 Project Structure

```
AI Resume Filter/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── database_schema.sql         # Database structure
├── .env                        # Environment variables (create this)
├── .env.example               # Environment template
├── README.md                  # This file
├── app/
│   ├── __init__.py            # Package initializer
│   ├── database.py            # Database utilities
│   ├── resume_parser.py       # Resume parsing logic
│   ├── job_matcher.py         # Matching algorithm
│   ├── red_flag_detector.py   # Red flag detection
│   ├── fix_encoding.py        # UTF8MB4 encoding fix
│   ├── templates/             # HTML templates
│   │   ├── base.html          # Base template with navigation
│   │   ├── index.html         # Dashboard
│   │   ├── create_job.html    # Job creation page
│   │   ├── upload.html        # Resume upload
│   │   ├── candidates.html    # Candidate list
│   │   ├── candidate_detail.html  # Detailed view
│   │   └── jobs.html          # Job listings
│   └── static/                # CSS and assets
├── uploads/                   # Uploaded resume storage
├── fix_cascade.py             # CASCADE DELETE fix script
└── check_cascade.py           # Verify CASCADE constraints
```

## 🔐 Security Notes

1. **Change the secret key** in `.env` before production
2. **Use strong MySQL passwords**
3. **Don't commit `.env` file** to version control
4. **Enable HTTPS** in production
5. **Limit file upload sizes** (currently 16MB)
6. **Validate all user inputs**
7. **CASCADE DELETE** ensures data integrity - deleting a job or candidate removes all related records
8. **Uploaded files** are stored in `uploads/` and deleted when candidates are removed

## 🎨 Customization

### Change Matching Weights
Edit `app/job_matcher.py`:
```python
weights = {
    'semantic_similarity': 0.30,  # Adjust these
    'keyword_match': 0.25,
    'skill_match': 0.30,
    'experience_match': 0.15
}
```

### Modify Tier Thresholds
Edit `_determine_tier` method in `app/job_matcher.py`:
```python
if score >= 80:  # Change threshold
    return "Top Tier"
```

### Add More Skills
Edit `_extract_skills` method in `app/resume_parser.py`

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Ensure database is properly configured
4. Check Python and MySQL logs for errors

## 🚀 Next Steps

After setup:
1. Test with sample resumes
2. Upload a real job description
3. Review the matching algorithm performance
4. Adjust weights if needed
5. Customize UI colors/branding (in templates)

---

**Congratulations! Your AI Resume Filter is ready to use! 🎉**
