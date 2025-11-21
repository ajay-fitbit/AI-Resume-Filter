# Production Deployment Guide

## ⚠️ Current Status: Development Mode

The application is currently configured for **development only**. Before deploying to production, you **MUST** make the following changes.

---

## 🚀 Production Readiness Checklist

### ✅ Critical Security Changes (REQUIRED)

#### 1. **Disable Debug Mode**
**File**: `app.py`

**Current (Development)**:
```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
```

**Change to (Production)**:
```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

**Why**: Debug mode exposes sensitive information and allows code execution through the browser.

---

#### 2. **Use Production WSGI Server**
**Do NOT use Flask's built-in server in production!**

**Install Gunicorn** (Linux/Mac) or **Waitress** (Windows):
```bash
# For Linux/Mac
pip install gunicorn

# For Windows
pip install waitress
```

**Run with Gunicorn** (Linux/Mac):
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

**Run with Waitress** (Windows):
```python
# Create production_server.py
from waitress import serve
from app import app

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, threads=4)
```

Run:
```bash
python production_server.py
```

---

#### 3. **Secure Environment Variables**
**File**: `.env`

**Required Changes**:
```env
# Generate strong random secret key (DON'T use default!)
FLASK_SECRET_KEY=<use output from: python -c "import secrets; print(secrets.token_hex(32))">

# Change to production
FLASK_ENV=production

# Use strong MySQL password
DB_PASSWORD=<strong_password_here>

# Create dedicated database user (not root!)
DB_USER=resume_app_prod
```

**Generate Secret Key**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

#### 4. **Database Security**

**Create Production Database User**:
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create production user with limited privileges
CREATE USER 'resume_app_prod'@'localhost' IDENTIFIED BY 'your_strong_password_here';
GRANT SELECT, INSERT, UPDATE, DELETE ON resume_filter_db.* TO 'resume_app_prod'@'localhost';
FLUSH PRIVILEGES;

-- DO NOT use root user in production!
```

**Enable SSL for MySQL** (if database on separate server):
```env
DB_SSL_ENABLED=true
DB_SSL_CA=/path/to/ca-cert.pem
```

---

#### 5. **File Upload Security**

**Add to `app.py`**:
```python
import os
from werkzeug.utils import secure_filename

# File upload configuration
UPLOAD_FOLDER = '/var/www/ai-resume-filter/uploads'  # Use absolute path
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# In your upload route, always use:
filename = secure_filename(file.filename)
```

**Set Proper Permissions**:
```bash
# Linux/Mac
chmod 755 /var/www/ai-resume-filter/uploads
chown www-data:www-data /var/www/ai-resume-filter/uploads

# Windows (PowerShell as Admin)
icacls "C:\inetpub\ai-resume-filter\uploads" /grant "IIS_IUSRS:(OI)(CI)F"
```

---

#### 6. **Enable HTTPS (SSL/TLS)**

**Option A: Nginx Reverse Proxy** (Recommended)
```nginx
# /etc/nginx/sites-available/ai-resume-filter
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    location /static {
        alias /var/www/ai-resume-filter/app/static;
        expires 30d;
    }
}
```

**Get Free SSL Certificate** (Let's Encrypt):
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

**Option B: Apache Reverse Proxy**
```apache
# /etc/apache2/sites-available/ai-resume-filter.conf
<VirtualHost *:80>
    ServerName your-domain.com
    Redirect permanent / https://your-domain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName your-domain.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/your-domain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/your-domain.com/privkey.pem

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/

    <Directory "/var/www/ai-resume-filter">
        Require all granted
    </Directory>
</VirtualHost>
```

---

#### 7. **Input Validation & Sanitization**

**Add validation to all routes**:
```python
from flask import request, abort
import re

@app.route('/api/rag/query', methods=['POST'])
def rag_query():
    data = request.get_json()
    
    # Validate input
    if not data or 'question' not in data:
        abort(400, 'Missing question parameter')
    
    question = data['question'].strip()
    
    # Length validation
    if len(question) > 500:
        abort(400, 'Question too long (max 500 characters)')
    
    if len(question) < 3:
        abort(400, 'Question too short (min 3 characters)')
    
    # Sanitize input (remove potentially dangerous characters)
    question = re.sub(r'[<>{}]', '', question)
    
    # Continue with processing...
```

---

#### 8. **Rate Limiting**

**Install Flask-Limiter**:
```bash
pip install Flask-Limiter
```

**Add to `app.py`**:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Apply to specific routes
@app.route('/api/rag/query', methods=['POST'])
@limiter.limit("30 per minute")
def rag_query():
    # Your code here
    pass

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per hour")
def upload():
    # Your code here
    pass
```

---

#### 9. **Logging & Monitoring**

**Add Production Logging**:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    # Create logs directory
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # File handler
    file_handler = RotatingFileHandler(
        'logs/ai_resume_filter.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('AI Resume Filter startup')
```

**Monitor with External Tools**:
- **Sentry**: Error tracking and monitoring
- **New Relic**: Application performance monitoring
- **Prometheus + Grafana**: Metrics and dashboards

---

#### 10. **Database Connection Pooling**

**Update `app/database.py`**:
```python
import mysql.connector
from mysql.connector import pooling

# Create connection pool (reuse connections)
connection_pool = pooling.MySQLConnectionPool(
    pool_name="resume_pool",
    pool_size=10,  # Adjust based on traffic
    pool_reset_session=True,
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

def get_db_connection():
    return connection_pool.get_connection()
```

---

### 📦 Deployment Options

#### Option 1: Linux Server (Ubuntu/Debian)

**Step-by-Step**:
```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install python3.10 python3-pip python3-venv mysql-server nginx -y

# 3. Create application directory
sudo mkdir -p /var/www/ai-resume-filter
sudo chown $USER:$USER /var/www/ai-resume-filter

# 4. Upload application files
scp -r "AI Resume Filter/*" user@server:/var/www/ai-resume-filter/

# 5. Create virtual environment
cd /var/www/ai-resume-filter
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt
pip install gunicorn
python -m spacy download en_core_web_sm

# 7. Configure MySQL
sudo mysql_secure_installation
sudo mysql -e "CREATE DATABASE resume_filter_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql resume_filter_db < database_schema.sql

# 8. Setup environment
cp .env.example .env
nano .env  # Edit with production values

# 9. Setup Nginx (see above config)
sudo nano /etc/nginx/sites-available/ai-resume-filter
sudo ln -s /etc/nginx/sites-available/ai-resume-filter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 10. Create systemd service
sudo nano /etc/systemd/system/ai-resume-filter.service
```

**Systemd Service File**:
```ini
[Unit]
Description=AI Resume Filter Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-resume-filter
Environment="PATH=/var/www/ai-resume-filter/venv/bin"
ExecStart=/var/www/ai-resume-filter/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 --timeout 120 app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Start Service**:
```bash
sudo systemctl daemon-reload
sudo systemctl start ai-resume-filter
sudo systemctl enable ai-resume-filter
sudo systemctl status ai-resume-filter
```

---

#### Option 2: Docker Deployment

**Create `Dockerfile`**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn && \
    python -m spacy download en_core_web_sm

# Copy application files
COPY . .

# Create uploads directory
RUN mkdir -p uploads logs && \
    chmod 755 uploads logs

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
```

**Create `docker-compose.yml`**:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_USER=resume_app
      - DB_PASSWORD=secure_password
      - DB_NAME=resume_filter_db
      - FLASK_SECRET_KEY=your_secret_key
      - FLASK_ENV=production
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    depends_on:
      - db
    restart: always

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=resume_filter_db
      - MYSQL_USER=resume_app
      - MYSQL_PASSWORD=secure_password
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database_schema.sql:/docker-entrypoint-initdb.d/schema.sql
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: always

volumes:
  mysql_data:
```

**Deploy**:
```bash
# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f web

# Stop
docker-compose down
```

---

#### Option 3: Cloud Platforms

##### **AWS Elastic Beanstalk**
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.10 ai-resume-filter --region us-east-1

# Create environment
eb create production-env --database.engine mysql --database.username admin

# Deploy
eb deploy

# Open in browser
eb open
```

##### **Google Cloud Run**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/your-project/ai-resume-filter
gcloud run deploy ai-resume-filter \
  --image gcr.io/your-project/ai-resume-filter \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 120
```

##### **Azure App Service**
```bash
# Create resource group
az group create --name ResumeFilterRG --location eastus

# Create App Service plan
az appservice plan create --name ResumeFilterPlan --resource-group ResumeFilterRG --sku B1 --is-linux

# Create web app
az webapp create --resource-group ResumeFilterRG --plan ResumeFilterPlan --name ai-resume-filter --runtime "PYTHON:3.10"

# Deploy from Git
az webapp deployment source config --name ai-resume-filter --resource-group ResumeFilterRG --repo-url https://github.com/your-repo --branch main
```

---

### 🔧 Performance Optimizations

#### 1. **Cache AI Model Loading**
Model already lazy-loads, but consider:
```python
# Preload model at startup
@app.before_first_request
def preload_models():
    semantic_agent._load_model()
    rag_agent._load_model()
    app.logger.info("AI models preloaded")
```

#### 2. **Database Indexing**
```sql
-- Add indexes for faster queries
CREATE INDEX idx_candidate_name ON candidates(name);
CREATE INDEX idx_resume_skills ON resume_data(skills(255));
CREATE INDEX idx_analysis_score ON analysis_results(match_score DESC);
CREATE INDEX idx_job_title ON jobs(title);
```

#### 3. **Static File Caching**
```python
# Add cache headers
@app.after_request
def add_cache_headers(response):
    if request.path.startswith('/static/'):
        response.cache_control.max_age = 2592000  # 30 days
    return response
```

#### 4. **Gzip Compression**
```python
from flask_compress import Compress

compress = Compress()
compress.init_app(app)
```

---

### 🔐 Security Headers

**Add to `app.py`**:
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    return response
```

---

### 📊 Backup Strategy

**Automated MySQL Backups**:
```bash
#!/bin/bash
# backup.sh - Run daily via cron

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/resume_filter"
mkdir -p $BACKUP_DIR

# Database backup
mysqldump -u backup_user -p$BACKUP_PASSWORD resume_filter_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Uploads backup
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /var/www/ai-resume-filter/uploads

# Delete backups older than 30 days
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

**Cron Job**:
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup.sh >> /var/log/backup.log 2>&1
```

---

### 🧪 Pre-Deployment Testing

**Checklist**:
```bash
# 1. Test database connection
python -c "from app.database import get_db_connection; print(get_db_connection())"

# 2. Test AI model loading
python -c "from app.agents.semantic_agent import SemanticMatchingAgent; agent = SemanticMatchingAgent(); agent._load_model(); print('Model loaded')"

# 3. Run with production settings
FLASK_ENV=production python app.py

# 4. Test uploads
curl -X POST -F "file=@test_resume.pdf" http://localhost:5000/upload

# 5. Test RAG queries
curl -X POST -H "Content-Type: application/json" -d '{"question":"Find Python developers"}' http://localhost:5000/api/rag/query

# 6. Load testing
pip install locust
locust -f load_test.py --host=http://localhost:5000
```

---

### 📝 Production Checklist

- [ ] Debug mode disabled (`debug=False`)
- [ ] Using production WSGI server (Gunicorn/Waitress)
- [ ] Strong `FLASK_SECRET_KEY` generated
- [ ] Database user is NOT root
- [ ] HTTPS/SSL configured
- [ ] File upload validation enabled
- [ ] Rate limiting implemented
- [ ] Logging configured
- [ ] Security headers added
- [ ] Database connection pooling enabled
- [ ] Backups automated
- [ ] Monitoring setup (optional but recommended)
- [ ] Error tracking configured (optional)
- [ ] Domain name configured
- [ ] Firewall rules set (only 80, 443, 22 open)
- [ ] `.env` file secured (not in Git)
- [ ] Tested with production settings

---

## 💰 Estimated Costs

### **Self-Hosted (VPS)**
- **DigitalOcean/Linode**: $12-24/month (2GB RAM, 2 vCPU)
- **AWS Lightsail**: $10-20/month
- **Hetzner**: €5-10/month

### **Cloud Platforms**
- **AWS Elastic Beanstalk**: ~$30-50/month
- **Google Cloud Run**: Pay-per-use (~$10-30/month for light traffic)
- **Azure App Service**: ~$50-100/month

### **Additional Costs**
- Domain name: ~$10-15/year
- SSL certificate: Free (Let's Encrypt) or $50-200/year (commercial)
- Monitoring tools: Free (basic) to $50-200/month (advanced)

---

## 🚨 Important Notes

1. **No API Costs**: AI models run locally (no OpenAI/AWS charges)
2. **Model Size**: ~80MB SentenceTransformer downloads once
3. **RAM Requirements**: Minimum 2GB (4GB recommended)
4. **Storage**: Estimate 100MB per 100 resumes + database
5. **Concurrent Users**: Adjust Gunicorn workers (`-w 4`) based on traffic

---

## 📞 Support & Maintenance

**Regular Tasks**:
- Weekly: Check logs for errors
- Monthly: Database backup verification
- Quarterly: Security updates (`pip list --outdated`)
- Yearly: SSL certificate renewal (automatic with Let's Encrypt)

**Monitoring Alerts**:
- Disk space < 20%
- CPU usage > 80%
- Database connection failures
- Application crashes

---

## ✅ Ready for Production!

Once you've completed the checklist above, your AI Resume Filter will be production-ready with:
- ✅ Enterprise-grade security
- ✅ Scalable architecture
- ✅ Automated backups
- ✅ Performance optimization
- ✅ Monitoring & logging
- ✅ HTTPS encryption
- ✅ Rate limiting
- ✅ Error handling

**Need help?** Review individual sections above for detailed instructions.
