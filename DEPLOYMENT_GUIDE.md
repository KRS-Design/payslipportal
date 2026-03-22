# Deployment Guide for Online Payslip Portal

## Overview
This guide covers deployment options for the Online Payslip Portal on various hosting platforms.

## Table of Contents
1. [Local Development](#local-development)
2. [Vercel Deployment](#vercel-deployment)
3. [Render.com Deployment](#rendercom-deployment)
4. [Railway.app Deployment](#railwayapp-deployment)
5. [Docker & Self-Hosted](#docker--self-hosted)
6. [Troubleshooting](#troubleshooting)

---

## Local Development

### Quick Start
```bash
# 1. Extract the project
cd payslip-portal

# 2. Setup backend
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python init_db.py

# 5. Start backend
python app.py

# Backend runs at: http://localhost:5000

# ============= In another terminal =============

# 6. Serve frontend
cd frontend
python -m http.server 8000

# Frontend runs at: http://localhost:8000
```

### Test the Application
- Main Portal: http://localhost:8000
- Admin Panel: http://localhost:8000/admin.html
- API Health: http://localhost:5000/health

### Create Sample PDF (Optional)
```bash
cd backend
python create_sample_pdf.py
# Creates: sample_payslip.pdf
# Use this to test PDF upload in Admin Panel
```

---

## Vercel Deployment

### Setup with Vercel

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Payslip Portal"
   git remote add origin https://github.com/yourusername/payslip-portal.git
   git push -u origin main
   ```

2. **Sign up at Vercel**
   - Go to https://vercel.com
   - Sign up with GitHub
   - Click "Import Project"

3. **Import Repository**
   - Select your payslip-portal repository
   - Click Import

4. **Configure Project**
   - Framework: None (custom)
   - Root Directory: Leave blank
   - Build Command: Leave blank

5. **Add Environment Variables**
   - Click "Environment Variables"
   - Add:
     ```
     FLASK_ENV=production
     FLASK_DEBUG=False
     ```

6. **Configure Serverless Functions (Backend)**
   - Rename `backend/app.py` to `backend/index.py`:
     ```bash
     mv backend/app.py backend/index.py
     ```
   - Update imports if needed
   - Add `vercel.json` configuration (included in project)

7. **Deploy**
   - Click Deploy
   - Wait for deployment to complete
   - Your URL will be displayed

### Post-Deployment Configuration

```bash
# Update frontend API_BASE_URL
# In frontend/script.js, change:
const API_BASE_URL = 'http://localhost:5000';
# To:
const API_BASE_URL = 'https://your-project.vercel.app/api';
```

---

## Render.com Deployment

### Step 1: Prepare Repository
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Backend Service on Render

1. Go to https://render.com
2. Click "New +"
3. Select "Web Service"
4. Connect GitHub repository
5. Configure:
   - **Name**: `payslip-portal-backend`
   - **Environment**: `Docker`
   - **Build Command**: (leave blank - uses Dockerfile)
   - **Start Command**: (leave blank - uses Dockerfile)

### Step 3: Create Frontend Service on Render

1. Click "New +"
2. Select "Static Site"
3. Connect repository
4. Configure:
   - **Name**: `payslip-portal-frontend`
   - **Build Command**: (leave blank for static files)
   - **Publish directory**: `frontend`

### Step 4: Configure Environment Variables

For backend service:
- Go to Environment
- Add:
  ```
  FLASK_ENV=production
  FLASK_DEBUG=False
  ```

### Step 5: Update Frontend Configuration

After deployment, update frontend API URL:

```javascript
// frontend/script.js
const API_BASE_URL = 'https://payslip-portal-backend.onrender.com';
```

---

## Railway.app Deployment

### Prerequisites
- GitHub account
- Railway account (https://railway.app)

### Backend Deployment

1. **Create Service**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your payslip-portal repo

2. **Configure Service**
   - Service Name: `api`
   - Root Directory: `backend`
   - Start Command: `python app.py`

3. **Add Environment Variables**
   - Click on service
   - Go to Variables
   - Add:
     ```
     FLASK_ENV=production
     FLASK_DEBUG=False
     ```

4. **Deploy**
   - Railway auto-deploys from GitHub
   - Check deployment status in dashboard

### Frontend Deployment

1. **Create Static Service**
   - Click "New +" in project
   - Select "Empty Service"
   - Name: `web`

2. **Configure**
   - Set up to serve `frontend/` folder
   - Can use nginx or similar

3. **Update API URL**
   ```javascript
   const API_BASE_URL = 'https://your-railway-app.up.railway.app';
   ```

---

## Docker & Self-Hosted

### Using Docker Compose (Recommended)

```bash
# 1. Build images
docker-compose build

# 2. Start services
docker-compose up -d

# 3. Check logs
docker-compose logs -f

# 4. Access application
# Frontend: http://localhost
# Backend: http://localhost:5000
# API Health: http://localhost:5000/health
```

### Using Docker Commands

```bash
# Build backend image
docker build -t payslip-backend:latest ./backend

# Run backend
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=False \
  -v $(pwd)/backend/uploads:/app/uploads \
  -v $(pwd)/backend/database:/app/database \
  payslip-backend:latest

# Run frontend with nginx
docker run -p 80:80 \
  -v $(pwd)/frontend:/usr/share/nginx/html:ro \
  nginx:latest
```

### Self-Hosted on VPS (Ubuntu)

1. **Install Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip nginx
   ```

2. **Setup Application**
   ```bash
   git clone https://github.com/yourusername/payslip-portal.git
   cd payslip-portal/backend
   pip3 install -r requirements.txt
   python3 init_db.py
   ```

3. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/payslip-portal.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Payslip Portal Backend
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/home/user/payslip-portal/backend
   ExecStart=/usr/bin/python3 app.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

4. **Start Service**
   ```bash
   sudo systemctl enable payslip-portal
   sudo systemctl start payslip-portal
   sudo systemctl status payslip-portal
   ```

5. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/payslip-portal
   ```
   
   Add:
   ```nginx
   upstream payslip_backend {
       server 127.0.0.1:5000;
   }

   server {
       listen 80;
       server_name yourdomain.com;

       location /api {
           proxy_pass http://payslip_backend;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location / {
           root /home/user/payslip-portal/frontend;
           try_files $uri $uri/ /index.html;
       }
   }
   ```

6. **Enable and Start Nginx**
   ```bash
   sudo ln -s /etc/nginx/sites-available/payslip-portal /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renew
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Update Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Database Backup

### Backup SQLite Database

```bash
# Manual backup
cp backend/database/payslip.db backups/payslip_$(date +%Y%m%d_%H%M%S).db

# Automated backup (cron job)
# Add to crontab: crontab -e
0 2 * * * cp /path/to/payslip.db /path/to/backups/payslip_$(date +\%Y\%m\%d).db
```

---

## Performance Optimization

### Production Configuration

```python
# app.py - Production settings
app.config['JSON_SORT_KEYS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

# Add caching headers
@app.after_request
def add_header(response):
    if response.content_type.startswith("text/html"):
        response.cache_control.max_age = 0
    else:
        response.cache_control.max_age = 604800
    return response
```

### Enable Gzip Compression
```bash
# In Nginx configuration
gzip on;
gzip_types text/css text/javascript application/javascript;
gzip_min_length 1000;
```

---

## Monitoring & Logging

### Application Logs
```bash
# View logs (Systemd)
sudo journalctl -u payslip-portal -f

# View logs (Docker)
docker logs -f <container_id>
```

### Check Health
```bash
curl https://yourdomain.com/health
```

### Monitor Disk Space
```bash
df -h /
# Check uploads folder size
du -sh backend/uploads/
```

---

## Troubleshooting

### Issue: "Connection refused" when accessing backend

**Solution:**
```bash
# Check if backend is running
curl http://localhost:5000/health

# Check ports
netstat -an | grep 5000

# Restart service
sudo systemctl restart payslip-portal
```

### Issue: "PDF library not found"

**Solution:**
```bash
pip3 install PyMuPDF reportlab
# Restart application
```

### Issue: "Permission denied" on database

**Solution:**
```bash
sudo chown www-data:www-data backend/database/payslip.db
sudo chmod 644 backend/database/payslip.db
```

### Issue: CORS errors in browser

**Solution:** Update `API_BASE_URL` in `frontend/script.js` with correct backend URL

### Issue: 502 Bad Gateway

**Solution:**
```bash
# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Check if backend is running
sudo systemctl status payslip-portal

# Restart Nginx
sudo systemctl restart nginx
```

---

## Maintenance Checklist

- [ ] Weekly: Check application logs for errors
- [ ] Weekly: Verify database backups exist
- [ ] Monthly: Update dependencies
- [ ] Monthly: Review server resources (disk, CPU, memory)
- [ ] Quarterly: Review security settings
- [ ] Quarterly: Test backup restoration process
- [ ] Annually: Update SSL certificates (automated with Certbot)

---

## Support & Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app/)
- [Docker Docs](https://docs.docker.com/)
- [Nginx Docs](https://nginx.org/en/docs/)

---

**Powered by PAVI TECH**
