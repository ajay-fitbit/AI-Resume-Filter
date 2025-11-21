import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.resume_parser import ResumeParser
import re

parser = ResumeParser()

# Test resumes
test_files = [
    'uploads/Sr_Database_Engineer.pdf',
    'uploads/Emily_Johnson-resume.pdf'
]

for file in test_files:
    if os.path.exists(file):
        print(f"\n{'='*60}")
        print(f"Analyzing: {file}")
        print('='*60)
        
        # Parse resume
        data = parser.parse_resume(file)
        
        if data:
            print(f"\nExtracted by parser: {data.get('skills', 'None')}")
            
            # Get raw text and look for potential skills
            raw_text = data.get('raw_text', '')
            
            # Common programming/tech terms not in current list
            additional_tech = {
                'TypeScript', 'Go', 'Rust', 'Scala', 'R', 'MATLAB', 'Perl',
                'Express', 'FastAPI', 'Laravel', 'Rails', 'ASP.NET', '.NET',
                'GraphQL', 'REST API', 'SOAP', 'gRPC',
                'Linux', 'Unix', 'Windows Server', 'MacOS',
                'Bash', 'PowerShell', 'Shell', 'CMD',
                'CI/CD', 'DevOps', 'Kanban',
                'Tableau', 'Power BI', 'Looker', 'Qlik',
                'Spark', 'Hadoop', 'Kafka', 'RabbitMQ', 'Cassandra', 'DynamoDB',
                'Terraform', 'Ansible', 'Chef', 'Puppet', 'CloudFormation',
                'Nginx', 'Apache', 'Tomcat', 'IIS',
                'Excel', 'Word', 'PowerPoint', 'Outlook',
                'Postman', 'Swagger', 'Insomnia',
                'VS Code', 'Visual Studio', 'IntelliJ', 'Eclipse', 'PyCharm',
                'Figma', 'Sketch', 'Adobe XD',
                'Photoshop', 'Illustrator', 'Premiere',
                'ETL', 'Data Warehouse', 'Data Pipeline', 'Big Data',
                'ElasticSearch', 'Solr', 'Splunk',
                'Grafana', 'Prometheus', 'Datadog', 'New Relic',
                'GitLab', 'GitHub', 'Bitbucket',
                'SAP', 'Salesforce', 'ServiceNow', 'Workday',
                'Snowflake', 'Redshift', 'BigQuery'
            }
            
            found_in_text = []
            for skill in additional_tech:
                if re.search(r'\b' + re.escape(skill) + r'\b', raw_text, re.IGNORECASE):
                    found_in_text.append(skill)
            
            if found_in_text:
                print(f"\nMISSING skills found in resume: {', '.join(found_in_text)}")
            else:
                print("\nNo additional common skills found")
            
    else:
        print(f"\n{file} not found")
