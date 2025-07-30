from langchain.document_loaders import CSVLoader, PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI, HuggingFaceHub
import os

class DataAnalyzer:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = None
        self.qa_chain = None
        
    def load_data(self, file_path: str):
        """Load documents using LangChain's auto-detecting loader"""
        if file_path.endswith('.csv'):
            loader = CSVLoader(file_path)
        elif file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            raise ValueError("Unsupported file type")
            
        documents = loader.load()
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=HuggingFaceHub(repo_id="google/flan-t5-base"),
            retriever=self.vectorstore.as_retriever()
        )
    
    def query_data(self, question: str, chat_history: list = []):
        """Query the loaded data using natural language"""
        if not self.qa_chain:
            raise RuntimeError("No data loaded for analysis")
        return self.qa_chain({"question": question, "chat_history": chat_history})