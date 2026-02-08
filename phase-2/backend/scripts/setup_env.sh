#!/bin/bash

# Script to set up the backend development environment
# This script automates the setup process described in the README

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Setting up Backend Development Framework..."

# Check if Python 3.11+ is available
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
MIN_VERSION="3.11"

if [[ $(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1) == "$MIN_VERSION" ]]; then
    echo "✅ Python version $PYTHON_VERSION is sufficient (need $MIN_VERSION or higher)"
else
    echo "❌ Python version $PYTHON_VERSION is too low (need $MIN_VERSION or higher)"
    exit 1
fi

# Check if virtual environment module is available
if python3 -m venv --help > /dev/null 2>&1; then
    echo "✅ Python venv module is available"
else
    echo "❌ Python venv module is not available"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔨 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Check if requirements files exist
if [ ! -f "backend/requirements/dev.txt" ]; then
    echo "❌ Requirements file backend/requirements/dev.txt not found"
    exit 1
fi

echo "📦 Installing dependencies from backend/requirements/dev.txt..."
pip install -r backend/requirements/dev.txt

# Check if .env file exists, if not create from .env.example
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📝 Copying .env.example to .env..."
        cp .env.example .env
        echo "ℹ️  Please update .env with your specific configuration"
    else
        echo "⚠️  Neither .env nor .env.example found"
    fi
else
    echo "✅ Environment file .env already exists"
fi

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✅ Docker is available"
else
    echo "⚠️  Docker is not available, some features may not work"
fi

# Check if Docker Compose is available
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose is available"
else
    echo "⚠️  Docker Compose is not available, some features may not work"
fi

# Check if alembic is available
if command -v alembic &> /dev/null; then
    echo "✅ Alembic is available"
else
    echo "⚠️  Alembic is not available, database migrations may not work"
fi

echo "✅ Backend Development Framework setup completed!"
echo ""
echo "💡 Next steps:"
echo "   1. Make sure your database is running"
echo "   2. Run 'alembic upgrade head' to initialize the database (if using alembic)"
echo "   3. Run 'uvicorn backend.src.api.main:app --reload' to start the server"
echo "   4. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "🔧 To activate the virtual environment in the future, run:"
echo "   source venv/bin/activate"