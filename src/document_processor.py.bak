"""
Document processing module for loading, chunking, and preparing legal documents
for the RAG system.
"""
import os
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredHTMLLoader
)
from langchain.schema import Document


class LegalDocumentProcessor:
    """Processes legal documents for ingestion into the RAG system."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a document based on its file extension.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of loaded documents
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")
            
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path)
        elif ext in [".html", ".htm"]:
            loader = UnstructuredHTMLLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
            
        return loader.load()
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for processing.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of chunked documents
        """
        chunked_docs = self.text_splitter.split_documents(documents)
        
        # Add chunk metadata
        for i, doc in enumerate(chunked_docs):
            doc.metadata.update({
                "chunk_id": i,
                "chunk_count": len(chunked_docs)
            })
            
        return chunked_docs
    
    def process_document(self, file_path: str) -> List[Document]:
        """
        Complete document processing pipeline: load and chunk.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of processed document chunks
        """
        documents = self.load_document(file_path)
        chunked_documents = self.chunk_documents(documents)
        
        # Add source file metadata
        for doc in chunked_documents:
            doc.metadata["source"] = file_path
            doc.metadata["document_type"] = self._get_document_type(file_path)
            
        return chunked_documents
    
    def _get_document_type(self, file_path: str) -> str:
        """
        Determine document type based on file path or name.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Document type string
        """
        file_name = os.path.basename(file_path).lower()
        
        if any(term in file_name for term in ["contract", "agreement", "nda", "terms"]):
            return "contract"
        elif any(term in file_name for term in ["statute", "regulation", "code", "law"]):
            return "statute"
        elif any(term in file_name for term in ["case", "opinion", "judgment", "ruling"]):
            return "case_law"
        else:
            return "legal_document"