"""
Semantic Matching Agent

Uses transformer models for AI-powered semantic similarity between resume and job description
"""

from typing import Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SemanticMatchingAgent(BaseAgent):
    """Agent responsible for semantic similarity analysis using AI"""
    
    def __init__(self):
        super().__init__(name="SemanticMatchingAgent")
        self.model = None
        self._model_loaded = False
        self.log("Initialized (model will lazy-load on first use)")
        
    def _load_model(self):
        """Lazy load the transformer model"""
        if not self._model_loaded:
            try:
                self.log("Loading sentence-transformers model (all-MiniLM-L6-v2)...")
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self._model_loaded = True
                self.log("AI model loaded successfully!", "success")
            except Exception as e:
                self.log(f"Failed to load model: {str(e)}", "error")
                self.model = None
                self._model_loaded = True
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate semantic similarity using transformer embeddings
        
        Args:
            input_data: {
                "resume_text": str - Full resume text,
                "job_description": str - Job description text
            }
            
        Returns:
            {
                "success": bool,
                "semantic_similarity_score": float (0-100),
                "keyword_match_score": float (0-100),
                "embedding_dimension": int,
                "model_name": str
            }
        """
        resume_text = input_data.get("resume_text", "")
        job_description = input_data.get("job_description", "")
        
        if not resume_text or not job_description:
            self.log("Missing resume_text or job_description", "error")
            return {
                "success": False,
                "error": "Missing required text inputs",
                "semantic_similarity_score": 0.0,
                "keyword_match_score": 0.0
            }
        
        self.log(f"Analyzing semantic similarity (Resume: {len(resume_text)} chars, "
                f"JD: {len(job_description)} chars)")
        
        # Load model if needed
        if not self._model_loaded:
            self._load_model()
        
        # Calculate semantic similarity
        semantic_score = self._calculate_semantic_similarity(resume_text, job_description)
        
        # Calculate keyword-based similarity (TF-IDF)
        keyword_score = self._calculate_keyword_match(resume_text, job_description)
        
        self.log(f"Semantic: {semantic_score:.2f}%, Keywords: {keyword_score:.2f}%")
        
        return {
            "success": True,
            "semantic_similarity_score": round(semantic_score, 2),
            "keyword_match_score": round(keyword_score, 2),
            "embedding_dimension": 384 if self.model else None,
            "model_name": "all-MiniLM-L6-v2" if self.model else "TF-IDF only"
        }
    
    def _calculate_semantic_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate semantic similarity using transformer embeddings"""
        if not self.model:
            self.log("Model not available, returning default score", "warning")
            return 50.0
        
        try:
            # Encode texts to 384-dimensional vectors
            resume_embedding = self.model.encode([resume_text])
            jd_embedding = self.model.encode([job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
            
            # Convert to percentage
            score = float(similarity * 100)
            return max(0.0, min(100.0, score))
            
        except Exception as e:
            self.log(f"Semantic similarity calculation failed: {str(e)}", "error")
            return 50.0
    
    def _calculate_keyword_match(self, resume_text: str, job_description: str) -> float:
        """Calculate TF-IDF based keyword matching"""
        try:
            vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=500,
                ngram_range=(1, 2)
            )
            
            # Fit on both documents
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage
            score = float(similarity * 100)
            return max(0.0, min(100.0, score))
            
        except Exception as e:
            self.log(f"Keyword match calculation failed: {str(e)}", "error")
            return 50.0
