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