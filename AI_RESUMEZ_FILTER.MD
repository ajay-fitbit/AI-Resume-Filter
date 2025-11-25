# AI Resume Filter – Complete Blueprint

## 1. Core Purpose

Automatically scan resumes and shortlist the best candidates based on:

- Skills (100+ technical skills including databases, BI tools, frameworks)
- Experience (years, job titles, career progression)
- Keywords and semantic matching
- Job description match score (semantic similarity)
- Red flags (job hopping, career gaps, missing skills)
- Role profiling and suitability analysis

## 2. Key Features

### A. Resume Parsing

Extract comprehensive data:

- **Contact Info:** Name, email, phone
- **Technical Skills:** 100+ skills including:
  - Databases: PostgreSQL, MySQL, MongoDB, Oracle, MariaDB, Neo4j, InfluxDB, CouchDB, etc.
  - SQL Languages: T-SQL, PL/SQL, Stored Procedures, Triggers, Views
  - BI Tools: Power BI, Tableau, QlikView, Qlik Sense, MicroStrategy, SAP BusinessObjects, Cognos, SSRS, SSIS, SSAS, DAX, Alteryx, Talend, Informatica, dbt, Airflow, etc.
  - Cloud: AWS, Azure, GCP, Docker, Kubernetes
  - Frameworks: React, Angular, Node.js, Django, Flask, Spring Boot
- **Experience:** Years, job titles, company names, date ranges
- **Education:** Degrees, institutions, graduation years
- **Certifications:** Professional certifications and courses
- **Projects:** Project descriptions and technologies used

**Tech:** Python, spaCy, regex patterns, custom NLP extraction

### B. Dual Upload Modes

#### 1. Job-Based Analysis
- Upload resumes against specific job descriptions
- Calculate match scores (0-100) using semantic similarity
- Rank candidates by relevance to JD
- Show skill gaps and missing requirements

#### 2. Bulk Upload Analysis
- Upload resumes independently (no JD required)
- AI profiles candidates for best-fit roles:
  - Full Stack Developer
  - DevOps Engineer
  - Data Scientist
  - Cloud Architect
  - QA Engineer
  - Database Administrator
  - Mobile Developer
  - AI/ML Engineer
  - Frontend/Backend Developer
- Comprehensive skills analysis with expandable badges
- Experience-based categorization

### C. Red Flag Detection

Multi-level severity system detecting:

- **High Severity:**
  - Significant career gaps (>1 year, with merged overlapping periods)
  - Excessive job hopping (>4 jobs in 3 years)
  - Critical missing skills (required skills absent)
  
- **Medium Severity:**
  - Moderate career gaps (6-12 months)
  - Frequent job changes (3-4 jobs in 3 years)
  - Partial skill gaps
  - Education mismatches

**Smart Detection:** Validates resume text, merges overlapping employment periods, provides detailed recommendations

### D. AI-Powered Chatbot (RAG Agent)

Intelligent resume querying system:

- **Natural Language Queries:**
  - "Who is good fit for database roles?"
  - "Show me DevOps candidates"
  - "Find data scientists with 5+ years experience"
  - "Who knows React and Node.js?"

- **Role-Based Intelligence:** Maps generic terms to relevant skills:
  - DevOps → Docker, Kubernetes, Jenkins, CI/CD, Terraform, Ansible
  - Database → SQL, MySQL, PostgreSQL, MongoDB, Oracle
  - Data Science → Python, R, SQL, Machine Learning, Pandas, Tableau
  - BI → Power BI, Tableau, SQL, Excel, ETL, Data Analysis

- **AI Semantic Search:** Uses SentenceTransformer (all-MiniLM-L6-v2) for intelligent matching

- **Context-Aware:** Shows resume counts per job, filters by job descriptions

### E. Interactive HR Dashboard

**Homepage Features:**
- Real-time statistics (total resumes, jobs, analyses)
- Recent candidate profile cards with:
  - Avatar with candidate initial
  - AI-generated role profile
  - Experience level and skills count
  - Red flag indicators
  - Color-coded borders (red for flags, green for senior, blue default)
  - Quick access to full details
- Recent job-based analyses with match scores
- One-click navigation to bulk analysis or chatbot

**Bulk Analysis Page:**
- Comprehensive candidate cards (desktop + mobile optimized)
- Expandable skills badges (click "+X more" to show all)
- Detailed red flag breakdowns with severity levels
- Quick stats: total candidates, senior level count, flagged profiles, avg skills
- Download resumes, view full profiles, delete candidates

**Candidate Detail Page:**
- Full resume information
- All red flags with recommendations
- Complete skills list with role profiling
- Contact information and experience timeline
- Resume download option

**Job Analysis Page:**
- Match score visualization
- Ranked candidate list
- Skill gap analysis
- Top matched skills display
- Side-by-side JD comparison

### F. Advanced Features

- **Multi-Agent Architecture:** Orchestrator coordinates specialized agents (skills, semantic, red flags, RAG)
- **Responsive Design:** Mobile-optimized views for all pages
- **Batch Processing:** Handle multiple resume uploads simultaneously
- **Database Persistence:** MySQL storage with candidates, resume_data, red_flags, job_descriptions, analysis_results tables
- **Error Handling:** Resume text validation, duplicate detection, graceful fallbacks
- **Export Capabilities:** Download individual resumes or full analysis reports