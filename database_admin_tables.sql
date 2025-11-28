-- Admin Configuration Tables for Skills and Role Profiles
-- Add these tables to your existing database

USE resume_filter_db;

-- Skill Categories Table
CREATE TABLE IF NOT EXISTS skill_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    display_order INT DEFAULT 0,
    icon VARCHAR(10),
    color VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_active (is_active),
    INDEX idx_display_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Skills Master Table
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(255) NOT NULL UNIQUE,
    category_id INT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category_id (category_id),
    INDEX idx_active (is_active),
    CONSTRAINT fk_skill_category 
        FOREIGN KEY (category_id) 
        REFERENCES skill_categories(id) 
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Skill Variations Table
CREATE TABLE IF NOT EXISTS skill_variations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    skill_id INT NOT NULL,
    variation_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_skill_id (skill_id),
    INDEX idx_active (is_active),
    UNIQUE KEY unique_variation (skill_id, variation_name),
    CONSTRAINT fk_variation_skill 
        FOREIGN KEY (skill_id) 
        REFERENCES skills(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Role Profiles Table
CREATE TABLE IF NOT EXISTS role_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Role Skills Mapping Table (Many-to-Many relationship)
CREATE TABLE IF NOT EXISTS role_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    skill_id INT NOT NULL,
    weight INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_role_id (role_id),
    INDEX idx_skill_id (skill_id),
    UNIQUE KEY unique_role_skill (role_id, skill_id),
    CONSTRAINT fk_roleskill_role 
        FOREIGN KEY (role_id) 
        REFERENCES role_profiles(id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_roleskill_skill 
        FOREIGN KEY (skill_id) 
        REFERENCES skills(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert skill categories
INSERT INTO skill_categories (category_name, description, display_order, icon, color) VALUES
('Programming Languages', 'General purpose and scripting languages', 1, '💻', '#667eea'),
('Databases', 'Relational and NoSQL databases', 2, '🗄️', '#10b981'),
('Vector Databases', 'Vector storage and similarity search databases', 3, '🔍', '#8b5cf6'),
('Web Frameworks', 'Frontend and backend web frameworks', 4, '🌐', '#3b82f6'),
('Cloud Platforms', 'Cloud services and DevOps tools', 5, '☁️', '#06b6d4'),
('AI/ML', 'Artificial intelligence and machine learning', 6, '🤖', '#ec4899'),
('Data & Analytics', 'BI tools, data processing, and analytics', 7, '📊', '#f59e0b'),
('Mobile Development', 'Mobile app development tools and frameworks', 8, '📱', '#14b8a6'),
('Testing', 'Testing frameworks and QA tools', 9, '🧪', '#84cc16'),
('Other', 'Miscellaneous technical skills', 10, '🔧', '#6b7280')
ON DUPLICATE KEY UPDATE category_name=VALUES(category_name);

-- Insert skills using category_id
INSERT INTO skills (skill_name, category_id)
SELECT skill, cat.id FROM (
    -- Programming Languages
    SELECT 'Python' as skill, 'Programming Languages' as category UNION ALL
    SELECT 'Java', 'Programming Languages' UNION ALL
    SELECT 'JavaScript', 'Programming Languages' UNION ALL
    SELECT 'TypeScript', 'Programming Languages' UNION ALL
    SELECT 'C#', 'Programming Languages' UNION ALL
    SELECT 'C++', 'Programming Languages' UNION ALL
    SELECT 'Go', 'Programming Languages' UNION ALL
    SELECT 'Ruby', 'Programming Languages' UNION ALL
    SELECT 'PHP', 'Programming Languages' UNION ALL
    SELECT 'Swift', 'Programming Languages' UNION ALL
    SELECT 'Kotlin', 'Programming Languages' UNION ALL
    SELECT 'R', 'Programming Languages' UNION ALL
    SELECT 'Scala', 'Programming Languages' UNION ALL
    SELECT 'Rust', 'Programming Languages' UNION ALL
    
    -- Databases
    SELECT 'SQL', 'Databases' UNION ALL
    SELECT 'MySQL', 'Databases' UNION ALL
    SELECT 'PostgreSQL', 'Databases' UNION ALL
    SELECT 'MongoDB', 'Databases' UNION ALL
    SELECT 'Redis', 'Databases' UNION ALL
    SELECT 'Oracle', 'Databases' UNION ALL
    SELECT 'SQL Server', 'Databases' UNION ALL
    SELECT 'DynamoDB', 'Databases' UNION ALL
    SELECT 'Cassandra', 'Databases' UNION ALL
    SELECT 'Elasticsearch', 'Databases' UNION ALL
    SELECT 'Neo4j', 'Databases' UNION ALL
    SELECT 'Cosmos DB', 'Databases' UNION ALL
    SELECT 'BigQuery', 'Databases' UNION ALL
    SELECT 'Snowflake', 'Databases' UNION ALL
    
    -- Vector Databases
    SELECT 'ChromaDB', 'Vector Databases' UNION ALL
    SELECT 'Pinecone', 'Vector Databases' UNION ALL
    SELECT 'Weaviate', 'Vector Databases' UNION ALL
    SELECT 'Milvus', 'Vector Databases' UNION ALL
    SELECT 'Qdrant', 'Vector Databases' UNION ALL
    SELECT 'FAISS', 'Vector Databases' UNION ALL
    SELECT 'Vector Store', 'Vector Databases' UNION ALL
    SELECT 'Vector Database', 'Vector Databases' UNION ALL
    SELECT 'Embeddings', 'Vector Databases' UNION ALL
    SELECT 'Vector Search', 'Vector Databases' UNION ALL
    
    -- Web Frameworks
    SELECT 'React', 'Web Frameworks' UNION ALL
    SELECT 'Angular', 'Web Frameworks' UNION ALL
    SELECT 'Vue', 'Web Frameworks' UNION ALL
    SELECT 'Django', 'Web Frameworks' UNION ALL
    SELECT 'Flask', 'Web Frameworks' UNION ALL
    SELECT 'Spring', 'Web Frameworks' UNION ALL
    SELECT 'Express', 'Web Frameworks' UNION ALL
    SELECT '.NET', 'Web Frameworks' UNION ALL
    SELECT 'FastAPI', 'Web Frameworks' UNION ALL
    SELECT 'Node.js', 'Web Frameworks' UNION ALL
    
    -- Cloud Platforms
    SELECT 'AWS', 'Cloud Platforms' UNION ALL
    SELECT 'Azure', 'Cloud Platforms' UNION ALL
    SELECT 'GCP', 'Cloud Platforms' UNION ALL
    SELECT 'Docker', 'Cloud Platforms' UNION ALL
    SELECT 'Kubernetes', 'Cloud Platforms' UNION ALL
    SELECT 'Terraform', 'Cloud Platforms' UNION ALL
    SELECT 'Jenkins', 'Cloud Platforms' UNION ALL
    SELECT 'CI/CD', 'Cloud Platforms' UNION ALL
    
    -- AI/ML
    SELECT 'Machine Learning', 'AI/ML' UNION ALL
    SELECT 'Deep Learning', 'AI/ML' UNION ALL
    SELECT 'TensorFlow', 'AI/ML' UNION ALL
    SELECT 'PyTorch', 'AI/ML' UNION ALL
    SELECT 'NLP', 'AI/ML' UNION ALL
    SELECT 'LLM', 'AI/ML' UNION ALL
    SELECT 'GPT', 'AI/ML' UNION ALL
    SELECT 'BERT', 'AI/ML' UNION ALL
    SELECT 'Transformer', 'AI/ML' UNION ALL
    SELECT 'RAG', 'AI/ML' UNION ALL
    SELECT 'AI', 'AI/ML' UNION ALL
    
    -- Data & Analytics
    SELECT 'ETL', 'Data & Analytics' UNION ALL
    SELECT 'Data Warehouse', 'Data & Analytics' UNION ALL
    SELECT 'Data Pipeline', 'Data & Analytics' UNION ALL
    SELECT 'Tableau', 'Data & Analytics' UNION ALL
    SELECT 'Power BI', 'Data & Analytics' UNION ALL
    SELECT 'Crystal Reports', 'Data & Analytics' UNION ALL
    SELECT 'SSRS', 'Data & Analytics' UNION ALL
    SELECT 'SSIS', 'Data & Analytics' UNION ALL
    SELECT 'SSAS', 'Data & Analytics' UNION ALL
    SELECT 'Databricks', 'Data & Analytics' UNION ALL
    SELECT 'Spark', 'Data & Analytics' UNION ALL
    SELECT 'Kafka', 'Data & Analytics' UNION ALL
    SELECT 'Airflow', 'Data & Analytics' UNION ALL
    SELECT 'dbt', 'Data & Analytics' UNION ALL
    
    -- Mobile Development
    SELECT 'iOS', 'Mobile Development' UNION ALL
    SELECT 'Android', 'Mobile Development' UNION ALL
    SELECT 'React Native', 'Mobile Development' UNION ALL
    SELECT 'Flutter', 'Mobile Development' UNION ALL
    SELECT 'SwiftUI', 'Mobile Development' UNION ALL
    SELECT 'Jetpack Compose', 'Mobile Development' UNION ALL
    SELECT 'Android Studio', 'Mobile Development' UNION ALL
    SELECT 'Xcode', 'Mobile Development' UNION ALL
    
    -- Testing
    SELECT 'Selenium', 'Testing' UNION ALL
    SELECT 'Pytest', 'Testing' UNION ALL
    SELECT 'JUnit', 'Testing' UNION ALL
    SELECT 'Cypress', 'Testing' UNION ALL
    SELECT 'QA', 'Testing' UNION ALL
    SELECT 'Automated Testing', 'Testing'
) skills_data
JOIN skill_categories cat ON cat.category_name = skills_data.category
ON DUPLICATE KEY UPDATE skill_name=VALUES(skill_name);

-- Insert skill variations
INSERT INTO skill_variations (skill_id, variation_name)
SELECT id, variation FROM skills s
CROSS JOIN (
    SELECT 'js' as variation WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'JavaScript')
    UNION SELECT 'nodejs' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'JavaScript')
    UNION SELECT 'ts' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'TypeScript')
    UNION SELECT 'py' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Python')
    UNION SELECT 'postgres' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'PostgreSQL')
    UNION SELECT 'k8s' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Kubernetes')
    UNION SELECT 'powerbi' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Power BI')
    UNION SELECT 'pbi' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Power BI')
    UNION SELECT 'chroma' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'ChromaDB')
    UNION SELECT 'vectordb' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'Vector Database')
    UNION SELECT 'rn' WHERE EXISTS (SELECT 1 FROM skills WHERE skill_name = 'React Native')
) v
WHERE 
    (s.skill_name = 'JavaScript' AND v.variation IN ('js', 'nodejs')) OR
    (s.skill_name = 'TypeScript' AND v.variation = 'ts') OR
    (s.skill_name = 'Python' AND v.variation = 'py') OR
    (s.skill_name = 'PostgreSQL' AND v.variation = 'postgres') OR
    (s.skill_name = 'Kubernetes' AND v.variation = 'k8s') OR
    (s.skill_name = 'Power BI' AND v.variation IN ('powerbi', 'pbi')) OR
    (s.skill_name = 'ChromaDB' AND v.variation = 'chroma') OR
    (s.skill_name = 'Vector Database' AND v.variation = 'vectordb') OR
    (s.skill_name = 'React Native' AND v.variation = 'rn')
ON DUPLICATE KEY UPDATE variation_name=VALUES(variation_name);

-- Insert role profiles
INSERT INTO role_profiles (role_name, description) VALUES
('Full Stack Developer', 'Develops both frontend and backend applications'),
('Frontend Developer', 'Specializes in user interface development'),
('Backend Developer', 'Specializes in server-side development'),
('DevOps Engineer', 'Manages infrastructure and deployment pipelines'),
('Data Scientist', 'Analyzes data and builds ML models'),
('Cloud Engineer', 'Manages cloud infrastructure and services'),
('Mobile Developer', 'Develops mobile applications for iOS/Android'),
('QA Engineer', 'Tests and ensures software quality'),
('Database Administrator', 'Manages and optimizes databases'),
('AI/ML Engineer', 'Develops AI and machine learning systems'),
('BI Developer', 'Creates business intelligence reports and dashboards'),
('Data Engineer', 'Builds data pipelines and infrastructure')
ON DUPLICATE KEY UPDATE role_name=VALUES(role_name);
