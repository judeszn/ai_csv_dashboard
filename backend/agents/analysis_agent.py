import pandas as pd
import os
import traceback
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
    if df.empty:
        raise ValueError("The provided DataFrame is empty. Please upload a CSV with data.")

    try:
        model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        print(f"[Agent] Using model: {model_name}")
        
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        
        llm = ChatGoogleGenerativeAI(
            model=model_name, 
            temperature=0, 
            convert_system_message_to_human=True,
            google_api_key=api_key
        )
        
        agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            allow_dangerous_code=allow_dangerous_code
        )
        return agent
    except Exception as e:
        print(f"[Error] Failed to create agent: {e}")
        traceback.print_exc()
        raise

def query_agent(agent, question: str):
    """Queries the agent and returns the answer."""
    try:
        # Add a timeout for agent execution (not directly supported in LangChain, but we can add our own)
        print(f"[Agent] Querying with question: '{question}'")
        response = agent.invoke(question)
        answer = response.get("output", "Sorry, I was unable to find an answer.")
        print(f"[Agent] Successfully generated response")
        return answer
    except Exception as e:
        print(f"[Error] Agent query failed: {e}")
        traceback.print_exc()
        error_msg = str(e)
        
        # Handle common errors with more user-friendly messages
        if "rate limit" in error_msg.lower():
            return "Sorry, the AI service is currently experiencing high traffic. Please try again in a few moments."
        elif "api key" in error_msg.lower():
            return "There is a configuration issue with the AI service. Please contact the administrator to check the API key."
        elif "context length" in error_msg.lower():
            return "Your dataset is too large or complex for a single analysis. Try asking a more specific question about a subset of the data."
        else:
            return f"The analysis encountered an error: {error_msg}. Please try a different question or check the data format."