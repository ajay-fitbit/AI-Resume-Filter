# AI Resume Filter – Complete Blueprint

## 1. Core Purpose

Automatically scan resumes and shortlist the best candidates based on:

- Skills
- Experience
- Keywords
- Job description match score
- Red flags (job hopping, irrelevant roles, gaps)
- Soft skills signals

## 2. Key Features (MVP)

### A. Resume Parsing

Extract:

- Name, email, phone
- Skills (technical + soft)
- Experience (years, job titles)
- Education
- Projects
- Certifications
- Keywords frequency

**Use:** spaCy / HuggingFace / Python resume parsers.

### B. JD Matching (Match Score %)

AI matches resume with job description using:

- Semantic similarity
- Keyword overlap
- Skill relevance
- Experience relevance
- Industry match

**Output:** Match Score (0–100)

### C. Red Flag Detection

Flag issues like:

- Too many job changes
- Unexplained career gaps
- No relevant experience
- Missing required skills
- Fake-looking job titles / certificates

### D. Ranking System

Rank candidates:

- **Top Tier:** 80–100
- **Medium Tier:** 60–79
- **Low Tier:** <60

### E. Interactive HR Dashboard

HR can:

- Upload multiple resumes (PDF/DOC)
- Upload job description
- View ranked candidates
- Download shortlists
- Get AI explanation: *"Why this candidate matched or did not match."*