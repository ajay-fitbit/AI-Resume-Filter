import re
from datetime import datetime

class RedFlagDetector:
    def __init__(self):
        self.flags = []
    
    def detect_all_flags(self, resume_data, job_description):
        """Detect all red flags in the resume"""
        self.flags = []
        
        self._check_job_hopping(resume_data['raw_text'])
        self._check_career_gaps(resume_data['raw_text'])
        self._check_missing_skills(resume_data['skills'], job_description)
        self._check_irrelevant_experience(resume_data['job_titles'], job_description)
        self._check_minimal_experience(resume_data['experience_years'], job_description)
        
        return self.flags
    
    def _check_job_hopping(self, resume_text):
        """Detect frequent job changes"""
        # Find all year ranges
        year_patterns = re.findall(r'(20\d{2})\s*[-–—]\s*(20\d{2}|present|current)', resume_text.lower())
        
        if len(year_patterns) >= 4:
            # Calculate average tenure
            tenures = []
            for start, end in year_patterns:
                end_year = datetime.now().year if end.lower() in ['present', 'current'] else int(end)
                tenure = end_year - int(start)
                tenures.append(tenure)
            
            if tenures:
                avg_tenure = sum(tenures) / len(tenures)
                if avg_tenure < 1.5:
                    self.flags.append({
                        'type': 'Job Hopping',
                        'severity': 'High',
                        'description': f'Frequent job changes detected. Average tenure: {avg_tenure:.1f} years across {len(tenures)} positions.'
                    })
                elif avg_tenure < 2.5:
                    self.flags.append({
                        'type': 'Job Hopping',
                        'severity': 'Medium',
                        'description': f'Short job tenure detected. Average: {avg_tenure:.1f} years.'
                    })
    
    def _check_career_gaps(self, resume_text):
        """Detect unexplained gaps in employment"""
        # Split resume into sections
        lines = resume_text.split('\n')
        
        # Find employment date ranges, excluding education section
        employment_periods = []
        in_education_section = False
        in_experience_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Detect section headers
            if any(keyword in line_lower for keyword in ['education', 'academic', 'qualification']):
                in_education_section = True
                in_experience_section = False
            elif any(keyword in line_lower for keyword in ['experience', 'employment', 'work history', 'career']):
                in_experience_section = True
                in_education_section = False
            elif line_lower and any(keyword in line_lower for keyword in ['skills', 'certifications', 'projects']):
                in_education_section = False
                in_experience_section = False
            
            # Only extract dates from experience section or if no clear sections
            if not in_education_section:
                year_matches = re.findall(r'(20\d{2}|19\d{2})\s*[-–—]\s*(20\d{2}|present|current)', line.lower())
                for start, end in year_matches:
                    start_year = int(start)
                    end_year = datetime.now().year if end.lower() in ['present', 'current'] else int(end)
                    if end_year >= start_year and start_year >= 1990:  # Valid employment date range
                        employment_periods.append((start_year, end_year))
        
        if len(employment_periods) < 2:
            return  # Need at least 2 jobs to check for gaps
        
        if len(employment_periods) < 2:
            return
        
        # Sort by start year
        employment_periods.sort()
        
        # Check for gaps between consecutive employment periods
        gaps = []
        for i in range(len(employment_periods) - 1):
            current_end = employment_periods[i][1]
            next_start = employment_periods[i + 1][0]
            gap = next_start - current_end
            
            # A gap of 1 year or less is acceptable (could be months, job searching, etc.)
            if gap > 1:
                gaps.append((current_end, next_start, gap))
        
        for end_year, start_year, gap_size in gaps:
            if gap_size >= 2:
                self.flags.append({
                    'type': 'Career Gap',
                    'severity': 'High' if gap_size >= 3 else 'Medium',
                    'description': f'Employment gap detected: {gap_size} year(s) between {end_year} and {start_year}.'
                })
    
    def _check_missing_skills(self, resume_skills, job_description):
        """Check for missing required skills"""
        if not resume_skills or resume_skills == 'Not specified':
            self.flags.append({
                'type': 'Missing Skills',
                'severity': 'High',
                'description': 'No technical skills mentioned in resume.'
            })
            return
        
        # Extract critical skills from JD
        critical_keywords = ['required', 'must have', 'essential', 'mandatory']
        jd_lower = job_description.lower()
        
        resume_skills_list = [s.strip().lower() for s in resume_skills.split(',')]
        
        # Look for required skills in JD
        missing_critical = []
        lines = jd_lower.split('.')
        
        for line in lines:
            if any(keyword in line for keyword in critical_keywords):
                # Extract potential skill words
                words = re.findall(r'\b[a-z]{3,}\b', line)
                for word in words:
                    if word not in resume_skills_list and len(word) > 4:
                        missing_critical.append(word)
        
        if missing_critical:
            self.flags.append({
                'type': 'Missing Required Skills',
                'severity': 'High',
                'description': f'Missing critical skills mentioned in job description.'
            })
    
    def _check_irrelevant_experience(self, job_titles, job_description):
        """Check if experience is relevant to the job"""
        if not job_titles or job_titles == 'Not specified':
            self.flags.append({
                'type': 'No Job Titles',
                'severity': 'Medium',
                'description': 'No clear job titles or roles mentioned.'
            })
            return
        
        # Extract job role keywords from JD
        role_keywords = ['engineer', 'developer', 'analyst', 'manager', 'designer', 
                         'architect', 'consultant', 'scientist', 'specialist', 'lead']
        
        jd_lower = job_description.lower()
        titles_lower = job_titles.lower()
        
        # Check if any role keyword matches
        has_relevant_role = any(keyword in titles_lower for keyword in role_keywords if keyword in jd_lower)
        
        if not has_relevant_role:
            self.flags.append({
                'type': 'Irrelevant Experience',
                'severity': 'High',
                'description': 'Work experience does not align with job requirements.'
            })
    
    def _check_minimal_experience(self, experience_years, job_description):
        """Check if candidate has minimal or no experience"""
        # Extract required experience from JD
        required_exp = self._extract_required_experience(job_description)
        
        if experience_years == 0:
            self.flags.append({
                'type': 'No Experience',
                'severity': 'High',
                'description': 'No work experience mentioned in resume.'
            })
        elif required_exp > 0 and experience_years < required_exp * 0.5:
            self.flags.append({
                'type': 'Insufficient Experience',
                'severity': 'High',
                'description': f'Has {experience_years} years but requires {required_exp}+ years.'
            })
    
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
    
    def get_flags_summary(self):
        """Get a summary of all detected flags"""
        if not self.flags:
            return "No red flags detected."
        
        high_severity = [f for f in self.flags if f['severity'] == 'High']
        medium_severity = [f for f in self.flags if f['severity'] == 'Medium']
        
        summary = []
        if high_severity:
            summary.append(f"{len(high_severity)} High severity issues")
        if medium_severity:
            summary.append(f"{len(medium_severity)} Medium severity issues")
        
        return " | ".join(summary)
