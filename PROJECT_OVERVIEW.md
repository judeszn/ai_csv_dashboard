# Project Overview: Zero-Config AI Analytics Dashboard

## 1. Project Summary

This project is a web-based AI analytics dashboard that allows users to upload data (likely CSV files) and interact with it using natural language. It features a decoupled architecture with a Python-based backend providing an API and a Streamlit-based frontend for the user interface. The core AI functionality is powered by Google's Generative AI models, orchestrated through the LangChain framework to analyze and interpret user queries against the data.

---

## 2. Architecture

The application follows a classic client-server model:

*   **Backend (FastAPI):** A RESTful API server that handles the core business logic. This includes receiving data uploads, processing user queries, interacting with the Large Language Model (LLM), and returning the results.
*   **Frontend (Streamlit):** A web-based user interface where the user can upload their data file and type in questions. It communicates with the backend API to send requests and display the AI-generated analysis.
*   **Process Management (`start.sh`):** A shell script orchestrates the startup of both the backend and frontend services, managing them as separate processes. This mimics a microservices-style deployment.

---

## 3. Core Technologies & Concepts

Here is a breakdown of the key libraries and tools used in this project, perfect for a CV or technical discussion.

### Backend & API

*   **Python:** The primary programming language for the entire stack.
*   **FastAPI:** A modern, high-performance Python web framework used to build the backend REST API. Its key benefit is speed and automatic generation of interactive API documentation (e.g., Swagger UI), which is excellent for development and testing.
*   **Uvicorn:** An ASGI (Asynchronous Server Gateway Interface) server used to run the FastAPI application. It's the production-grade server that handles incoming HTTP requests and passes them to the FastAPI application. The `[standard]` option includes recommended libraries for better performance and websocket support.

### AI & Data Processing

*   **LangChain (`langchain`):** A powerful framework for developing applications powered by language models. It was used to "chain" together different components: the LLM, user prompts, and data tools. It simplifies the process of building complex AI workflows.
*   **LangChain Google Generative AI (`langchain-google-genai`):** The specific LangChain integration library for connecting to and using Google's Generative AI models (like Gemini). This is the "brain" of the application.
*   **Google Generative AI (`google-generativeai`):** The official Google Python SDK that the LangChain integration is built upon. It handles the low-level communication with the Google AI platform.
*   **LangChain Experimental (`langchain-experimental`):** This library contains more advanced or beta features. Its presence strongly suggests the use of the **Pandas DataFrame Agent**. This is a key component that allows the LLM to be given a Pandas DataFrame and a set of tools to directly execute Python code on the DataFrame to answer questions. For example, it can perform filtering, sorting, aggregations, and even generate plots.
*   **Pandas (`pandas`):** The de-facto standard library for data manipulation and analysis in Python. It's used to load the user's uploaded data (e.g., from a CSV) into a DataFrame, which is then passed to the LangChain agent for analysis.
*   **Tabulate (`tabulate`):** A simple library for creating well-formatted tables from data. This is likely used by the backend or the LangChain agent to format data neatly before sending it back to the frontend.

### Frontend

*   **Streamlit (`streamlit`):** An open-source Python framework for building and sharing data applications. It was chosen for the frontend because it allows for rapid development of interactive UIs with minimal code, making it ideal for data-centric projects. The frontend is responsible for the file uploader and the chat interface.

### Tooling & Environment

*   **Bash Scripting (`start.sh`):** The startup script demonstrates skills in shell scripting for process management. It starts the backend as a background process, checks its health, and then starts the frontend. It also includes a `trap` for cleanup, ensuring the backend process is terminated when the script exits.
*   **Python DotEnv (`python-dotenv`):** A utility to manage environment variables. This is used to load sensitive information like API keys (e.g., `GOOGLE_API_KEY`) from a `.env` file, which is a best practice for keeping secrets out of source code.
*   **Dependency Management (`requirements.txt`):** The standard file for declaring Python project dependencies. It ensures that the application can be reliably installed in any environment.

---

## 4. How to Describe This on a CV

**Project: AI-Powered Data Analytics Chatbot**

*   Developed a full-stack "Zero-Configuration" analytics dashboard enabling users to upload CSV data and perform natural language queries.
*   Engineered a Python backend using **FastAPI** and **Uvicorn** to serve a REST API for data processing and AI inference.
*   Integrated **Google's Generative AI (Gemini)** models using the **LangChain** framework to interpret user questions and generate insights.
*   Implemented a **LangChain Pandas DataFrame Agent** to dynamically execute Python code on user-provided data, allowing for complex queries, aggregations, and analysis.
*   Built an interactive frontend with **Streamlit**, providing a seamless user experience for file uploads and conversational analytics.
*   Authored a **Bash** script to orchestrate the deployment of the decoupled frontend and backend services, ensuring proper startup and resource cleanup.
*   Managed application configuration and secrets securely using environment variables via `python-dotenv`.