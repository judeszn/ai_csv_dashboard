#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

BACKEND_PID=""

# Function to clean up background processes on script exit.
cleanup() {
    echo "Shutting down services..."
    if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        kill "$BACKEND_PID"
    fi
}

# Define a log file to capture backend output for easier debugging.
trap cleanup EXIT
BACKEND_LOG="backend.log"

# Start the backend API in the background.
echo "Starting backend service..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 > "$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!

# Wait a moment and check if the backend process is still running.
echo "Waiting for backend to initialize..."
sleep 5

if ! kill -0 "$BACKEND_PID" > /dev/null 2>&1; then
    echo "----------------------------------------"
    echo "!!! Backend service failed to start. See logs below for details. !!!"
    echo "----------------------------------------"
    # Print the log file to show the actual error from the backend.
    cat "$BACKEND_LOG"
    exit 1
fi

# Start the Streamlit frontend in the foreground.
# When this process stops, the script will exit, and the trap will clean up the backend.
echo "Backend started successfully. Starting frontend..."
streamlit run frontend/app.py --server.port=8501 --server.headless=true --server.enableCORS=false
