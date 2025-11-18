"""
Debug script to check skills extraction for Yuki Tanaka resume
"""
import sys
sys.path.insert(0, '.')

from app.resume_parser import ResumeParser
from app.agents.skills_agent import SkillsAssessmentAgent

# Parse the resume
parser = ResumeParser()
resume_path = r"uploads\Yuki_Tanaka-resume.pdf"
resume_data = parser.parse_resume(resume_path)

print("=" * 80)
print("RESUME DATA")
print("=" * 80)
print(f"Name: {resume_data.get('name')}")
print(f"Email: {resume_data.get('email')}")
print(f"Experience: {resume_data.get('experience_years')} years")
print(f"\nSkills ({len(resume_data.get('skills', []))} found):")
for skill in resume_data.get('skills', []):
    print(f"  - {skill}")

# Sample job description (you can replace with actual JD from database)
job_description = """
We are looking for a Python developer with experience in web development.
Must have skills in Django, Flask, and database management.
Experience with MySQL and PostgreSQL is required.
"""

print("\n" + "=" * 80)
print("JOB DESCRIPTION")
print("=" * 80)
print(job_description)

# Test skills agent
# Convert skills string to list (same as orchestrator does)
skills_str = resume_data.get('skills', '')
if isinstance(skills_str, str):
    resume_skills = [s.strip() for s in skills_str.split(',') if s.strip() and s.strip() != 'Not specified']
else:
    resume_skills = skills_str

skills_agent = SkillsAssessmentAgent()
result = skills_agent.execute({
    "resume_skills": resume_skills,
    "job_description": job_description
})

print("\n" + "=" * 80)
print("SKILLS ASSESSMENT RESULT")
print("=" * 80)
print(f"Success: {result.get('success')}")
print(f"Skill Match Score: {result.get('skill_match_score')}%")
print(f"\nRequired Skills ({len(result.get('required_skills', []))}):")
for skill in result.get('required_skills', []):
    print(f"  - {skill}")
print(f"\nMatched Skills ({len(result.get('matched_skills', []))}):")
for skill in result.get('matched_skills', []):
    print(f"  ✓ {skill}")
print(f"\nMissing Skills ({len(result.get('missing_skills', []))}):")
for skill in result.get('missing_skills', []):
    print(f"  ✗ {skill}")
print(f"\nAdditional Skills in Resume ({len(result.get('additional_skills', []))}):")
for skill in result.get('additional_skills', []):
    print(f"  + {skill}")

print("\n" + "=" * 80)
print("ANALYSIS")
print("=" * 80)
if len(result.get('required_skills', [])) == 0:
    print("⚠️  WARNING: No required skills found in job description!")
    print("    This means the JD doesn't contain any skills from the predefined list.")
elif result.get('skill_match_score') == 100:
    print("✓ Perfect match! All required skills found in resume.")
else:
    print(f"Partial match: {len(result.get('matched_skills', []))} out of {len(result.get('required_skills', []))} required skills matched.")
