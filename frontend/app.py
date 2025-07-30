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