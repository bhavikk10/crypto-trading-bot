@echo off
REM Hybrid Crypto Trading Bot Dashboard Startup Script for Windows
REM Runs both Clojure crypto system and Python FastAPI backend

echo 🚀 Starting Hybrid Crypto Trading Bot Dashboard...

REM Check prerequisites
echo Checking prerequisites...

REM Check if Redis is running
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo ❌ Redis is not running. Please start Redis first.
    echo Download Redis from: https://github.com/microsoftarchive/redis/releases
    pause
    exit /b 1
)
echo ✅ Redis is running

REM Check if Java is available
java -version >nul 2>&1
if errorlevel 1 (
    echo ❌ Java is not installed. Please install Java 8+ first.
    echo Download from: https://adoptopenjdk.net/
    pause
    exit /b 1
)
echo ✅ Java is available

REM Check if Leiningen is available
lein version >nul 2>&1
if errorlevel 1 (
    echo ❌ Leiningen is not installed. Please install Leiningen first.
    echo Visit: https://leiningen.org/
    pause
    exit /b 1
)
echo ✅ Leiningen is available

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python is available

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js is available

echo All prerequisites met!

REM Start Clojure HTTP API Server
echo Starting Clojure HTTP API Server...
cd crypto
start "Clojure API" cmd /k "lein run -m crypto.api.http/start-api-server!"
cd ..

REM Wait a bit for Clojure to start
timeout /t 10 /nobreak >nul

REM Start Python FastAPI Backend
echo Starting Python FastAPI Backend...
cd crypto-bot-mvp\backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Start FastAPI server
start "Python FastAPI" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
cd ..\..

REM Wait a bit for Python to start
timeout /t 5 /nobreak >nul

REM Start React Frontend
echo Starting React Frontend...
cd crypto-bot-mvp\frontend

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
)

REM Start React development server
start "React Frontend" cmd /k "npm start"
cd ..\..

echo 🎉 All services started successfully!
echo.
echo Service URLs:
echo   Clojure API:     http://localhost:8080
echo   Python FastAPI:  http://localhost:8000
echo   React Frontend:  http://localhost:3000
echo   API Documentation: http://localhost:8000/docs
echo.
echo Check the opened command windows for service status.
echo Close the command windows to stop the services.
echo.
pause
