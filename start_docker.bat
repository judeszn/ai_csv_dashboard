@echo off
echo ===== Starting AI CSV Dashboard with Docker =====
echo.

REM Check if Docker is installed
docker --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker is not installed or not in PATH.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

REM Check if Docker is running
docker info > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Docker is not running. Please start Docker Desktop.
    echo.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found. Creating a template .env file.
    echo GOOGLE_API_KEY=your_api_key_here> .env
    echo GEMINI_MODEL=gemini-2.0-flash>> .env
    echo.
    echo Please edit the .env file and add your Google API key.
    notepad .env
)

echo Building and starting containers...
docker-compose up --build

echo.
echo If the process was interrupted, you can stop any running containers with:
echo docker-compose down
echo.
pause
