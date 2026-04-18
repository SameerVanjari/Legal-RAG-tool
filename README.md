# Legal RAG System

A Retrieval-Augmented Generation (RAG) system designed specifically for legal documents related to personal finance. This system allows users to ask questions in natural language and receive accurate answers based on a knowledge base of legal documents including case law, contracts, statutes, and regulations.

## 🎯 Project Overview

The Legal RAG system combines document processing, vector storage, and language model capabilities to create an intelligent legal assistant that can:
- Process and index various legal document formats
- Retrieve relevant information using semantic search
- Generate natural language responses with proper source attribution
- Handle personal finance legal queries effectively

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│   Document      │    │   Vector Store   │    │   Query Processing │
│   Processor     │───▶│   (ChromaDB)     │───▶│   & LLM Service    │
└─────────────────┘    └──────────────────┘    └────────────────────┘
        │                         │                         │
        ▼                         ▼                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│ Legal Documents │    │   Embeddings     │    │   Natural Language │
│ (PDF, DOCX, TXT,│    │   & Metadata     │    │      Responses     │
│   HTML)         │    └──────────────────┘    └────────────────────┘
└─────────────────┘
```

## 🔧 Technology Stack

- **Backend Framework**: FastAPI (RESTful API)
- **Document Processing**: LangChain with custom processors
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (planned)
- **Frontend**: Streamlit (planned for initial UI, React for production)
- **Environment**: Python 3.13+
- **Additional Tools**: Uvicorn, Python-DotEnv, Pydantic

## 📁 Project Structure

```
legal_rag_system/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── src/                      # Source code
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── document_processor.py # Document loading & chunking
│   ├── vector_store.py      # ChromaDB operations
│   └── llm_service.py       # Response generation
├── data/                     # Data directory (for documents)
├── docs/                     # Documentation
└── tests/                    # Test files
```

## 🚀 Features Implemented

### Core Functionality
- **Document Processing Pipeline**: Load and chunk legal documents (PDF, DOCX, TXT, HTML)
- **Metadata Management**: Automatic detection of document types (contracts, case law, statutes)
- **Vector Storage**: Persistent storage and retrieval using ChromaDB
- **Similarity Search**: Semantic search capabilities for finding relevant legal content
- **Query Processing**: Natural language question answering with source attribution
- **REST API Interface**: FastAPI endpoints for document upload and querying

### Planned Features
- Streamlit-based UI for natural language interaction
- Enhanced LLM integration (OpenAI, HuggingFace, or local models)
- Improved citation handling and source verification
- Document versioning and update capabilities
- Batch document processing
- Advanced legal-specific chunking strategies
- User authentication and access control
- Analytics and usage tracking

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd legal_rag_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   # Start the API server
   python src/main.py
   
   # In another terminal, start the Streamlit UI (when implemented)
   # streamlit run src/ui.py
   ```

## 📚 Usage

### API Endpoints

#### Upload Document
```
POST /upload
```
Uploads and processes a legal document for inclusion in the knowledge base.

**Parameters:**
- `file`: Legal document (PDF, DOCX, TXT, HTML)

**Response:**
```json
{
  "message": "Document uploaded and processed successfully",
  "document_id": "generated-id",
  "chunks_created": 15
}
```

#### Query Documents
```
POST /query
```
Ask a question about the legal documents in the knowledge base.

**Parameters:**
```json
{
  "question": "What are the requirements for a valid personal loan agreement?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Based on the legal documents in my knowledge base...",
  "sources": [
    {
      "content": "Relevant text excerpt from document...",
      "metadata": {
        "source": "path/to/document.pdf",
        "document_type": "contract",
        "chunk_id": 3
      }
    }
  ],
  "confidence": 0.85
}
```

## 🛠️ Development

### Running Tests
```bash
# Run tests when implemented
pytest tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints consistently
- Document public APIs with docstrings

## 📖 Legal Document Support

The system is designed to handle various types of legal documents commonly encountered in personal finance:

- **Contracts**: Loan agreements, credit card terms, service contracts
- **Case Law**: Court opinions related to consumer finance, lending practices
- **Statutes & Regulations**: Truth in Lending Act, Fair Credit Reporting Act, etc.
- **Legal Notices**: Privacy policies, terms of service, disclosure statements

## 🔒 Security & Privacy

- Document processing occurs locally or in secure environments
- No sensitive data is transmitted to external services without explicit consent
- Configurable data retention policies
- Role-based access control (planned)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangChain team for the excellent RAG framework
- ChromaDB team for the vector database solution
- FastAPI team for the high-performance API framework
- Streamlit team for rapid prototyping capabilities
- Open-source legal NLP communities

---

*Built with ⚖️ for accessible legal knowledge*