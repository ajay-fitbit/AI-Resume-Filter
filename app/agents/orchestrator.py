"""
Ranking Orchestrator Agent

Coordinates all agents in the multi-agent workflow and produces final candidate ranking
"""

from typing import Dict, Any, List
import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent, AgentState
from .resume_parser_agent import ResumeParserAgent
from .skills_agent import SkillsAssessmentAgent
from .semantic_agent import SemanticMatchingAgent
from .red_flag_agent import RedFlagAgent


class RankingOrchestratorAgent(BaseAgent):
    """
    Orchestrator that coordinates all agents and produces final rankings
    
    Workflow:
    1. ResumeParserAgent: Extract structured data
    2. SkillsAssessmentAgent: Evaluate skills match
    3. SemanticMatchingAgent: AI-powered semantic similarity
    4. RedFlagAgent: Detect potential issues
    5. Calculate final weighted score and tier
    """
    
    def __init__(self):
        super().__init__(name="RankingOrchestratorAgent")
        
        # Initialize all agents
        self.resume_parser = ResumeParserAgent()
        self.skills_agent = SkillsAssessmentAgent()
        self.semantic_agent = SemanticMatchingAgent()
        self.red_flag_agent = RedFlagAgent()
        
        self.log("Initialized all sub-agents")
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute full multi-agent workflow
        
        Args:
            input_data: {
                "file_path": str - Path to resume file,
                "job_description": str - Job description text,
                "required_experience": int - Years required (optional)
            }
            
        Returns:
            {
                "success": bool,
                "candidate_data": dict,
                "scores": dict with all score components,
                "overall_score": float,
                "tier": str,
                "red_flags": list,
                "agent_execution_log": list,
                "total_execution_time": float
            }
        """
        start_time = time.time()
        state = AgentState()
        
        file_path = input_data.get("file_path")
        job_description = input_data.get("job_description", "")
        required_experience = input_data.get("required_experience", 0)
        
        if not file_path or not job_description:
            self.log("Missing required inputs: file_path or job_description", "error")
            return {
                "success": False,
                "error": "Missing file_path or job_description"
            }
        
        self.log(f"Starting workflow for: {os.path.basename(file_path)}")
        
        # ===== STEP 1: Parse Resume =====
        parse_result = self.resume_parser.timed_execute({"file_path": file_path})
        state.add_agent_result("ResumeParserAgent", parse_result)
        
        if not parse_result.get("success"):
            self.log("Resume parsing failed, aborting workflow", "error")
            return self._build_error_response(state, start_time)
        
        resume_data = parse_result.get("resume_data")
        state.set("resume_data", resume_data)
        
        # ===== STEP 2: Assess Skills =====
        # Convert skills string to list (skills are comma-separated in resume_data)
        skills_str = resume_data.get("skills", "")
        if isinstance(skills_str, str):
            resume_skills = [s.strip() for s in skills_str.split(',') if s.strip() and s.strip() != 'Not specified']
        else:
            resume_skills = skills_str  # Already a list
            
        skills_result = self.skills_agent.timed_execute({
            "resume_skills": resume_skills,
            "job_description": job_description
        })
        state.add_agent_result("SkillsAssessmentAgent", skills_result)
        
        # ===== STEP 3: Semantic Matching =====
        semantic_result = self.semantic_agent.timed_execute({
            "resume_text": resume_data.get("raw_text", ""),
            "job_description": job_description
        })
        state.add_agent_result("SemanticMatchingAgent", semantic_result)
        
        # ===== STEP 4: Red Flag Detection =====
        red_flag_result = self.red_flag_agent.timed_execute({
            "resume_data": resume_data,
            "job_description": job_description,
            "required_experience": required_experience
        })
        state.add_agent_result("RedFlagAgent", red_flag_result)
        
        # ===== STEP 5: Calculate Final Score =====
        final_result = self._calculate_final_score(state, job_description, required_experience)
        
        total_time = time.time() - start_time
        final_result["total_execution_time"] = round(total_time, 3)
        
        # Collect all agent logs
        final_result["agent_execution_log"] = self._collect_agent_logs()
        
        self.log(f"Workflow completed in {total_time:.3f}s - "
                f"Final Score: {final_result.get('overall_score', 0):.2f}%", "success")
        
        return final_result
    
    def _calculate_final_score(self, state: AgentState, job_description: str, 
                               required_experience: int) -> Dict[str, Any]:
        """Calculate final weighted score from all agent results"""
        
        resume_data = state.get("resume_data")
        skills_result = state.get_agent_result("SkillsAssessmentAgent")
        semantic_result = state.get_agent_result("SemanticMatchingAgent")
        red_flag_result = state.get_agent_result("RedFlagAgent")
        
        # Extract scores
        skill_score = skills_result.get("skill_match_score", 0.0)
        semantic_score = semantic_result.get("semantic_similarity_score", 0.0)
        keyword_score = semantic_result.get("keyword_match_score", 0.0)
        experience_score = self._calculate_experience_score(
            resume_data.get("experience_years", 0),
            required_experience
        )
        
        # Weighted average (same as original system)
        weights = {
            "semantic": 0.30,
            "keyword": 0.25,
            "skill": 0.30,
            "experience": 0.15
        }
        
        overall_score = (
            semantic_score * weights["semantic"] +
            keyword_score * weights["keyword"] +
            skill_score * weights["skill"] +
            experience_score * weights["experience"]
        )
        
        # Determine tier
        tier = self._determine_tier(overall_score)
        
        # Generate explanation
        explanation = self._generate_explanation(
            overall_score, tier, skill_score, 
            semantic_score, experience_score,
            skills_result.get("matched_skills", []),
            skills_result.get("missing_skills", [])
        )
        
        return {
            "success": True,
            "candidate_data": {
                "name": resume_data.get("name", "Unknown"),
                "email": resume_data.get("email", ""),
                "phone": resume_data.get("phone", ""),
                "experience_years": resume_data.get("experience_years", 0),
                "education": resume_data.get("education", ""),
                "skills": resume_data.get("skills", [])
            },
            "scores": {
                "overall_score": round(overall_score, 2),
                "skill_match_score": round(skill_score, 2),
                "experience_match_score": round(experience_score, 2),
                "keyword_match_score": round(keyword_score, 2),
                "semantic_similarity_score": round(semantic_score, 2)
            },
            "overall_score": round(overall_score, 2),
            "tier": tier,
            "explanation": explanation,
            "red_flags": red_flag_result.get("red_flags", []),
            "red_flag_count": red_flag_result.get("red_flag_count", 0),
            "weights_used": weights
        }
    
    def _calculate_experience_score(self, candidate_years: int, required_years: int) -> float:
        """Calculate experience match score"""
        if required_years == 0:
            return 100.0
        
        if candidate_years >= required_years:
            return 100.0
        else:
            # Partial credit for close matches
            return max(0.0, (candidate_years / required_years) * 100)
    
    def _determine_tier(self, score: float) -> str:
        """Determine candidate tier based on score"""
        if score >= 75:
            return "Top Tier"
        elif score >= 50:
            return "Medium Tier"
        else:
            return "Low Tier"
    
    def _generate_explanation(self, overall_score: float, tier: str, 
                             skill_score: float, semantic_score: float,
                             experience_score: float, matched_skills: List[str],
                             missing_skills: List[str]) -> str:
        """Generate human-readable explanation"""
        
        explanation_parts = [f"This candidate is rated as {tier} with an overall score of {overall_score:.1f}%."]
        
        # Skills analysis
        if skill_score >= 75:
            explanation_parts.append(f"Strong skill match ({skill_score:.1f}%) with {len(matched_skills)} key skills aligned.")
        elif skill_score >= 50:
            explanation_parts.append(f"Moderate skill match ({skill_score:.1f}%). Some key skills are missing.")
        else:
            explanation_parts.append(f"Limited skill match ({skill_score:.1f}%). Significant skill gaps exist.")
        
        # Experience
        if experience_score >= 90:
            explanation_parts.append("Experience level meets requirements.")
        elif experience_score >= 50:
            explanation_parts.append("Experience is somewhat below requirements.")
        else:
            explanation_parts.append("Experience level is insufficient.")
        
        # Semantic alignment
        if semantic_score >= 70:
            explanation_parts.append("Resume content aligns well with job requirements.")
        else:
            explanation_parts.append("Resume content partially aligns with job requirements.")
        
        return " ".join(explanation_parts)
    
    def _collect_agent_logs(self) -> List[Dict[str, Any]]:
        """Collect logs from all agents"""
        all_logs = []
        
        for agent in [self.resume_parser, self.skills_agent, 
                     self.semantic_agent, self.red_flag_agent]:
            all_logs.extend(agent.get_logs())
        
        return all_logs
    
    def _build_error_response(self, state: AgentState, start_time: float) -> Dict[str, Any]:
        """Build error response when workflow fails"""
        return {
            "success": False,
            "error": "Workflow failed during execution",
            "agent_results": state.agent_results,
            "errors": state.errors,
            "total_execution_time": round(time.time() - start_time, 3)
        }
