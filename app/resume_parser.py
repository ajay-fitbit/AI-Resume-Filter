import re
import PyPDF2
import docx
from datetime import datetime

class ResumeParser:
    def __init__(self):
        self.email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
        # Enhanced phone pattern for various formats including +1 (555) 123-4567, +91 9000239990, etc.
        self.phone_pattern = r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
    def parse_resume(self, file_path):
        """Main function to parse resume from PDF or DOCX"""
        if file_path.endswith('.pdf'):
            text = self._extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = self._extract_text_from_docx(file_path)
        else:
            return None
        
        return self._extract_information(text)
    
    def _extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def _extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""
    
    def _extract_information(self, text):
        """Extract structured information from resume text"""
        data = {
            'raw_text': text,
            'name': self._extract_name(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'skills': self._extract_skills(text),
            'experience_years': self._calculate_experience(text),
            'education': self._extract_education(text),
            'certifications': self._extract_certifications(text),
            'job_titles': self._extract_job_titles(text),
            'projects': self._extract_projects(text)
        }
        return data
    
    def _extract_name(self, text):
        """Extract name from resume (usually first line)"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Look for name in first few lines
            for line in lines[:5]:
                # Skip lines with email, phone, or URLs
                if '@' in line or 'http' in line.lower() or 'linkedin' in line.lower():
                    continue
                # Name should be 2-4 words and under 50 chars
                words = line.split()
                if 2 <= len(words) <= 4 and len(line) < 50:
                    # Check if it's not a title/header
                    if not any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum', 'vitae', 'profile', 'summary']):
                        print(f"[DEBUG] Extracted name: {line}")
                        return line
        print("[DEBUG] Could not extract name, using 'Unknown'")
        return "Unknown"
    
    def _extract_email(self, text):
        """Extract email address"""
        # Search for email with word boundary or after common separators
        # This ensures we don't get "ONmichael@..." but get "michael@..."
        email_match = re.search(r'(?:^|[\s,|]|[0-9])([a-z][a-z0-9._%+-]*@[a-z0-9.-]+\.[a-z]{2,})', text, re.IGNORECASE | re.MULTILINE)
        
        if email_match:
            email = email_match.group(1)
            print(f"[DEBUG] Found email: {email}")
            return email
        
        # Fallback: just find any email pattern
        fallback = re.search(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}', text, re.IGNORECASE)
        if fallback:
            email = fallback.group(0)
            print(f"[DEBUG] Found email (fallback): {email}")
            return email
            
        print("[DEBUG] No email found")
        return None
    
    def _extract_phone(self, text):
        """Extract phone number"""
        phones = re.findall(self.phone_pattern, text)
        if phones:
            # Return the first phone number found
            phone = phones[0] if isinstance(phones[0], str) else str(phones[0])
            print(f"[DEBUG] Found phone: {phone}")
            return phone
        print("[DEBUG] No phone found")
        return None
    
    def _extract_skills(self, text):
        """Extract skills from resume - returns comma-separated string for database compatibility"""
        # Common technical skills (comprehensive list)
        skills_keywords = [
            # Programming Languages
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C\\+\\+', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin',
            'Go', 'Rust', 'Scala', 'R', 'MATLAB', 'Perl', 'Objective-C',
            
            # Web Frameworks & Libraries
            'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'Spring', 
            'ASP.NET', '.NET', 'FastAPI', 'Laravel', 'Rails',
            
            # Databases
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQL Server',
            'Cassandra', 'DynamoDB', 'ElasticSearch', 'Snowflake', 'Redshift', 'BigQuery',
            'MariaDB', 'DB2', 'SQLite', 'CouchDB', 'Neo4j', 'InfluxDB', 'TimescaleDB',
            'HBase', 'Amazon RDS', 'Azure SQL', 'Cosmos DB', 'Firebase', 'Supabase',
            'PlanetScale', 'CockroachDB', 'ClickHouse', 'Vertica', 'Greenplum',
            'T-SQL', 'TSQL', 'PL/SQL', 'PLSQL', 'PL-SQL', 'MySQL Workbench', 'pgAdmin',
            'SQL Developer', 'Stored Procedures', 'Triggers', 'Views', 'Indexes',
            
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'CI/CD', 'DevOps',
            'Terraform', 'Ansible', 'Chef', 'Puppet', 'CloudFormation',
            
            # Version Control & Collaboration
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN',
            
            # Methodologies & Practices
            'Agile', 'Scrum', 'Kanban', 'Waterfall', 'TDD', 'BDD',
            
            # API & Protocols
            'REST', 'REST API', 'API', 'GraphQL', 'SOAP', 'gRPC', 'Microservices',
            
            # AI/ML & Data Science
            'Machine Learning', 'Deep Learning', 'AI', 'Data Science', 'NLP', 'LLM', 'RAG',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Keras',
            'OpenAI', 'ChatGPT', 'GPT', 'BERT', 'Transformer', 'Hugging Face',
            
            # Frontend Technologies
            'HTML', 'CSS', 'JavaScript', 'Bootstrap', 'Tailwind', 'SASS', 'LESS', 'jQuery',
            
            # Testing & QA
            'Selenium', 'JIRA', 'TestNG', 'JUnit', 'Pytest', 'Cucumber', 'Cypress',
            'QA', 'Quality Assurance', 'Testing', 'Automated Testing',
            'Manual Testing', 'Performance Testing', 'Load Testing',
            'Regression Testing', 'Integration Testing', 'Unit Testing',
            
            # Operating Systems & Shells
            'Linux', 'Unix', 'Windows', 'Windows Server', 'MacOS',
            'Bash', 'Shell', 'PowerShell', 'CMD',
            
            # Data & Analytics
            'ETL', 'Data Warehouse', 'Data Pipeline', 'Big Data', 'Hadoop', 'Spark', 'Kafka',
            'Tableau', 'Power BI', 'Looker', 'Qlik', 'QlikView', 'Qlik Sense', 'Excel',
            'MicroStrategy', 'SAP BusinessObjects', 'Cognos', 'SSRS', 'SSIS', 'SSAS',
            'DAX', 'Power Query', 'Data Modeling', 'Data Visualization', 'Alteryx',
            'Talend', 'Informatica', 'Pentaho', 'dbt', 'Airflow', 'Dagster', 'Prefect',
            'Azure Data Factory', 'AWS Glue', 'Fivetran', 'Stitch', 'Metabase', 'Superset',
            'Redash', 'Google Data Studio', 'Mode Analytics', 'Sisense', 'Domo',
            'Dataiku', 'Databricks', 'Synapse Analytics', 'Azure Synapse',
            
            # Web Servers & Tools
            'Nginx', 'Apache', 'Tomcat', 'IIS',
            
            # Monitoring & Logging
            'Grafana', 'Prometheus', 'Datadog', 'New Relic', 'Splunk',
            
            # IDEs & Development Tools
            'VS Code', 'Visual Studio', 'IntelliJ', 'Eclipse', 'PyCharm', 'Postman', 'Swagger',
            
            # Design Tools
            'Figma', 'Sketch', 'Adobe XD', 'Photoshop', 'Illustrator',
            
            # Message Queues
            'RabbitMQ', 'ActiveMQ', 'SQS',
            
            # Enterprise Software
            'SAP', 'Salesforce', 'ServiceNow', 'Workday'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skills_keywords:
            if re.search(r'\b' + skill.lower().replace('\\', '') + r'\b', text_lower):
                found_skills.append(skill.replace('\\', ''))
        
        # Return comma-separated string for database storage
        return ', '.join(found_skills) if found_skills else 'Not specified'
    
    def _calculate_experience(self, text):
        """Calculate total years of experience"""
        # First, look for explicitly stated experience like "20 years of experience"
        # More flexible patterns to catch variations like "20 years of IT experience"
        exp_patterns = [
            r'(\d+)\+?\s*years?\s+of\s+\w+\s+experience',  # "20 years of IT experience"
            r'(\d+)\+?\s*years?\s+of\s+experience',         # "20 years of experience"
            r'(\d+)\+?\s*years?\s+experience',              # "20 years experience"
            r'experience\s+(?:of\s+)?(\d+)\+?\s*years?',    # "experience of 20 years"
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience',      # "20 yrs experience"
            r'over\s+(\d+)\s+years?',                       # "over 20 years"
            r'more\s+than\s+(\d+)\s+years?',                # "more than 20 years"
            r'(\d+)\+\s+years?\s+(?:of\s+)?experience'      # "20+ years experience"
        ]
        
        years = []
        for pattern in exp_patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(y) for y in matches])
        
        # If explicitly mentioned, use that
        if years:
            max_exp = max(years)
            print(f"[DEBUG] Found explicit experience mention: {max_exp} years")
            return max_exp
        
        # Otherwise, calculate from employment date ranges
        year_ranges = re.findall(r'(20\d{2}|19\d{2})\s*[-–—]\s*(20\d{2}|present|current)', text.lower())
        if year_ranges:
            print(f"[DEBUG] Found {len(year_ranges)} date ranges: {year_ranges}")
            # Convert to list of (start_year, end_year)
            employment_periods = []
            for start, end in year_ranges:
                start_year = int(start)
                end_year = datetime.now().year if end.lower() in ['present', 'current'] else int(end)
                if end_year >= start_year:  # Valid range
                    employment_periods.append((start_year, end_year))
                    print(f"[DEBUG] Added period: {start_year} to {end_year} = {end_year - start_year} years")
            
            if employment_periods:
                # Calculate total experience from earliest start to latest end
                earliest_start = min(period[0] for period in employment_periods)
                latest_end = max(period[1] for period in employment_periods)
                total_exp = latest_end - earliest_start
                print(f"[DEBUG] Total career span: {earliest_start} to {latest_end} = {total_exp} years")
                return total_exp
        
        print(f"[DEBUG] No experience found")
        return 0
    
    def _extract_education(self, text):
        """Extract education information"""
        education_keywords = [
            'B.Tech', 'B.E.', 'Bachelor', 'Master', 'M.Tech', 'M.E.', 'MBA',
            'PhD', 'Doctorate', 'Diploma', 'B.Sc', 'M.Sc', 'BCA', 'MCA'
        ]
        
        education = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            for keyword in education_keywords:
                if keyword.lower() in line.lower():
                    education.append(line.strip())
                    break
        
        return ' | '.join(education[:3]) if education else 'Not specified'
    
    def _extract_certifications(self, text):
        """Extract certifications"""
        cert_keywords = [
            'certified', 'certification', 'certificate', 'AWS Certified',
            'Azure Certified', 'Google Certified', 'PMP', 'CCNA', 'CISSP'
        ]
        
        certifications = []
        lines = text.split('\n')
        
        for line in lines:
            for keyword in cert_keywords:
                if keyword.lower() in line.lower():
                    certifications.append(line.strip())
                    break
        
        return ' | '.join(certifications[:5]) if certifications else 'None'
    
    def _extract_job_titles(self, text):
        """Extract job titles"""
        title_keywords = [
            'Software Engineer', 'Developer', 'Analyst', 'Manager', 'Lead',
            'Senior', 'Junior', 'Architect', 'Consultant', 'Specialist',
            'Data Scientist', 'DevOps', 'Full Stack', 'Frontend', 'Backend'
        ]
        
        job_titles = []
        lines = text.split('\n')
        
        for line in lines:
            for keyword in title_keywords:
                if keyword.lower() in line.lower():
                    job_titles.append(line.strip())
                    break
        
        return ' | '.join(list(set(job_titles))[:5]) if job_titles else 'Not specified'
    
    def _extract_projects(self, text):
        """Extract project information"""
        projects = []
        
        # Look for sections with "project" keyword
        project_section = False
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if 'project' in line.lower() and len(line) < 30:
                project_section = True
                continue
            
            if project_section:
                if line.strip() and not any(keyword in line.lower() for keyword in ['education', 'experience', 'skill']):
                    projects.append(line.strip())
                    if len(projects) >= 3:
                        break
                elif any(keyword in line.lower() for keyword in ['education', 'experience', 'skill']):
                    break
        
        return ' | '.join(projects) if projects else 'Not specified'
