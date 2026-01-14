@echo off
REM Production startup script for AI Agent Toolbox Backend (Windows)

echo 🚀 Starting AI Agent Toolbox Backend (Production)
echo ==================================================

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Virtual environment not found!
    echo    Run: python -m venv venv
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo    Copying from .env.example...
    copy .env.example .env
    echo    Please update .env with your API keys
    exit /b 1
)

REM Install/update dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Run database migrations if needed
echo 🗄️  Setting up database...
python -c "from app.database.db import init_db; init_db()"

REM Start the server with Gunicorn (or uvicorn on Windows)
echo 🌐 Starting server...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
