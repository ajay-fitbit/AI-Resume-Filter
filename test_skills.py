import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.resume_parser import ResumeParser

parser = ResumeParser()

# Test resumes
test_files = [
    'uploads/Sr_Database_Engineer.pdf',
    'uploads/Emily_Johnson-resume.pdf'
]

for file in test_files:
    if os.path.exists(file):
        print(f"\n{'='*60}")
        print(f"Resume: {os.path.basename(file)}")
        print('='*60)
        
        data = parser.parse_resume(file)
        
        if data:
            skills = data.get('skills', 'None')
            skill_list = [s.strip() for s in skills.split(',') if s.strip()]
            
            print(f"\nTotal skills detected: {len(skill_list)}")
            print(f"\nSkills found:")
            for i, skill in enumerate(skill_list, 1):
                print(f"  {i}. {skill}")
