# Quick Start Guide

## Fast Setup (3 Steps)

### Step 1: Configure Environment
```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env and set your MySQL password
notepad .env
```

### Step 2: Install Dependencies
```powershell
# Activate virtual environment (already created)
.\venv\Scripts\Activate.ps1

# Install packages (if not already installed)
.\venv\Scripts\pip.exe install -r requirements.txt

# Download spaCy model
.\venv\Scripts\pip.exe install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl

# Upgrade sentence-transformers for compatibility
.\venv\Scripts\pip.exe install --upgrade sentence-transformers
```

### Step 3: Setup Database and Run
```powershell
# Make sure MySQL is running
net start MySQL

# Initialize database
.\venv\Scripts\python.exe -c "from app.database import create_connection; import mysql.connector; conn = mysql.connector.connect(host='localhost', user='root', password='your_password'); cursor = conn.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS resume_filter_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'); conn.close(); print('Database created')"

# Run database schema
Get-Content database_schema.sql | mysql -u root -p resume_filter_db

# Convert tables to InnoDB (required for foreign keys!)
.\venv\Scripts\python.exe convert_to_innodb.py

# Apply CASCADE DELETE constraints
.\venv\Scripts\python.exe force_cascade_fix.py

# Setup Admin Configuration System (Optional but Recommended)
Get-Content database_admin_tables.sql | mysql -u root -p resume_filter_db
Get-Content insert_hardcoded_data.sql | mysql -u root -p resume_filter_db

# Start the application
.\venv\Scripts\python.exe app.py
```

Open browser: **http://localhost:5000**

## Default Credentials

- **Database**: resume_filter_db
- **Host**: localhost
- **Port**: 5000

## Important Notes

⚠️ **Make sure MySQL is running** before setting up the database:
```powershell
net start MySQL
```

💡 **All commands use the virtual environment** (.\venv\Scripts\python.exe)

## First Use

1. Make sure Flask is running (you'll see "Running on http://127.0.0.1:5000")
2. Open browser and go to http://localhost:5000
3. Click **"Create Job"** in the navigation
4. Enter a job title and paste the full job description
5. Click **"Upload Resumes"** and select the job from dropdown
6. Upload one or more resume PDF/DOCX files
7. View ranked candidates with AI analysis!

## Key Features to Try

- **Dashboard**: View statistics, recent analyses, and bulk candidate profile cards
- **Create Job**: Add new job descriptions
- **Upload Resumes**: Process resumes for a specific job
- **Bulk Upload** 🆕: Upload resumes without job descriptions
  - AI automatically profiles candidates for best-fit roles
  - **Collapsible accordion view**: Expand/collapse candidate details
  - **Expand All / Collapse All buttons**: Bulk control for all candidates
  - Expandable skills badges (click "+X more")
  - View on dedicated Bulk Analysis page or dashboard cards
- **Admin Configuration** 🆕: Manage skills, categories, and roles
  - Access: http://localhost:5000/admin/config
  - Add/edit categories with emoji icon dropdown
  - Manage 200+ skills with variations
  - Configure role profiles and skill mappings
  - Category filtering with dual search
  - Compact one-line listings
  - Changes take effect immediately
- **AI Chatbot (RAG)** 🆕: Ask natural language questions like:
  - "Who is good fit for database roles?"
  - "Find DevOps candidates"
  - "Show me data scientists with 5+ years"
  - Features: Role-based intelligence, AI semantic search, View Profile button with smart back navigation, chat history, markdown formatting, resume count display
- **All Candidates**: See all uploaded resumes across jobs
- **All Jobs**: Manage job postings and view statistics
- **Agent Monitoring**: View multi-agent system execution logs
- **Delete Options**: Remove jobs or candidates (with CASCADE delete of related data)

## Admin Configuration Quick Reference

**Access Admin Panel**: http://localhost:5000/admin/config

**Categories Tab:**
- Add categories with 12 emoji icon options (💻🎨📊🔧🌐📱☁️🗄️🤖🔒📝⚙️)
- Set colors with color picker
- Edit/toggle/delete existing categories

**Skills Tab:**
- Add skills with category selection
- Add variations (comma-separated): js, javascript, JS
- Filter by category dropdown
- Search by skill name
- Dual filtering (both work together)

**Roles Tab:**
- Add/edit role profiles
- Toggle active/inactive status
- Manage 12 pre-configured roles

**Role-Skill Mapping Tab:**
- Select role from dropdown
- Filter skills by category
- Search for specific skills
- Check boxes to map skills to role
- Filters persist after mapping

**Documentation:**
- `ADMIN_SYSTEM_SUMMARY.md` - Complete overview
- `EDIT_FUNCTIONALITY_GUIDE.md` - Edit features and bug fixes
- `insert_hardcoded_data.sql` - Data population script (safe to re-run)

---

Need help? See **README.md** for detailed instructions.
