import streamlit as st
import requests
import os
import time
import pandas as pd

st.set_page_config(page_title="Zero-Config AI Analytics", layout="wide")
st.title("🤖 Zero-Config AI Analytics Engine")
st.markdown("Upload a CSV file and ask a question in natural language.")

# Check if backend is running
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
HEALTH_ENDPOINT = f"{BACKEND_URL}/"
ANALYZE_ENDPOINT = f"{BACKEND_URL}/analyze"

# Backend status check in sidebar
with st.sidebar:
    st.subheader("Backend Status")
    
    def check_backend():
        try:
            response = requests.get(HEALTH_ENDPOINT, timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend is running")
                return True
            else:
                st.error("❌ Backend error: " + str(response.status_code))
                return False
        except requests.exceptions.RequestException:
            st.error("❌ Backend is not running")
            st.info("Please make sure the backend is started. Run the start_windows.bat script.")
            return False
    
    backend_running = check_backend()
    
    # Show some example questions
    st.subheader("Example Questions")
    st.markdown("""
    - What are the top 5 values in column X?
    - Find the correlation between column A and B
    - Create a scatter plot of X vs Y
    - What's the average of column Z grouped by column A?
    - Show a summary of the data
    """)

# Main area
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Preview the data if a file is uploaded
if uploaded_file is not None:
    try:
        df_preview = pd.read_csv(uploaded_file)
        st.subheader("Data Preview")
        st.dataframe(df_preview.head(5), use_container_width=True)
        # Reset file pointer for later use
        uploaded_file.seek(0)
    except Exception as e:
        st.error(f"Error previewing the CSV: {e}")

question = st.text_input("Ask a question about your data:", "What are the main insights from this data?")

if st.button("Analyze", disabled=not backend_running):
    if uploaded_file is not None and question:
        with st.spinner("The AI is thinking... This might take a moment."):
            files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
            data = {'question': question}

            try:
                # Add retry logic
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        response = requests.post(ANALYZE_ENDPOINT, files=files, data=data, timeout=300)
                        response.raise_for_status()
                        result = response.json()
                        
                        if "error" in result:
                            st.error(f"Backend error: {result['error']}")
                        else:
                            st.subheader("Analysis Result:")
                            st.success(result.get('answer', 'No answer found.'))
                        break
                    except requests.exceptions.HTTPError as e:
                        if response.status_code == 500 and retry_count < max_retries - 1:
                            retry_count += 1
                            st.info(f"Retrying ({retry_count}/{max_retries})...")
                            time.sleep(2)  # Wait before retrying
                        else:
                            # Try to get detailed error if available
                            try:
                                error_detail = response.json().get('error', str(e))
                                st.error(f"Server error: {error_detail}")
                            except:
                                st.error(f"Server error: {str(e)}")
                            break
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to the backend at {BACKEND_URL}. Please ensure it's running. Error: {e}")
                st.info("Try restarting the application using start_windows.bat")
    else:
        st.warning("Please upload a file and enter a question.")