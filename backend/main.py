
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
