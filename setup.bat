@echo off
REM Complete setup script for AI Agent Toolbox (Windows)

echo ========================================
echo 🤖 AI Agent Toolbox - Complete Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    exit /b 1
)
echo ✅ Python found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found! Please install Node.js 18+
    exit /b 1
)
echo ✅ Node.js found
echo.

REM Backend Setup
echo ========================================
echo 📦 Setting up Backend...
echo ========================================
cd backend

if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit backend\.env and add your API keys!
    echo.
)

echo Initializing database...
python -c "from app.database.db import init_db; init_db()"

cd ..
echo ✅ Backend setup complete!
echo.

REM Frontend Setup
echo ========================================
echo 📦 Setting up Frontend...
echo ========================================
cd frontend

echo Installing Node dependencies...
call npm install

if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

cd ..
echo ✅ Frontend setup complete!
echo.

echo ========================================
echo 🎉 Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\.env and add your API keys
echo 2. Start backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload
echo 3. Start frontend: cd frontend ^&^& npm run dev
echo 4. Open http://localhost:5173
echo.
echo For production deployment, see deploy.md
echo ========================================

pause
