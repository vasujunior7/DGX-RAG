#!/bin/bash

# HackRX Platform Startup Script
echo "🚀 HackRX Platform Startup Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the DGX-RAG directory."
    exit 1
fi

# Check for virtual environment
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
fi

# Kill any existing processes on ports 8000 and 3000
echo "🧹 Cleaning up any existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Wait a moment for ports to be freed
sleep 2

# Check if Frontend/index.html exists
if [ ! -f "Frontend/index.html" ]; then
    echo "❌ Error: Frontend/index.html not found!"
    exit 1
fi

echo "✅ All checks passed. Starting HackRX Platform..."
echo ""

# Start the main application
python main.py 