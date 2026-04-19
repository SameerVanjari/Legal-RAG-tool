"""
Streamlit UI for the Legal RAG System.
Provides a natural language interface for querying legal documents.
"""
import streamlit as st
import requests
import json
from typing import Dict, Any
import os

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "api_ready" not in st.session_state:
        st.session_state.api_ready = False

def check_api_health() -> bool:
    """Check if the API server is running and healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_document(uploaded_file) -> Dict[str, Any]:
    """Upload a document to the API."""
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

def query_documents(question: str, top_k: int = 5) -> Dict[str, Any]:
    """Query the legal knowledge base."""
    try:
        payload = {
            "question": question,
            "top_k": top_k
        }
        response = requests.post(f"{API_BASE_URL}/query", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

def display_conversation():
    """Display the conversation history."""
    for i, (question, answer, sources) in enumerate(st.session_state.conversation_history):
        with st.container():
            st.markdown(f"**You:** {question}")
            st.markdown(f"**Assistant:** {answer}")
            if sources:
                with st.expander(f"View Sources ({len(sources)} documents)"):
                    for j, source in enumerate(sources):
                        st.markdown(f"**Source {j+1}:**")
                        st.text(source.get("content", "No content available"))
                        if source.get("metadata"):
                            st.json(source["metadata"])
            st.divider()

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Legal RAG Assistant",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("⚖️ Legal RAG Assistant")
    st.markdown("Ask questions about legal documents related to personal finance")
    
    # Sidebar
    with st.sidebar:
        st.header("System Status")
        
        # API Health Check
        api_healthy = check_api_health()
        if api_healthy:
            st.success("🟢 API Server Connected")
            st.session_state.api_ready = True
        else:
            st.error("🔴 API Server Disconnected")
            st.session_state.api_ready = False
            st.info("Make sure the FastAPI server is running:")
            st.code("python src/main.py")
        
        st.divider()
        
        # Document Upload Section
        st.header("Document Management")
        uploaded_file = st.file_uploader(
            "Upload Legal Document",
            type=["pdf", "docx", "txt", "html"],
            help="Upload legal documents to add to the knowledge base"
        )
        
        if uploaded_file is not None:
            if st.button("Process Document"):
                with st.spinner("Processing document..."):
                    result = upload_document(uploaded_file)
                    if "error" in result:
                        st.error(f"Error: {result['error']}")
                    else:
                        st.success(result.get("message", "Document processed successfully"))
                        st.json(result)
        
        st.divider()
        
        # Settings
        st.header("Settings")
        top_k = st.slider(
            "Number of sources to retrieve",
            min_value=1,
            max_value=10,
            value=5,
            help="How many relevant documents to consider for each query"
        )
        
        if st.button("Clear Conversation"):
            st.session_state.conversation_history = []
            st.rerun()
    
    # Main content area
    if not st.session_state.api_ready:
        st.warning("⚠️ Please start the API server to use the system.")
        st.info("Run: `python src/main.py` in a separate terminal")
        return
    
    # Chat interface
    st.header("Ask a Legal Question")
    
    # Display conversation history
    display_conversation()
    
    # Question input
    with st.form(key="question_form", clear_on_submit=True):
        question = st.text_area(
            "Your question:",
            placeholder="e.g., What are the requirements for a valid personal loan agreement?",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submit_button = st.form_submit_button("Ask Question", type="primary")
        with col2:
            st.caption(f"Will retrieve {top_k} relevant sources")
    
    # Process question
    if submit_button and question.strip():
        with st.spinner("Searching legal knowledge base..."):
            result = query_documents(question.strip(), top_k)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                # Add to conversation history
                st.session_state.conversation_history.append((
                    question.strip(),
                    result.get("answer", "No answer provided"),
                    result.get("sources", [])
                ))
                st.rerun()  # Refresh to show the new conversation entry
    
    elif submit_button:
        st.warning("Please enter a question before submitting.")

if __name__ == "__main__":
    main()