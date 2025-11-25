"""
Skills Assessment Agent

Evaluates candidate skills against job requirements
"""

from typing import Dict, Any, List
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_agent import BaseAgent


class SkillsAssessmentAgent(BaseAgent):
    """Agent responsible for evaluating candidate skills"""
    
    def __init__(self):
        super().__init__(name="SkillsAssessmentAgent")
        self.log("Initialized")
        
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess candidate skills against job requirements
        
        Args:
            input_data: {
                "resume_skills": List[str] - Skills from resume,
                "job_description": str - Job description text
            }
            
        Returns:
            {
                "success": bool,
                "skill_match_score": float (0-100),
                "matched_skills": List[str],
                "missing_skills": List[str],
                "additional_skills": List[str]
            }
        """
        resume_skills = input_data.get("resume_skills", [])
        job_description = input_data.get("job_description", "")
        
        if not job_description:
            self.log("No job description provided", "error")
            return {
                "success": False,
                "error": "Missing job_description",
                "skill_match_score": 0.0
            }
        
        self.log(f"Assessing {len(resume_skills)} skills against job requirements")
        
        # Extract required skills from JD
        required_skills = self._extract_required_skills(job_description)
        self.log(f"Identified {len(required_skills)} required skills from JD: {required_skills}")
        
        # Normalize skills for comparison
        resume_skills_lower = [s.lower().strip() for s in resume_skills]
        required_skills_lower = [s.lower().strip() for s in required_skills]
        
        self.log(f"Resume skills: {resume_skills_lower}")
        
        # Find matches
        matched_skills = []
        for req_skill in required_skills_lower:
            for res_skill in resume_skills_lower:
                if self._skills_match(req_skill, res_skill):
                    matched_skills.append(req_skill)
                    break
        
        # Find missing skills
        missing_skills = [s for s in required_skills_lower if s not in matched_skills]
        
        # Find additional skills (in resume but not required)
        additional_skills = [s for s in resume_skills_lower 
                           if s not in required_skills_lower]
        
        # Calculate score
        if len(required_skills) > 0:
            skill_match_score = (len(matched_skills) / len(required_skills)) * 100
        else:
            # If no skills identified in JD, check if resume has any skills
            if len(resume_skills) > 0:
                self.log(f"WARNING: No required skills found in JD, but resume has {len(resume_skills)} skills", "warning")
                skill_match_score = 50.0  # Neutral score
            else:
                skill_match_score = 50.0  # Both have no skills
        
        self.log(f"Matched: {len(matched_skills)}/{len(required_skills)} required skills - "
                f"Score: {skill_match_score:.1f}% | Matched: {matched_skills} | Missing: {missing_skills}")
        
        return {
            "success": True,
            "skill_match_score": round(skill_match_score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "additional_skills": additional_skills,
            "required_skills": required_skills_lower,
            "total_resume_skills": len(resume_skills)
        }
    
    def _extract_required_skills(self, job_description: str) -> List[str]:
        """Extract skills from job description"""
        # Common skills database (must match resume_parser.py skills)
        common_skills = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust',
            'scala', 'r', 'matlab', 'perl', 'swift', 'kotlin',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server',
            'cassandra', 'dynamodb', 'elasticsearch', 'snowflake', 'redshift', 'bigquery',
            'mariadb', 'db2', 'sqlite', 'couchdb', 'neo4j', 'influxdb', 'timescaledb',
            'hbase', 'amazon rds', 'azure sql', 'cosmos db', 'firebase', 'supabase',
            'planetscale', 'cockroachdb', 'clickhouse', 'vertica', 'greenplum',
            't-sql', 'tsql', 'pl/sql', 'plsql', 'pl-sql', 'mysql workbench', 'pgadmin',
            'sql developer', 'stored procedures', 'triggers', 'views', 'indexes',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins',
            'ci/cd', 'devops', 'cloudformation',
            
            # Web Frameworks
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
            'asp.net', '.net', 'fastapi', 'laravel', 'rails',
            
            # Version Control
            'git', 'github', 'gitlab', 'bitbucket', 'svn',
            
            # Methodologies
            'agile', 'scrum', 'kanban', 'waterfall', 'tdd', 'bdd',
            
            # AI/ML & Data Science
            'ai', 'machine learning', 'deep learning', 'nlp', 'llm', 'rag', 'computer vision',
            'data science', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'keras',
            'openai', 'chatgpt', 'gpt', 'bert', 'transformer', 'hugging face',
            
            # API & Architecture
            'rest api', 'rest', 'api', 'graphql', 'soap', 'grpc', 'microservices',
            
            # Frontend
            'html', 'css', 'sass', 'less', 'bootstrap', 'tailwind', 'jquery',
            
            # Testing
            'selenium', 'jira', 'testng', 'junit', 'pytest', 'cucumber', 'cypress',
            'qa', 'quality assurance', 'testing', 'automated testing', 'unit testing',
            
            # Data & Analytics
            'etl', 'data warehouse', 'data pipeline', 'big data', 'hadoop', 'spark', 'kafka',
            'tableau', 'power bi', 'looker', 'excel', 'qlik', 'qlikview', 'qlik sense',
            'microstrategy', 'sap businessobjects', 'cognos', 'ssrs', 'ssis', 'ssas',
            'dax', 'power query', 'data modeling', 'data visualization', 'alteryx',
            'talend', 'informatica', 'pentaho', 'dbt', 'airflow', 'dagster', 'prefect',
            'azure data factory', 'aws glue', 'fivetran', 'stitch', 'metabase', 'superset',
            'redash', 'google data studio', 'mode analytics', 'sisense', 'domo',
            'dataiku', 'databricks', 'synapse analytics', 'azure synapse',
            
            # Operating Systems
            'linux', 'unix', 'windows', 'windows server', 'macos', 'bash', 'shell', 'powershell',
            
            # Other
            'networking', 'security', 'vs code', 'visual studio', 'postman'
        ]
        
        jd_lower = job_description.lower()
        found_skills = []
        
        for skill in common_skills:
            # Use word boundary to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, jd_lower):
                found_skills.append(skill)
        
        return found_skills
    
    def _skills_match(self, skill1: str, skill2: str) -> bool:
        """Check if two skills are equivalent (fuzzy match)"""
        # Direct match
        if skill1 == skill2:
            return True
        
        # Partial match (one contains the other) - but only for skills longer than 2 chars
        # This prevents single chars like 'a' matching 'postgresql'
        if len(skill1) > 2 and len(skill2) > 2:
            if skill1 in skill2 or skill2 in skill1:
                return True
        
        # Common variations
        variations = {
            'javascript': ['js', 'node.js', 'nodejs'],
            'typescript': ['ts'],
            'python': ['py'],
            'postgresql': ['postgres', 'psql'],
            'mongodb': ['mongo'],
            'kubernetes': ['k8s'],
            'aws': ['amazon web services'],
            'gcp': ['google cloud platform'],
            'azure': ['microsoft azure'],
            'ai': ['artificial intelligence'],
            'llm': ['large language model', 'large language models'],
            'rag': ['retrieval augmented generation', 'retrieval-augmented generation'],
            'nlp': ['natural language processing'],
            'ml': ['machine learning'],
            'power bi': ['powerbi', 'pbi'],
            'sql server': ['mssql', 'microsoft sql server'],
            'ssrs': ['sql server reporting services'],
            'ssis': ['sql server integration services'],
            'ssas': ['sql server analysis services'],
            'etl': ['extract transform load'],
            'bi': ['business intelligence'],
            'data warehouse': ['data warehousing', 'dwh'],
            'cosmos db': ['cosmosdb'],
            'dynamodb': ['dynamo db'],
            'bigquery': ['big query'],
            't-sql': ['tsql', 'transact-sql', 'transact sql'],
            'pl/sql': ['plsql', 'pl-sql'],
            'stored procedures': ['stored procedure', 'sproc', 'sprocs']
        }
        
        for canonical, variants in variations.items():
            if (skill1 == canonical and skill2 in variants) or \
               (skill2 == canonical and skill1 in variants):
                return True
        
        return False
