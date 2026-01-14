#!/bin/bash

# Complete setup script for AI Agent Toolbox (Linux/Mac)

echo "========================================"
echo "🤖 AI Agent Toolbox - Complete Setup"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found! Please install Python 3.8+"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found! Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"
echo ""

# Backend Setup
echo "========================================"
echo "📦 Setting up Backend..."
echo "========================================"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env and add your API keys!"
    echo ""
fi

echo "Initializing database..."
python -c "from app.database.db import init_db; init_db()"

cd ..
echo "✅ Backend setup complete!"
echo ""

# Frontend Setup
echo "========================================"
echo "📦 Setting up Frontend..."
echo "========================================"
cd frontend

echo "Installing Node dependencies..."
npm install

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

cd ..
echo "✅ Frontend setup complete!"
echo ""

# Make scripts executable
chmod +x backend/start.sh
chmod +x backend/healthcheck.py
chmod +x setup.sh

echo "========================================"
echo "🎉 Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your API keys"
echo "2. Start backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "3. Start frontend: cd frontend && npm run dev"
echo "4. Open http://localhost:5173"
echo ""
echo "For production deployment, see deploy.md"
echo "========================================"
