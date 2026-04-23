from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv
import sys
import os
# Add the src directory to the path in a more robust way
src_path = os.path.join(os.path.dirname(__file__))
if src_path not in sys.path:
    sys.path.append(src_path)

from document_processor import LegalDocumentProcessor
from vector_store import LegalVectorStore
from llm_service import LegalLLMService

# Load environment variables
load_dotenv()

app = FastAPI(title="Legal RAG System API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
document_processor = LegalDocumentProcessor()
vector_store = LegalVectorStore()
llm_service = LegalLLMService()

# Pydantic models
class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence: Optional[float] = None

class DocumentResponse(BaseModel):
    message: str
    document_id: str
    chunks_created: int

@app.get("/")
async def root():
    return {"message": "Legal RAG System API is running"}

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a legal document"""
    try:
        # Save uploaded file temporarily
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process the document
        documents = document_processor.process_document(temp_file_path)
        
        # Add to vector store
        ids = vector_store.add_documents(documents)
        
        # Clean up temp file
        os.remove(temp_file_path)
        
        return {
            "message": "Document uploaded and processed successfully",
            "document_id": ids[0] if ids else "",
            "chunks_created": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the legal knowledge base"""
    try:
        # Search for relevant documents
        relevant_docs = vector_store.similarity_search(
            query=request.question,
            k=request.top_k if request.top_k is not None else 5
        )
        
        # Generate response using LLM service
        result = llm_service.generate_response(request.question, relevant_docs)
        
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "confidence": result["confidence"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)