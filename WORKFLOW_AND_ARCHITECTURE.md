# AI Resume Filter - Application Workflow & Architecture

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Application Architecture](#application-architecture)
3. [User Workflows](#user-workflows)
4. [Multi-Agent System Architecture](#multi-agent-system-architecture)
5. [RAG System Workflow](#rag-system-workflow)
6. [Database Architecture](#database-architecture)
7. [Component Interactions](#component-interactions)
8. [Technology Stack](#technology-stack)

---

## 🎯 System Overview

**AI Resume Filter** is an intelligent resume screening system that uses a multi-agent architecture combined with AI-powered semantic search to automate candidate evaluation, ranking, and natural language querying.

### Key Capabilities
- **Automated Resume Parsing**: Extract structured data from PDF/DOCX files
- **AI-Powered Matching**: Semantic similarity using SentenceTransformer embeddings
- **Multi-Agent Analysis**: 5 specialized agents for comprehensive evaluation
- **Natural Language Chat**: RAG-based conversational interface for querying candidates
- **Red Flag Detection**: Identify potential issues in candidate profiles
- **Intelligent Ranking**: Multi-factor scoring with tier classification

---

## 🏗️ Application Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │Dashboard │  │Create Job│  │  Upload  │  │  RAG Chatbot     │   │
│  │          │  │          │  │ Resumes  │  │  (Q&A Interface) │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        FLASK APPLICATION                             │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                     Route Handlers                             │ │
│  │  /  /create_job  /upload  /candidates  /rag_chat  /api/*     │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                                            ↓
┌────────────────────────────┐      ┌──────────────────────────────┐
│   MULTI-AGENT SYSTEM       │      │      RAG AGENT SYSTEM        │
│                            │      │                              │
│  ┌──────────────────────┐ │      │  ┌────────────────────────┐ │
│  │ Ranking Orchestrator │ │      │  │   RAG Agent            │ │
│  │      Agent           │ │      │  │                        │ │
│  └──────────┬───────────┘ │      │  │ • Query Understanding  │ │
│             │              │      │  │ • AI Semantic Search   │ │
│  ┌──────────┴───────────┐ │      │  │ • Candidate Ranking    │ │
│  │  Resume Parser       │ │      │  │ • Answer Generation    │ │
│  │  Skills Assessment   │ │      │  └────────────────────────┘ │
│  │  Semantic Matching   │ │      │                              │
│  │  Red Flag Detection  │ │      │  🤖 AI Model:                │
│  └──────────────────────┘ │      │  SentenceTransformer         │
│                            │      │  all-MiniLM-L6-v2            │
│  🤖 AI Model:              │      │  384-dim embeddings          │
│  SentenceTransformer       │      └──────────────────────────────┘
│  all-MiniLM-L6-v2          │
└────────────────────────────┘
                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        DATABASE LAYER                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      MySQL Database                           │  │
│  │  • candidates  • resume_data  • analysis_results  • jobs     │  │
│  │  • red_flags   • agent_execution_logs                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Layer Architecture

#### **1. Presentation Layer (Frontend)**
- HTML5/CSS3 with Bootstrap styling
- Responsive design (mobile, tablet, desktop)
- JavaScript for dynamic interactions
- Markdown rendering in chat interface
- localStorage for chat history persistence

#### **2. Application Layer (Flask)**
- RESTful API endpoints
- Request routing and validation
- Session management
- File upload handling
- Error handling and logging

#### **3. Business Logic Layer**
- **Multi-Agent System**: Resume analysis workflow
- **RAG System**: Natural language query processing
- **AI Models**: Semantic matching and embeddings

#### **4. Data Layer**
- MySQL relational database
- Connection pooling
- Foreign key relationships with CASCADE DELETE
- UTF8MB4 encoding for emoji support

---

## 👤 User Workflows

### Workflow 1: Job Description Creation

```
START
  ↓
User accesses "Create Job" page
  ↓
User enters:
  • Job Title
  • Full Job Description
  ↓
User clicks "Create Job Description"
  ↓
Flask validates input
  ↓
Job saved to database (jobs table)
  ↓
Success message displayed
  ↓
User redirected to Jobs list
  ↓
END
```

**Database Operations**:
- `INSERT INTO jobs (title, description, created_at)`

---

### Workflow 2: Resume Upload & Analysis

```
START
  ↓
User accesses "Upload Resumes" page
  ↓
User selects Job Description from dropdown
  ↓
User uploads one or more PDF/DOCX files
  ↓
User clicks "Process Resumes"
  ↓
Flask receives files
  ↓
FOR EACH resume file:
  │
  ├─→ Save file to uploads/ directory
  │
  ├─→ Create candidate record in database
  │
  ├─→ Initialize Multi-Agent System
  │   │
  │   ├─→ AGENT 1: Resume Parser Agent
  │   │   • Extract text from PDF/DOCX
  │   │   • Parse name, email, phone
  │   │   • Extract skills (160+ skills recognized)
  │   │   • Calculate experience years
  │   │   • Extract education, certifications
  │   │   • Store in resume_data table
  │   │
  │   ├─→ AGENT 2: Skills Assessment Agent
  │   │   • Compare candidate skills vs job requirements
  │   │   • Fuzzy matching for skill variations
  │   │   • Calculate skill match score (0-100%)
  │   │   • Identify matched, missing, additional skills
  │   │
  │   ├─→ AGENT 3: Semantic Matching Agent
  │   │   • Load AI model (SentenceTransformer)
  │   │   • Encode resume text → 384-dim vector
  │   │   • Encode job description → 384-dim vector
  │   │   • Calculate cosine similarity
  │   │   • Generate semantic similarity score
  │   │
  │   ├─→ AGENT 4: Red Flag Agent
  │   │   • Detect job hopping (>3 jobs in 2 years)
  │   │   • Identify career gaps (>2 years)
  │   │   • Check missing critical skills
  │   │   • Verify experience requirements
  │   │   • Assign severity levels
  │   │
  │   └─→ AGENT 5: Ranking Orchestrator Agent
  │       • Collect all agent results
  │       • Calculate weighted final score:
  │         - Semantic: 30%
  │         - Keywords: 25%
  │         - Skills: 30%
  │         - Experience: 15%
  │       • Assign tier (Top/Medium/Low)
  │       • Generate explanation
  │       • Store in analysis_results table
  │
  └─→ Log agent execution details
  ↓
Display results with ranked candidates
  ↓
User can view detailed analysis
  ↓
END
```

**Database Operations**:
- `INSERT INTO candidates (name, email, phone, resume_path, job_id)`
- `INSERT INTO resume_data (candidate_id, skills, experience_years, education, raw_text)`
- `INSERT INTO analysis_results (candidate_id, job_id, match_score, skills_score, semantic_score, tier, explanation)`
- `INSERT INTO red_flags (candidate_id, flag_type, severity, description)`

**Time Complexity**: ~2-3 seconds per resume

---

### Workflow 3: RAG Chatbot Query

```
START
  ↓
User accesses "Resume Q&A" page
  ↓
[OPTIONAL] User selects Job Context from dropdown
  ↓
User types natural language question
Examples:
  • "Who is best for DevOps engineering?"
  • "Find candidates with database skills"
  • "Show me cloud experts"
  • "List all Python developers with 5+ years"
  ↓
User clicks "Send" or presses Enter
  ↓
Frontend sends POST to /api/rag/query
  ↓
RAG Agent processes query:
  │
  ├─→ STEP 1: Query Understanding
  │   • Detect query type (8 types):
  │     1. Greeting ("Hi", "Hello")
  │     2. Help ("What can you do?")
  │     3. Count ("How many candidates...")
  │     4. Comparison ("Who is better: A vs B")
  │     5. Specific Person ("Show me [name] profile")
  │     6. Recommendation ("Who should I hire...")
  │     7. Listing ("List all...")
  │     8. Search ("Find candidates...")
  │   • Extract skills mentioned
  │   • Extract experience requirements
  │   • Extract keywords
  │
  ├─→ STEP 2: Candidate Retrieval
  │   • Fetch candidates from database
  │   • Filter by job_id if context selected
  │   • Load resume data for each candidate
  │
  ├─→ STEP 3: AI Semantic Matching
  │   • Load SentenceTransformer model (lazy-load)
  │   • Encode user question → 384-dim vector
  │   • FOR EACH candidate:
  │     - Create profile text:
  │       "Skills: Python, AWS. Experience: 5 years. Summary: ..."
  │     - Encode profile → 384-dim vector
  │     - Calculate cosine similarity with question
  │     - Convert to semantic score (0-30 points)
  │
  ├─→ STEP 4: Hybrid Scoring
  │   • Combine multiple factors:
  │     - Exact skill match: 30 points
  │     - Fuzzy skill match: 20 points
  │     - Experience match: 25 points
  │     - Keyword match: 5 points each
  │     - AI semantic score: 0-30 points (adaptive)
  │   • Apply intelligent boosting:
  │     - Skill queries: 15 points max
  │     - General queries: 30 points max
  │   • Fallback to fuzzy matching if AI fails
  │
  ├─→ STEP 5: Ranking & Filtering
  │   • Sort candidates by total score (descending)
  │   • Apply minimum threshold:
  │     - Skill queries: 20 points
  │     - General queries: 25 points
  │   • Select top 10 matches
  │
  └─→ STEP 6: Answer Generation
      • Generate natural language response
      • Format in Markdown:
        - Headers (##, ###)
        - Bold text (**)
        - Bullet lists (•)
        - Code blocks (`)
      • Include candidate details
      • Show match scores (2 decimal places)
  ↓
Response sent back to frontend
  ↓
Frontend renders:
  • Markdown-formatted answer
  • Candidate result cards
  • Match percentages with progress bars
  ↓
Chat saved to localStorage (50 message limit)
  ↓
END
```

**Database Operations**:
- `SELECT * FROM candidates WHERE job_id = ? OR job_id IS NULL`
- `JOIN resume_data ON candidates.id = resume_data.candidate_id`
- `JOIN analysis_results ON candidates.id = analysis_results.candidate_id`

**Time Complexity**: <1 second for 100 candidates

---

### Workflow 4: Candidate Detail View

```
START
  ↓
User clicks "View Details" on candidate
  ↓
Flask fetches from database:
  • Candidate info
  • Resume data
  • Analysis results
  • Red flags
  • Job description
  ↓
Display comprehensive profile:
  • Personal info (name, email, phone)
  • Skills breakdown (matched, missing, additional)
  • Experience details
  • Match scores (overall, skills, experience, semantic)
  • Tier classification
  • Red flags with severity
  • AI-generated explanation
  ↓
User can download resume or delete candidate
  ↓
END
```

---

### Workflow 5: Job & Candidate Management

```
┌─────────────────────────────────────────┐
│         Job Management                  │
├─────────────────────────────────────────┤
│ View All Jobs                           │
│   ↓                                     │
│ Display:                                │
│   • Job title                           │
│   • Description preview                 │
│   • Candidate count                     │
│   • Average match score                 │
│   • Created date                        │
│   ↓                                     │
│ Actions:                                │
│   • View job details                    │
│   • View candidates for job             │
│   • Delete job (CASCADE deletes:        │
│     - All candidates                    │
│     - Resume data                       │
│     - Analysis results                  │
│     - Red flags)                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│      Candidate Management               │
├─────────────────────────────────────────┤
│ View All Candidates                     │
│   ↓                                     │
│ Display:                                │
│   • Ranked list with scores             │
│   • Filter by job                       │
│   • Sort by rank/score/tier             │
│   ↓                                     │
│ Actions:                                │
│   • View full profile                   │
│   • Delete candidate (CASCADE deletes:  │
│     - Resume data                       │
│     - Analysis results                  │
│     - Red flags                         │
│     - Uploaded file)                    │
└─────────────────────────────────────────┘
```

---

## 🤖 Multi-Agent System Architecture

### Agent Hierarchy

```
                    ┌─────────────────────────────────┐
                    │  RankingOrchestratorAgent       │
                    │  (Coordinator)                  │
                    │                                 │
                    │  • Manages workflow             │
                    │  • Maintains shared state       │
                    │  • Calculates final score       │
                    │  • Generates explanation        │
                    └────────────┬────────────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
        ┌────────▼────────┐ ┌───▼────────┐ ┌───▼───────────┐
        │ ResumeParser    │ │ Skills     │ │  Semantic     │
        │ Agent           │ │ Assessment │ │  Matching     │
        │                 │ │ Agent      │ │  Agent        │
        │ • PyPDF2        │ │            │ │               │
        │ • python-docx   │ │ • FuzzyWuz │ │ • Sentence    │
        │ • spaCy NLP     │ │ • Levensh  │ │   Transform   │
        │ • Regex         │ │ • 160+     │ │ • 384-dim     │
        │                 │ │   skills   │ │   embeddings  │
        └─────────────────┘ └────────────┘ └───────────────┘
                 │
                 │
        ┌────────▼────────┐
        │  RedFlag        │
        │  Agent          │
        │                 │
        │ • Job hopping   │
        │ • Career gaps   │
        │ • Missing skills│
        │ • Experience    │
        └─────────────────┘
```

### Agent Communication Flow

```
1. User uploads resume
   ↓
2. Orchestrator receives file path + job description
   ↓
3. Orchestrator creates AgentState (shared memory)
   ↓
4. Orchestrator executes agents sequentially:
   
   ┌─────────────────────────────────────────────┐
   │  Phase 1: Data Extraction                   │
   └─────────────────────────────────────────────┘
   ResumeParserAgent.execute()
     Input:  {"file_path": "/path/to/resume.pdf"}
     Output: {
       "name": "John Doe",
       "email": "john@example.com",
       "skills": ["Python", "AWS", "Docker"],
       "experience_years": 5,
       "raw_text": "..."
     }
     → Stored in AgentState
   
   ┌─────────────────────────────────────────────┐
   │  Phase 2: Skills Analysis                   │
   └─────────────────────────────────────────────┘
   SkillsAssessmentAgent.execute()
     Input:  {
       "resume_skills": ["Python", "AWS", "Docker"],
       "job_description": "Looking for Python dev..."
     }
     Output: {
       "skill_match_score": 80.0,
       "matched_skills": ["Python", "AWS"],
       "missing_skills": ["Kubernetes"],
       "additional_skills": ["Docker"]
     }
     → Stored in AgentState
   
   ┌─────────────────────────────────────────────┐
   │  Phase 3: AI Semantic Matching              │
   └─────────────────────────────────────────────┘
   SemanticMatchingAgent.execute()
     Input:  {
       "resume_text": "Full resume text...",
       "job_description": "Job description..."
     }
     Process:
       1. Load SentenceTransformer model
       2. Encode resume → [0.234, -0.567, ..., 0.123] (384 dims)
       3. Encode JD → [0.345, -0.234, ..., 0.456] (384 dims)
       4. Calculate cosine_similarity(resume_vec, jd_vec)
     Output: {
       "semantic_score": 78.45,
       "keyword_score": 65.23,
       "embedding_similarity": 0.7845
     }
     → Stored in AgentState
   
   ┌─────────────────────────────────────────────┐
   │  Phase 4: Red Flag Detection                │
   └─────────────────────────────────────────────┘
   RedFlagAgent.execute()
     Input:  {
       "resume_data": {...},
       "job_description": "...",
       "required_experience": 5
     }
     Output: {
       "red_flags": [
         {
           "type": "career_gap",
           "severity": "medium",
           "description": "2.5 year gap between jobs"
         }
       ],
       "high_severity_count": 0,
       "medium_severity_count": 1
     }
     → Stored in AgentState
   
   ┌─────────────────────────────────────────────┐
   │  Phase 5: Final Ranking & Scoring           │
   └─────────────────────────────────────────────┘
   Orchestrator.calculate_final_score()
     Input: All agent results from AgentState
     Process:
       final_score = (
         semantic_score * 0.30 +
         keyword_score * 0.25 +
         skill_score * 0.30 +
         experience_score * 0.15
       )
       
       tier = determine_tier(final_score)
         • ≥75: "Top Tier"
         • 50-74: "Medium Tier"
         • <50: "Low Tier"
     
     Output: {
       "overall_score": 76.50,
       "tier": "Top Tier",
       "explanation": "Strong match with excellent Python...",
       "component_scores": {
         "semantic": 78.45,
         "keyword": 65.23,
         "skills": 80.0,
         "experience": 75.0
       }
     }
   
5. Orchestrator saves all results to database
   ↓
6. Return complete analysis to user
```

### Agent State Management

```python
class AgentState:
    """Shared memory across all agents"""
    
    data = {
        "file_path": "/uploads/john_doe.pdf",
        "job_description": "...",
        "required_experience": 5
    }
    
    agent_results = {
        "ResumeParserAgent": {...},
        "SkillsAssessmentAgent": {...},
        "SemanticMatchingAgent": {...},
        "RedFlagAgent": {...}
    }
    
    errors = []
    execution_logs = [
        {"agent": "ResumeParser", "time": 0.234, "status": "success"},
        {"agent": "SkillsAssessment", "time": 0.567, "status": "success"},
        ...
    ]
```

---

## 💬 RAG System Workflow

### RAG Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    USER QUESTION                                │
│  "Find candidates with Python and 5 years of cloud experience" │
└───────────────────────────┬────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│                  RAG Agent Query Processing                     │
├────────────────────────────────────────────────────────────────┤
│  STEP 1: Intent Detection                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Pattern Matching:                                        │ │
│  │  ✓ Type: "search" (matches "find candidates...")        │ │
│  │  ✓ Skills: ["Python"]                                   │ │
│  │  ✓ Experience: 5 years                                  │ │
│  │  ✓ Keywords: ["cloud"]                                  │ │
│  │  ✓ Expanded: cloud → [AWS, Azure, GCP]                 │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│              STEP 2: Candidate Retrieval                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ SQL Query:                                               │ │
│  │   SELECT c.*, r.*, a.*                                   │ │
│  │   FROM candidates c                                      │ │
│  │   JOIN resume_data r ON c.id = r.candidate_id           │ │
│  │   JOIN analysis_results a ON c.id = a.candidate_id      │ │
│  │   WHERE (job_id = ? OR job_id IS NULL)                  │ │
│  │                                                          │ │
│  │ Result: [John, Sarah, Michael, ...] (100 candidates)    │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│         STEP 3: AI Semantic Matching (SentenceTransformer)     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Load Model: all-MiniLM-L6-v2                            │ │
│  │                                                          │ │
│  │ Question Encoding:                                       │ │
│  │   Input: "Find candidates with Python and 5 years..."   │ │
│  │   Output: [0.123, -0.456, 0.789, ..., -0.234]          │ │
│  │           (384 dimensions)                               │ │
│  │                                                          │ │
│  │ For Each Candidate:                                      │ │
│  │   1. Create profile text:                               │ │
│  │      "Skills: Python, Java, AWS, Docker.                │ │
│  │       Experience: 5 years. Summary: Backend dev..."      │ │
│  │                                                          │ │
│  │   2. Encode profile → 384-dim vector                    │ │
│  │                                                          │ │
│  │   3. Calculate cosine similarity:                       │ │
│  │      similarity = dot(question_vec, profile_vec) /      │ │
│  │                   (norm(q_vec) * norm(p_vec))           │ │
│  │                                                          │ │
│  │   4. Convert to semantic score:                         │ │
│  │      semantic_score = similarity * 30  (0-30 points)    │ │
│  │                                                          │ │
│  │ John's similarity: 0.58 → 17.5 points                   │ │
│  │ Sarah's similarity: 0.42 → 12.6 points                  │ │
│  │ Michael's similarity: 0.29 → 8.7 points                 │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│              STEP 4: Hybrid Scoring System                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ For John Doe:                                            │ │
│  │                                                          │ │
│  │ Component Scores:                                        │ │
│  │   ✓ Exact Skill Match (Python): 30 points              │ │
│  │   ✓ Fuzzy Match (AWS for cloud): 15 points             │ │
│  │   ✓ Experience (5 years): 25 points                    │ │
│  │   ✓ Keywords (2 matched): 10 points                    │ │
│  │   ✓ AI Semantic Score: 17.5 points                     │ │
│  │   ─────────────────────────────────────                 │ │
│  │   Total: 97.5 points                                    │ │
│  │                                                          │ │
│  │ Intelligent Boosting Applied:                            │ │
│  │   • Query type: "search with skills"                    │ │
│  │   • Boost limit: 15 points (skill-specific query)      │ │
│  │   • Semantic contribution capped at 15 points           │ │
│  │   • Final Score: 95.0 points                            │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│           STEP 5: Ranking & Filtering                           │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ All Candidate Scores:                                    │ │
│  │   1. John Doe: 95.0                                     │ │
│  │   2. Sarah Smith: 87.3                                  │ │
│  │   3. Michael Johnson: 76.8                              │ │
│  │   4. Emma Wilson: 65.2                                  │ │
│  │   ... (96 more candidates below threshold)              │ │
│  │                                                          │ │
│  │ Apply Threshold:                                         │ │
│  │   • Minimum: 20 points (skill queries)                  │ │
│  │   • Filter: Keep candidates >= 20                       │ │
│  │                                                          │ │
│  │ Select Top 10 Matches                                    │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│           STEP 6: Answer Generation (Markdown)                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Generated Response:                                      │ │
│  │                                                          │ │
│  │ ## Found 4 Candidates                                   │ │
│  │                                                          │ │
│  │ I found **4 excellent candidates** with Python and      │ │
│  │ cloud experience:                                        │ │
│  │                                                          │ │
│  │ **Top Match:**                                          │ │
│  │ • **John Doe** - 95.00% match                           │ │
│  │   - Skills: Python, AWS, Docker, Kubernetes             │ │
│  │   - Experience: 5 years                                 │ │
│  │                                                          │ │
│  │ **Other Strong Matches:**                               │ │
│  │ • Sarah Smith - 87.30% match                            │ │
│  │ • Michael Johnson - 76.80% match                        │ │
│  │ • Emma Wilson - 65.20% match                            │ │
│  │                                                          │ │
│  │ All candidates have the required `Python` skills and    │ │
│  │ cloud platform experience!                              │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│                 Frontend Rendering                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 1. Parse Markdown:                                       │ │
│  │    ## → <h2 style="color: #667eea;">                    │ │
│  │    ** → <strong style="color: #667eea;">                │ │
│  │    • → <li> with styled bullets                         │ │
│  │                                                          │ │
│  │ 2. Render Candidate Cards:                              │ │
│  │    ┌─────────────────────────────────────┐             │ │
│  │    │ 👤 John Doe        95.00% match    │             │ │
│  │    │ john@example.com                    │             │ │
│  │    │ Skills: Python, AWS, Docker         │             │ │
│  │    │ Experience: 5 years                 │             │ │
│  │    │ [████████████████████░░] 95%        │             │ │
│  │    └─────────────────────────────────────┘             │ │
│  │                                                          │ │
│  │ 3. Save to localStorage (chat history)                  │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

### Query Type Handling Matrix

| Query Type | Example | Processing |
|------------|---------|------------|
| **Greeting** | "Hi", "Hello" | Return welcome message, no DB query |
| **Help** | "What can you do?" | Return capabilities list |
| **Count** | "How many Python devs?" | Extract skills → COUNT query → Return number |
| **Comparison** | "Who is better: John vs Sarah?" | Extract names → Compare scores → Return winner |
| **Specific Person** | "Show me John's profile" | Name detection → Fetch full profile → Display |
| **Recommendation** | "Who should I hire for DevOps?" | Extract requirements → AI ranking → Top 3 |
| **Listing** | "List all SQL developers" | Extract skills → Filter → Return all matches |
| **Search** | "Find cloud experts" | Full hybrid scoring → Top 10 |

---

## 🗄️ Database Architecture

### Entity Relationship Diagram

```
┌─────────────────────────┐
│        jobs             │
├─────────────────────────┤
│ PK │ id               │
│    │ title            │
│    │ description      │
│    │ created_at       │
└──────────┬──────────────┘
           │ 1
           │
           │ N
┌──────────▼──────────────┐
│     candidates          │
├─────────────────────────┤
│ PK │ id               │
│ FK │ job_id           │───────┐
│    │ name             │       │ CASCADE
│    │ email            │       │ DELETE
│    │ phone            │       │
│    │ resume_path      │       │
│    │ created_at       │       │
└──────────┬──────────────┘       │
           │ 1                    │
           ├──────────────────────┘
           │
    ┌──────┴───────┬────────────┬──────────────┐
    │ 1            │ 1          │ 1            │
    │ N            │ N          │ N            │
    ▼              ▼            ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│resume_data │ │analysis_   │ │ red_flags  │ │agent_exec  │
│            │ │ results    │ │            │ │_logs       │
├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤
│PK│id      │ │PK│id      │ │PK│id      │ │PK│id      │
│FK│cand_id │ │FK│cand_id │ │FK│cand_id │ │FK│cand_id │
│  │skills  │ │FK│job_id  │ │  │type    │ │  │agent   │
│  │exp_yrs │ │  │match   │ │  │severity│ │  │output  │
│  │educatn │ │  │tier    │ │  │desc    │ │  │time    │
│  │raw_txt │ │  │explana │ │  │created │ │  │created │
└────────────┘ └────────────┘ └────────────┘ └────────────┘

CASCADE DELETE Rules:
• Delete job → Deletes all candidates + related data
• Delete candidate → Deletes resume_data, analysis_results, 
                     red_flags, agent_execution_logs
```

### Table Schemas

#### **jobs**
```sql
CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_title (title)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### **candidates**
```sql
CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    resume_path VARCHAR(500),
    job_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    INDEX idx_name (name),
    INDEX idx_job_id (job_id)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### **resume_data**
```sql
CREATE TABLE resume_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    skills TEXT,
    experience_years INT,
    education TEXT,
    certifications TEXT,
    raw_text LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    INDEX idx_candidate_id (candidate_id),
    FULLTEXT idx_skills (skills)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### **analysis_results**
```sql
CREATE TABLE analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    match_score DECIMAL(5,2),
    skills_score DECIMAL(5,2),
    experience_match_score DECIMAL(5,2),
    semantic_score DECIMAL(5,2),
    keyword_score DECIMAL(5,2),
    tier VARCHAR(50),
    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    INDEX idx_candidate_id (candidate_id),
    INDEX idx_job_id (job_id),
    INDEX idx_match_score (match_score DESC)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### **red_flags**
```sql
CREATE TABLE red_flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    flag_type VARCHAR(100),
    severity ENUM('low', 'medium', 'high'),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    INDEX idx_candidate_id (candidate_id),
    INDEX idx_severity (severity)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 🔗 Component Interactions

### Resume Upload Flow Sequence

```
User Browser          Flask App          Multi-Agent System          Database
     │                    │                      │                      │
     ├─── POST /upload ──→│                      │                      │
     │    (resume files)  │                      │                      │
     │                    ├─ Save files to disk ─┤                      │
     │                    │                      │                      │
     │                    ├─ INSERT candidate ───────────────────────→ │
     │                    │                      │                      │
     │                    ├─ Initialize Orchestrator ─→                │
     │                    │                      │                      │
     │                    │              ┌───────┴────────┐             │
     │                    │              │ Parse Resume   │             │
     │                    │              │ (Agent 1)      │             │
     │                    │              └───────┬────────┘             │
     │                    │                      │                      │
     │                    │              ┌───────┴────────┐             │
     │                    │              │ Assess Skills  │             │
     │                    │              │ (Agent 2)      │             │
     │                    │              └───────┬────────┘             │
     │                    │                      │                      │
     │                    │              ┌───────┴────────┐             │
     │                    │              │ AI Semantic    │             │
     │                    │              │ Match (Agent 3)│             │
     │                    │              └───────┬────────┘             │
     │                    │                      │                      │
     │                    │              ┌───────┴────────┐             │
     │                    │              │ Detect Flags   │             │
     │                    │              │ (Agent 4)      │             │
     │                    │              └───────┬────────┘             │
     │                    │                      │                      │
     │                    │              ┌───────┴────────┐             │
     │                    │              │ Calculate Score│             │
     │                    │              │ (Orchestrator) │             │
     │                    │              └───────┬────────┘             │
     │                    │                      │                      │
     │                    │   ← Return results ──┤                      │
     │                    │                      │                      │
     │                    ├─ INSERT resume_data ──────────────────────→│
     │                    ├─ INSERT analysis_results ──────────────────→│
     │                    ├─ INSERT red_flags ────────────────────────→│
     │                    │                      │                      │
     │←─── 200 OK ────────┤                      │                      │
     │   (redirect to     │                      │                      │
     │    candidates)     │                      │                      │
```

### RAG Query Flow Sequence

```
User Browser          Flask API          RAG Agent          AI Model          Database
     │                    │                  │                 │                 │
     ├─ POST /api/rag/query ─→              │                 │                 │
     │   {"question": "..."}                 │                 │                 │
     │                    │                  │                 │                 │
     │                    ├─ rag_agent.query() ─→             │                 │
     │                    │                  │                 │                 │
     │                    │                  ├─ Detect intent ─┤                 │
     │                    │                  ├─ Extract skills─┤                 │
     │                    │                  │                 │                 │
     │                    │                  ├─ SELECT candidates ──────────────→│
     │                    │                  │                 │                 │
     │                    │                  │←─ Return rows ──────────────────┤
     │                    │                  │                 │                 │
     │                    │                  ├─ Load model ───→│                 │
     │                    │                  │                 │                 │
     │                    │                  ├─ Encode question →                │
     │                    │                  │                 │                 │
     │                    │         FOR EACH CANDIDATE:        │                 │
     │                    │                  ├─ Create profile ─┤                 │
     │                    │                  ├─ Encode profile →│                 │
     │                    │                  ├─ Calc similarity →                │
     │                    │                  │←─ Score (0-1) ───┤                 │
     │                    │                  │                 │                 │
     │                    │                  ├─ Apply hybrid scoring ─┤          │
     │                    │                  ├─ Rank candidates ┤                 │
     │                    │                  ├─ Generate answer ┤                 │
     │                    │                  │                 │                 │
     │                    │←─ Return JSON ───┤                 │                 │
     │                    │   {answer, candidates}             │                 │
     │                    │                  │                 │                 │
     │←─── 200 OK ────────┤                  │                 │                 │
     │   {"answer": "...",                   │                 │                 │
     │    "candidates": [...]}               │                 │                 │
     │                    │                  │                 │                 │
     ├─ Render markdown ─┤                  │                 │                 │
     ├─ Save to localStorage ─┤              │                 │                 │
```

---

## 🛠️ Technology Stack

### Backend Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Web Framework** | Flask | 3.0.0 | HTTP routing, request handling |
| **Database** | MySQL | 8.0+ | Relational data storage |
| **DB Connector** | mysql-connector-python | 8.2.0 | Python-MySQL interface |
| **PDF Parsing** | PyPDF2 | 3.0.1 | Extract text from PDF resumes |
| **Word Parsing** | python-docx | 1.1.0 | Extract text from DOCX files |
| **NLP** | spaCy | 3.7.2 | Natural language processing |
| **AI Embeddings** | sentence-transformers | 3.0.1 | Semantic embeddings (384-dim) |
| **ML Utilities** | scikit-learn | 1.3.2 | Cosine similarity, TF-IDF |
| **Array Operations** | numpy | 1.26.2 | Vector operations |
| **Fuzzy Matching** | fuzzywuzzy | 0.18.0 | Skill variation matching |
| **String Similarity** | python-Levenshtein | 0.21.1 | Fast edit distance |
| **Data Processing** | pandas | 2.1.4 | Data manipulation |
| **Environment** | python-dotenv | 1.0.0 | Environment variable management |
| **File Handling** | Werkzeug | 3.0.1 | Secure filename handling |

### Frontend Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **HTML** | HTML5 | Semantic markup |
| **CSS** | CSS3 | Styling, gradients, animations |
| **JavaScript** | Vanilla ES6+ | Dynamic interactions, AJAX |
| **Template Engine** | Jinja2 | Server-side rendering |
| **Icons** | Unicode Emojis | Visual indicators |
| **Storage** | localStorage | Chat history persistence |

### AI Model Specifications

**SentenceTransformer: all-MiniLM-L6-v2**

| Property | Value |
|----------|-------|
| **Model Type** | Sentence Embedding |
| **Base Architecture** | MiniLM (Distilled BERT) |
| **Embedding Dimension** | 384 |
| **Max Sequence Length** | 256 tokens |
| **Model Size** | ~80MB |
| **Parameters** | ~23 million |
| **Training Data** | 1B+ sentence pairs |
| **Performance** | 68.06 STS score |
| **Speed** | ~2800 sentences/sec (CPU) |
| **Use Cases** | Resume-JD matching, RAG queries |

### Development Tools

| Tool | Purpose |
|------|---------|
| **VS Code** | IDE |
| **Git** | Version control |
| **PowerShell** | Windows terminal |
| **Virtual Environment** | Python dependency isolation |
| **MySQL Workbench** | Database management |

---

## 📊 Performance Characteristics

### Processing Times

| Operation | Time | Bottleneck |
|-----------|------|-----------|
| Resume parsing | 0.5-1s | PDF text extraction |
| Skills assessment | 0.2-0.3s | Fuzzy matching loops |
| AI semantic matching | 0.5-0.8s | Model inference |
| Red flag detection | 0.1-0.2s | Pattern matching |
| Total per resume | 2-3s | AI model encoding |
| RAG query (100 candidates) | <1s | Vector calculations |
| AI model loading | ~2s | One-time on first use |

### Scalability

| Metric | Current | Optimized |
|--------|---------|-----------|
| Concurrent users | 10-20 | 100+ (with Gunicorn) |
| Resumes per batch | 10-50 | 100+ (parallel processing) |
| Database records | 1,000s | 100,000+ (with indexing) |
| Chat history | 50 messages | Unlimited (with backend storage) |
| RAG query candidates | 100-500 | 10,000+ (with vector DB) |

### Resource Requirements

| Resource | Development | Production |
|----------|------------|------------|
| **RAM** | 2GB | 4GB+ |
| **Storage** | 1GB | 10GB+ (for resumes) |
| **CPU** | 2 cores | 4+ cores |
| **Bandwidth** | Low | Medium (file uploads) |

---

## 🔐 Security Architecture

### Security Layers

```
┌─────────────────────────────────────────────────────────┐
│              Network Security Layer                      │
│  • HTTPS/SSL encryption (production)                    │
│  • Firewall rules (ports 80, 443, 3306)                │
├─────────────────────────────────────────────────────────┤
│            Application Security Layer                    │
│  • Input validation (file types, sizes)                 │
│  • Rate limiting (Flask-Limiter)                        │
│  • CSRF protection (Flask forms)                        │
│  • SQL injection prevention (parameterized queries)     │
│  • XSS prevention (output escaping)                     │
│  • Security headers (X-Frame-Options, CSP)              │
├─────────────────────────────────────────────────────────┤
│             Authentication Layer                         │
│  • Session management (Flask sessions)                  │
│  • Secret key (FLASK_SECRET_KEY)                        │
│  • Future: User authentication (login/logout)           │
├─────────────────────────────────────────────────────────┤
│              Database Security Layer                     │
│  • Dedicated DB user (not root)                         │
│  • Limited privileges (SELECT, INSERT, UPDATE, DELETE)  │
│  • Password protection                                  │
│  • Connection pooling                                   │
├─────────────────────────────────────────────────────────┤
│               File Security Layer                        │
│  • Secure filename generation (Werkzeug)                │
│  • File type validation                                 │
│  • Size limits (16MB max)                               │
│  • Isolated uploads directory                           │
│  • CASCADE DELETE (orphan prevention)                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Architecture

### Production Deployment

```
                          INTERNET
                             │
                             ↓
                    ┌────────────────┐
                    │  Load Balancer │ (Optional)
                    │   (Nginx/HAProxy)│
                    └────────┬───────┘
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
       ┌──────────┐   ┌──────────┐   ┌──────────┐
       │ Nginx    │   │ Nginx    │   │ Nginx    │
       │ (Reverse │   │ (Reverse │   │ (Reverse │
       │  Proxy)  │   │  Proxy)  │   │  Proxy)  │
       └────┬─────┘   └────┬─────┘   └────┬─────┘
            │              │              │
            ↓              ↓              ↓
       ┌──────────┐   ┌──────────┐   ┌──────────┐
       │ Gunicorn │   │ Gunicorn │   │ Gunicorn │
       │ Worker 1 │   │ Worker 2 │   │ Worker 3 │
       └────┬─────┘   └────┬─────┘   └────┬─────┘
            │              │              │
            └──────────────┼──────────────┘
                           ↓
                  ┌─────────────────┐
                  │  Flask App      │
                  │  (Multi-Agent + │
                  │   RAG System)   │
                  └────────┬────────┘
                           │
            ┌──────────────┼──────────────┐
            ↓              ↓              ↓
      ┌──────────┐   ┌──────────┐   ┌──────────┐
      │  MySQL   │   │  Redis   │   │  File    │
      │ Database │   │  Cache   │   │ Storage  │
      │          │   │ (Future) │   │ (uploads)│
      └──────────┘   └──────────┘   └──────────┘
```

---

## 📈 Future Enhancements

### Phase 1: Vector Database (Planned)
- ChromaDB integration for semantic search
- Store embeddings for faster retrieval
- Scale to 10,000+ resumes

### Phase 2: LangGraph Integration (Planned)
- Visual workflow orchestration
- Conditional agent branching
- Parallel agent execution
- State persistence

### Phase 3: Advanced Features
- User authentication & authorization
- Multi-tenant support (multiple companies)
- Email integration (automated outreach)
- Interview scheduling
- Salary prediction agent
- Culture fit assessment

---

## 📝 Summary

**AI Resume Filter** is a production-ready intelligent hiring system featuring:

✅ **Multi-Agent Architecture** - 5 specialized agents working in harmony  
✅ **AI-Powered Matching** - SentenceTransformer embeddings for semantic understanding  
✅ **RAG Chatbot** - Natural language querying with 8 query types  
✅ **Hybrid Scoring** - Combines AI, fuzzy matching, and keyword analysis  
✅ **Scalable Design** - Modular, extensible, production-ready  
✅ **Local Execution** - No API costs, privacy-first  
✅ **Comprehensive Workflow** - From resume upload to candidate ranking  

**Total Processing Time**: 2-3 seconds per resume  
**Query Response Time**: <1 second for 100 candidates  
**AI Model**: all-MiniLM-L6-v2 (384-dim, ~80MB, local)  
**Database**: MySQL with CASCADE DELETE for data integrity  

---

**Document Version**: 1.0  
**Last Updated**: November 18, 2025  
**Status**: Production Ready ✅
