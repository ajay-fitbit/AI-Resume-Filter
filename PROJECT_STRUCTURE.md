# Python Files Structure & Usage

## 📁 Root Directory Files

### Core Application Files

| File | Purpose | Used By |
|------|---------|---------|
| `app.py` | Main Flask application entry point. Contains all route handlers, orchestrates multi-agent system, handles file uploads, database operations, and API endpoints. | Direct execution (`python app.py`) |
| `config.py` | Configuration management. Stores database credentials, Flask secret key, upload folder settings, and allowed file extensions. | Imported by `app.py` and `app/database.py` |

---

## 📂 app/ Directory

### Core Utilities

| File | Purpose | Used By |
|------|---------|---------|
| `app/__init__.py` | Package initializer for app module. Makes `app` a Python package. | Python import system |
| `app/database.py` | Database connection and query utilities. Provides `create_connection()`, `execute_query()`, `fetch_query()` functions. | `app.py`, all database operations |
| `app/resume_parser.py` | Resume text extraction and parsing. Extracts text from PDF/DOCX, parses name, email, phone, skills (160+), experience years, education. | `app/agents/resume_parser_agent.py` |
| `app/red_flag_detector.py` | Red flag detection logic. Identifies job hopping, career gaps, missing skills, irrelevant experience, insufficient experience. | `app/agents/red_flag_agent.py` |

---

## 🤖 app/agents/ Directory - Multi-Agent System

### Agent Architecture

| File | Purpose | Description |
|------|---------|-------------|
| `app/agents/__init__.py` | Agents package initializer. Exports all agent classes for easy importing. | Python import system |
| `app/agents/base_agent.py` | Base agent class. Provides common functionality: logging, timing, execution tracking, error handling. | Inherited by all agents |

### Specialized Agents

| Agent File | Purpose | Technology | Used By |
|------------|---------|------------|---------|
| `app/agents/orchestrator.py` | **Ranking Orchestrator Agent** - Coordinates all agents, manages workflow, calculates final scores (weighted: semantic 30%, keywords 25%, skills 30%, experience 15%), assigns tiers, generates explanations. | AgentState, weighted scoring | `app.py` (main orchestrator) |
| `app/agents/resume_parser_agent.py` | **Resume Parser Agent** - Extracts structured data from PDF/DOCX resumes using NLP and regex patterns. | ResumeParser, spaCy, PyPDF2, python-docx | orchestrator.py |
| `app/agents/skills_agent.py` | **Skills Assessment Agent** - Evaluates candidate skills vs job requirements. 100+ skills database (databases, BI tools, SQL languages, frameworks), fuzzy matching (80%+ threshold), identifies matched/missing/additional skills, skill variations (t-sql → tsql, pl/sql → plsql). | FuzzyWuzzy, Levenshtein, regex | orchestrator.py |
| `app/agents/semantic_agent.py` | **Semantic Matching Agent** - AI-powered similarity analysis. Encodes resume & job description to 384-dim vectors, calculates cosine similarity. | SentenceTransformer (all-MiniLM-L6-v2), scikit-learn | orchestrator.py |
| `app/agents/red_flag_agent.py` | **Red Flag Detection Agent** - Identifies career issues: job hopping, gaps, missing skills, irrelevant experience. | RedFlagDetector, pattern matching | orchestrator.py |
| `app/agents/rag_agent.py` | **RAG Agent** - Natural language chatbot with role-based intelligence. Maps 10+ job roles to technical skills (DevOps, Database, Data Science, BI, etc.). Processes 8 query types, AI semantic search, hybrid scoring, markdown responses, chat history, resume count display. | SentenceTransformer, FuzzyWuzzy, regex | `app.py` (/api/rag/query) |

---

## 📊 Summary

**Total Python Files**: 14 (3 test scripts removed)

**By Category**:
- Core Application: 2 files (`app.py`, `config.py`)
- App Utilities: 4 files (`__init__.py`, `database.py`, `resume_parser.py`, `red_flag_detector.py`)
- Multi-Agent System: 8 files (base, orchestrator, 5 specialized agents, rag agent)

---

**Last Updated**: November 21, 2025
**Project Status**: ✅ Production Ready
