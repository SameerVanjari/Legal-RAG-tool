"""
Vector store management for the Legal RAG system using ChromaDB.
"""
import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document


class LegalVectorStore:
    """Manages the vector store for legal documents."""
    
    def __init__(self, 
                 persist_directory: str = "./chroma_db",
                 embedding_model: str = "all-MiniLM-L6-v2",
                 collection_name: str = "legal_documents"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the ChromaDB data
            embedding_model: Name of the sentence transformer model to use
            collection_name: Name of the ChromaDB collection
        """
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        
        # Initialize embeddings
        self.embeddings = SentenceTransformerEmbeddings(model_name=embedding_model)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize LangChain Chroma wrapper
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=collection_name,
            embedding_function=self.embeddings
        )
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents to add
            
        Returns:
            List of document IDs
        """
        if not documents:
            return []
            
        # Add documents to vector store
        ids = self.vectorstore.add_documents(documents)
        return ids
    
    def similarity_search(self, 
                         query: str, 
                         k: int = 5,
                         filter_dict: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query: Query text to search for
            k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of relevant documents
        """
        if filter_dict:
            results = self.vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vectorstore.similarity_search(
                query=query,
                k=k
            )
        return results
    
    def similarity_search_with_score(self, 
                                   query: str, 
                                   k: int = 5,
                                   filter_dict: Optional[Dict[str, Any]] = None) -> List[tuple]:
        """
        Perform similarity search with scores.
        
        Args:
            query: Query text to search for
            k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of (document, score) tuples
        """
        if filter_dict:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k
            )
        return results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        return {
            "total_documents": count,
            "collection_name": self.collection_name,
            "persist_directory": self.persist_directory
        }
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        self.client.delete_collection(name=self.collection_name)
        # Recreate the collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        # Reinitialize the vectorstore wrapper
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embeddings
        )