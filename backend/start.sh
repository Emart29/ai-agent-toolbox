#!/bin/bash

# Production startup script for AI Agent Toolbox Backend

echo "🚀 Starting AI Agent Toolbox Backend (Production)"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "   Copying from .env.example..."
    cp .env.example .env
    echo "   Please update .env with your API keys"
    exit 1
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations if needed
echo "🗄️  Setting up database..."
python -c "from app.database.db import init_db; init_db()"

# Start the server with Gunicorn
echo "🌐 Starting server..."
gunicorn app.main:app -c gunicorn.conf.py
