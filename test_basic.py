#!/usr/bin/env python3
"""
Basic test to verify the core components can be imported and instantiated.
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from document_processor import LegalDocumentProcessor
        print("✓ DocumentProcessor imported successfully")
    except Exception as e:
        print(f"✗ Failed to import DocumentProcessor: {e}")
        return False
    
    try:
        from vector_store import LegalVectorStore
        print("✓ LegalVectorStore imported successfully")
    except Exception as e:
        print(f"✗ Failed to import LegalVectorStore: {e}")
        return False
        
    try:
        from llm_service import LegalLLMService
        print("✓ LegalLLMService imported successfully")
    except Exception as e:
        print(f"✗ Failed to import LegalLLMService: {e}")
        return False
        
    try:
        from main import app
        print("✓ Main FastAPI app imported successfully")
    except Exception as e:
        print(f"✗ Failed to import main app: {e}")
        return False
    
    return True

def test_instantiation():
    """Test that components can be instantiated."""
    print("\nTesting instantiation...")
    
    try:
        from document_processor import LegalDocumentProcessor
        processor = LegalDocumentProcessor()
        print("✓ DocumentProcessor instantiated successfully")
    except Exception as e:
        print(f"✗ Failed to instantiate DocumentProcessor: {e}")
        return False
    
    try:
        from vector_store import LegalVectorStore
        # Use a test directory to avoid interfering with existing data
        vector_store = LegalVectorStore(persist_directory="./test_chroma_db")
        print("✓ LegalVectorStore instantiated successfully")
    except Exception as e:
        print(f"✗ Failed to instantiate LegalVectorStore: {e}")
        return False
        
    try:
        from llm_service import LegalLLMService
        llm_service = LegalLLMService()
        print("✓ LegalLLMService instantiated successfully")
    except Exception as e:
        print(f"✗ Failed to instantiate LegalLLMService: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Running basic tests for Legal RAG System\n")
    
    import_success = test_imports()
    instantiation_success = test_instantiation()
    
    if import_success and instantiation_success:
        print("\n🎉 All basic tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)