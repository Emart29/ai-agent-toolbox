# 🚀 Quick Start Guide

Get the AI Agent Toolbox running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 18+ installed
- API keys ready (see below)

## Step 1: Get API Keys (Free Tier Available)

1. **Groq** (Required) - https://console.groq.com/keys
   - Sign up for free
   - Create API key
   
2. **Tavily** (Required) - https://tavily.com/
   - Free tier: 1000 searches/month
   
3. **OpenWeather** (Optional) - https://openweathermap.org/api
   - Free tier: 1000 calls/day
   
4. **Fixer.io** (Optional) - https://fixer.io/
   - Free tier: 100 requests/month
   
5. **SerpAPI** (Optional) - https://serpapi.com/
   - Free tier: 100 searches/month

## Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Edit .env and add your API keys
# Windows: notepad .env
# Mac/Linux: nano .env

# Initialize database
python -c "from app.database.db import init_db; init_db()"

# Start backend
uvicorn app.main:app --reload
```

Backend running at: http://localhost:8000

## Step 3: Frontend Setup (2 minutes)

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Setup environment (optional - defaults work)
cp .env.example .env

# Start frontend
npm run dev
```

Frontend running at: http://localhost:5173

## Step 4: Test It! (1 minute)

1. Open http://localhost:5173 in your browser
2. Try these queries:
   - "What's 25 * 48?"
   - "What's the weather in London?"
   - "Search for latest AI news"
   - "Save a note: Buy groceries tomorrow"

## Troubleshooting

### Backend won't start
- Check if Python 3.8+ is installed: `python --version`
- Make sure virtual environment is activated
- Verify API keys in .env file

### Frontend won't start
- Check if Node.js is installed: `node --version`
- Delete node_modules and run `npm install` again
- Check if port 5173 is available

### Can't connect to backend
- Ensure backend is running on port 8000
- Check VITE_API_URL in frontend/.env
- Look for CORS errors in browser console

### Agent not responding
- Verify GROQ_API_KEY is set correctly
- Check backend logs for errors
- Ensure you have internet connection

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [deploy.md](deploy.md) for production deployment
- Visit http://localhost:8000/docs for API documentation

## Need Help?

- Check backend logs in terminal
- Check browser console for frontend errors
- Verify all API keys are valid
- Make sure both servers are running

---

Enjoy using AI Agent Toolbox! 🤖
