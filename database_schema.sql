-- AI Resume Filter Database Schema
-- Updated: 2025-11-15
-- Features: UTF8MB4 encoding for emoji support, CASCADE DELETE for data integrity

-- Create database with UTF8MB4 character set
CREATE DATABASE IF NOT EXISTS resume_filter_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE resume_filter_db;

-- Set default character set for the session
SET NAMES utf8mb4;
SET CHARACTER_SET_CLIENT = utf8mb4;
SET CHARACTER_SET_CONNECTION = utf8mb4;

-- Job Descriptions table
CREATE TABLE IF NOT EXISTS job_descriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT,
    required_experience INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Candidates table
CREATE TABLE IF NOT EXISTS candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    resume_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Resume Data table
-- Stores parsed information from uploaded resumes
CREATE TABLE IF NOT EXISTS resume_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    skills TEXT,
    experience_years FLOAT DEFAULT 0,
    education TEXT,
    projects TEXT,
    certifications TEXT,
    job_titles TEXT,
    raw_text TEXT,
    INDEX idx_candidate_id (candidate_id),
    CONSTRAINT fk_resume_candidate 
        FOREIGN KEY (candidate_id) 
        REFERENCES candidates(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Analysis Results table
-- Stores AI-generated match scores and analysis for each candidate-job pair
CREATE TABLE IF NOT EXISTS analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    job_description_id INT NOT NULL,
    match_score FLOAT NOT NULL,
    skill_match_score FLOAT NOT NULL,
    experience_match_score FLOAT NOT NULL,
    keyword_match_score FLOAT NOT NULL,
    semantic_similarity_score FLOAT NOT NULL,
    tier VARCHAR(20) NOT NULL,
    red_flags TEXT,
    explanation TEXT,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_candidate_id (candidate_id),
    INDEX idx_job_id (job_description_id),
    INDEX idx_match_score (match_score),
    CONSTRAINT fk_analysis_candidate 
        FOREIGN KEY (candidate_id) 
        REFERENCES candidates(id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_analysis_job 
        FOREIGN KEY (job_description_id) 
        REFERENCES job_descriptions(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Red Flags table
-- Stores individual red flags detected for each candidate
CREATE TABLE IF NOT EXISTS red_flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    flag_type VARCHAR(100) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_candidate_id (candidate_id),
    INDEX idx_severity (severity),
    CONSTRAINT fk_redflag_candidate 
        FOREIGN KEY (candidate_id) 
        REFERENCES candidates(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Notes:
-- 1. All tables use utf8mb4 character set to support emojis and special characters
-- 2. All foreign keys have ON DELETE CASCADE to automatically clean up related data
-- 3. Indexes added on frequently queried columns for better performance
-- 4. InnoDB engine ensures ACID compliance and foreign key support
-- 5. IMPORTANT: Tables MUST be InnoDB (not MyISAM) for foreign keys to work

-- ============================================================
-- MAINTENANCE: If foreign keys are not working
-- ============================================================

-- Step 1: Verify table engines (should all be InnoDB)
-- SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'resume_filter_db';

-- Step 2: Convert MyISAM to InnoDB if needed (run python script):
-- python convert_to_innodb.py

-- Step 3: Apply CASCADE DELETE constraints (run python script):
-- python force_cascade_fix.py

-- Step 4: Verify constraints are active:
-- SELECT TABLE_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, DELETE_RULE 
-- FROM information_schema.REFERENTIAL_CONSTRAINTS 
-- WHERE CONSTRAINT_SCHEMA = 'resume_filter_db';

-- Expected output: All DELETE_RULE should be 'CASCADE'
