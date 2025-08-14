@echo off
REM Windows startup script for Zero-Config AI Analytics Dashboard

echo ===== Starting AI CSV Dashboard =====
echo.

REM Activate your virtual environment if needed
REM call .venv\Scripts\activate

echo Checking required packages...
pip install -r requirements.txt

echo.
echo Checking for processes using port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
  echo Found process using port 8000: %%a
  echo Terminating process...
  taskkill /F /PID %%a >nul 2>&1
  if ERRORLEVEL 0 echo Process terminated successfully.
)

echo.
echo Starting backend server on a different port (8005)...
start "Backend" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8005 --log-level debug && echo Backend terminated. Press any key to close window. && pause"

echo Waiting for backend to initialize...
ping 127.0.0.1 -n 6 > nul

echo.
echo Starting frontend application (please keep this window open)...
start "Frontend" cmd /k "set BACKEND_URL=http://localhost:8005 && streamlit run frontend/app.py --server.port=8501 --server.headless=true --server.enableCORS=false && echo Frontend terminated. Press any key to close window. && pause"

echo.
echo ===== Setup Complete =====
echo Both backend and frontend started in separate windows.
echo Backend running on: http://localhost:8005
echo Frontend running on: http://localhost:8501
echo.
echo Open http://localhost:8501 in your browser.
echo.
echo IMPORTANT: Keep both terminal windows open while using the application.
echo If you encounter any errors, check the backend terminal window for details.
echo.Windows startup script for Zero-Config AI Analytics Dashboard

REM Activate your virtual environment if needed
REM call .venv\Scripts\activate

start "Backend" cmd /k python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

REM Wait a few seconds for backend to start
ping 127.0.0.1 -n 6 > nul

start "Frontend" cmd /k streamlit run frontend/app.py --server.port=8501 --server.headless=true --server.enableCORS=false

echo Both backend and frontend started in new windows.
echo Open http://localhost:8500 in your browser.
