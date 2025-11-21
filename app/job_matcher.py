import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

class JobMatcher:
    def __init__(self):
        # Load sentence transformer for semantic similarity (lazy loading)
        self.model = None
        self._model_loaded = False
    
    def _load_model(self):
        """Lazy load the sentence transformer model"""
        if not self._model_loaded:
            try:
                print("Loading AI model (this may take a moment on first run)...")
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self._model_loaded = True
                print("AI model loaded successfully!")
            except Exception as e:
                print(f"Warning: Could not load sentence transformer model: {e}")
                self.model = None
                self._model_loaded = True
    
    def calculate_match_score(self, resume_data, job_description):
        """Calculate overall match score between resume and JD"""
        
        scores = {
            'semantic_similarity': self._semantic_similarity(resume_data['raw_text'], job_description),
            'keyword_match': self._keyword_match(resume_data['raw_text'], job_description),
            'skill_match': self._skill_match(resume_data['skills'], job_description),
            'experience_match': self._experience_match(resume_data['experience_years'], job_description)
        }
        
        # Weighted average
        weights = {
            'semantic_similarity': 0.30,
            'keyword_match': 0.25,
            'skill_match': 0.30,
            'experience_match': 0.15
        }
        
        overall_score = sum(scores[key] * weights[key] for key in scores)
        
        return {
            'overall_score': round(overall_score, 2),
            'skill_match_score': round(scores['skill_match'], 2),
            'experience_match_score': round(scores['experience_match'], 2),
            'keyword_match_score': round(scores['keyword_match'], 2),
            'semantic_similarity_score': round(scores['semantic_similarity'], 2),
            'tier': self._determine_tier(overall_score)
        }
    
    def _semantic_similarity(self, resume_text, job_description):
        """Calculate semantic similarity using sentence transformers"""
        # Load model if not loaded yet
        if not self._model_loaded:
            self._load_model()
        
        if not self.model:
            return 50.0  # Default score if model not available
        
        try:
            # Encode texts
            resume_embedding = self.model.encode([resume_text])
            jd_embedding = self.model.encode([job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
            
            # Convert to percentage
            return float(similarity * 100)
        except Exception as e:
            print(f"Error in semantic similarity: {e}")
            return 50.0
    
    def _keyword_match(self, resume_text, job_description):
        """Calculate keyword overlap score"""
        try:
            # Use TF-IDF vectorizer
            vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
            
            # Fit and transform both texts
            tfidf_matrix = vectorizer.fit_transform([resume_text.lower(), job_description.lower()])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity * 100)
        except Exception as e:
            print(f"Error in keyword match: {e}")
            return 50.0
    
    def _skill_match(self, resume_skills, job_description):
        """Calculate skill matching score"""
        if not resume_skills or resume_skills == 'Not specified':
            return 0.0
        
        resume_skills_list = [s.strip().lower() for s in resume_skills.split(',')]
        jd_lower = job_description.lower()
        
        matched_skills = 0
        for skill in resume_skills_list:
            if skill in jd_lower:
                matched_skills += 1
        
        if resume_skills_list:
            score = (matched_skills / len(resume_skills_list)) * 100
            return min(score, 100.0)
        
        return 0.0
    
    def _experience_match(self, resume_experience, job_description):
        """Calculate experience matching score"""
        # Extract required experience from JD
        required_exp = self._extract_required_experience(job_description)
        
        if required_exp == 0:
            return 100.0  # No specific requirement
        
        if resume_experience >= required_exp:
            return 100.0
        elif resume_experience >= required_exp * 0.8:
            return 80.0
        elif resume_experience >= required_exp * 0.6:
            return 60.0
        elif resume_experience >= required_exp * 0.4:
            return 40.0
        else:
            return 20.0
    
    def _extract_required_experience(self, job_description):
        """Extract required years of experience from JD"""
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience\s+(?:of\s+)?(\d+)\+?\s*years?',
            r'minimum\s+(\d+)\s+years?'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, job_description.lower())
            if matches:
                return int(matches[0])
        
        return 0
    
    def _determine_tier(self, score):
        """Determine tier based on score"""
        if score >= 80:
            return "Top Tier"
        elif score >= 60:
            return "Medium Tier"
        else:
            return "Low Tier"
    
    def generate_explanation(self, resume_data, job_description, scores):
        """Generate human-readable explanation of the match"""
        explanation_parts = []
        
        # Overall assessment
        tier = scores['tier']
        overall = scores['overall_score']
        
        if tier == "Top Tier":
            explanation_parts.append(f"[EXCELLENT] Match score {overall}% - Strong candidate for this position.")
        elif tier == "Medium Tier":
            explanation_parts.append(f"[MODERATE] Match score {overall}% - Meets most requirements, some areas for improvement.")
        else:
            explanation_parts.append(f"[LOW] Match score {overall}% - Does not meet several key requirements.")
        
        # Skill assessment
        skill_score = scores['skill_match_score']
        if skill_score >= 70:
            explanation_parts.append(f"Strong skill alignment ({skill_score}%).")
        elif skill_score >= 40:
            explanation_parts.append(f"Partial skill match ({skill_score}%) - may need training.")
        else:
            explanation_parts.append(f"Limited skill match ({skill_score}%).")
        
        # Experience assessment
        exp_score = scores['experience_match_score']
        if exp_score >= 80:
            explanation_parts.append(f"Experience requirement met ({exp_score}%).")
        elif exp_score >= 60:
            explanation_parts.append(f"Slightly less experience than required ({exp_score}%).")
        else:
            explanation_parts.append(f"Insufficient experience ({exp_score}%).")
        
        # Semantic relevance
        semantic_score = scores['semantic_similarity_score']
        if semantic_score >= 70:
            explanation_parts.append("Content highly relevant to job description.")
        elif semantic_score >= 50:
            explanation_parts.append("Moderately relevant background.")
        else:
            explanation_parts.append("Limited relevance to job requirements.")
        
        return " ".join(explanation_parts)
