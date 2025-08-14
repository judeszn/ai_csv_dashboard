# AI CSV Dashboard: Code Walkthrough

This document explains how the Zero-Config AI Analytics Dashboard works, going through the code step by step in the order of execution when you use the application.

## Table of Contents
1. [Starting the Application](#starting-the-application)
2. [Backend Structure](#backend-structure)
3. [Frontend Application](#frontend-application)
4. [Data Flow Process](#data-flow-process)
5. [Key Components Explained](#key-components-explained)

## Starting the Application

The entry point for Windows users is the `start_windows.bat` file:

```bat
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
```

What this script does:
1. It starts the backend server using `uvicorn` (a fast ASGI server) which runs your FastAPI application
   - The command `python -m uvicorn backend.main:app` tells Python to run the app variable from the backend/main.py file
   - It runs on localhost (127.0.0.1) on port 8000
2. It waits for 6 seconds using the `ping` command as a delay timer
3. It starts the Streamlit frontend on port 8501
4. Both services run in separate command windows

For Mac/Linux users, there's `start.sh` which does the same thing but uses bash commands instead.

## Backend Structure

### Main API (backend/main.py)

```python
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import pandas as pd
import io
from dotenv import load_dotenv
from .agents.analysis_agent import create_analysis_agent, query_agent

# Load environment variables from .env if present
load_dotenv()

print("[Startup] Environment loaded. GOOGLE_API_KEY and GEMINI_MODEL should be set.")

app = FastAPI(title="Zero-Config AI Analytics Engine")

@app.post("/analyze")
async def analyze_data(file: UploadFile = File(...), question: str = Form(...)):
    
    """
    Accepts a CSV file and a natural language question, performs data analysis
    using a Gemini-powered LangChain agent, and returns the result.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")

    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))

        print(f"[Request] Analysis started for question: '{question}'")
        agent = create_analysis_agent(df, allow_dangerous_code=True)
        answer = query_agent(agent, question)
        print("[Request] Analysis finished successfully.")

        return JSONResponse(content={"answer": answer})
    except Exception as e:
        print(f"[Error] {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {e}")
```

This file:
1. Sets up a FastAPI application 
2. Loads environment variables from a `.env` file (like your Google API key)
3. Creates an `/analyze` endpoint that:
   - Accepts a CSV file and a question as input
   - Checks that the file is actually a CSV
   - Reads the CSV into a pandas DataFrame
   - Creates an AI analysis agent with the data
   - Sends the question to the agent
   - Returns the agent's answer as JSON

### Analysis Agent (backend/agents/analysis_agent.py)

```python
import pandas as pd
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

def create_analysis_agent(df: pd.DataFrame, allow_dangerous_code: bool = False):
    """
    Creates a LangChain agent for analyzing a pandas DataFrame.

    Args:
        df: The pandas DataFrame to be analyzed.
        allow_dangerous_code: A flag to explicitly allow the agent to execute
                              Python code. Must be set to True.

    Returns:
        A LangChain agent executor.
    """
    model_name = os.environ.get("GEMINI_MODEL", "gemini-pro")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, convert_system_message_to_human=True)
    
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        allow_dangerous_code=allow_dangerous_code
    )
    return agent

def query_agent(agent, question: str):
    """Queries the agent and returns the answer."""
    response = agent.invoke(question)
    return response.get("output", "Sorry, I was unable to find an answer.")
```

This file contains two important functions:

1. `create_analysis_agent()`:
   - Takes a pandas DataFrame (your CSV data)
   - Gets the Gemini model name from environment variables 
   - Sets up a connection to Google's Generative AI with temperature=0 (for consistent, non-random results)
   - Creates a special LangChain "pandas dataframe agent" that can:
     - Access your data
     - Run Python code to analyze it
     - Use AI reasoning to figure out the best way to answer questions
   - Returns the agent ready to use

2. `query_agent()`:
   - Takes the agent and your question
   - Asks the agent to answer the question
   - Gets the response and returns the output

## Frontend Application

### Streamlit App (frontend/app.py)

```python
import streamlit as st
import requests
import os

st.set_page_config(page_title="Zero-Config AI Analytics", layout="wide")
st.title("🤖 Zero-Config AI Analytics Engine")
st.markdown("Upload a CSV file and ask a question in natural language.")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
ANALYZE_ENDPOINT = f"{BACKEND_URL}/analyze"

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
question = st.text_input("Ask a question about your data:", "What are the main insights from this data?")

if st.button("Analyze"):
    if uploaded_file is not None and question:
        with st.spinner("The AI is thinking... This might take a moment."):
            files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
            data = {'question': question}

            try:
                response = requests.post(ANALYZE_ENDPOINT, files=files, data=data, timeout=300)
                response.raise_for_status() 
                result = response.json()
                st.subheader("Analysis Result:")
                st.success(result.get('answer', 'No answer found.'))
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to the backend at {BACKEND_URL}. Please ensure it's running. Error: {e}")
    else:
        st.warning("Please upload a file and enter a question.")
```

The frontend is a simple Streamlit app that:

1. Creates a web interface with:
   - A title and description
   - A file uploader for CSVs
   - A text input for your question
   - An "Analyze" button

2. When you click "Analyze":
   - Checks that you've uploaded a file and entered a question
   - Shows a spinner while processing
   - Prepares the file and question to send to the backend
   - Makes a POST request to the backend API
   - Waits for the response (up to 5 minutes with timeout=300)
   - Shows the answer from the AI
   - Shows an error if something goes wrong

## Data Flow Process

Now let's follow how data flows through the application when you use it:

1. **Starting the App**:
   - You run `start_windows.bat`
   - The backend server starts on port 8000
   - The frontend starts on port 8501
   - Your browser opens to http://localhost:8501

2. **User Interaction**:
   - You upload a CSV file
   - You type a question about the data
   - You click the "Analyze" button

3. **Frontend to Backend**:
   - The frontend prepares your file and question
   - It sends them to the backend API at http://localhost:8000/analyze
   - It waits for a response, showing a spinner

4. **Backend Processing**:
   - The backend receives your file and question
   - It loads the CSV into a pandas DataFrame
   - It creates an AI analysis agent with your data
   - It asks the agent your question

5. **AI Analysis**:
   - The agent (using Google's Gemini model) thinks about your question
   - It decides what Python code to run to answer your question
   - It might run multiple steps (filtering data, calculating averages, making charts)
   - It formats an answer with the results

6. **Response Flow**:
   - The agent's answer goes back to the backend API
   - The backend wraps it in a JSON response
   - The JSON response goes to the frontend
   - The frontend displays the answer to you

## Key Components Explained

### Environment Setup
- The `.env` file (which you need to create) should contain your `GOOGLE_API_KEY` and optionally `GEMINI_MODEL`
- `requirements.txt` lists all the Python packages needed for the project

### LangChain DataFrame Agent
This is the most interesting part! The DataFrame agent:
- Is an AI "agent" that can write and execute Python code
- Has access to a pandas DataFrame (your CSV data)
- Uses an "Agent" architecture that lets it:
  1. Think about what steps are needed to answer the question
  2. Write Python code to perform those steps
  3. Execute the code
  4. Analyze the results
  5. Decide if more steps are needed
  6. Format a final answer

For example, if you ask "What are the top 3 countries by sales?", it might:
1. Check if "country" and "sales" columns exist
2. Group by country and sum the sales
3. Sort in descending order
4. Take the top 3 entries
5. Format them into a readable answer

All this happens automatically because of the LangChain and Gemini integration!

### Security Note
- The `allow_dangerous_code=True` parameter allows the AI to execute arbitrary Python code
- This is needed for full functionality but should be used carefully
- The code execution is sandboxed within the application

## Final Thoughts

This project combines several powerful technologies:
- FastAPI for a robust API backend
- Streamlit for an easy-to-use frontend
- pandas for data handling
- Google's Gemini AI for natural language understanding
- LangChain for connecting AI capabilities to data analysis

The result is a system where you can talk to your data in plain English, with the AI doing all the technical work for you. It's a great example of how AI can make data analysis accessible to everyone, regardless of their technical background.
