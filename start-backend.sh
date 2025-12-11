#!/bin/bash
# Script to start the RAG chatbot backend

echo "Starting RAG Chatbot Backend..."

# Navigate to the backend directory
cd backend

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies (in case they're not installed)
pip install -r requirements.txt

# Start the FastAPI server
echo "Starting FastAPI server on port 8000..."
uvicorn main:app --reload --port 8000