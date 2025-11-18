# RAG Pipeline Integration Guide

## 🎯 What is RAG?

**RAG (Retrieval-Augmented Generation)** combines:
1. **Retrieval**: Search relevant documents using vector similarity
2. **Augmentation**: Provide context to LLM
3. **Generation**: LLM generates intelligent response

## 🏗️ Current System (Multi-Agent)

```
User Query → SQL Database → Fixed Analysis → Structured Results
```

## 🚀 Future System (RAG-Enhanced)

```
User Query → Vector DB (Embeddings) → Semantic Search → 
LLM (GPT-4/Claude) → Natural Language Response
```

## 📊 Architecture Comparison

### Without RAG (Current)
```python
# Hard-coded query
candidates = fetch_query(conn, "SELECT * FROM candidates WHERE experience_years >= 5")

# Fixed analysis
match_score = calculate_score(resume, job_description)  # Returns number
```

### With RAG (Future)
```python
# Natural language query
user_input = "Find senior Python developers with cloud experience who worked at startups"

# Semantic search in vector DB
embeddings = vectordb.similarity_search(user_input, k=10)

# LLM generates response
response = llm.generate(f"""
Based on these resumes:
{embeddings}

Answer: {user_input}
""")

# Output: "I found 3 candidates matching your criteria. Sarah Johnson has 
#          7 years Python with AWS experience at TechStartup Inc..."
```

## 🛠️ Implementation Plan

### Phase 1: Vector Database Setup

#### 1.1 Install Dependencies
```bash
pip install chromadb openai sentence-transformers
```

#### 1.2 Create Vector Store
```python
# app/rag/vector_store.py
import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("resumes")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_resume(self, candidate_id, resume_text):
        """Store resume embedding"""
        embedding = self.model.encode(resume_text).tolist()
        self.collection.add(
            embeddings=[embedding],
            documents=[resume_text],
            ids=[str(candidate_id)]
        )
    
    def search(self, query, k=5):
        """Search similar resumes"""
        query_embedding = self.model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results
```

#### 1.3 Migrate Existing Data
```python
# scripts/migrate_to_vectordb.py
from app.rag.vector_store import VectorStore
from app.database import fetch_query, create_connection

def migrate():
    conn = create_connection()
    vector_store = VectorStore()
    
    # Get all candidates
    candidates = fetch_query(conn, """
        SELECT c.id, rd.raw_text 
        FROM candidates c 
        JOIN resume_data rd ON c.id = rd.candidate_id
    """)
    
    for candidate in candidates:
        vector_store.add_resume(
            candidate['id'], 
            candidate['raw_text']
        )
    
    print(f"✅ Migrated {len(candidates)} resumes to vector DB")
```

### Phase 2: LLM Integration

#### 2.1 Add OpenAI Client
```python
# app/rag/llm_client.py
import openai

class LLMClient:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def generate_response(self, context, query):
        """Generate natural language response"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert recruiter analyzing resumes."},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ]
        )
        return response.choices[0].message.content
```

#### 2.2 Create RAG Agent
```python
# app/agents/rag_agent.py
from .base_agent import BaseAgent
from app.rag.vector_store import VectorStore
from app.rag.llm_client import LLMClient

class RAGAgent(BaseAgent):
    def __init__(self, openai_key):
        super().__init__(name="RAGAgent")
        self.vector_store = VectorStore()
        self.llm = LLMClient(openai_key)
    
    def execute(self, input_data):
        """
        Process natural language query
        
        Input: {"query": "Find Python developers with 5+ years"}
        Output: {"response": "I found 3 candidates..."}
        """
        query = input_data.get("query")
        
        # Step 1: Retrieve similar resumes
        self.log(f"Searching for: {query}")
        results = self.vector_store.search(query, k=5)
        
        # Step 2: Prepare context
        context = "\n\n".join([
            f"Resume {i+1}: {doc}" 
            for i, doc in enumerate(results['documents'][0])
        ])
        
        # Step 3: Generate response with LLM
        self.log("Generating LLM response")
        response = self.llm.generate_response(context, query)
        
        return {
            "success": True,
            "response": response,
            "retrieved_candidates": results['ids'][0]
        }
```

### Phase 3: Flask Integration

#### 3.1 Add RAG Search Route
```python
# app.py
from app.agents.rag_agent import RAGAgent

rag_agent = RAGAgent(openai_key=os.getenv("OPENAI_API_KEY"))

@app.route('/rag_search', methods=['GET', 'POST'])
def rag_search():
    if request.method == 'POST':
        query = request.form.get('query')
        
        # Execute RAG agent
        result = rag_agent.execute({"query": query})
        
        return render_template('rag_search.html', 
                             query=query,
                             response=result['response'],
                             candidate_ids=result['retrieved_candidates'])
    
    return render_template('rag_search.html')
```

#### 3.2 Create RAG Search Template
```html
<!-- app/templates/rag_search.html -->
<form method="POST">
    <textarea name="query" placeholder="Ask anything about candidates..."></textarea>
    <button type="submit">Search</button>
</form>

{% if response %}
<div class="rag-response">
    <h3>AI Response:</h3>
    <p>{{ response }}</p>
    
    <h4>Matching Candidates:</h4>
    <ul>
        {% for id in candidate_ids %}
        <li><a href="{{ url_for('candidate_detail', candidate_id=id) }}">Candidate #{{ id }}</a></li>
        {% endfor %}
    </ul>
</div>
{% endif %}
```

### Phase 4: Advanced Features

#### 4.1 Interview Question Generator
```python
class InterviewQuestionAgent(BaseAgent):
    def execute(self, input_data):
        resume_data = input_data['resume_data']
        
        prompt = f"""
        Based on this candidate's profile:
        - Skills: {resume_data['skills']}
        - Experience: {resume_data['experience_years']} years
        - Education: {resume_data['education']}
        
        Generate 5 technical interview questions.
        """
        
        questions = llm.generate_response(prompt)
        return {"questions": questions}
```

#### 4.2 Email Generator Agent
```python
class EmailGeneratorAgent(BaseAgent):
    def execute(self, input_data):
        candidate_name = input_data['candidate_name']
        decision = input_data['decision']  # "accept" or "reject"
        
        prompt = f"""
        Write a professional email to {candidate_name}.
        Decision: {decision}
        Tone: Professional and encouraging
        """
        
        email = llm.generate_response(prompt)
        return {"email": email}
```

#### 4.3 Salary Estimator Agent
```python
class SalaryEstimatorAgent(BaseAgent):
    def execute(self, input_data):
        resume_data = input_data['resume_data']
        location = input_data['location']
        
        prompt = f"""
        Estimate salary range for:
        - Skills: {resume_data['skills']}
        - Experience: {resume_data['experience_years']} years
        - Location: {location}
        
        Provide min, max, and average salary.
        """
        
        estimate = llm.generate_response(prompt)
        return {"salary_estimate": estimate}
```

## 📈 Benefits of RAG Integration

### 1. Natural Language Queries
**Before**:
```sql
SELECT * FROM candidates WHERE experience_years >= 5 AND skills LIKE '%python%'
```

**After**:
```
"Find senior Python developers who have startup experience and know AWS"
```

### 2. Contextual Understanding
- RAG understands synonyms: "cloud" = "AWS" or "Azure" or "GCP"
- Understands intent: "senior" = 5+ years experience
- Handles complex queries: "worked at startups" searches job history

### 3. Intelligent Responses
Instead of returning raw data, get:
```
"I found 3 candidates matching your criteria:

1. Sarah Johnson (8 years Python, AWS certified)
   - Worked at TechStartup Inc. for 3 years
   - Strong DevOps background
   - Match Score: 87%

2. Michael Chen (6 years Python, Azure experience)
   - Led team of 5 at StartupXYZ
   - Expert in microservices
   - Match Score: 82%

3. Emily Davis (7 years Python, GCP)
   - Built scalable cloud infrastructure
   - Startup culture fit
   - Match Score: 79%

Would you like me to generate interview questions for any of these candidates?"
```

## 💰 Cost Estimation

### ChromaDB (Free)
- Self-hosted vector database
- No API costs

### OpenAI (Paid)
- GPT-4: $0.03 per 1K tokens (input), $0.06 per 1K tokens (output)
- GPT-3.5-turbo: $0.0015 per 1K tokens (much cheaper)
- Estimated cost: ~$0.05 per complex query

### Alternative: Open Source LLMs
- LLaMA 2 (Free, self-hosted)
- Mistral (Free, self-hosted)
- Ollama (Free, local inference)

## 🎯 Quick Start (RAG)

### 1. Install Dependencies
```powershell
.\venv\Scripts\pip.exe install chromadb openai
```

### 2. Set OpenAI Key
```powershell
# .env
OPENAI_API_KEY=sk-your-key-here
```

### 3. Initialize Vector Store
```powershell
.\venv\Scripts\python.exe scripts/migrate_to_vectordb.py
```

### 4. Start Using RAG
```python
# In Flask route
result = rag_agent.execute({
    "query": "Find Python developers with cloud experience"
})
```

## 🔄 Hybrid Approach (Recommended)

Use **both** SQL and RAG:

```python
def search_candidates(query):
    # Step 1: RAG for semantic understanding
    rag_result = rag_agent.execute({"query": query})
    candidate_ids = rag_result['retrieved_candidates']
    
    # Step 2: SQL for structured data
    conn = create_connection()
    candidates = fetch_query(conn, f"""
        SELECT c.*, ar.match_score 
        FROM candidates c
        JOIN analysis_results ar ON c.id = ar.candidate_id
        WHERE c.id IN ({','.join(map(str, candidate_ids))})
        ORDER BY ar.match_score DESC
    """)
    
    # Step 3: LLM for explanation
    explanation = llm.generate_response(
        context=str(candidates),
        query=query
    )
    
    return {
        "candidates": candidates,
        "explanation": explanation
    }
```

## 📝 Next Steps

1. ✅ Multi-Agent System (COMPLETE)
2. ⏭️ Add ChromaDB integration
3. ⏭️ Migrate resumes to vector store
4. ⏭️ Add OpenAI/LLM client
5. ⏭️ Create RAGAgent
6. ⏭️ Build RAG search interface
7. ⏭️ Add interview question generator
8. ⏭️ Add email generator

## 📚 Resources

- [ChromaDB Docs](https://docs.trychroma.com/)
- [OpenAI API](https://platform.openai.com/docs/api-reference)
- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering/)
- [Ollama (Local LLMs)](https://ollama.ai/)

---

**Status**: 📋 Ready for Implementation
**Estimated Time**: 3-4 days
**Complexity**: Medium
