"""
Database helper functions for loading skills, variations, and role profiles
This allows dynamic configuration without modifying code
"""

from app.database import create_connection, fetch_query

_skills_cache = None
_variations_cache = None
_roles_cache = None

def clear_cache():
    """Clear all cached data - call this when data is updated via admin panel"""
    global _skills_cache, _variations_cache, _roles_cache
    _skills_cache = None
    _variations_cache = None
    _roles_cache = None

def get_all_skills():
    """Get all active skills from database"""
    global _skills_cache
    
    if _skills_cache is not None:
        return _skills_cache
    
    conn = create_connection()
    query = """
        SELECT s.skill_name, sc.category_name as category
        FROM skills s
        JOIN skill_categories sc ON s.category_id = sc.id
        WHERE s.is_active = 1 AND sc.is_active = 1
        ORDER BY s.skill_name
    """
    
    skills = fetch_query(conn, query)
    conn.close()
    
    # Convert to list of skill names
    _skills_cache = [skill['skill_name'].lower() for skill in skills]
    return _skills_cache

def get_skill_variations():
    """Get all skill variations as a dictionary"""
    global _variations_cache
    
    if _variations_cache is not None:
        return _variations_cache
    
    conn = create_connection()
    query = """
        SELECT s.skill_name, GROUP_CONCAT(sv.variation_name SEPARATOR '|||') as variations
        FROM skills s
        LEFT JOIN skill_variations sv ON s.id = sv.skill_id AND sv.is_active = 1
        WHERE s.is_active = 1
        GROUP BY s.id, s.skill_name
        HAVING variations IS NOT NULL
    """
    
    results = fetch_query(conn, query)
    conn.close()
    
    # Build variations dictionary
    _variations_cache = {}
    for row in results:
        canonical = row['skill_name'].lower()
        variations = row['variations'].split('|||')
        _variations_cache[canonical] = [v.lower() for v in variations]
    
    return _variations_cache

def get_role_profiles():
    """Get all role profiles with their associated skills"""
    global _roles_cache
    
    if _roles_cache is not None:
        return _roles_cache
    
    conn = create_connection()
    query = """
        SELECT rp.id, rp.role_name, rp.description,
               GROUP_CONCAT(s.skill_name SEPARATOR '|||') as skills
        FROM role_profiles rp
        LEFT JOIN role_skills rs ON rp.id = rs.role_id
        LEFT JOIN skills s ON rs.skill_id = s.id AND s.is_active = 1
        WHERE rp.is_active = 1
        GROUP BY rp.id, rp.role_name, rp.description
        ORDER BY rp.role_name
    """
    
    results = fetch_query(conn, query)
    conn.close()
    
    # Build role profiles dictionary
    _roles_cache = {}
    for row in results:
        role_name = row['role_name']
        if row['skills']:
            skills = row['skills'].split('|||')
            _roles_cache[role_name] = skills
        else:
            _roles_cache[role_name] = []
    
    return _roles_cache

def get_skills_by_category():
    """Get skills organized by category"""
    conn = create_connection()
    query = """
        SELECT sc.category_name as category, GROUP_CONCAT(s.skill_name SEPARATOR '|||') as skills
        FROM skills s
        JOIN skill_categories sc ON s.category_id = sc.id
        WHERE s.is_active = 1 AND sc.is_active = 1
        GROUP BY sc.category_name, sc.display_order
        ORDER BY sc.display_order, sc.category_name
    """
    
    results = fetch_query(conn, query)
    conn.close()
    
    categories = {}
    for row in results:
        category = row['category']
        if row['skills']:
            skills = row['skills'].split('|||')
            categories[category] = [s.lower() for s in skills]
    
    return categories

# Fallback data in case database is empty or not yet populated
FALLBACK_SKILLS = [
    'python', 'java', 'javascript', 'typescript', 'c#', 'c++', 'go', 'ruby', 'php',
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server',
    'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node.js',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd',
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'nlp', 'ai',
    'chromadb', 'pinecone', 'vector store', 'embeddings', 'rag'
]

FALLBACK_VARIATIONS = {
    'javascript': ['js', 'node.js', 'nodejs'],
    'typescript': ['ts'],
    'python': ['py'],
    'postgresql': ['postgres', 'psql'],
    'mongodb': ['mongo'],
    'kubernetes': ['k8s'],
    'power bi': ['powerbi', 'pbi'],
    'chromadb': ['chroma', 'chroma db']
}

FALLBACK_ROLES = {
    "Full Stack Developer": ["React", "Angular", "Vue", "Node.js", "JavaScript", "Python", "Java"],
    "Backend Developer": ["Python", "Java", "Node.js", "C#", ".NET", "Go", "API", "REST"],
    "AI/ML Engineer": ["Machine Learning", "Deep Learning", "AI", "TensorFlow", "PyTorch", "NLP"]
}

def get_skills_with_fallback():
    """Get skills from database, or use fallback if empty"""
    try:
        skills = get_all_skills()
        if not skills:
            return FALLBACK_SKILLS
        return skills
    except Exception as e:
        print(f"Error loading skills from database: {e}")
        return FALLBACK_SKILLS

def get_variations_with_fallback():
    """Get variations from database, or use fallback if empty"""
    try:
        variations = get_skill_variations()
        if not variations:
            return FALLBACK_VARIATIONS
        return variations
    except Exception as e:
        print(f"Error loading variations from database: {e}")
        return FALLBACK_VARIATIONS

def get_roles_with_fallback():
    """Get role profiles from database, or use fallback if empty"""
    try:
        roles = get_role_profiles()
        if not roles:
            return FALLBACK_ROLES
        return roles
    except Exception as e:
        print(f"Error loading roles from database: {e}")
        return FALLBACK_ROLES
