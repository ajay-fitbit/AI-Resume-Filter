from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import sys

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from config import Config
from app.database import create_connection, execute_query, fetch_query

# Import multi-agent orchestrator
from app.agents.orchestrator import RankingOrchestratorAgent
from app.agents.rag_agent import RAGAgent

# Initialize Flask with correct template folder
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(Config)

# Initialize multi-agent orchestrator
orchestrator = RankingOrchestratorAgent()
rag_agent = RAGAgent()
print("✅ Multi-Agent System Initialized")
print("✅ RAG Agent Initialized")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def _generate_candidate_profile(skills, experience_years):
    """Generate a profile summary indicating what roles the candidate would be good for"""
    skills = [s.strip() for s in skills if s.strip()]
    
    # Try to load role profiles from database, fall back to hardcoded if empty
    try:
        from app.database_config import get_roles_with_fallback
        role_profiles = get_roles_with_fallback()
    except Exception as e:
        print(f"Note: Using hardcoded role profiles (database not set up yet): {e}")
        # Fallback: Define role categories based on skills (hardcoded)
        role_profiles = {
            "Full Stack Developer": ["React", "Angular", "Vue", "Node.js", "JavaScript", "TypeScript", "Python", "Java", "Django", "Flask", "Express", "MongoDB", "PostgreSQL", "MySQL"],
            "Frontend Developer": ["React", "Angular", "Vue", "JavaScript", "TypeScript", "HTML", "CSS", "Bootstrap", "Tailwind", "jQuery", "Webpack"],
            "Backend Developer": ["Python", "Java", "Node.js", "C#", ".NET", "PHP", "Ruby", "Go", "Django", "Flask", "Spring", "Express", "API", "REST"],
            "DevOps Engineer": ["Docker", "Kubernetes", "Jenkins", "CI/CD", "AWS", "Azure", "GCP", "Terraform", "Ansible", "Linux", "Git"],
            "Data Scientist": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Data Science", "R", "Scikit-learn"],
            "Cloud Engineer": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CloudFormation", "Lambda", "EC2", "S3"],
            "Mobile Developer": ["Swift", "Kotlin", "React", "iOS", "Android", "Flutter", "React Native", "Jetpack Compose", "SwiftUI", "Xamarin", "Ionic", "Cordova", "Android Studio", "Xcode", "Firebase", "Room", "Realm", "SQLite", "Retrofit", "Alamofire", "Material Design", "UIKit", "Core Data", "Push Notifications", "In-App Purchases", "Google Play", "App Store"],
            "QA Engineer": ["Selenium", "Testing", "QA", "Automated Testing", "Pytest", "JUnit", "TestNG", "Cypress", "JIRA"],
            "Database Administrator": ["SQL", "MySQL", "PostgreSQL", "Oracle", "MongoDB", "Redis", "Database", "DynamoDB", "SQL Server"],
            "AI/ML Engineer": ["Machine Learning", "Deep Learning", "AI", "TensorFlow", "PyTorch", "NLP", "LLM", "GPT", "BERT", "Transformer", "ChromaDB", "Pinecone", "Vector Store", "Embeddings", "RAG"],
            "BI Developer": ["Power BI", "Tableau", "Looker", "Qlik", "SQL", "DAX", "Power Query", "Data Modeling", "ETL", "SSRS", "SSIS", "SSAS", "Crystal Reports", "Cognos", "MicroStrategy", "Data Visualization"],
            "Data Engineer": ["Python", "SQL", "Spark", "Kafka", "Airflow", "ETL", "Data Pipeline", "Big Data", "Hadoop", "AWS Glue", "Azure Data Factory", "Databricks", "Snowflake", "dbt"]
        }
    
    # Calculate match scores for each role
    role_matches = {}
    for role, required_skills in role_profiles.items():
        matches = sum(1 for skill in skills if any(req.lower() in skill.lower() for req in required_skills))
        if matches > 0:
            role_matches[role] = matches
    
    # Sort by match count
    sorted_roles = sorted(role_matches.items(), key=lambda x: x[1], reverse=True)
    
    # Generate profile
    if sorted_roles:
        top_role = sorted_roles[0][0]
        exp_level = "Senior" if experience_years >= 5 else "Mid-level" if experience_years >= 2 else "Junior"
        
        # Get top 3 roles
        top_roles = [role for role, _ in sorted_roles[:3]]
        
        if len(top_roles) > 1:
            profile = f"{exp_level} {top_role} (also suitable for {', '.join(top_roles[1:])})"
        else:
            profile = f"{exp_level} {top_role}"
        
        return profile
    else:
        exp_level = "Senior" if experience_years >= 5 else "Mid-level" if experience_years >= 2 else "Entry-level"
        return f"{exp_level} Professional with {experience_years} years experience"

@app.route('/')
def index():
    """Home page / Dashboard"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('index.html', stats={})
    
    # Get statistics
    stats = {
        'total_candidates': fetch_query(conn, "SELECT COUNT(*) as count FROM candidates")[0]['count'],
        'total_jobs': fetch_query(conn, "SELECT COUNT(*) as count FROM job_descriptions")[0]['count'],
        'top_tier': fetch_query(conn, "SELECT COUNT(*) as count FROM analysis_results WHERE tier = 'Top Tier'")[0]['count'],
        'medium_tier': fetch_query(conn, "SELECT COUNT(*) as count FROM analysis_results WHERE tier = 'Medium Tier'")[0]['count'],
        'low_tier': fetch_query(conn, "SELECT COUNT(*) as count FROM analysis_results WHERE tier = 'Low Tier'")[0]['count']
    }
    
    # Get recent analyses
    recent_analyses = fetch_query(conn, """
        SELECT c.id as candidate_id, c.name, c.email, ar.match_score, ar.tier, ar.analyzed_at, jd.title as job_title
        FROM analysis_results ar
        JOIN candidates c ON ar.candidate_id = c.id
        JOIN job_descriptions jd ON ar.job_description_id = jd.id
        ORDER BY ar.analyzed_at DESC
        LIMIT 10
    """)
    
    # Ensure recent_analyses is not None
    if recent_analyses is None:
        recent_analyses = []
    
    # Get bulk upload candidate briefs (top 6 most recent)
    bulk_candidates = fetch_query(conn, """
        SELECT 
            c.id,
            c.name,
            c.email,
            c.created_at,
            rd.experience_years,
            rd.skills,
            (SELECT COUNT(*) FROM red_flags rf WHERE rf.candidate_id = c.id) as total_flags,
            (SELECT COUNT(*) FROM red_flags rf WHERE rf.candidate_id = c.id AND rf.severity = 'High') as high_flags
        FROM candidates c
        INNER JOIN resume_data rd ON c.id = rd.candidate_id
        LEFT JOIN analysis_results ar ON c.id = ar.candidate_id
        WHERE ar.id IS NULL
        ORDER BY c.created_at DESC
        LIMIT 6
    """)
    
    # Generate profiles for bulk candidates
    if bulk_candidates:
        for candidate in bulk_candidates:
            candidate['profile'] = _generate_candidate_profile(
                candidate.get('skills', ''),
                candidate.get('experience_years', 0)
            )
            # Get skill count
            skills = candidate.get('skills', '')
            candidate['skills_count'] = len([s.strip() for s in skills.split(',') if s.strip()]) if skills else 0
    
    conn.close()
    return render_template('index.html', stats=stats, recent_analyses=recent_analyses, bulk_candidates=bulk_candidates or [])

@app.route('/create_job', methods=['GET', 'POST'])
def create_job():
    """Create a new job description"""
    if request.method == 'POST':
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        
        if not job_title or not job_description:
            flash('Please provide both job title and description', 'error')
            return redirect(url_for('create_job'))
        
        conn = create_connection()
        if not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('create_job'))
        
        jd_id = execute_query(conn, 
            "INSERT INTO job_descriptions (title, description) VALUES (%s, %s)",
            (job_title, job_description)
        )
        
        conn.close()
        flash(f'Job description "{job_title}" created successfully!', 'success')
        return redirect(url_for('upload'))
    
    return render_template('create_job.html')

@app.route('/bulk_upload', methods=['GET', 'POST'])
def bulk_upload():
    """Bulk upload resumes independent of job descriptions - Parse, analyze skills, detect red flags"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('bulk_upload.html')
    
    if request.method == 'POST':
        # Process uploaded resumes from folder
        files = request.files.getlist('resumes')
        processed_count = 0
        failed_count = 0
        
        # Create a generic job description for skill analysis and candidate profiling
        generic_jd = """
        Looking for talented professionals with strong technical skills, relevant experience,
        and a solid educational background. Key areas: software development, data analysis,
        project management, communication skills, problem-solving abilities, teamwork,
        cloud technologies, databases, programming languages, and industry-relevant certifications.
        """
        
        for file in files:
            if file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    
                    print(f"\n📄 Processing: {filename}")
                    
                    # ===== USE EXISTING MULTI-AGENT SYSTEM =====
                    # Execute orchestrator with generic profile for skill analysis
                    agent_result = orchestrator.execute({
                        "file_path": filepath,
                        "job_description": generic_jd,
                        "required_experience": 0
                    })
                    
                    if agent_result.get("success"):
                        candidate_data = agent_result['candidate_data']
                        scores = agent_result['scores']
                        
                        print(f"   Name: {candidate_data['name']}")
                        print(f"   Email: {candidate_data.get('email', 'N/A')}")
                        print(f"   Phone: {candidate_data.get('phone', 'N/A')}")
                        print(f"   Skills: {candidate_data.get('skills', 'N/A')[:100]}...")
                        print(f"   Experience: {candidate_data['experience_years']} years")
                        print(f"   Skill Assessment Score: {scores['skill_match_score']}%")
                        
                        # Save candidate
                        candidate_id = execute_query(conn,
                            "INSERT INTO candidates (name, email, phone, resume_path) VALUES (%s, %s, %s, %s)",
                            (candidate_data['name'], candidate_data.get('email'), 
                             candidate_data.get('phone'), filepath)
                        )
                        
                        # Save resume data with comprehensive analysis
                        execute_query(conn,
                            """INSERT INTO resume_data (candidate_id, skills, experience_years, education, 
                               projects, certifications, job_titles, raw_text) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            (candidate_id, 
                             candidate_data['skills'],
                             candidate_data['experience_years'],
                             candidate_data['education'], 
                             candidate_data.get('projects', ''),  # projects
                             candidate_data.get('certifications', ''),  # certifications
                             candidate_data.get('job_titles', ''),  # job_titles
                             candidate_data.get('raw_text', ''))  # raw_text
                        )
                        
                        # Filter red flags - only save job-independent flags for bulk upload
                        # Exclude: "Irrelevant Experience", "Missing Skills", "Minimal Experience"
                        job_independent_flag_types = ['Job Hopping', 'Career Gap', 'Frequent Job Changes', 
                                                      'Employment Gap', 'Short Tenure']
                        
                        for flag in agent_result.get('red_flags', []):
                            # Only save flags that don't require job description context
                            if any(flag_type.lower() in flag['type'].lower() for flag_type in job_independent_flag_types):
                                execute_query(conn,
                                    "INSERT INTO red_flags (candidate_id, flag_type, description, severity) VALUES (%s, %s, %s, %s)",
                                    (candidate_id, flag['type'], flag['description'], flag['severity'])
                                )
                        
                        # Generate candidate profile summary based on skills
                        skills_list = candidate_data['skills'].split(',') if isinstance(candidate_data['skills'], str) else candidate_data['skills']
                        profile_summary = _generate_candidate_profile(skills_list, candidate_data['experience_years'])
                        
                        print(f"   Profile: {profile_summary}")
                        print(f"✅ Successfully processed: {candidate_data['name']}")
                        
                        processed_count += 1
                    else:
                        failed_count += 1
                        error_msg = agent_result.get('error', 'Unknown error')
                        print(f"❌ Agent processing failed: {filename} - {error_msg}")
                        
                except Exception as e:
                    failed_count += 1
                    print(f"❌ Error processing {filename}: {str(e)}")
                    import traceback
                    traceback.print_exc()
        
        conn.close()
        flash(f'Successfully processed {processed_count} resumes. Failed: {failed_count}', 'success' if failed_count == 0 else 'error')
        return redirect(url_for('candidates'))
    
    conn.close()
    return render_template('bulk_upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload resumes for an existing job description"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('upload.html', jobs=[])
    
    # Get all job descriptions for dropdown
    jobs = fetch_query(conn, "SELECT id, title FROM job_descriptions ORDER BY created_at DESC")
    
    if request.method == 'POST':
        # Get selected job description
        jd_id = request.form.get('job_description_id')
        
        if not jd_id:
            flash('Please select a job description', 'error')
            conn.close()
            return redirect(url_for('upload'))
        
        # Get the job description text
        job_data = fetch_query(conn, "SELECT description FROM job_descriptions WHERE id = %s", (jd_id,))
        if not job_data:
            flash('Job description not found', 'error')
            conn.close()
            return redirect(url_for('upload'))
        
        job_description = job_data[0]['description']
        
        # Process uploaded resumes
        files = request.files.getlist('resumes')
        processed_count = 0
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                # ===== MULTI-AGENT WORKFLOW =====
                # Execute orchestrator with all agents
                agent_result = orchestrator.execute({
                    "file_path": filepath,
                    "job_description": job_description,
                    "required_experience": 0  # Can extract from JD in future
                })
                
                if agent_result.get("success"):
                    candidate_data = agent_result['candidate_data']
                    scores = agent_result['scores']
                    
                    # Save candidate
                    candidate_id = execute_query(conn,
                        "INSERT INTO candidates (name, email, phone, resume_path) VALUES (%s, %s, %s, %s)",
                        (candidate_data['name'], candidate_data['email'], 
                         candidate_data['phone'], filepath)
                    )
                    
                    # Save resume data
                    execute_query(conn,
                        """INSERT INTO resume_data (candidate_id, skills, experience_years, education, 
                           projects, certifications, job_titles, raw_text) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (candidate_id, 
                         candidate_data['skills'],  # Already a comma-separated string from parser
                         candidate_data['experience_years'],
                         candidate_data['education'], 
                         candidate_data.get('projects', ''),  # projects
                         candidate_data.get('certifications', ''),  # certifications
                         candidate_data.get('job_titles', ''),  # job_titles
                         candidate_data.get('raw_text', ''))  # raw_text (stored in state but not needed here)
                    )
                    
                    # Save analysis results
                    execute_query(conn,
                        """INSERT INTO analysis_results (candidate_id, job_description_id, match_score,
                           skill_match_score, experience_match_score, keyword_match_score, 
                           semantic_similarity_score, tier, red_flags, explanation)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (candidate_id, jd_id, 
                         scores['overall_score'],
                         scores['skill_match_score'], 
                         scores['experience_match_score'],
                         scores['keyword_match_score'], 
                         scores['semantic_similarity_score'],
                         agent_result['tier'], 
                         str(agent_result['red_flags']), 
                         agent_result['explanation'])
                    )
                    
                    # Save individual red flags
                    for flag in agent_result['red_flags']:
                        execute_query(conn,
                            "INSERT INTO red_flags (candidate_id, flag_type, description, severity) VALUES (%s, %s, %s, %s)",
                            (candidate_id, flag['type'], flag['description'], flag['severity'])
                        )
                    
                    processed_count += 1
                    print(f"✅ Multi-Agent processed: {candidate_data['name']} - Score: {scores['overall_score']:.2f}%")
        
        conn.close()
        flash(f'Successfully processed {processed_count} resume(s)', 'success')
        return redirect(url_for('candidates', job_id=jd_id))
    
    conn.close()
    return render_template('upload.html', jobs=jobs)

@app.route('/bulk_analysis')
def bulk_analysis():
    """View comprehensive analysis of all bulk uploaded candidates"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('bulk_analysis.html', candidates=[], jobs=[])
    
    # Get all job descriptions for dropdown
    jobs = fetch_query(conn, "SELECT id, title FROM job_descriptions ORDER BY created_at DESC")
    
    # Get all candidates with their resume data and red flags
    query = """
        SELECT 
            c.id, c.name, c.email, c.phone, c.created_at,
            rd.skills, rd.experience_years, rd.education, 
            rd.certifications, rd.job_titles,
            (SELECT COUNT(*) FROM red_flags rf WHERE rf.candidate_id = c.id) as total_flags,
            (SELECT COUNT(*) FROM red_flags rf WHERE rf.candidate_id = c.id AND rf.severity = 'High') as high_flags,
            (SELECT COUNT(*) FROM red_flags rf WHERE rf.candidate_id = c.id AND rf.severity = 'Medium') as medium_flags
        FROM candidates c
        LEFT JOIN resume_data rd ON c.id = rd.candidate_id
        ORDER BY c.created_at DESC
    """
    candidates_list = fetch_query(conn, query)
    
    # Enhance each candidate with profile analysis and detailed red flags
    for candidate in candidates_list:
        # Fetch detailed red flags for each candidate
        red_flags_query = """
            SELECT flag_type, description, severity 
            FROM red_flags 
            WHERE candidate_id = %s 
            ORDER BY 
                CASE severity 
                    WHEN 'High' THEN 1 
                    WHEN 'Medium' THEN 2 
                    ELSE 3 
                END
        """
        candidate['red_flags_list'] = fetch_query(conn, red_flags_query, (candidate['id'],))
        if candidate.get('skills'):
            skills_list = [s.strip() for s in candidate['skills'].split(',') if s.strip()]
            candidate['skills_list'] = skills_list
            candidate['profile'] = _generate_candidate_profile(skills_list, candidate.get('experience_years', 0))
            candidate['skills_count'] = len(skills_list)
        else:
            candidate['skills_list'] = []
            candidate['profile'] = 'Profile not available'
            candidate['skills_count'] = 0
    
    conn.close()
    return render_template('bulk_analysis.html', candidates=candidates_list, jobs=jobs)

@app.route('/candidates')
def candidates():
    """View all candidates for a specific job"""
    job_id = request.args.get('job_id', type=int)
    
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('candidates.html', candidates=[], job=None)
    
    # Get job details
    job = None
    if job_id:
        jobs = fetch_query(conn, "SELECT * FROM job_descriptions WHERE id = %s", (job_id,))
        job = jobs[0] if jobs else None
    
    # Get candidates with analysis results
    if job_id:
        query = """
            SELECT c.id, c.name, c.email, c.phone, c.created_at,
                   ar.match_score, ar.tier, ar.skill_match_score, 
                   ar.experience_match_score, ar.explanation,
                   (SELECT COUNT(*) FROM red_flags rf WHERE rf.candidate_id = c.id AND rf.severity = 'High') as high_flags,
                   rd.job_titles
            FROM candidates c
            JOIN analysis_results ar ON c.id = ar.candidate_id
            LEFT JOIN resume_data rd ON c.id = rd.candidate_id
            WHERE ar.job_description_id = %s
            ORDER BY ar.match_score DESC
        """
        candidates_list = fetch_query(conn, query, (job_id,))
    else:
        # Get all candidates with their latest analysis
        query = """
            SELECT c.id, c.name, c.email, c.phone, c.created_at,
                   COALESCE(ar.match_score, 0) as match_score, 
                   COALESCE(ar.tier, 'No Analysis') as tier,
                   COALESCE(ar.skill_match_score, 0) as skill_match_score,
                   COALESCE(ar.experience_match_score, 0) as experience_match_score,
                   COALESCE(ar.explanation, 'No analysis available') as explanation,
                   (SELECT COUNT(*) FROM red_flags rf WHERE rf.candidate_id = c.id AND rf.severity = 'High') as high_flags,
                   rd.job_titles
            FROM candidates c
            LEFT JOIN analysis_results ar ON c.id = ar.candidate_id
            LEFT JOIN resume_data rd ON c.id = rd.candidate_id
            GROUP BY c.id
            ORDER BY c.created_at DESC
        """
        candidates_list = fetch_query(conn, query)
    
    conn.close()
    return render_template('candidates.html', candidates=candidates_list, job=job)

@app.route('/candidate/<int:candidate_id>')
def candidate_detail(candidate_id):
    """View detailed information about a candidate"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('index'))
    
    # Get candidate info
    candidate = fetch_query(conn, "SELECT * FROM candidates WHERE id = %s", (candidate_id,))
    if not candidate:
        flash('Candidate not found', 'error')
        conn.close()
        return redirect(url_for('index'))
    
    candidate = candidate[0]
    
    # Get resume data
    resume_data = fetch_query(conn, "SELECT * FROM resume_data WHERE candidate_id = %s", (candidate_id,))
    resume_data = resume_data[0] if resume_data else None
    
    # Get analysis results
    analysis = fetch_query(conn, """
        SELECT ar.*, jd.title as job_title, jd.description as job_description
        FROM analysis_results ar
        JOIN job_descriptions jd ON ar.job_description_id = jd.id
        WHERE ar.candidate_id = %s
        ORDER BY ar.analyzed_at DESC
    """, (candidate_id,))
    
    # Get red flags
    red_flags = fetch_query(conn, 
        "SELECT * FROM red_flags WHERE candidate_id = %s ORDER BY severity DESC", 
        (candidate_id,)
    )
    
    conn.close()
    return render_template('candidate_detail.html', 
                         candidate=candidate, 
                         resume_data=resume_data,
                         analysis=analysis,
                         red_flags=red_flags)

@app.route('/jobs')
def jobs():
    """View all job descriptions"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('jobs.html', jobs=[])
    
    jobs_list = fetch_query(conn, """
        SELECT jd.*, 
               COUNT(DISTINCT ar.candidate_id) as candidate_count,
               AVG(ar.match_score) as avg_score
        FROM job_descriptions jd
        LEFT JOIN analysis_results ar ON jd.id = ar.job_description_id
        GROUP BY jd.id
        ORDER BY jd.created_at DESC
    """)
    
    conn.close()
    return render_template('jobs.html', jobs=jobs_list)

@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    """Delete a job description and all associated data"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('jobs'))
    
    try:
        # Get job title before deleting
        job = fetch_query(conn, "SELECT title FROM job_descriptions WHERE id = %s", (job_id,))
        job_title = job[0]['title'] if job else "Job"
        
        # Delete job description (CASCADE will handle related records)
        execute_query(conn, "DELETE FROM job_descriptions WHERE id = %s", (job_id,))
        
        conn.close()
        flash(f'Job "{job_title}" and all associated data deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting job: {str(e)}', 'error')
    
    return redirect(url_for('jobs'))

@app.route('/delete_candidate/<int:candidate_id>', methods=['POST'])
def delete_candidate(candidate_id):
    """Delete a candidate and all associated data"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('candidates'))
    
    try:
        # Get candidate name before deleting
        candidate = fetch_query(conn, "SELECT name, resume_path FROM candidates WHERE id = %s", (candidate_id,))
        candidate_name = candidate[0]['name'] if candidate else "Candidate"
        resume_path = candidate[0]['resume_path'] if candidate else None
        
        # Delete uploaded resume file if it exists
        if resume_path and os.path.exists(resume_path):
            try:
                os.remove(resume_path)
            except Exception as e:
                print(f"Could not delete resume file: {e}")
        
        # Delete candidate (CASCADE will handle related records in resume_data, analysis_results, red_flags)
        execute_query(conn, "DELETE FROM candidates WHERE id = %s", (candidate_id,))
        
        conn.close()
        flash(f'Candidate "{candidate_name}" and all associated data deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting candidate: {str(e)}', 'error')
    
    return redirect(url_for('candidates'))

@app.route('/download_resume/<int:candidate_id>')
def download_resume(candidate_id):
    """Download resume file for a candidate"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('candidates'))
    
    try:
        # Get candidate resume path
        candidate = fetch_query(conn, "SELECT name, resume_path FROM candidates WHERE id = %s", (candidate_id,))
        conn.close()
        
        if not candidate:
            flash('Candidate not found', 'error')
            return redirect(url_for('candidates'))
        
        resume_path = candidate[0]['resume_path']
        candidate_name = candidate[0]['name']
        
        if not resume_path or not os.path.exists(resume_path):
            flash('Resume file not found', 'error')
            return redirect(url_for('candidates'))
        
        # Extract file extension
        file_ext = os.path.splitext(resume_path)[1]
        # Create download filename
        download_name = f"{candidate_name}_Resume{file_ext}"
        
        return send_file(resume_path, as_attachment=True, download_name=download_name)
        
    except Exception as e:
        flash(f'Error downloading resume: {str(e)}', 'error')
        return redirect(url_for('candidates'))

@app.route('/agent_monitoring')
def agent_monitoring():
    """Multi-Agent System Monitoring Dashboard"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('agent_monitoring.html', executions=[])
    
    # Get recent candidate analyses with timing information
    executions = fetch_query(conn, """
        SELECT 
            c.id as candidate_id,
            c.name as candidate_name,
            ar.analyzed_at as timestamp,
            ar.match_score as score,
            0.5 as execution_time
        FROM candidates c
        JOIN analysis_results ar ON c.id = ar.candidate_id
        ORDER BY ar.analyzed_at DESC
        LIMIT 20
    """)
    
    conn.close()
    return render_template('agent_monitoring.html', executions=executions)

@app.route('/api/agent_logs/<int:candidate_id>')
def api_agent_logs(candidate_id):
    """API endpoint to fetch detailed agent execution logs for a candidate"""
    conn = create_connection()
    if not conn:
        return jsonify({"error": "Database connection error"}), 500
    
    try:
        # Get candidate information
        candidate = fetch_query(conn, 
            "SELECT name, email, phone FROM candidates WHERE id = %s", 
            (candidate_id,))
        
        if not candidate:
            conn.close()
            return jsonify({"error": "Candidate not found"}), 404
        
        candidate_data = candidate[0]
        
        # Get resume data
        resume_data = fetch_query(conn,
            "SELECT skills, experience_years, education FROM resume_data WHERE candidate_id = %s",
            (candidate_id,))
        
        # Get analysis results
        analysis = fetch_query(conn,
            """SELECT match_score, skill_match_score, experience_match_score, 
                      keyword_match_score, semantic_similarity_score, tier, explanation
               FROM analysis_results WHERE candidate_id = %s
               ORDER BY analyzed_at DESC LIMIT 1""",
            (candidate_id,))
        
        # Get red flags
        red_flags = fetch_query(conn,
            "SELECT flag_type, description, severity FROM red_flags WHERE candidate_id = %s",
            (candidate_id,))
        
        conn.close()
        
        # Prepare response
        response = {
            "candidate_name": candidate_data['name'],
            "email": candidate_data.get('email'),
            "phone": candidate_data.get('phone'),
            "skills": resume_data[0]['skills'] if resume_data else "Not specified",
            "experience_years": resume_data[0]['experience_years'] if resume_data else 0,
            "education": resume_data[0]['education'] if resume_data else "Not specified",
            "scores": {
                "match_score": round(analysis[0]['match_score'], 2) if analysis else 0,
                "semantic_similarity": round(analysis[0]['semantic_similarity_score'], 2) if analysis else 0,
                "keyword_match": round(analysis[0]['keyword_match_score'], 2) if analysis else 0,
                "skill_match": round(analysis[0]['skill_match_score'], 2) if analysis else 0,
                "experience_match": round(analysis[0]['experience_match_score'], 2) if analysis else 0
            },
            "tier": analysis[0]['tier'] if analysis else "Not analyzed",
            "explanation": analysis[0]['explanation'] if analysis else "",
            "red_flags": [
                {
                    "flag_type": flag['flag_type'],
                    "description": flag['description'],
                    "severity": flag['severity']
                }
                for flag in red_flags
            ]
        }
        
        return jsonify(response)
    
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/rag_chat')
def rag_chat():
    """RAG-powered resume Q&A interface"""
    conn = create_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('rag_chat.html', jobs=[], total_candidates=0)
    
    # Get all job descriptions with candidate counts
    jobs = fetch_query(conn, """
        SELECT 
            jd.id, 
            jd.title, 
            COUNT(DISTINCT c.id) as candidate_count
        FROM job_descriptions jd
        LEFT JOIN analysis_results ar ON jd.id = ar.job_description_id
        LEFT JOIN candidates c ON ar.candidate_id = c.id
        GROUP BY jd.id, jd.title
        ORDER BY jd.created_at DESC
    """)
    
    # Get total candidate count (all candidates with resume data)
    total_result = fetch_query(conn, """
        SELECT COUNT(DISTINCT c.id) as total
        FROM candidates c
        INNER JOIN resume_data rd ON c.id = rd.candidate_id
    """)
    total_candidates = total_result[0]['total'] if total_result else 0
    
    conn.close()
    return render_template('rag_chat.html', jobs=jobs, total_candidates=total_candidates)

@app.route('/api/rag/query', methods=['POST'])
def rag_query():
    """Process RAG query and return relevant candidates"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        job_id = data.get('job_id')
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        conn = create_connection()
        if not conn:
            return jsonify({"error": "Database connection error"}), 500
        
        # Get candidates based on job_id (or all if not specified)
        if job_id and job_id.strip():
            candidates_query = """
                SELECT 
                    c.id,
                    c.name,
                    c.email,
                    rd.skills,
                    CONCAT(rd.experience_years, ' years') as experience,
                    rd.raw_text as summary,
                    COALESCE(ar.match_score, 0) as match_score,
                    COALESCE(ar.skill_match_score, 0) as skill_match_score,
                    COALESCE(ar.experience_match_score, 0) as experience_match_score
                FROM candidates c
                LEFT JOIN resume_data rd ON c.id = rd.candidate_id
                LEFT JOIN analysis_results ar ON c.id = ar.candidate_id AND ar.job_description_id = %s
                WHERE rd.id IS NOT NULL
                ORDER BY ar.match_score DESC
            """
            candidates = fetch_query(conn, candidates_query, (job_id,))
        else:

            candidates_query = """
                SELECT 
                    c.id,
                    c.name,
                    c.email,
                    rd.skills,
                    CONCAT(rd.experience_years, ' years') as experience,
                    rd.raw_text as summary,
                    COALESCE(MAX(ar.match_score), 0) as match_score,
                    COALESCE(MAX(ar.skill_match_score), 0) as skill_match_score,
                    COALESCE(MAX(ar.experience_match_score), 0) as experience_match_score
                FROM candidates c
                LEFT JOIN resume_data rd ON c.id = rd.candidate_id
                LEFT JOIN analysis_results ar ON c.id = ar.candidate_id
                WHERE rd.id IS NOT NULL
                GROUP BY c.id, c.name, c.email, rd.skills, rd.experience_years, rd.raw_text
                ORDER BY match_score DESC
            """
            candidates = fetch_query(conn, candidates_query)
        
        print(f"RAG Query: Found {len(candidates)} candidates for question: {question}")
        
        # Get job context if specified
        job_context = None
        if job_id and job_id.strip():
            job_result = fetch_query(conn, 
                "SELECT title, description FROM job_descriptions WHERE id = %s", 
                (job_id,)
            )
            if job_result:
                job_context = job_result[0]
        
        conn.close()
        
        # Debug: Print candidate data
        if candidates:
            print(f"First candidate sample: {candidates[0]}")
        else:
            print("No candidates returned from database query")
        
        # Process query with RAG agent
        result = rag_agent.query(question, candidates, job_context)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"RAG Query Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/match_candidate', methods=['POST'])
def match_candidate():
    """Match a bulk uploaded candidate with a specific job description"""
    try:
        data = request.get_json()
        candidate_id = data.get('candidate_id')
        job_id = data.get('job_id')
        
        if not candidate_id or not job_id:
            return jsonify({"success": False, "error": "Missing candidate_id or job_id"}), 400
        
        conn = create_connection()
        if not conn:
            return jsonify({"success": False, "error": "Database connection error"}), 500
        
        # Get job description
        job_result = fetch_query(conn, 
            "SELECT title, description, required_skills, required_experience FROM job_descriptions WHERE id = %s", 
            (job_id,)
        )
        if not job_result:
            conn.close()
            return jsonify({"success": False, "error": "Job description not found"}), 404
        
        job = job_result[0]
        
        # Get candidate resume data including file path
        candidate_result = fetch_query(conn,
            "SELECT c.id, c.name, c.resume_path FROM candidates c WHERE c.id = %s",
            (candidate_id,)
        )
        if not candidate_result:
            conn.close()
            return jsonify({"success": False, "error": "Candidate not found"}), 404
        
        candidate = candidate_result[0]
        
        if not candidate.get('resume_path') or not os.path.exists(candidate['resume_path']):
            conn.close()
            return jsonify({"success": False, "error": "Resume file not found"}), 404
        
        # Check if analysis already exists
        existing = fetch_query(conn,
            "SELECT id FROM analysis_results WHERE candidate_id = %s AND job_description_id = %s",
            (candidate_id, job_id)
        )
        
        # Run orchestrator analysis
        print(f"🎯 Matching candidate {candidate['name']} with job {job['title']}")
        
        # Ensure required_experience is an integer
        required_exp = job.get('required_experience')
        if required_exp is None:
            required_exp = 0
        
        agent_result = orchestrator.execute({
            "file_path": candidate['resume_path'],
            "job_description": job['description'],
            "required_experience": int(required_exp)
        })
        
        if not agent_result.get("success"):
            conn.close()
            return jsonify({"success": False, "error": "Analysis failed"}), 500
        
        result = agent_result['scores']
        tier = agent_result['tier']
        explanation = agent_result['explanation']
        
        # Store or update analysis results
        if existing:
            # Update existing analysis
            update_query = """
                UPDATE analysis_results 
                SET match_score = %s, skill_match_score = %s, experience_match_score = %s,
                    keyword_match_score = %s, semantic_similarity_score = %s, tier = %s,
                    explanation = %s, analyzed_at = NOW()
                WHERE candidate_id = %s AND job_description_id = %s
            """
            execute_query(conn, update_query, (
                result['overall_score'],
                result['skill_match_score'],
                result['experience_match_score'],
                result['keyword_match_score'],
                result['semantic_similarity_score'],
                tier,
                explanation,
                candidate_id,
                job_id
            ))
        else:
            # Insert new analysis
            insert_query = """
                INSERT INTO analysis_results 
                (candidate_id, job_description_id, match_score, skill_match_score, 
                experience_match_score, keyword_match_score, semantic_similarity_score, 
                tier, explanation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            execute_query(conn, insert_query, (
                candidate_id,
                job_id,
                result['overall_score'],
                result['skill_match_score'],
                result['experience_match_score'],
                result['keyword_match_score'],
                result['semantic_similarity_score'],
                tier,
                explanation
            ))
        
        conn.close()
        
        return jsonify({
            "success": True,
            "match_score": round(result['overall_score'], 1),
            "tier": tier,
            "candidate_name": candidate['name'],
            "job_title": job['title']
        }), 200
        
    except Exception as e:
        print(f"Match Candidate Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================
# ADMIN CONFIGURATION ROUTES
# ============================================================

@app.route('/admin/config')
def admin_config():
    """Admin page for managing skills, variations, and role profiles"""
    return render_template('admin_config.html')

# Skill Categories Management APIs
@app.route('/api/admin/categories', methods=['GET'])
def get_categories():
    """Get all skill categories"""
    conn = create_connection()
    
    query = """
        SELECT id, category_name, description, display_order, icon, color, is_active,
               (SELECT COUNT(*) FROM skills WHERE category_id = skill_categories.id) as skill_count
        FROM skill_categories
        ORDER BY display_order, category_name
    """
    
    categories = fetch_query(conn, query)
    conn.close()
    
    return jsonify(categories)

@app.route('/api/admin/categories', methods=['POST'])
def add_category():
    """Add a new skill category"""
    data = request.json
    category_name = data.get('category_name')
    description = data.get('description', '')
    icon = data.get('icon', '🔧')
    color = data.get('color', '#6b7280')
    
    conn = create_connection()
    
    # Get max display_order
    max_order = fetch_query(conn, "SELECT COALESCE(MAX(display_order), 0) as max_order FROM skill_categories")
    display_order = max_order[0]['max_order'] + 1 if max_order else 1
    
    query = """
        INSERT INTO skill_categories (category_name, description, icon, color, display_order, is_active)
        VALUES (%s, %s, %s, %s, %s, 1)
    """
    execute_query(conn, query, (category_name, description, icon, color, display_order))
    conn.close()
    
    return jsonify({"success": True}), 201

@app.route('/api/admin/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update category details"""
    data = request.json
    category_name = data.get('category_name')
    description = data.get('description', '')
    icon = data.get('icon', '🔧')
    color = data.get('color', '#6b7280')
    
    conn = create_connection()
    query = """
        UPDATE skill_categories 
        SET category_name = %s, description = %s, icon = %s, color = %s
        WHERE id = %s
    """
    execute_query(conn, query, (category_name, description, icon, color, category_id))
    conn.close()
    
    return jsonify({"success": True})

@app.route('/api/admin/categories/<int:category_id>/toggle', methods=['PUT'])
def toggle_category_status(category_id):
    """Toggle category active status"""
    data = request.json
    is_active = data.get('is_active')
    
    conn = create_connection()
    query = "UPDATE skill_categories SET is_active = %s WHERE id = %s"
    execute_query(conn, query, (is_active, category_id))
    conn.close()
    
    return jsonify({"success": True})

@app.route('/api/admin/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category (only if no skills are using it)"""
    conn = create_connection()
    
    # Check if category has skills
    check = fetch_query(conn, "SELECT COUNT(*) as count FROM skills WHERE category_id = %s", (category_id,))
    if check[0]['count'] > 0:
        conn.close()
        return jsonify({"success": False, "error": "Cannot delete category with existing skills"}), 400
    
    query = "DELETE FROM skill_categories WHERE id = %s"
    execute_query(conn, query, (category_id,))
    conn.close()
    
    return jsonify({"success": True})

# Skills Management APIs
@app.route('/api/admin/skills', methods=['GET'])
def get_skills():
    """Get all skills with their variations"""
    conn = create_connection()
    
    query = """
        SELECT s.id, s.skill_name, sc.category_name as category, s.description, s.is_active,
               GROUP_CONCAT(sv.variation_name SEPARATOR ', ') as variations
        FROM skills s
        JOIN skill_categories sc ON s.category_id = sc.id
        LEFT JOIN skill_variations sv ON s.id = sv.skill_id AND sv.is_active = 1
        GROUP BY s.id, s.skill_name, sc.category_name, s.description, s.is_active
        ORDER BY sc.display_order, s.skill_name
    """
    
    skills = fetch_query(conn, query)
    conn.close()
    
    return jsonify(skills)

@app.route('/api/admin/skills', methods=['POST'])
def add_skill():
    """Add a new skill with variations"""
    data = request.json
    skill_name = data.get('skill_name')
    category_id = data.get('category_id')
    variations = data.get('variations', '')
    
    conn = create_connection()
    
    # Insert skill and get the skill ID
    insert_skill = """
        INSERT INTO skills (skill_name, category_id, is_active) 
        VALUES (%s, %s, 1)
    """
    skill_id = execute_query(conn, insert_skill, (skill_name, category_id))
    
    # Insert variations
    if variations and skill_id:
        variation_list = [v.strip() for v in variations.split(',') if v.strip()]
        for variation in variation_list:
            insert_variation = """
                INSERT INTO skill_variations (skill_id, variation_name, is_active)
                VALUES (%s, %s, 1)
            """
            execute_query(conn, insert_variation, (skill_id, variation))
    
    conn.close()
    
    return jsonify({"success": True}), 201

@app.route('/api/admin/skills/<int:skill_id>', methods=['PUT'])
def update_skill(skill_id):
    """Update skill details"""
    data = request.json
    skill_name = data.get('skill_name')
    category_id = data.get('category_id')
    variations = data.get('variations', '')
    
    conn = create_connection()
    
    # Update skill
    update_skill = "UPDATE skills SET skill_name = %s, category_id = %s WHERE id = %s"
    execute_query(conn, update_skill, (skill_name, category_id, skill_id))
    
    # Delete existing variations
    execute_query(conn, "DELETE FROM skill_variations WHERE skill_id = %s", (skill_id,))
    
    # Insert new variations
    if variations:
        variation_list = [v.strip() for v in variations.split(',') if v.strip()]
        for variation in variation_list:
            insert_variation = "INSERT INTO skill_variations (skill_id, variation_name, is_active) VALUES (%s, %s, 1)"
            execute_query(conn, insert_variation, (skill_id, variation))
    
    conn.close()
    
    return jsonify({"success": True})

@app.route('/api/admin/skills/<int:skill_id>/toggle', methods=['PUT'])
def toggle_skill_status(skill_id):
    """Toggle skill active status"""
    data = request.json
    is_active = data.get('is_active')
    
    conn = create_connection()
    query = "UPDATE skills SET is_active = %s WHERE id = %s"
    execute_query(conn, query, (is_active, skill_id))
    conn.close()
    
    return jsonify({"success": True})

@app.route('/api/admin/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    """Delete a skill and its variations"""
    conn = create_connection()
    
    # CASCADE will automatically delete variations
    query = "DELETE FROM skills WHERE id = %s"
    execute_query(conn, query, (skill_id,))
    conn.close()
    
    return jsonify({"success": True})

# Role Profile Management APIs
@app.route('/api/admin/roles', methods=['GET'])
def get_roles():
    """Get all role profiles"""
    conn = create_connection()
    
    query = """
        SELECT id, role_name, description, is_active, created_at
        FROM role_profiles
        ORDER BY role_name
    """
    
    roles = fetch_query(conn, query)
    conn.close()
    
    return jsonify(roles)

@app.route('/api/admin/roles', methods=['POST'])
def add_role():
    """Add a new role profile"""
    data = request.json
    role_name = data.get('role_name')
    description = data.get('description', '')
    
    conn = create_connection()
    
    query = """
        INSERT INTO role_profiles (role_name, description, is_active)
        VALUES (%s, %s, 1)
    """
    execute_query(conn, query, (role_name, description))
    conn.close()
    
    return jsonify({"success": True}), 201

@app.route('/api/admin/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    """Update role profile"""
    data = request.json
    role_name = data.get('role_name')
    description = data.get('description', '')
    
    conn = create_connection()
    query = "UPDATE role_profiles SET role_name = %s, description = %s WHERE id = %s"
    execute_query(conn, query, (role_name, description, role_id))
    conn.close()
    
    return jsonify({"success": True})

@app.route('/api/admin/roles/<int:role_id>/toggle', methods=['PUT'])
def toggle_role_status(role_id):
    """Toggle role active status"""
    data = request.json
    is_active = data.get('is_active')
    
    conn = create_connection()
    query = "UPDATE role_profiles SET is_active = %s WHERE id = %s"
    execute_query(conn, query, (is_active, role_id))
    conn.close()
    
    return jsonify({"success": True})

@app.route('/api/admin/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """Delete a role profile"""
    conn = create_connection()
    
    # CASCADE will automatically delete role-skill mappings
    query = "DELETE FROM role_profiles WHERE id = %s"
    execute_query(conn, query, (role_id,))
    conn.close()
    
    return jsonify({"success": True})

# Role-Skill Mapping APIs
@app.route('/api/admin/roles/<int:role_id>/skills', methods=['GET'])
def get_role_skills(role_id):
    """Get all skills assigned to a role"""
    conn = create_connection()
    
    query = """
        SELECT rs.id, rs.skill_id, s.skill_name, sc.category_name as category
        FROM role_skills rs
        JOIN skills s ON rs.skill_id = s.id
        JOIN skill_categories sc ON s.category_id = sc.id
        WHERE rs.role_id = %s
        ORDER BY s.skill_name
    """
    
    skills = fetch_query(conn, query, (role_id,))
    conn.close()
    
    return jsonify(skills)

@app.route('/api/admin/role-skills', methods=['POST'])
def add_role_skill():
    """Add a skill to a role"""
    data = request.json
    role_id = data.get('role_id')
    skill_id = data.get('skill_id')
    
    conn = create_connection()
    
    query = """
        INSERT INTO role_skills (role_id, skill_id)
        VALUES (%s, %s)
    """
    execute_query(conn, query, (role_id, skill_id))
    conn.close()
    
    return jsonify({"success": True}), 201

@app.route('/api/admin/role-skills/<int:role_id>/<int:skill_id>', methods=['DELETE'])
def remove_role_skill(role_id, skill_id):
    """Remove a skill from a role"""
    conn = create_connection()
    
    query = "DELETE FROM role_skills WHERE role_id = %s AND skill_id = %s"
    execute_query(conn, query, (role_id, skill_id))
    conn.close()
    
    return jsonify({"success": True})

if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
