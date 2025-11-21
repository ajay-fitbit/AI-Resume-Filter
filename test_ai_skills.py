import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.skills_agent import SkillsAssessmentAgent

# Test job description with LLM, RAG, AI
job_desc = """
We are looking for an AI Engineer with experience in:
- Large Language Models (LLM)
- Retrieval Augmented Generation (RAG)
- Machine Learning and AI
- Python programming
- TensorFlow or PyTorch
"""

# Test resume skills
resume_skills_1 = ["AI", "LLM", "RAG", "Python", "TensorFlow", "Machine Learning"]
resume_skills_2 = ["Python", "SQL", "Django"]  # No AI skills

agent = SkillsAssessmentAgent()

print("="*60)
print("Test 1: Resume WITH LLM, RAG, AI skills")
print("="*60)
result1 = agent.execute({
    "resume_skills": resume_skills_1,
    "job_description": job_desc
})

print(f"\nSkill Match Score: {result1['skill_match_score']}%")
print(f"Required Skills: {result1['required_skills']}")
print(f"Matched Skills: {result1['matched_skills']}")
print(f"Missing Skills: {result1['missing_skills']}")

print("\n" + "="*60)
print("Test 2: Resume WITHOUT AI skills")
print("="*60)
result2 = agent.execute({
    "resume_skills": resume_skills_2,
    "job_description": job_desc
})

print(f"\nSkill Match Score: {result2['skill_match_score']}%")
print(f"Required Skills: {result2['required_skills']}")
print(f"Matched Skills: {result2['matched_skills']}")
print(f"Missing Skills: {result2['missing_skills']}")
