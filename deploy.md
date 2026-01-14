# Deployment Guide - AI Agent Toolbox

## Production Deployment

### Prerequisites
- Python 3.8+
- Node.js 18+
- API Keys (Groq, Tavily, OpenWeather, etc.)

---

## Backend Deployment

### 1. Setup Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your API keys
# Set DEBUG=False for production
# Update ALLOWED_ORIGINS with your frontend domain
```

### 3. Initialize Database

```bash
python -c "from app.database.db import init_db; init_db()"
```

### 4. Start Production Server

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

**Manual Start:**
```bash
# Using Gunicorn (Linux/Mac)
gunicorn app.main:app -c gunicorn.conf.py

# Using Uvicorn (Windows or development)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Frontend Deployment

### 1. Setup Environment

```bash
cd frontend

# Install dependencies
npm install
```

### 2. Configure Environment Variables

```bash
# Copy example file
cp .env.example .env.production

# Edit .env.production
# Set VITE_API_URL to your backend URL
```

### 3. Build for Production

```bash
npm run build:prod
```

This creates optimized files in the `dist/` folder.

### 4. Serve Production Build

**Option A: Using Vite Preview**
```bash
npm run serve
```

**Option B: Using a Static Server**
```bash
npm install -g serve
serve -s dist -p 4173
```

**Option C: Using Nginx**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    root /path/to/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## Platform-Specific Deployment

### Deploy to VPS (DigitalOcean, AWS EC2, etc.)

1. **SSH into your server**
```bash
ssh user@your-server-ip
```

2. **Clone repository**
```bash
git clone https://github.com/yourusername/ai-agent-toolbox.git
cd ai-agent-toolbox
```

3. **Setup Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
nano .env
```

4. **Setup Frontend**
```bash
cd ../frontend
npm install
cp .env.example .env.production
# Edit .env.production
nano .env.production
npm run build:prod
```

5. **Setup Process Manager (PM2)**
```bash
# Install PM2
npm install -g pm2

# Start backend
cd ../backend
pm2 start "gunicorn app.main:app -c gunicorn.conf.py" --name ai-agent-backend

# Start frontend (if serving with Node)
cd ../frontend
pm2 start "npm run serve" --name ai-agent-frontend

# Save PM2 configuration
pm2 save
pm2 startup
```

### Deploy to Heroku

**Backend:**
```bash
cd backend

# Create Procfile
echo "web: gunicorn app.main:app -c gunicorn.conf.py" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
heroku create your-app-name-backend
heroku config:set GROQ_API_KEY=your_key
heroku config:set TAVILY_API_KEY=your_key
# ... set other env vars
git push heroku main
```

**Frontend:**
```bash
cd frontend

# Build
npm run build:prod

# Deploy to Netlify/Vercel
# Or use Heroku with static buildpack
heroku create your-app-name-frontend
heroku buildpacks:set heroku/nodejs
# Add static.json for routing
echo '{"root": "dist/", "routes": {"/**": "index.html"}}' > static.json
git push heroku main
```

### Deploy to Vercel (Frontend)

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod

# Set environment variables in Vercel dashboard
# VITE_API_URL=https://your-backend-url.com
```

### Deploy to Railway

1. Connect your GitHub repository
2. Create two services: backend and frontend
3. Configure environment variables in Railway dashboard
4. Railway will auto-deploy on git push

---

## Environment Variables Reference

### Backend (.env)
```
APP_NAME=AI Agent Toolbox
APP_VERSION=1.0.0
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
GROQ_API_KEY=your_key
GROQ_MODEL=llama-3.3-70b-versatile
TAVILY_API_KEY=your_key
SERPAPI_API_KEY=your_key
OPENWEATHER_API_KEY=your_key
FIXER_API_KEY=your_key
DATABASE_URL=sqlite:///./agent_data.db
MAX_ITERATIONS=10
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=2000
PORT=8000
HOST=0.0.0.0
WORKERS=4
```

### Frontend (.env.production)
```
VITE_API_URL=https://your-backend-url.com
VITE_APP_NAME=AI Agent Toolbox
VITE_APP_VERSION=1.0.0
```

---

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong API keys
- [ ] Configure CORS properly (ALLOWED_ORIGINS)
- [ ] Use HTTPS in production
- [ ] Keep dependencies updated
- [ ] Don't commit .env files
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting if needed
- [ ] Set up monitoring and logging
- [ ] Regular security audits

---

## Monitoring & Maintenance

### Check Backend Health
```bash
curl https://your-backend-url.com/system/health
```

### View Logs (PM2)
```bash
pm2 logs ai-agent-backend
pm2 logs ai-agent-frontend
```

### Update Application
```bash
git pull origin main
cd backend && pip install -r requirements.txt
cd ../frontend && npm install && npm run build:prod
pm2 restart all
```

---

## Troubleshooting

### Backend won't start
- Check if all API keys are set in .env
- Verify Python version (3.8+)
- Check if port 8000 is available
- Review logs for errors

### Frontend can't connect to backend
- Verify VITE_API_URL is correct
- Check CORS settings in backend
- Ensure backend is running
- Check network/firewall rules

### Database errors
- Ensure database file has write permissions
- Run database initialization
- Check DATABASE_URL in .env

---

## Performance Optimization

1. **Backend:**
   - Adjust WORKERS based on CPU cores
   - Enable response caching if needed
   - Use connection pooling for database
   - Monitor memory usage

2. **Frontend:**
   - Enable gzip compression
   - Use CDN for static assets
   - Implement lazy loading
   - Optimize images

---

## Support

For issues or questions:
- Check logs first
- Review environment variables
- Test API endpoints manually
- Check API key validity
