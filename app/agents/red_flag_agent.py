"""
Red Flag Detection Agent

Analyzes candidate history for potential issues: job hopping, career gaps, missing skills, etc.
"""

from typing import Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent
from app.red_flag_detector import RedFlagDetector


class RedFlagAgent(BaseAgent):
    """Agent responsible for detecting red flags in candidate profiles"""
    
    def __init__(self):
        super().__init__(name="RedFlagAgent")
        self.detector = RedFlagDetector()
        self.log("Initialized with RedFlagDetector")
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect red flags in candidate profile
        
        Args:
            input_data: {
                "resume_data": dict - Parsed resume data,
                "job_description": str - Job description,
                "required_experience": int - Years of experience required
            }
            
        Returns:
            {
                "success": bool,
                "red_flags": List[dict] - List of detected red flags,
                "red_flag_count": int,
                "severity_breakdown": dict
            }
        """
        resume_data = input_data.get("resume_data")
        job_description = input_data.get("job_description", "")
        required_experience = input_data.get("required_experience", 0)
        
        if not resume_data:
            self.log("No resume_data provided", "error")
            return {
                "success": False,
                "error": "Missing resume_data",
                "red_flags": [],
                "red_flag_count": 0
            }
        
        self.log("Detecting red flags in candidate profile")
        
        try:
            red_flags = self.detector.detect_all_flags(
                resume_data,
                job_description
            )
            
            # Count by severity
            severity_breakdown = {
                "low": 0,
                "medium": 0,
                "high": 0
            }
            
            for flag in red_flags:
                severity = flag.get("severity", "low")
                severity_breakdown[severity] = severity_breakdown.get(severity, 0) + 1
            
            self.log(f"Detected {len(red_flags)} red flags - "
                    f"High: {severity_breakdown['high']}, "
                    f"Medium: {severity_breakdown['medium']}, "
                    f"Low: {severity_breakdown['low']}")
            
            return {
                "success": True,
                "red_flags": red_flags,
                "red_flag_count": len(red_flags),
                "severity_breakdown": severity_breakdown
            }
            
        except Exception as e:
            self.log(f"Red flag detection failed: {str(e)}", "error")
            return {
                "success": False,
                "error": str(e),
                "red_flags": [],
                "red_flag_count": 0
            }
