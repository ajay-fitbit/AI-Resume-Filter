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
    
    conn.close()
    return render_template('index.html', stats=stats, recent_analyses=recent_analyses)

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
                         '',  # projects
                         '',  # certifications
                         '',  # job_titles
                         '')  # raw_text (stored in state but not needed here)
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
                   (SELECT COUNT(*) FROM red_flags rf WHERE rf.candidate_id = c.id AND rf.severity = 'High') as high_flags
            FROM candidates c
            JOIN analysis_results ar ON c.id = ar.candidate_id
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
                   (SELECT COUNT(*) FROM red_flags rf WHERE rf.candidate_id = c.id AND rf.severity = 'High') as high_flags
            FROM candidates c
            LEFT JOIN analysis_results ar ON c.id = ar.candidate_id
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
        return render_template('rag_chat.html', jobs=[])
    
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
    
    conn.close()
    return render_template('rag_chat.html', jobs=jobs)

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

if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
