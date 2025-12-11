@echo off
echo Starting RAG Chatbot Backend...

REM Navigate to the backend directory
cd backend

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies (in case they're not installed)
pip install -r requirements.txt

REM Start the FastAPI server
echo Starting FastAPI server on port 8000...
python -m uvicorn main:app --reload --port 8000

pause