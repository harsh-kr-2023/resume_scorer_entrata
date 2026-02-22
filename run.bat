@echo off
REM Resume Matcher - Windows Setup and Run Script
REM This script sets up the Python environment and runs the FastAPI server

echo ========================================
echo Resume Matcher - Setup and Run
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo [2/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo.
    echo [2/5] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/upgrade dependencies
echo.
echo [4/5] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Check if .env exists, if not create from .env.example
if not exist ".env" (
    echo.
    echo [5/5] Creating .env file from template...
    copy .env.example .env
    echo.
    echo ========================================
    echo IMPORTANT: Please edit .env file and add your LLM_API_KEY
    echo ========================================
    echo.
    echo Opening .env file in notepad...
    timeout /t 2 >nul
    notepad .env
    echo.
    echo After adding your API key, press any key to start the server...
    pause >nul
) else (
    echo.
    echo [5/5] .env file already exists
)

REM Create results directory if it doesn't exist
if not exist "results" (
    mkdir results
)

REM Start the FastAPI server
echo.
echo ========================================
echo Starting Resume Matcher API Server
echo ========================================
echo.
echo Server will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

REM If server stops, pause to show any error messages
pause
