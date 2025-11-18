"""
Resume Parser Agent

Wraps the existing ResumeParser class as an agent that extracts structured data from resumes
"""

from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent
from app.resume_parser import ResumeParser


class ResumeParserAgent(BaseAgent):
    """Agent responsible for parsing resume documents"""
    
    def __init__(self):
        super().__init__(name="ResumeParserAgent")
        self.parser = ResumeParser()
        self.log("Initialized with ResumeParser")
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse resume from file path
        
        Args:
            input_data: {
                "file_path": str - Path to resume file (PDF/DOCX)
            }
            
        Returns:
            {
                "success": bool,
                "resume_data": dict with extracted information,
                "error": str (if failed)
            }
        """
        file_path = input_data.get("file_path")
        
        if not file_path:
            self.log("No file_path provided", "error")
            return {
                "success": False,
                "error": "Missing file_path in input",
                "resume_data": None
            }
        
        self.log(f"Parsing resume: {os.path.basename(file_path)}")
        
        try:
            resume_data = self.parser.parse_resume(file_path)
            
            if resume_data:
                self.log(f"Successfully parsed - Name: {resume_data.get('name', 'Unknown')}, "
                        f"Experience: {resume_data.get('experience_years', 0)} years, "
                        f"Skills: {len(resume_data.get('skills', []))} found")
                
                return {
                    "success": True,
                    "resume_data": resume_data,
                    "error": None
                }
            else:
                self.log("Parser returned None - file may be corrupted", "warning")
                return {
                    "success": False,
                    "error": "Failed to parse resume - file may be corrupted",
                    "resume_data": None
                }
                
        except Exception as e:
            self.log(f"Parsing error: {str(e)}", "error")
            return {
                "success": False,
                "error": str(e),
                "resume_data": None
            }
