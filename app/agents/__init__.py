"""
Multi-Agent System for AI Resume Filtering

This package contains specialized agents that work together to analyze resumes:
- ResumeParserAgent: Extracts structured data from documents
- SkillsAssessmentAgent: Evaluates candidate skills
- SemanticMatchingAgent: Performs AI-powered semantic similarity
- RedFlagAgent: Detects potential issues in candidate history
- RankingOrchestratorAgent: Coordinates all agents and produces final rankings
"""

from .resume_parser_agent import ResumeParserAgent
from .skills_agent import SkillsAssessmentAgent
from .semantic_agent import SemanticMatchingAgent
from .red_flag_agent import RedFlagAgent
from .orchestrator import RankingOrchestratorAgent

__all__ = [
    'ResumeParserAgent',
    'SkillsAssessmentAgent',
    'SemanticMatchingAgent',
    'RedFlagAgent',
    'RankingOrchestratorAgent'
]
