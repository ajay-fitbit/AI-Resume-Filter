-- =====================================================
-- INSERT SCRIPT FOR HARDCODED SKILLS AND ROLES
-- This script populates the database with all hardcoded
-- skills, variations, and role profiles from the application
-- 
-- SAFE MODE: Uses INSERT IGNORE to skip existing records
-- Will NOT overwrite existing data, only adds new records
-- =====================================================

USE resume_filter_db;

-- =====================================================
-- OPTION 1: CLEAN START (Uncomment to delete all existing data)
-- =====================================================
-- DELETE FROM role_skills;
-- DELETE FROM skill_variations;
-- DELETE FROM skills;
-- DELETE FROM role_profiles;
-- Note: skill_categories should remain as they are pre-populated

-- =====================================================
-- 1. INSERT SKILLS INTO THEIR CATEGORIES
-- =====================================================

-- Programming Languages
INSERT IGNORE INTO skills (skill_name, category_id, is_active) 
SELECT 'Python', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'Java', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'JavaScript', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'TypeScript', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'C++', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'C#', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'Ruby', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'PHP', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'Go', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'Rust', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'Scala', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'R', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'MATLAB', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'Perl', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'Swift', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages'
UNION ALL SELECT 'Kotlin', id, 1 FROM skill_categories WHERE category_name = 'Programming Languages';

-- Databases
INSERT IGNORE INTO skills (skill_name, category_id, is_active) 
SELECT 'SQL', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'MySQL', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'PostgreSQL', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'MongoDB', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Redis', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Oracle', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'SQL Server', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Cassandra', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'DynamoDB', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Elasticsearch', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Snowflake', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Redshift', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'BigQuery', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'MariaDB', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'DB2', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'SQLite', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'CouchDB', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Neo4j', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'InfluxDB', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'TimescaleDB', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'HBase', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Amazon RDS', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Azure SQL', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Cosmos DB', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Firebase', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Supabase', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'PlanetScale', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'CockroachDB', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'ClickHouse', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Vertica', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Greenplum', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'T-SQL', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'PL/SQL', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'MySQL Workbench', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'pgAdmin', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'SQL Developer', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Stored Procedures', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Triggers', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Views', id, 1 FROM skill_categories WHERE category_name = 'Databases'
UNION ALL SELECT 'Indexes', id, 1 FROM skill_categories WHERE category_name = 'Databases';

-- Web Frameworks
INSERT IGNORE INTO skills (skill_name, category_id, is_active) 
SELECT 'React', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Angular', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Vue', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Node.js', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Express', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Django', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Flask', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Spring', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'ASP.NET', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT '.NET', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'FastAPI', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Laravel', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Rails', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'HTML', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'CSS', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'SASS', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'LESS', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Bootstrap', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'Tailwind', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks'
UNION ALL SELECT 'jQuery', id, 1 FROM skill_categories WHERE category_name = 'Web Frameworks';

-- Cloud Platforms
INSERT IGNORE INTO skills (skill_name, category_id, is_active) 
SELECT 'AWS', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'Azure', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'GCP', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'Docker', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'Kubernetes', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'Terraform', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'Ansible', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'Jenkins', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'CI/CD', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'DevOps', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'CloudFormation', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'Lambda', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'EC2', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms'
UNION ALL SELECT 'S3', id, 1 FROM skill_categories WHERE category_name = 'Cloud Platforms';

-- AI/ML
INSERT IGNORE INTO skills (skill_name, category_id, is_active) 
SELECT 'AI', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Machine Learning', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Deep Learning', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'NLP', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'LLM', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'RAG', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Computer Vision', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Data Science', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'TensorFlow', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'PyTorch', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Scikit-learn', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Pandas', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'NumPy', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Keras', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'OpenAI', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'ChatGPT', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'GPT', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'BERT', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Transformer', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Hugging Face', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'ChromaDB', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Pinecone', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Weaviate', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Milvus', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Qdrant', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'FAISS', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Annoy', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Vector Store', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Vector Database', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Embeddings', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Vector Search', id, 1 FROM skill_categories WHERE category_name = 'AI/ML'
UNION ALL SELECT 'Similarity Search', id, 1 FROM skill_categories WHERE category_name = 'AI/ML';

-- Data Analytics & BI
INSERT IGNORE INTO skills (skill_name, category_id, is_active) 
SELECT 'ETL', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Data Warehouse', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Data Pipeline', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Big Data', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Hadoop', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Spark', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Kafka', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Tableau', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Power BI', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Looker', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Excel', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Qlik', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'QlikView', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Qlik Sense', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'MicroStrategy', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'SAP BusinessObjects', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Cognos', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Crystal Reports', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'SSRS', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'SSIS', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'SSAS', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'DAX', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Power Query', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Data Modeling', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Data Visualization', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Alteryx', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Talend', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Informatica', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Pentaho', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'dbt', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Airflow', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Dagster', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Prefect', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Azure Data Factory', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'AWS Glue', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Fivetran', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Stitch', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Metabase', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Superset', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Redash', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Google Data Studio', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Mode Analytics', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Sisense', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Domo', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Dataiku', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Databricks', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Synapse Analytics', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI'
UNION ALL SELECT 'Azure Synapse', id, 1 FROM skill_categories WHERE category_name = 'Data Analytics & BI';

-- Mobile Development
INSERT IGNORE INTO skills (skill_name, category_id, is_active) 
SELECT 'iOS', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Android', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Flutter', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'React Native', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Jetpack Compose', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'SwiftUI', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Xamarin', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Ionic', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Cordova', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Android Studio', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Xcode', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Room', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Realm', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Retrofit', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Alamofire', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Material Design', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'UIKit', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Core Data', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Push Notifications', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'In-App Purchases', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'Google Play', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development'
UNION ALL SELECT 'App Store', id, 1 FROM skill_categories WHERE category_name = 'Mobile Development';

-- Testing & QA
INSERT IGNORE INTO skills (skill_name, category_id, is_active) 
SELECT 'Selenium', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'JIRA', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'TestNG', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'JUnit', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'Pytest', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'Cucumber', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'Cypress', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'QA', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'Quality Assurance', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'Testing', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'Automated Testing', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA'
UNION ALL SELECT 'Unit Testing', id, 1 FROM skill_categories WHERE category_name = 'Testing & QA';

-- Other Tools
INSERT IGNORE INTO skills (skill_name, category_id, is_active) 
SELECT 'Git', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'GitHub', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'GitLab', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Bitbucket', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'SVN', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Agile', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Scrum', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Kanban', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Waterfall', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'TDD', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'BDD', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'REST API', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'REST', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'API', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'GraphQL', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'SOAP', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'gRPC', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Microservices', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Linux', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Unix', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Windows', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Windows Server', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'macOS', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Bash', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Shell', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'PowerShell', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Networking', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Security', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'VS Code', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Visual Studio', id, 1 FROM skill_categories WHERE category_name = 'Other Tools'
UNION ALL SELECT 'Postman', id, 1 FROM skill_categories WHERE category_name = 'Other Tools';

-- =====================================================
-- 2. INSERT SKILL VARIATIONS
-- =====================================================

-- Get skill IDs and insert variations
INSERT IGNORE INTO skill_variations (skill_id, variation_name, is_active)
SELECT s.id, 'js', 1 FROM skills s WHERE s.skill_name = 'JavaScript'
UNION ALL SELECT s.id, 'nodejs', 1 FROM skills s WHERE s.skill_name = 'JavaScript'
UNION ALL SELECT s.id, 'ts', 1 FROM skills s WHERE s.skill_name = 'TypeScript'
UNION ALL SELECT s.id, 'py', 1 FROM skills s WHERE s.skill_name = 'Python'
UNION ALL SELECT s.id, 'postgres', 1 FROM skills s WHERE s.skill_name = 'PostgreSQL'
UNION ALL SELECT s.id, 'psql', 1 FROM skills s WHERE s.skill_name = 'PostgreSQL'
UNION ALL SELECT s.id, 'mongo', 1 FROM skills s WHERE s.skill_name = 'MongoDB'
UNION ALL SELECT s.id, 'k8s', 1 FROM skills s WHERE s.skill_name = 'Kubernetes'
UNION ALL SELECT s.id, 'amazon web services', 1 FROM skills s WHERE s.skill_name = 'AWS'
UNION ALL SELECT s.id, 'google cloud platform', 1 FROM skills s WHERE s.skill_name = 'GCP'
UNION ALL SELECT s.id, 'microsoft azure', 1 FROM skills s WHERE s.skill_name = 'Azure'
UNION ALL SELECT s.id, 'artificial intelligence', 1 FROM skills s WHERE s.skill_name = 'AI'
UNION ALL SELECT s.id, 'large language model', 1 FROM skills s WHERE s.skill_name = 'LLM'
UNION ALL SELECT s.id, 'large language models', 1 FROM skills s WHERE s.skill_name = 'LLM'
UNION ALL SELECT s.id, 'retrieval augmented generation', 1 FROM skills s WHERE s.skill_name = 'RAG'
UNION ALL SELECT s.id, 'retrieval-augmented generation', 1 FROM skills s WHERE s.skill_name = 'RAG'
UNION ALL SELECT s.id, 'natural language processing', 1 FROM skills s WHERE s.skill_name = 'NLP'
UNION ALL SELECT s.id, 'ml', 1 FROM skills s WHERE s.skill_name = 'Machine Learning'
UNION ALL SELECT s.id, 'powerbi', 1 FROM skills s WHERE s.skill_name = 'Power BI'
UNION ALL SELECT s.id, 'pbi', 1 FROM skills s WHERE s.skill_name = 'Power BI'
UNION ALL SELECT s.id, 'power bi desktop', 1 FROM skills s WHERE s.skill_name = 'Power BI'
UNION ALL SELECT s.id, 'mssql', 1 FROM skills s WHERE s.skill_name = 'SQL Server'
UNION ALL SELECT s.id, 'microsoft sql server', 1 FROM skills s WHERE s.skill_name = 'SQL Server'
UNION ALL SELECT s.id, 'sql server reporting services', 1 FROM skills s WHERE s.skill_name = 'SSRS'
UNION ALL SELECT s.id, 'sql server integration services', 1 FROM skills s WHERE s.skill_name = 'SSIS'
UNION ALL SELECT s.id, 'sql server analysis services', 1 FROM skills s WHERE s.skill_name = 'SSAS'
UNION ALL SELECT s.id, 'extract transform load', 1 FROM skills s WHERE s.skill_name = 'ETL'
UNION ALL SELECT s.id, 'business intelligence', 1 FROM skills s WHERE s.skill_name = 'Data Analytics & BI'
UNION ALL SELECT s.id, 'data warehousing', 1 FROM skills s WHERE s.skill_name = 'Data Warehouse'
UNION ALL SELECT s.id, 'dwh', 1 FROM skills s WHERE s.skill_name = 'Data Warehouse'
UNION ALL SELECT s.id, 'cosmosdb', 1 FROM skills s WHERE s.skill_name = 'Cosmos DB'
UNION ALL SELECT s.id, 'dynamo db', 1 FROM skills s WHERE s.skill_name = 'DynamoDB'
UNION ALL SELECT s.id, 'big query', 1 FROM skills s WHERE s.skill_name = 'BigQuery'
UNION ALL SELECT s.id, 'tsql', 1 FROM skills s WHERE s.skill_name = 'T-SQL'
UNION ALL SELECT s.id, 'transact-sql', 1 FROM skills s WHERE s.skill_name = 'T-SQL'
UNION ALL SELECT s.id, 'transact sql', 1 FROM skills s WHERE s.skill_name = 'T-SQL'
UNION ALL SELECT s.id, 'plsql', 1 FROM skills s WHERE s.skill_name = 'PL/SQL'
UNION ALL SELECT s.id, 'pl-sql', 1 FROM skills s WHERE s.skill_name = 'PL/SQL'
UNION ALL SELECT s.id, 'stored procedure', 1 FROM skills s WHERE s.skill_name = 'Stored Procedures'
UNION ALL SELECT s.id, 'sproc', 1 FROM skills s WHERE s.skill_name = 'Stored Procedures'
UNION ALL SELECT s.id, 'sprocs', 1 FROM skills s WHERE s.skill_name = 'Stored Procedures'
UNION ALL SELECT s.id, 'chroma db', 1 FROM skills s WHERE s.skill_name = 'ChromaDB'
UNION ALL SELECT s.id, 'chroma', 1 FROM skills s WHERE s.skill_name = 'ChromaDB'
UNION ALL SELECT s.id, 'vector db', 1 FROM skills s WHERE s.skill_name = 'Vector Store'
UNION ALL SELECT s.id, 'vector storage', 1 FROM skills s WHERE s.skill_name = 'Vector Store'
UNION ALL SELECT s.id, 'vectorstore', 1 FROM skills s WHERE s.skill_name = 'Vector Store'
UNION ALL SELECT s.id, 'vector db', 1 FROM skills s WHERE s.skill_name = 'Vector Database'
UNION ALL SELECT s.id, 'vectordb', 1 FROM skills s WHERE s.skill_name = 'Vector Database'
UNION ALL SELECT s.id, 'vector databases', 1 FROM skills s WHERE s.skill_name = 'Vector Database'
UNION ALL SELECT s.id, 'embedding', 1 FROM skills s WHERE s.skill_name = 'Embeddings'
UNION ALL SELECT s.id, 'text embeddings', 1 FROM skills s WHERE s.skill_name = 'Embeddings'
UNION ALL SELECT s.id, 'word embeddings', 1 FROM skills s WHERE s.skill_name = 'Embeddings'
UNION ALL SELECT s.id, 'sentence embeddings', 1 FROM skills s WHERE s.skill_name = 'Embeddings'
UNION ALL SELECT s.id, 'vector similarity', 1 FROM skills s WHERE s.skill_name = 'Vector Search'
UNION ALL SELECT s.id, 'semantic search', 1 FROM skills s WHERE s.skill_name = 'Vector Search'
UNION ALL SELECT s.id, 'crystal report', 1 FROM skills s WHERE s.skill_name = 'Crystal Reports'
UNION ALL SELECT s.id, 'sap crystal reports', 1 FROM skills s WHERE s.skill_name = 'Crystal Reports'
UNION ALL SELECT s.id, 'crystal', 1 FROM skills s WHERE s.skill_name = 'Crystal Reports'
UNION ALL SELECT s.id, 'data pipelines', 1 FROM skills s WHERE s.skill_name = 'Data Pipeline'
UNION ALL SELECT s.id, 'etl pipeline', 1 FROM skills s WHERE s.skill_name = 'Data Pipeline'
UNION ALL SELECT s.id, 'data integration', 1 FROM skills s WHERE s.skill_name = 'Data Pipeline'
UNION ALL SELECT s.id, 'databricks spark', 1 FROM skills s WHERE s.skill_name = 'Databricks'
UNION ALL SELECT s.id, 'databricks notebook', 1 FROM skills s WHERE s.skill_name = 'Databricks'
UNION ALL SELECT s.id, 'azure synapse', 1 FROM skills s WHERE s.skill_name = 'Synapse Analytics'
UNION ALL SELECT s.id, 'synapse', 1 FROM skills s WHERE s.skill_name = 'Synapse Analytics'
UNION ALL SELECT s.id, 'azure synapse analytics', 1 FROM skills s WHERE s.skill_name = 'Synapse Analytics'
UNION ALL SELECT s.id, 'jetpack', 1 FROM skills s WHERE s.skill_name = 'Jetpack Compose'
UNION ALL SELECT s.id, 'compose', 1 FROM skills s WHERE s.skill_name = 'Jetpack Compose'
UNION ALL SELECT s.id, 'swift ui', 1 FROM skills s WHERE s.skill_name = 'SwiftUI'
UNION ALL SELECT s.id, 'android ide', 1 FROM skills s WHERE s.skill_name = 'Android Studio'
UNION ALL SELECT s.id, 'reactnative', 1 FROM skills s WHERE s.skill_name = 'React Native'
UNION ALL SELECT s.id, 'rn', 1 FROM skills s WHERE s.skill_name = 'React Native';

-- =====================================================
-- 3. INSERT ROLE PROFILES
-- =====================================================

INSERT IGNORE INTO role_profiles (role_name, description, is_active) VALUES
('Full Stack Developer', 'Develops both frontend and backend applications with modern frameworks', 1),
('Frontend Developer', 'Specializes in building user interfaces and client-side applications', 1),
('Backend Developer', 'Focuses on server-side logic, APIs, and database management', 1),
('DevOps Engineer', 'Manages infrastructure, CI/CD pipelines, and cloud deployments', 1),
('Data Scientist', 'Analyzes data and builds machine learning models', 1),
('Cloud Engineer', 'Designs and manages cloud infrastructure and services', 1),
('Mobile Developer', 'Develops native and cross-platform mobile applications', 1),
('QA Engineer', 'Ensures software quality through testing and automation', 1),
('Database Administrator', 'Manages, optimizes, and secures database systems', 1),
('AI/ML Engineer', 'Builds AI models, LLMs, and vector search systems', 1),
('BI Developer', 'Creates data visualizations, reports, and business intelligence solutions', 1),
('Data Engineer', 'Builds data pipelines, warehouses, and ETL processes', 1);

-- =====================================================
-- 4. MAP SKILLS TO ROLES
-- =====================================================

-- Full Stack Developer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'Full Stack Developer' 
AND s.skill_name IN ('React', 'Angular', 'Vue', 'Node.js', 'JavaScript', 'TypeScript', 'Python', 'Java', 'Django', 'Flask', 'Express', 'MongoDB', 'PostgreSQL', 'MySQL');

-- Frontend Developer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'Frontend Developer' 
AND s.skill_name IN ('React', 'Angular', 'Vue', 'JavaScript', 'TypeScript', 'HTML', 'CSS', 'Bootstrap', 'Tailwind', 'jQuery');

-- Backend Developer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'Backend Developer' 
AND s.skill_name IN ('Python', 'Java', 'Node.js', 'C#', '.NET', 'PHP', 'Ruby', 'Go', 'Django', 'Flask', 'Spring', 'Express', 'API', 'REST');

-- DevOps Engineer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'DevOps Engineer' 
AND s.skill_name IN ('Docker', 'Kubernetes', 'Jenkins', 'CI/CD', 'AWS', 'Azure', 'GCP', 'Terraform', 'Ansible', 'Linux', 'Git');

-- Data Scientist
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'Data Scientist' 
AND s.skill_name IN ('Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Pandas', 'NumPy', 'Data Science', 'R', 'Scikit-learn');

-- Cloud Engineer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'Cloud Engineer' 
AND s.skill_name IN ('AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'CloudFormation', 'Lambda', 'EC2', 'S3');

-- Mobile Developer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'Mobile Developer' 
AND s.skill_name IN ('Swift', 'Kotlin', 'React Native', 'iOS', 'Android', 'Flutter', 'Jetpack Compose', 'SwiftUI', 'Xamarin', 'Ionic', 'Cordova', 'Android Studio', 'Xcode', 'Firebase', 'Room', 'Realm', 'Retrofit', 'Alamofire', 'Material Design', 'UIKit', 'Core Data', 'Push Notifications', 'In-App Purchases', 'Google Play', 'App Store');

-- QA Engineer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'QA Engineer' 
AND s.skill_name IN ('Selenium', 'Testing', 'QA', 'Automated Testing', 'Pytest', 'JUnit', 'TestNG', 'Cypress', 'JIRA');

-- Database Administrator
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'Database Administrator' 
AND s.skill_name IN ('SQL', 'MySQL', 'PostgreSQL', 'Oracle', 'MongoDB', 'Redis', 'DynamoDB', 'SQL Server');

-- AI/ML Engineer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'AI/ML Engineer' 
AND s.skill_name IN ('Machine Learning', 'Deep Learning', 'AI', 'TensorFlow', 'PyTorch', 'NLP', 'LLM', 'GPT', 'BERT', 'Transformer', 'ChromaDB', 'Pinecone', 'Vector Store', 'Embeddings', 'RAG');

-- BI Developer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'BI Developer' 
AND s.skill_name IN ('Power BI', 'Tableau', 'Looker', 'Qlik', 'SQL', 'DAX', 'Power Query', 'Data Modeling', 'ETL', 'SSRS', 'SSIS', 'SSAS', 'Crystal Reports', 'Cognos', 'MicroStrategy', 'Data Visualization');

-- Data Engineer
INSERT IGNORE INTO role_skills (role_id, skill_id)
SELECT rp.id, s.id FROM role_profiles rp, skills s 
WHERE rp.role_name = 'Data Engineer' 
AND s.skill_name IN ('Python', 'SQL', 'Spark', 'Kafka', 'Airflow', 'ETL', 'Data Pipeline', 'Big Data', 'Hadoop', 'AWS Glue', 'Azure Data Factory', 'Databricks', 'Snowflake', 'dbt');

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Count inserted records
SELECT 'Skills Inserted' as Item, COUNT(*) as Count FROM skills
UNION ALL
SELECT 'Variations Inserted', COUNT(*) FROM skill_variations
UNION ALL
SELECT 'Roles Inserted', COUNT(*) FROM role_profiles
UNION ALL
SELECT 'Role-Skill Mappings', COUNT(*) FROM role_skills;

-- Show sample data
SELECT 
    sc.category_name,
    COUNT(s.id) as skill_count
FROM skill_categories sc
LEFT JOIN skills s ON sc.id = s.category_id
GROUP BY sc.category_name
ORDER BY sc.display_order;
