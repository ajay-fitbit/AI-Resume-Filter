# Multi-Agent System Architecture

## 🤖 Overview

The AI Resume Filter has been converted to a **Multi-Agent System** where specialized agents work together to analyze resumes. Each agent has a specific responsibility and communicates through a centralized orchestrator.

## 📊 Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Ranking Orchestrator Agent                  │
│              (Coordinates entire workflow)                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌───────────────┐              ┌──────────────────┐
│ Resume Parser │              │  Skills Assessor │
│    Agent      │──────────────│     Agent        │
└───────┬───────┘              └────────┬─────────┘
        │                               │
        │       ┌───────────────┐       │
        └───────│   Semantic    │───────┘
                │   Matcher     │
                │    Agent      │
                └───────┬───────┘
                        │
                        ▼
                ┌──────────────┐
                │  Red Flag    │
                │  Detector    │
                │    Agent     │
                └──────┬───────┘
                       │
                       ▼
              ┌────────────────┐
              │ Final Ranking  │
              │  & Tier Score  │
              └────────────────┘
```

## 🎯 Agent Responsibilities

### 1. **Resume Parser Agent**
- **Purpose**: Extract structured data from resume documents
- **Input**: File path to PDF/DOCX resume
- **Output**: Structured data (name, email, phone, skills, experience, education)
- **Technology**: PyPDF2, python-docx, regex patterns
- **Location**: `app/agents/resume_parser_agent.py`

### 2. **Skills Assessment Agent**
- **Purpose**: Evaluate candidate skills against job requirements
- **Input**: Resume skills list, job description text
- **Output**: Skill match score, matched skills, missing skills, additional skills
- **Technology**: Fuzzy matching, skill database (100+ common skills)
- **Location**: `app/agents/skills_agent.py`

**Key Features**:
- Recognizes skill variations (e.g., "javascript" = "js" = "node.js")
- Extracts required skills from JD using regex
- Calculates match percentage

### 3. **Semantic Matching Agent**
- **Purpose**: AI-powered semantic similarity between resume and JD
- **Input**: Resume text, job description text
- **Output**: Semantic similarity score, keyword match score, embedding info
- **Technology**: 
  - Sentence Transformers (all-MiniLM-L6-v2)
  - TF-IDF vectorization
  - Cosine similarity
- **Location**: `app/agents/semantic_agent.py`

**AI Model Details**:
- Model: all-MiniLM-L6-v2 (23M parameters)
- Embedding Dimension: 384
- Lazy Loading: Model loads on first use
- Fallback: TF-IDF if model fails

**Note**: Same AI model used by RAG Agent for consistency

### 4. **Red Flag Agent**
- **Purpose**: Detect potential issues in candidate profile
- **Input**: Resume data, job description, required experience
- **Output**: List of red flags with severity levels
- **Technology**: Pattern matching, date analysis, heuristics
- **Location**: `app/agents/red_flag_agent.py`

**Detects**:
- Job hopping (3+ jobs in 2 years)
- Career gaps (2+ years)
- Missing critical skills
- Insufficient experience
- Irrelevant experience

### 5. **Ranking Orchestrator Agent**
- **Purpose**: Coordinate all agents and calculate final score
- **Input**: File path, job description, required experience
- **Output**: Complete analysis with scores, tier, explanation, red flags
- **Technology**: State management, weighted scoring, workflow coordination
- **Location**: `app/agents/orchestrator.py`

### 6. **RAG Agent** 🆕 (Standalone Query System)
- **Purpose**: Natural language querying of candidate database
- **Input**: User question in plain English
- **Output**: Ranked candidates with relevance scores, formatted answer
- **Technology**:
  - SentenceTransformer (all-MiniLM-L6-v2) - AI semantic search
  - FuzzyWuzzy - Fuzzy string matching
  - Regex patterns - Query intent detection
  - localStorage - Chat history persistence
- **Location**: `app/agents/rag_agent.py`

**AI Features**:
- Question embedding encoding (384-dim)
- Candidate profile encoding
- Cosine similarity calculation
- Adaptive semantic scoring (0-30 points)
- Intelligent boosting based on query type
- Fallback to fuzzy matching if AI fails

**Query Types**: Greetings, Help, Count, Comparison, Profile, Recommendation, Listing, Search

**Workflow**:
1. Executes agents in sequence
2. Maintains shared state (AgentState)
3. Collects execution logs
4. Calculates weighted final score
5. Generates human-readable explanation

## 📐 Scoring Algorithm

### Weighted Components

| Component | Weight | Agent Responsible |
|-----------|--------|-------------------|
| Semantic Similarity | 30% | SemanticMatchingAgent |
| Keyword Match (TF-IDF) | 25% | SemanticMatchingAgent |
| Skills Match | 30% | SkillsAssessmentAgent |
| Experience Match | 15% | RankingOrchestratorAgent |

### Final Score Calculation

```python
overall_score = (
    semantic_score * 0.30 +
    keyword_score * 0.25 +
    skill_score * 0.30 +
    experience_score * 0.15
)
```

### Tier Assignment
- **Top Tier**: Score ≥ 75%
- **Medium Tier**: 50% ≤ Score < 75%
- **Low Tier**: Score < 50%

## 🔄 Execution Flow

### 1. User Uploads Resume
```
User → Flask (/upload) → Orchestrator.execute()
```

### 2. Agent Execution Sequence
```python
# Step 1: Parse Resume
parse_result = ResumeParserAgent.execute({
    "file_path": "/path/to/resume.pdf"
})

# Step 2: Assess Skills
skills_result = SkillsAssessmentAgent.execute({
    "resume_skills": ["python", "aws", "docker"],
    "job_description": "Looking for Python developer..."
})

# Step 3: Semantic Matching
semantic_result = SemanticMatchingAgent.execute({
    "resume_text": "Full resume text...",
    "job_description": "Job description text..."
})

# Step 4: Red Flag Detection
red_flag_result = RedFlagAgent.execute({
    "resume_data": {...},
    "job_description": "...",
    "required_experience": 5
})

# Step 5: Calculate Final Score
final_result = Orchestrator._calculate_final_score(state)
```

### 3. Database Storage
```
Orchestrator → Database → Candidates + Resume Data + Analysis Results + Red Flags
```

## 📊 State Management

### AgentState Class
Shared state passed between agents:

```python
class AgentState:
    data: Dict[str, Any]           # Shared data
    agent_results: Dict[str, Any]  # Results from each agent
    errors: List[Dict]             # Error tracking
```

**Methods**:
- `set(key, value)`: Store data
- `get(key)`: Retrieve data
- `add_agent_result(name, result)`: Store agent output
- `add_error(agent_name, error)`: Record errors

## 🕒 Execution Timing

Each agent tracks execution time:

```python
{
    "metadata": {
        "execution_time": 0.234,  # seconds
        "agent_name": "ResumeParserAgent"
    }
}
```

Total workflow time includes all agents:
```python
{
    "total_execution_time": 1.567  # seconds
}
```

## 📝 Logging System

### Agent Logs
Each agent maintains execution logs:

```python
{
    "agent": "SemanticMatchingAgent",
    "timestamp": "2025-11-15T10:30:45",
    "level": "info",  # info | warning | error | success
    "message": "Semantic: 78.45%, Keywords: 65.23%"
}
```

### Collected Logs
Orchestrator collects all agent logs:

```python
final_result["agent_execution_log"] = [
    {"agent": "ResumeParserAgent", "message": "Parsing resume..."},
    {"agent": "SkillsAssessmentAgent", "message": "Assessing skills..."},
    # ... more logs
]
```

## 🖥️ Monitoring Dashboard

Access at: **http://127.0.0.1:5000/agent_monitoring**

**Features**:
- Agent status indicators (Active/Idle)
- Recent executions table
- Workflow timing metrics
- Architecture diagram
- Execution logs (future feature)

## 🔧 Configuration

### Enable/Disable Agents
Currently all agents are required. Future enhancement: conditional agent execution.

### Adjust Weights
Modify in `orchestrator.py`:

```python
weights = {
    "semantic": 0.30,    # Adjust these
    "keyword": 0.25,
    "skill": 0.30,
    "experience": 0.15
}
```

## 🚀 Future Enhancements

### Phase 1: LangGraph Integration (Commented in requirements.txt)
```bash
# Uncomment these in requirements.txt:
langgraph==0.0.40
langchain==0.1.0
langchain-community==0.0.20
```

**Benefits**:
- Visual workflow graphs
- Conditional branching
- Parallel agent execution
- State persistence

### Phase 2: RAG Pipeline
```bash
# Uncomment these in requirements.txt:
chromadb==0.4.22
openai==1.12.0
```

**Features**:
- Vector database for resume embeddings
- Natural language queries: "Find Python developers with AWS"
- LLM-generated explanations
- Conversational candidate search

### Phase 3: Additional Agents
- **Interview Question Generator Agent**: Creates questions based on resume gaps
- **Email Composer Agent**: Generates personalized emails
- **Salary Estimator Agent**: Predicts salary range
- **Culture Fit Agent**: Evaluates soft skills

## 📁 File Structure

```
app/
├── agents/
│   ├── __init__.py                 # Agent exports
│   ├── base_agent.py               # BaseAgent + AgentState classes
│   ├── resume_parser_agent.py      # Document parsing
│   ├── skills_agent.py             # Skills assessment
│   ├── semantic_agent.py           # AI semantic matching
│   ├── red_flag_agent.py           # Issue detection
│   └── orchestrator.py             # Workflow coordinator
├── templates/
│   └── agent_monitoring.html       # Monitoring dashboard
└── [original files]
```

## 🧪 Testing

### Manual Test
1. Start application: `python app.py`
2. Navigate to: http://127.0.0.1:5000
3. Create job description
4. Upload resume
5. Check agent logs in console
6. View monitoring dashboard

### Console Output
```
[ResumeParserAgent] INFO: Parsing resume: John_Doe.pdf
[ResumeParserAgent] SUCCESS: Successfully parsed - Name: John Doe, Experience: 5 years
[SkillsAssessmentAgent] INFO: Assessing 12 skills against job requirements
[SkillsAssessmentAgent] SUCCESS: Matched: 8/10 skills - Score: 80.0%
[SemanticMatchingAgent] INFO: Loading AI model...
[SemanticMatchingAgent] SUCCESS: AI model loaded successfully!
[SemanticMatchingAgent] INFO: Semantic: 78.45%, Keywords: 65.23%
[RedFlagAgent] INFO: Detected 1 red flags - High: 0, Medium: 1, Low: 0
[RankingOrchestratorAgent] SUCCESS: Workflow completed in 1.234s - Final Score: 76.50%
✅ Multi-Agent processed: John Doe - Score: 76.50%
```

## 🎓 Learning Resources

### Multi-Agent Systems
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [AutoGen by Microsoft](https://microsoft.github.io/autogen/)
- [CrewAI](https://docs.crewai.com/)

### RAG Pipelines
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

## 🤝 Contributing

To add a new agent:

1. Create `app/agents/your_agent.py`:
```python
from .base_agent import BaseAgent

class YourAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="YourAgent")
    
    def execute(self, input_data):
        # Your logic here
        return {"success": True, ...}
```

2. Add to `orchestrator.py`:
```python
self.your_agent = YourAgent()
# Call in workflow
result = self.your_agent.timed_execute(input_data)
```

3. Update `__init__.py`:
```python
from .your_agent import YourAgent
```

---

**Status**: ✅ Multi-Agent System Active
**Version**: 2.0.0
**Last Updated**: November 15, 2025
