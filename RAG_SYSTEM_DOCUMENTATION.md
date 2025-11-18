# RAG (Retrieval Augmented Generation) System - Resume Q&A

## Overview
The RAG system allows users to ask natural language questions about candidate resumes and get intelligent, context-aware answers with ranked candidate matches.

**🆕 Now AI-Powered**: Uses SentenceTransformer model for semantic understanding!

## Features

### 🤖 AI-Powered Semantic Search
- **Model**: SentenceTransformer `all-MiniLM-L6-v2`
- **Embeddings**: 384-dimensional vectors
- **Technology**: Cosine similarity between question and candidate profiles
- **Scoring**: 0-30 points adaptive semantic boost
- **Execution**: Local, no API calls (~80MB model)

### 🎯 Natural Language Querying
- Ask questions in plain English about candidate resumes
- **8 Query Types Supported**:
  1. **Greetings** - "Hi", "Hello"
  2. **Help** - "What can you do?"
  3. **Count** - "How many candidates know Python?"
  4. **Comparison** - "Who is better: A or B?"
  5. **Specific Person** - "Show me Ajay Singh profile"
  6. **Recommendation** - "Who should I hire for DevOps?"
  7. **Listing** - "List all SQL developers"
  8. **Search** - "Find cloud experts"
- Examples:
  - "Which candidates have Python experience?"
  - "Find candidates with machine learning skills"
  - "Who has experience with cloud platforms like AWS or Azure?"
  - "List candidates with 5+ years of experience"
  - "Show me [name] full profile"
  - "Who is best for DevOps engineering?"

### 🔍 Intelligent Search
- **Skills Detection**: Automatically extracts mentioned skills from questions
- **Experience Matching**: Detects years of experience requirements (e.g., "5+ years")
- **Keyword Extraction**: Identifies relevant search terms
- **Fuzzy Matching**: Finds similar skills even with typos or variations
- **Skill Variations**: Recognizes abbreviations (ML → Machine Learning, AI → Artificial Intelligence)

### 🎚️ Relevance Scoring (AI-Enhanced)
Candidates are ranked using hybrid approach:
- **Skill Matches** (30 points per exact match, 20 points for fuzzy match)
- **Experience Years** (25 points if meets requirement)
- **Keyword Matches** (5 points per keyword)
- **AI Semantic Score** (0-30 points adaptive):
  - **Skill queries**: 15 points max boost (e.g., "find Python developers")
  - **General queries**: 30 points max boost (e.g., "who is best for DevOps?")
  - Calculated using cosine similarity of embeddings
- **Fallback**: Uses fuzzy matching if AI model unavailable
- Maximum score: 100%
- **Display**: Match scores shown with 2 decimal places

### 📊 Context-Aware Results
- **Job-Specific Mode**: Select a job description to search only candidates who applied for that role
- **All Resumes Mode**: Search across all candidates in the database
- Shows matched skills, experience, and email for each candidate
- Displays relevance score for each match (2 decimal places)

### 💾 Chat History (localStorage)
- **Persistent Storage**: Conversations saved across page refreshes
- **50 Message Limit**: Automatic cleanup of old messages
- **Clear History Button**: Reset conversation anytime
- **Timestamp Tracking**: Each message timestamped
- **Full Restoration**: Includes questions, answers, and candidate results

### 📝 Markdown Formatting
- **Headers**: ## and ### with purple theme
- **Bold Text**: **text** styled in purple
- **Italic Text**: *text* with emphasis
- **Bullet Lists**: •, -, * converted to styled lists
- **Code Blocks**: `code` with purple background
- **Line Breaks**: Proper spacing for readability

## How to Use

### 1. Access the Interface
Navigate to the "💬 Resume Q&A" menu item in the navigation bar

### 2. Select Context (Optional)
- Choose a specific job description from the dropdown to search within that candidate pool
- Or leave as "All Resumes" to search across all candidates

### 3. Ask a Question
Type your question in natural language, such as:
- "Which candidates know React and Node.js?"
- "Find candidates with database experience"
- "Who has Python and cloud platform skills?"

### 4. View Results
The system will:
1. Display your question in the chat history
2. Show an AI-generated answer summarizing the results
3. List matched candidates with:
   - Name and email
   - Relevance score (0-100%)
   - Matched skills highlighted
   - Experience information
   - Overall match score from original analysis

### 5. Use Example Questions
Click any of the example question buttons to quickly test the system

## Technical Implementation

### RAG Agent (`app/agents/rag_agent.py`) - AI-Enhanced
The RAG Agent implements intelligent resume querying using:

1. **AI Model Integration**:
   - **Model**: SentenceTransformer `all-MiniLM-L6-v2`
   - **Lazy Loading**: Model loads on first query (~2 seconds)
   - **Question Encoding**: Converts user query to 384-dim vector
   - **Profile Encoding**: Creates and encodes candidate profile text
   - **Cosine Similarity**: Calculates semantic match score
   - **Size**: ~80MB download (one-time)
   - **Execution**: Local CPU inference, no API calls

2. **Search Term Extraction**:
   - Identifies skills from 160+ skill database
   - Extracts years of experience from patterns like "5+ years" or "3 yrs"
   - Filters out stop words to get meaningful keywords
   - Expands terms: "cloud" → AWS/Azure/GCP, "database" → SQL/MongoDB

3. **Hybrid Ranking**:
   - **AI Semantic Scoring**: 0-30 points from embeddings
   - **Keyword Matching**: 5 points per relevant term
   - **Fuzzy Matching**: 80%+ similarity threshold
   - **Intelligent Boosting**: Adaptive based on query type
   - **Fallback Mechanism**: Uses fuzzy if AI fails

4. **Natural Language Understanding**:
   - **Intent Detection**: Classifies query into 8 types
   - **Name Detection**: Regex + word matching for profiles
   - **Pattern Matching**: 40+ query patterns
   - **Conversational**: Greetings, help requests handled

5. **Answer Generation**:
   - Creates markdown-formatted responses
   - Highlights top candidates with scores
   - Shows matched skills and experience
   - Provides context about match quality

### Flask Routes (`app.py`)

#### `/rag_chat` (GET)
- Renders the chat interface
- Loads all job descriptions with candidate counts

#### `/api/rag/query` (POST)
- Processes natural language questions
- Accepts JSON: `{"question": "...", "job_id": "..." (optional)}`
- Returns JSON:
  ```json
  {
    "answer": "Natural language response",
    "candidates": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "matched_skills": "Python, AWS, Docker",
        "relevance_score": 85
      }
    ],
    "question": "Original question",
    "search_terms": {
      "skills": ["Python", "AWS"],
      "experience_years": 5,
      "keywords": ["backend", "cloud"]
    }
  }
  ```

### Frontend (`app/templates/rag_chat.html`)
- Modern chat interface with gradient design
- Real-time question processing with loading states
- Example questions for quick testing
- Mobile-responsive card layout
- Animated message transitions
- Candidate result cards with hover effects

## Skills Database

The RAG system recognizes 120+ skills including:
- **Programming**: Python, Java, JavaScript, TypeScript, Go, Rust, C++, C#, etc.
- **Web Frameworks**: React, Angular, Vue.js, Node.js, Django, Flask, Spring Boot, etc.
- **Databases**: SQL, MySQL, PostgreSQL, MongoDB, Redis, Oracle, etc.
- **Cloud/DevOps**: AWS, Azure, GCP, Docker, Kubernetes, Jenkins, CI/CD, etc.
- **AI/ML**: Machine Learning, Deep Learning, NLP, LLM, RAG, TensorFlow, PyTorch, etc.
- **Data/Analytics**: Pandas, NumPy, Tableau, Power BI, Apache Spark, etc.
- **Tools**: Git, VS Code, JIRA, etc.

### Skill Variations Recognized
- `ml` → Machine Learning
- `ai` → Artificial Intelligence
- `llm` → Large Language Model
- `rag` → Retrieval Augmented Generation
- `nlp` → Natural Language Processing
- `k8s` → Kubernetes
- `js` → JavaScript
- `ts` → TypeScript

## Dependencies

```python
sentence-transformers==2.2.2  # AI semantic embeddings (ACTIVE)
fuzzywuzzy==0.18.0            # Fuzzy string matching
python-Levenshtein==0.21.1    # Fast Levenshtein distance calculation
scikit-learn==1.3.2           # Cosine similarity calculations
numpy==1.26.2                 # Vector operations
```

### AI Model Details
- **Name**: all-MiniLM-L6-v2
- **Source**: Hugging Face Model Hub
- **Type**: Sentence embedding model (distilled BERT)
- **Size**: ~80MB
- **Embedding Dim**: 384
- **Performance**: ~2800 sentences/sec (CPU)
- **Cost**: Free, open-source

## Future Enhancements

### Phase 1: Vector Database Integration
- Integrate ChromaDB for semantic vector search
- Store resume embeddings for faster similarity search
- Enable more sophisticated semantic matching

### Phase 2: LLM Integration
- Add OpenAI GPT or open-source LLM for answer generation
- Generate more detailed, conversational responses
- Summarize candidate strengths/weaknesses

### Phase 3: Advanced Features
- Multi-turn conversations (follow-up questions)
- Comparison queries ("Compare candidate A vs B")
- Skill gap analysis ("What skills are missing for this role?")
- Trend analysis ("Which skills are most common?")

## Performance Notes

- **AI Model Loading**: ~2 seconds (first query only, then cached)
- **Semantic Encoding**: ~0.5 seconds per candidate profile
- **Response Time**: <1 second for queries with 100 candidates
- **Hybrid Approach**: AI semantic + keyword + fuzzy matching
- **Scalability**: Handles hundreds of candidates efficiently
- **No API Calls**: Fully local execution
- **No Rate Limits**: Unlimited queries
- **Privacy**: All data stays local

## Example Queries

| Question | What it Searches For |
|----------|---------------------|
| "Python developers" | Candidates with Python in skills |
| "5 years experience" | Candidates with 5+ years experience |
| "AWS and Docker" | Candidates with both AWS and Docker skills |
| "machine learning experts" | Candidates with ML/AI skills |
| "React or Angular" | Candidates with either React or Angular |
| "backend developers" | Keyword match for "backend" in resumes |
| "database experience" | Candidates with database-related skills |

## Troubleshooting

### No Results Found
- Try broader search terms
- Check if resumes have been uploaded and analyzed
- Verify skills are in the database (see skills list above)

### Low Relevance Scores
- Questions may be too specific
- Skills might not match exactly (try variations)
- Candidates may lack the requested skills

### Empty Job Context
- Ensure job description has analyzed candidates
- Upload and analyze resumes for that job first

## License
Part of the AI Resume Filter Multi-Agent System
