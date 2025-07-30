@echo off
REM Windows startup script for Zero-Config AI Analytics Dashboard

REM Activate your virtual environment if needed
REM call .venv\Scripts\activate

start "Backend" cmd /k python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

REM Wait a few seconds for backend to start
ping 127.0.0.1 -n 6 > nul

start "Frontend" cmd /k streamlit run frontend/app.py --server.port=8501 --server.headless=true --server.enableCORS=false

echo Both backend and frontend started in new windows.
echo Open http://localhost:8501 in your browser.
