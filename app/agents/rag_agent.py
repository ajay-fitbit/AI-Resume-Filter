"""
RAG (Retrieval Augmented Generation) Agent for Resume Querying
Uses AI-powered semantic search to find relevant candidates based on natural language questions
"""

from typing import List, Dict, Any, Optional
import re
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RAGAgent:
    """
    RAG Agent for intelligent resume querying using AI semantic search and keyword matching
    """
    
    def __init__(self):
        """Initialize the RAG Agent with AI model"""
        # Lazy load AI model
        self.model = None
        self._model_loaded = False
        
        self.common_skills = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 'Ruby', 'PHP', 
            'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'Perl', 'Shell', 'Bash',
            'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring Boot', 
            'Express.js', 'Next.js', 'Svelte', 'ASP.NET', 'Laravel',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra', 'Oracle', 'SQL Server', 
            'MariaDB', 'DynamoDB', 'Elasticsearch', 'Neo4j', 'SQLite',
            'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'CI/CD', 
            'Terraform', 'Ansible', 'DevOps', 'Linux', 'Git', 'GitHub', 'GitLab', 'Bitbucket',
            'Machine Learning', 'ML', 'Deep Learning', 'AI', 'Artificial Intelligence', 'NLP', 
            'Natural Language Processing', 'Computer Vision', 'LLM', 'Large Language Model', 
            'RAG', 'Retrieval Augmented Generation', 'OpenAI', 'GPT', 'BERT', 'Transformer',
            'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy', 'Hugging Face',
            'Tableau', 'Power BI', 'Excel', 'Data Analysis', 'Data Science', 'Statistics', 
            'ETL', 'Apache Spark', 'Hadoop', 'Airflow', 'Databricks', 'Snowflake', 'dbt',
            'VS Code', 'Visual Studio', 'IntelliJ', 'PyCharm', 'Eclipse', 'Sublime Text', 'Vim',
            'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum', 'JIRA', 'Confluence',
            'Testing', 'QA', 'Quality Assurance', 'Unit Testing', 'Integration Testing', 
            'Automated Testing', 'Manual Testing', 'Test Automation', 'Selenium', 'Cypress',
            'HTML', 'CSS', 'SASS', 'SCSS', 'Bootstrap', 'Tailwind', 'jQuery', 'Redux',
            'Kafka', 'RabbitMQ', 'GraphQL', 'gRPC', 'WebSocket', 'OAuth', 'JWT', 'SAML'
        ]
        
        self.skill_variations = {
            'ml': 'machine learning',
            'ai': 'artificial intelligence',
            'nlp': 'natural language processing',
            'llm': 'large language model',
            'rag': 'retrieval augmented generation',
            'dl': 'deep learning',
            'cv': 'computer vision',
            'rdbms': 'relational database',
            'nosql': 'non-relational database',
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'k8s': 'kubernetes',
            'tf': 'tensorflow',
            'api': 'application programming interface',
            'qa': 'quality assurance',
            'db': 'database',
            'frontend': 'front-end',
            'backend': 'back-end',
            'fullstack': 'full-stack'
        }
        
        # Query intent patterns
        self.query_patterns = {
            'comparison': r'\b(best|top|better|strongest|most|highest|compare|versus|vs)\b',
            'requirement': r'\b(need|needs|require|requires|must|should)\b',
            'ability': r'\b(can|able|capable|proficient|expert|skilled)\b',
            'location': r'\b(where|location|based|from|near)\b',
            'education': r'\b(degree|education|graduate|university|college|bachelor|master|phd)\b',
            'specific_person': r'\b(tell me about|who is|information about|details of|profile of|show me .+ profile|show .+ profile|about)\b',
            'recommendation': r'\b(recommend|suggest|best fit|suitable|ideal|perfect)\b',
            'listing': r'\b(list all|show all|display all|enumerate)\b'
        }
        
        print("[RAG Agent] Initialized with AI-powered semantic search")
    
    def _load_model(self):
        """Lazy load the sentence transformer model"""
        if not self._model_loaded:
            try:
                print("[RAG Agent] Loading AI model (all-MiniLM-L6-v2)...")
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self._model_loaded = True
                print("[RAG Agent] ✅ AI model loaded successfully!")
            except Exception as e:
                print(f"[RAG Agent] ⚠️ Failed to load AI model: {str(e)}")
                print("[RAG Agent] Falling back to rule-based matching")
                self.model = None
                self._model_loaded = True
    
    def query(self, question: str, candidates: List[Dict[str, Any]], job_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a natural language question and return relevant candidates
        
        Args:
            question: Natural language question about resumes
            candidates: List of candidate dictionaries with resume data
            job_context: Optional job description for context
            
        Returns:
            Dictionary with answer and ranked candidates
        """
        if not candidates:
            return {
                'answer': 'I don\'t see any candidates in the database yet. Please upload some resumes first, and I\'ll be happy to help you find the right match! 😊',
                'candidates': [],
                'question': question
            }
        
        question_lower = question.lower().strip()
        
        # Detect query intent
        query_intent = self._detect_query_intent(question_lower)
        
        # Extract search intent and keywords from question first
        search_terms = self._extract_search_terms(question)
        
        # Handle different query types
        
        # 1. Greeting/Conversational queries
        if self._is_greeting(question_lower):
            return self._handle_greeting(candidates)
        
        # 2. Help/Guidance queries
        if self._is_help_query(question_lower):
            return self._handle_help_query()
        
        # 3. Count/Statistics queries
        is_count_query = re.search(r'\b(how many|count|number of|total)\b', question_lower)
        if is_count_query:
            return self._handle_count_query(candidates, search_terms, question)
        
        # 4. Specific person query - check before other intents
        # Detect if question contains a name by checking against candidate names
        if query_intent == 'specific_person' or self._contains_candidate_name(question_lower, candidates):
            return self._handle_specific_person_query(candidates, question)
        
        # 5. Comparison queries (best, top, strongest)
        if query_intent == 'comparison':
            return self._handle_comparison_query(candidates, search_terms, question)
        
        # 6. Recommendation queries
        if query_intent == 'recommendation':
            return self._handle_recommendation_query(candidates, search_terms, question, job_context)
        
        # 7. Listing queries
        if query_intent == 'listing':
            return self._handle_listing_query(candidates, search_terms, question)
        
        # 8. Regular search query
        ranked_candidates = self._rank_candidates(candidates, search_terms, question)
        
        # Generate natural language answer
        answer = self._generate_answer(question, ranked_candidates, search_terms, query_intent)
        
        return {
            'answer': answer,
            'candidates': ranked_candidates[:10],  # Return top 10 matches
            'question': question,
            'search_terms': search_terms
        }
    
    def _extract_search_terms(self, question: str) -> Dict[str, List[str]]:
        """
        Extract relevant search terms from the question
        
        Returns:
            Dictionary with skills, experience_years, and keywords
        """
        question_lower = question.lower()
        
        # Extract skills mentioned in question
        skills = []
        for skill in self.common_skills:
            # Use word boundary for single-letter or short skills to avoid false matches
            if len(skill) <= 2:
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', question_lower):
                    skills.append(skill)
            else:
                if skill.lower() in question_lower:
                    skills.append(skill)
        
        # Check for skill variations
        for abbr, full_name in self.skill_variations.items():
            if re.search(r'\b' + re.escape(abbr) + r'\b', question_lower):
                skills.append(full_name)
        
        # Handle broader terms that map to multiple skills
        if re.search(r'\b(cloud|cloud platform|cloud computing)\b', question_lower):
            if 'AWS' not in skills:
                skills.append('AWS')
            if 'Azure' not in skills:
                skills.append('Azure')
            if 'Google Cloud' not in skills:
                skills.append('Google Cloud')
        
        if re.search(r'\b(database|databases|db)\b', question_lower):
            if 'SQL' not in skills:
                skills.append('SQL')
            if 'MongoDB' not in skills:
                skills.append('MongoDB')
        
        if re.search(r'\b(frontend|front-end|front end)\b', question_lower):
            skills.extend(['React', 'JavaScript', 'HTML', 'CSS'])
        
        if re.search(r'\b(backend|back-end|back end)\b', question_lower):
            skills.extend(['Python', 'Java', 'Node.js', 'SQL'])
        
        # Extract experience years
        experience_years = None
        experience_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', question_lower)
        if experience_match:
            experience_years = int(experience_match.group(1))
        
        # Extract general keywords (remove common words)
        stop_words = {
            'which', 'candidates', 'have', 'with', 'who', 'has', 'are', 'is', 'the', 'a', 'an',
            'find', 'search', 'list', 'show', 'get', 'me', 'any', 'some', 'all', 'experience',
            'skills', 'knowledge', 'knows', 'know', 'working', 'worked', 'work', 'years', 'year',
            'candidate', 'resume', 'resumes', 'for', 'do', 'does', 'did', 'can', 'could', 'should',
            'how', 'many', 'much', 'count', 'number', 'total', 'there', 'what', 'when', 'where',
            'tell', 'give', 'provide', 'their', 'them', 'they', 'this', 'that', 'these', 'those'
        }
        
        words = re.findall(r'\b\w+\b', question_lower)
        # Filter out stop words and only keep words that might be actual skills/technologies
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return {
            'skills': list(set(skills)),
            'experience_years': experience_years,
            'keywords': keywords
        }
    
    def _rank_candidates(self, candidates: List[Dict[str, Any]], search_terms: Dict[str, List[str]], question: str) -> List[Dict[str, Any]]:
        """
        Rank candidates based on relevance to the search terms using AI + keyword matching
        
        Returns:
            List of candidates sorted by relevance score
        """
        # Load AI model if not already loaded
        if not self._model_loaded:
            self._load_model()
        
        # Encode the question using AI model for semantic matching
        question_embedding = None
        if self.model:
            try:
                question_embedding = self.model.encode([question])[0]
            except Exception as e:
                print(f"[RAG Agent] Error encoding question: {str(e)}")
        
        ranked = []
        
        print(f"[RAG Agent] Search terms extracted: skills={search_terms['skills']}, keywords={search_terms['keywords'][:5] if len(search_terms['keywords']) > 5 else search_terms['keywords']}")
        print(f"[RAG Agent] AI semantic matching: {'Enabled' if question_embedding is not None else 'Disabled (using keywords only)'}")
        
        for candidate in candidates:
            score = 0
            matched_skills = []
            
            # Get candidate data
            candidate_skills = candidate.get('skills', '').lower()
            candidate_experience = candidate.get('experience', '').lower()
            candidate_summary = candidate.get('summary', '').lower()
            
            # Combine all candidate text for keyword matching
            candidate_text = f"{candidate_skills} {candidate_experience} {candidate_summary}".lower()
            
            # Score based on skill matches
            for skill in search_terms['skills']:
                # Use word boundary for single-letter skills to avoid false matches
                if len(skill) <= 2:
                    if re.search(r'\b' + re.escape(skill.lower()) + r'\b', candidate_skills):
                        score += 30  # High weight for exact skill match
                        matched_skills.append(skill)
                elif skill.lower() in candidate_skills:
                    score += 30  # High weight for exact skill match
                    matched_skills.append(skill)
                elif self._fuzzy_match(skill, candidate_skills):
                    score += 20  # Medium weight for fuzzy skill match
                    matched_skills.append(skill)
            
            # Score based on experience years
            if search_terms['experience_years']:
                candidate_years = self._extract_years_experience(candidate_experience)
                if candidate_years and candidate_years >= search_terms['experience_years']:
                    score += 25
            
            # Score based on keyword matches in all text (only if we have skill matches)
            keyword_score = 0
            for keyword in search_terms['keywords']:
                if keyword in candidate_text:
                    keyword_score += 5
            
            # Only add keyword score if we have at least some skill match
            if matched_skills or keyword_score >= 15:
                score += keyword_score
            
            # AI-powered semantic similarity
            semantic_score = 0
            if question_embedding is not None and self.model:
                try:
                    # Create candidate profile text
                    candidate_profile = f"Skills: {candidate_skills}. Experience: {candidate_experience}. {candidate_summary[:200]}"
                    
                    # Encode candidate profile
                    candidate_embedding = self.model.encode([candidate_profile])[0]
                    
                    # Calculate cosine similarity
                    similarity = cosine_similarity(
                        question_embedding.reshape(1, -1),
                        candidate_embedding.reshape(1, -1)
                    )[0][0]
                    
                    # Convert to score (0-30 points for semantic match)
                    semantic_score = float(similarity * 30)
                    
                except Exception as e:
                    print(f"[RAG Agent] Error calculating semantic similarity: {str(e)}")
            
            # Add semantic score intelligently
            if search_terms['skills']:
                # For skill-specific queries, use semantic score as a boost (max 15 points)
                if matched_skills:
                    score += min(semantic_score, 15)
            else:
                # For general queries, semantic score is more important (full 30 points)
                score += semantic_score
                
                # Fallback to fuzzy matching if AI is not available
                if semantic_score == 0:
                    question_lower = question.lower()
                    if fuzz.partial_ratio(question_lower, candidate_text) > 60:
                        score += 15
            
            # Only include candidates with skill matches when skills are requested
            # If skills in query: require at least 20 points (fuzzy skill match)
            # If no skills in query: allow keyword-based matching with 25 point threshold
            min_threshold = 20 if search_terms['skills'] else 25
            if score >= min_threshold:
                semantic_info = f", semantic={semantic_score:.1f}" if semantic_score > 0 else ""
                print(f"[RAG Agent] {candidate.get('name')}: score={score:.1f}{semantic_info}, matched_skills={matched_skills}")
                ranked.append({
                    'id': candidate.get('id'),
                    'name': candidate.get('name', 'Unknown'),
                    'email': candidate.get('email', ''),
                    'skills': candidate.get('skills', ''),
                    'experience': candidate.get('experience', ''),
                    'matched_skills': ', '.join(matched_skills) if matched_skills else None,
                    'relevance_score': min(int(score), 100),  # Cap at 100
                    'match_score': candidate.get('match_score', 0)
                })
            else:
                print(f"[RAG Agent] {candidate.get('name')}: score={score} (below threshold, excluded)")
        
        # Sort by relevance score
        ranked.sort(key=lambda x: x['relevance_score'], reverse=True)
        print(f"[RAG Agent] Returning {len(ranked)} candidates after filtering")
        
        return ranked
    
    def _fuzzy_match(self, skill: str, text: str) -> bool:
        """
        Check if skill fuzzy matches any part of the text
        """
        if len(skill) <= 2:
            return False
        
        words = text.split()
        for word in words:
            if fuzz.ratio(skill.lower(), word.lower()) > 80:
                return True
        return False
    
    def _extract_years_experience(self, experience_text: str) -> Optional[int]:
        """
        Extract years of experience from text
        """
        match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', experience_text.lower())
        if match:
            return int(match.group(1))
        return None
    
    def _detect_query_intent(self, question: str) -> str:
        """Detect the intent of the query"""
        for intent, pattern in self.query_patterns.items():
            if re.search(pattern, question):
                return intent
        return 'search'
    
    def _is_greeting(self, question: str) -> bool:
        """Check if query is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings']
        return any(greeting in question for greeting in greetings) and len(question.split()) <= 5
    
    def _is_help_query(self, question: str) -> bool:
        """Check if user is asking for help"""
        help_patterns = [
            r'\b(help|guide|how to use|what can you do|how does this work|explain)\b',
            r'^(what|how)\s+(can|do|does|should|could)\s+(i|you)',
        ]
        return any(re.search(pattern, question) for pattern in help_patterns) and len(question.split()) <= 10
    
    def _contains_candidate_name(self, question: str, candidates: List[Dict[str, Any]]) -> bool:
        """Check if the question contains a candidate's name"""
        # Remove common words
        question_clean = re.sub(r'\b(show|me|tell|about|who|is|the|profile|full|information|details)\b', '', question)
        question_clean = question_clean.strip()
        
        # Check if at least 2 consecutive words match a candidate name
        for candidate in candidates:
            name = candidate.get('name', '').lower()
            if not name:
                continue
            
            # Split name into words
            name_words = name.split()
            
            # If name has 2+ words and both appear in question
            if len(name_words) >= 2:
                if all(word in question for word in name_words):
                    return True
            
            # Or if full name is in question
            if name in question:
                return True
            
            # Or if single name word appears in specific patterns like "show [name]", "about [name]"
            for name_word in name_words:
                if len(name_word) >= 4:  # Only match significant name parts (not "jr", "sr", etc)
                    if re.search(r'\b(show|tell|about|who is|profile of)\s+' + re.escape(name_word), question):
                        return True
        
        return False
    
    def _handle_greeting(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle greeting queries"""
        total_candidates = len(set(c['name'] for c in candidates))
        return {
            'answer': f"Hello! 👋 I'm your Resume Assistant. I currently have {total_candidates} candidates in the database. You can ask me questions like:\n• 'Who knows Python and Docker?'\n• 'Show me candidates with 5+ years experience'\n• 'Best candidates for cloud engineer role'\n• 'Total candidates with SQL experience'\n\nHow can I help you today?",
            'candidates': [],
            'question': 'greeting'
        }
    
    def _handle_help_query(self) -> Dict[str, Any]:
        """Handle help queries"""
        return {
            'answer': "I can help you find candidates by:\n\n📋 **Skills**: 'Who knows React and Node.js?'\n⏱️ **Experience**: 'Candidates with 3+ years Python'\n🏆 **Comparison**: 'Best candidate for DevOps role'\n📊 **Statistics**: 'How many candidates know AWS?'\n👤 **Specific Info**: 'Tell me about John Doe'\n💡 **Recommendations**: 'Suggest candidates for data science'\n\nJust ask naturally - I understand conversational language!",
            'candidates': [],
            'question': 'help'
        }
    
    def _handle_count_query(self, candidates: List[Dict[str, Any]], search_terms: Dict[str, List[str]], question: str) -> Dict[str, Any]:
        """Handle count/statistics queries"""
        if search_terms['skills']:
            # Rank candidates based on skill match
            ranked_candidates = self._rank_candidates(candidates, search_terms, question)
            skills_str = ', '.join(search_terms['skills'])
            
            # Get unique candidates (in case of duplicates)
            unique_names = set(c['name'] for c in ranked_candidates)
            unique_count = len(unique_names)
            
            if unique_count == 0:
                answer = f"I couldn't find any candidates with {skills_str} experience. Would you like me to search for similar skills?"
            elif unique_count == 1:
                name = list(unique_names)[0]
                answer = f"I found **1 candidate** with {skills_str} experience: **{name}**. Would you like to see their full profile?"
            else:
                answer = f"I found **{unique_count} candidates** with {skills_str} experience. Here they are below! 👇"
            
            return {
                'answer': answer,
                'candidates': ranked_candidates[:10],
                'question': question
            }
        else:
            # General count without skills
            total_unique = len(set(c['name'] for c in candidates))
            return {
                'answer': f"There are **{total_unique} candidates** in the database. Ask me about specific skills or experience to narrow down your search! 🔍",
                'candidates': [],
                'question': question
            }
    
    def _handle_comparison_query(self, candidates: List[Dict[str, Any]], search_terms: Dict[str, List[str]], question: str) -> Dict[str, Any]:
        """Handle comparison queries (best, top, strongest)"""
        ranked_candidates = self._rank_candidates(candidates, search_terms, question)
        
        if not ranked_candidates:
            skills_str = ', '.join(search_terms['skills']) if search_terms['skills'] else 'those requirements'
            return {
                'answer': f"I couldn't find candidates matching {skills_str}. Try adjusting your criteria or check available skills.",
                'candidates': [],
                'question': question
            }
        
        top_candidate = ranked_candidates[0]
        skills_str = ', '.join(search_terms['skills']) if search_terms['skills'] else 'your criteria'
        
        if len(ranked_candidates) == 1:
            answer = f"**{top_candidate['name']}** is the only candidate matching {skills_str} (relevance: {top_candidate['relevance_score']}%)."
        else:
            answer = f"Based on your query, **{top_candidate['name']}** is the top match with a {top_candidate['relevance_score']}% relevance score! 🌟\n\nI found {len(ranked_candidates)} candidates total. Here are the best matches:"
        
        return {
            'answer': answer,
            'candidates': ranked_candidates[:5],
            'question': question
        }
    
    def _handle_specific_person_query(self, candidates: List[Dict[str, Any]], question: str) -> Dict[str, Any]:
        """Handle queries about specific people"""
        # Extract name from question
        question_lower = question.lower()
        
        # Remove common query words to extract the name
        name_query = re.sub(r'\b(show|me|tell|about|who|is|information|details|of|profile|full|the)\b', '', question_lower)
        name_query = name_query.strip()
        
        # Find matching candidates by checking if name parts are in candidate name
        matches = []
        for candidate in candidates:
            candidate_name = candidate.get('name', '').lower()
            if not candidate_name:
                continue
            
            # Check if the name query matches the candidate name
            # Split both into words and check for matches
            query_words = set(name_query.split())
            name_words = set(candidate_name.split())
            
            # If at least 2 words match or full name query is in candidate name
            if (len(query_words & name_words) >= 2) or (name_query in candidate_name) or (candidate_name in question_lower):
                matches.append(candidate)
        
        if not matches:
            return {
                'answer': f"I couldn't find anyone matching '{name_query}' in the database. Try:\n• 'List all candidates' to see available names\n• Checking the spelling\n• Using first name or last name only",
                'candidates': [],
                'question': question
            }
        
        # Get unique matches (deduplicate by name)
        unique_matches_dict = {}
        for c in matches:
            name = c['name']
            if name not in unique_matches_dict:
                unique_matches_dict[name] = c
        
        match = list(unique_matches_dict.values())[0]
        
        # Create detailed profile
        answer = f"## 👤 **{match['name']}'s Full Profile**\n\n"
        
        if match.get('email'):
            answer += f"📧 **Email**: {match['email']}\n\n"
        
        if match.get('experience'):
            answer += f"⏱️ **Experience**: {match['experience']}\n\n"
        
        if match.get('skills'):
            skills = match['skills']
            # Show all skills, formatted nicely
            if len(skills) > 300:
                answer += f"💼 **Skills**:\n{skills[:300]}...\n\n"
            else:
                answer += f"💼 **Skills**: {skills}\n\n"
        
        if match.get('match_score') and match['match_score'] > 0:
            answer += f"📊 **Overall Match Score**: {match['match_score']:.1f}%\n"
            if match.get('skill_match_score'):
                answer += f"• Skill Match: {match['skill_match_score']:.1f}%\n"
            if match.get('experience_match_score'):
                answer += f"• Experience Match: {match['experience_match_score']:.1f}%\n"
        
        answer += f"\n✨ This is the complete profile I have for **{match['name']}**!"
        
        # Return the unique match
        return {
            'answer': answer,
            'candidates': list(unique_matches_dict.values())[:1],  # Only return first unique match
            'question': question
        }
    
    def _handle_recommendation_query(self, candidates: List[Dict[str, Any]], search_terms: Dict[str, List[str]], question: str, job_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle recommendation queries"""
        ranked_candidates = self._rank_candidates(candidates, search_terms, question)
        
        if not ranked_candidates:
            return {
                'answer': "I need more specific requirements to make a recommendation. Could you tell me what skills or experience you're looking for?",
                'candidates': [],
                'question': question
            }
        
        top_3 = ranked_candidates[:3]
        skills_str = ', '.join(search_terms['skills']) if search_terms['skills'] else 'your requirements'
        
        answer = f"Based on {skills_str}, I recommend these candidates:\n\n"
        for i, candidate in enumerate(top_3, 1):
            answer += f"{i}. **{candidate['name']}** (relevance: {candidate['relevance_score']}%)\n"
        
        answer += f"\n{top_3[0]['name']} stands out as the strongest match! Would you like more details?"
        
        return {
            'answer': answer,
            'candidates': ranked_candidates[:5],
            'question': question
        }
    
    def _handle_listing_query(self, candidates: List[Dict[str, Any]], search_terms: Dict[str, List[str]], question: str) -> Dict[str, Any]:
        """Handle listing queries"""
        if search_terms['skills']:
            ranked_candidates = self._rank_candidates(candidates, search_terms, question)
            skills_str = ', '.join(search_terms['skills'])
            
            if not ranked_candidates:
                answer = f"No candidates found with {skills_str}. Here's everyone I have:"
                # Return all candidates with proper structure
                unique_candidates_dict = {c['name']: c for c in candidates}
                formatted_candidates = []
                
                for candidate in unique_candidates_dict.values():
                    formatted_candidates.append({
                        'id': candidate.get('id'),
                        'name': candidate.get('name', 'Unknown'),
                        'email': candidate.get('email', ''),
                        'skills': candidate.get('skills', ''),
                        'experience': candidate.get('experience', ''),
                        'matched_skills': None,
                        'relevance_score': int(candidate.get('match_score', 0)),
                        'match_score': candidate.get('match_score', 0)
                    })
                
                return {
                    'answer': answer,
                    'candidates': formatted_candidates[:10],
                    'question': question
                }
            
            unique_count = len(set(c['name'] for c in ranked_candidates))
            answer = f"Here are **{unique_count} candidates** with {skills_str}:"
            
            return {
                'answer': answer,
                'candidates': ranked_candidates[:10],
                'question': question
            }
        else:
            # List all candidates
            unique_candidates_dict = {c['name']: c for c in candidates}
            unique_candidates_list = []
            
            for candidate in unique_candidates_dict.values():
                # Add relevance_score if not present
                if 'relevance_score' not in candidate:
                    unique_candidates_list.append({
                        'id': candidate.get('id'),
                        'name': candidate.get('name', 'Unknown'),
                        'email': candidate.get('email', ''),
                        'skills': candidate.get('skills', ''),
                        'experience': candidate.get('experience', ''),
                        'matched_skills': None,
                        'relevance_score': candidate.get('match_score', 0),  # Use existing match_score or 0
                        'match_score': candidate.get('match_score', 0)
                    })
                else:
                    unique_candidates_list.append(candidate)
            
            answer = f"Here are all **{len(unique_candidates_list)} candidates** in the database:"
            
            return {
                'answer': answer,
                'candidates': unique_candidates_list[:10],
                'question': question
            }
    
    def _generate_answer(self, question: str, ranked_candidates: List[Dict[str, Any]], search_terms: Dict[str, List[str]], query_intent: str = 'search') -> str:
        """
        Generate a natural language answer based on results
        """
        if not ranked_candidates:
            skills_str = ', '.join(search_terms['skills']) if search_terms['skills'] else 'your requirements'
            return f"I couldn't find any candidates matching {skills_str}. Try:\n• Broadening your search terms\n• Checking available skills\n• Asking 'list all candidates' to see everyone"
        
        count = len(set(c['name'] for c in ranked_candidates))
        skills_str = ', '.join(search_terms['skills']) if search_terms['skills'] else 'your requirements'
        
        if count == 1:
            answer = f"I found **1 candidate** matching {skills_str}! 🎯"
        elif count <= 5:
            answer = f"I found **{count} candidates** matching {skills_str}. Here they are:"
        else:
            answer = f"Great! I found **{count} candidates** matching {skills_str}. Here are the top matches:"
        
        # Add context about top candidate
        if ranked_candidates:
            top_candidate = ranked_candidates[0]
            if top_candidate['relevance_score'] >= 80:
                answer += f"\n\n⭐ **{top_candidate['name']}** is a strong match with {top_candidate['relevance_score']}% relevance!"
        
        return answer
    
    def index_resumes(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Index resumes for faster querying (placeholder for vector DB integration)
        
        Args:
            candidates: List of candidate dictionaries
            
        Returns:
            Indexing status
        """
        return {
            'indexed': len(candidates),
            'status': 'success'
        }
