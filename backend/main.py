
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import pandas as pd
import io
import traceback
import sys
from dotenv import load_dotenv
from .agents.analysis_agent import create_analysis_agent, query_agent

# Load environment variables from .env if present
load_dotenv()

# Check for required environment variables
if not os.getenv("GOOGLE_API_KEY"):
    print("[ERROR] GOOGLE_API_KEY is not set in .env file or environment variables!")
    print("[INFO] Please make sure you have a .env file with GOOGLE_API_KEY=your_api_key")
else:
    print("[Startup] Environment loaded. GOOGLE_API_KEY found.")

print(f"[Startup] Using GEMINI_MODEL: {os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')}")

app = FastAPI(title="Zero-Config AI Analytics Engine")

# Allow requests from the Streamlit frontend
origins = [
    "http://localhost:8500",
    "http://localhost:8501",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint to verify the API is running."""
    return {"status": "ok", "message": "Backend API is running"}

@app.post("/analyze")
async def analyze_data(file: UploadFile = File(...), question: str = Form(...)):
    
    """
    Accepts a CSV file and a natural language question, performs data analysis
    using a Gemini-powered LangChain agent, and returns the result.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")

    try:
        print(f"[Request] Received analysis request for file: {file.filename}, question: '{question}'")
        content = await file.read()
        
        try:
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
            print(f"[Request] CSV loaded successfully. Shape: {df.shape}")
        except Exception as e:
            print(f"[Error] Failed to parse CSV file: {e}")
            return JSONResponse(
                status_code=400,
                content={"error": f"Could not parse CSV file: {str(e)}"}
            )

        print(f"[Request] Analysis started for question: '{question}'")
        
        try:
            agent = create_analysis_agent(df, allow_dangerous_code=True)
            answer = query_agent(agent, question)
            print("[Request] Analysis finished successfully.")
        except Exception as e:
            print(f"[Error] Failed during agent analysis: {e}")
            traceback.print_exc()
            return JSONResponse(
                status_code=500,
                content={"error": f"Analysis failed: {str(e)}. Please check your question and try again."}
            )

        return JSONResponse(content={"answer": answer})
    except Exception as e:
        print(f"[Error] Unhandled exception: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500, 
            content={"error": f"An unexpected error occurred: {str(e)}"}
        )
