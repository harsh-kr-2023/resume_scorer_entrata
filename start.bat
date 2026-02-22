@echo off
REM Resume Matcher - Quick Start Script
REM Use this after initial setup with run.bat

echo Starting Resume Matcher API Server...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Create results directory if it doesn't exist
if not exist "results" (
    mkdir results
)

REM Start the server
echo Server will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
