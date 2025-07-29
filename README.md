# 🚀 HackRX - AI-Powered Document Processing API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

A high-performance FastAPI-based service that provides intelligent document processing and question-answering capabilities using advanced LLM integration. Built for the HackRX hackathon, this API enables users to upload documents and get AI-powered answers with both V1 and V2 endpoints for enhanced functionality.

## 🌟 Features

### 🚀 **V2 API - Enhanced Features**

- **🔥 Batch Processing** - Process multiple documents simultaneously
- **📊 Enhanced Metadata** - Processing time, model version, and performance metrics
- **🎯 Advanced Options** - Configurable temperature, max tokens, and processing parameters
- **⚡ Parallel Processing** - Improved efficiency with concurrent document handling

### 🛠️ **Core Features**

- **🤖 AI-Powered Analysis** - Advanced LLM integration with Groq and LangChain
- **📄 Multi-Format Support** - PDF, DOCX, TXT with LlamaParse integration
- **🚀 High-Performance API** - FastAPI with both V1 and V2 endpoints
- **📊 Comprehensive Logging** - Full request/response logging with rotation
- **📖 Interactive Documentation** - Auto-generated Swagger UI and ReDoc
- **🔒 API Key Authentication** - Secure Bearer token authentication with permissions
- **🎨 Interactive Web Interface** - Live API testing with version selection
- **🧠 Semantic Caching** - FAISS-powered caching for improved performance
- **⚡ PyTorch Integration** - CUDA-accelerated processing for enhanced ML capabilities

## 🏗️ Project Structure

```
HackRX/
├── 📄 main.py                    # Application launcher with logging
├── 📄 .env.example              # Environment variables template
├── 📁 Backend/                   # Core API implementation
│   ├── main_api.py              # Main FastAPI application with V1/V2 routes
│   └── api/
│       ├── v1/api.py            # Version 1 API endpoints
│       └── v2/api.py            # Version 2 API endpoints (Enhanced)
├── 📁 Model/                     # AI/ML models and processing
│   ├── MODEL_1/                 # Advanced RAG system with caching
│   │   └── src/                 # Core processing modules
│   │       ├── qa_system.py     # Question-answering system
│   │       ├── document_parser.py # LlamaParse integration
│   │       ├── vectorstore_manager.py # Vector storage
│   │       └── cache_manager.py # Semantic caching with FAISS
│   └── GOAT/                    # Alternative model implementation
├── 📁 utils/                     # Core utilities
│   ├── auth.py                  # Authentication manager
│   ├── logging_config.py        # Logging configuration
│   └── middleware.py            # Request middleware
├── 📁 templates/                 # Web interface
│   └── api_guide.html           # Interactive API documentation with V2 testing
├── 📁 Config/                   # Configuration management
│   ├── config.json             # Application settings
│   ├── api_keys.json           # API key definitions with permissions
│   └── README.md               # Configuration guide
├── 📁 Test/                     # Testing suite
│   ├── comprehensive_test.py   # Full API test suite
│   ├── test_auth.py           # Authentication testing
│   ├── quick_test.py          # Quick validation tests
│   └── example_usage.py       # Usage examples
├── 📁 logs/                     # Application logs (auto-created)
└── 📄 requirements.txt          # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- Git for version control
- CUDA-compatible GPU (optional, for enhanced performance)
- pip package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/vasujunior7/DGX-RAG.git
   cd HackRX
   ```

2. **Set up Python virtual environment**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your API keys:
   # GROQ_API_KEY=your_groq_api_key_here
   # LANGCHAIN_API_KEY=your_langchain_api_key_here
   ```

5. **Run the application**

   ```bash
   python main.py
   ```

6. **Access the API**
   - **🌐 Interactive Web Interface**: http://localhost:8000/
   - **📚 API Documentation**: http://localhost:8000/docs
   - **📋 Alternative Docs**: http://localhost:8000/redoc

## � Authentication

The API uses Bearer token authentication with different permission levels:

```bash
# Available API Keys (for development/testing)
Development: hackrx_2025_dev_key_123456789     # read + write permissions
Production:  hackrx_2025_prod_key_987654321    # read + write permissions
Testing:     hackrx_2025_test_key_555666777    # read-only permissions
```

## �📋 API Endpoints

### 🚀 **V2 API Endpoints (Enhanced)**

| Method | Endpoint               | Description                                     |
| ------ | ---------------------- | ----------------------------------------------- |
| `GET`  | `/api/v2/`             | V2 API welcome with feature list                |
| `POST` | `/api/v2/hackrx/run`   | **Enhanced document processing**                |
| `POST` | `/api/v2/hackrx/batch` | **Batch processing for multiple document sets** |

### 🛠️ **V1 API Endpoints (Standard)**

| Method | Endpoint                | Description                          |
| ------ | ----------------------- | ------------------------------------ |
| `GET`  | `/`                     | Interactive HTML API guide           |
| `GET`  | `/help`                 | Basic API information with endpoints |
| `GET`  | `/api/v1/`              | V1 API welcome message               |
| `GET`  | `/api/v1/auth/status`   | Check authentication status          |
| `GET`  | `/api/v1/auth/validate` | Validate API key and permissions     |
| `POST` | `/api/v1/hackrx/run`    | Standard document processing         |

### 🔥 **V2 API Usage Examples**

**Enhanced Document Processing:**

```bash
curl -X POST "http://localhost:8000/api/v2/hackrx/run" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer hackrx_2025_dev_key_123456789" \
     -d '{
       "documents": [
         "https://example.com/doc1.pdf",
         "https://example.com/doc2.pdf"
       ],
       "questions": [
         "What are the main topics across all documents?",
         "Compare key findings between documents"
       ],
       "options": {
         "enable_batch_processing": true,
         "max_tokens": 2000,
         "temperature": 0.1
       }
     }'
```

**V2 Response with Metadata:**

```json
{
  "answers": [
    "The main topics include...",
    "Comparing the documents reveals..."
  ],
  "metadata": {
    "processing_time": "2.3s",
    "documents_processed": 2,
    "model_version": "v2.1"
  },
  "sources": ["doc1.pdf", "doc2.pdf"]
}
```

**Batch Processing:**

```bash
curl -X POST "http://localhost:8000/api/v2/hackrx/batch" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer hackrx_2025_dev_key_123456789" \
     -d '{
       "batch_requests": [
         {
           "documents": ["doc1.pdf"],
           "questions": ["What is the main topic?"]
         },
         {
           "documents": ["doc2.pdf"],
           "questions": ["What are the key findings?"]
         }
       ],
       "options": {
         "parallel_processing": true,
         "max_concurrent": 3
       }
     }'
```

## 🛠️ Development

### Tech Stack

**Backend:**

- **FastAPI** - High-performance web framework
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server for production

**AI/ML:**

- **LangChain** - LLM framework and utilities
- **Groq** - High-speed LLM inference
- **PyTorch** - Deep learning with CUDA support
- **FAISS** - Vector similarity search and caching
- **Sentence Transformers** - Text embeddings
- **LlamaParse** - Advanced document parsing

**Infrastructure:**

- **Python 3.12+** - Core runtime
- **Virtual Environment** - Dependency isolation
- **Bearer Token Auth** - API security
- **Rotating Logs** - Production-ready logging

### Architecture Overview

```mermaid
graph TB
    A[Client Request] --> B[FastAPI Router]
    B --> C{Version Selection}
    C -->|V1| D[Standard Processing]
    C -->|V2| E[Enhanced Processing]
    D --> F[Document Parser]
    E --> F
    F --> G[Vector Store]
    G --> H[LLM Processing]
    H --> I[Response with Metadata]
    I --> J[Client Response]
```

### Development Workflow

1. **Setup Environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run Development Server**

   ```bash
   python main.py
   ```

4. **Test API**
   - Visit http://localhost:8000/ for interactive testing
   - Use http://localhost:8000/docs for Swagger UI
   - Run tests: `python -m pytest Test/`

### Adding New Features

**For V1 API:**

1. Edit `Backend/api/v1/api.py`
2. Add new endpoints following existing patterns
3. Update documentation in `templates/api_guide.html`

**For V2 API:**

1. Edit `Backend/api/v2/api.py`
2. Implement enhanced features with metadata
3. Add batch processing capabilities
4. Update interactive testing interface

**For Model Features:**

1. Add processing logic in `Model/MODEL_1/src/`
2. Update vector store management
3. Enhance caching mechanisms

## 📊 Logging & Monitoring

### Log Files

The application provides comprehensive logging with automatic rotation:

- **📝 Request Logs**: `logs/requests.log` - All HTTP requests/responses with timing
- **🔧 Application Logs**: `logs/app.log` - Application events and errors
- **🚀 Server Logs**: `logs/uvicorn.log` - Server startup/shutdown events
- **🌐 Access Logs**: `logs/uvicorn_access.log` - HTTP access logs

### Log Features

- **Automatic Rotation**: 10MB max file size, 5 backup files
- **Structured Format**: Timestamp, level, component, message
- **Performance Metrics**: Request processing times
- **Error Tracking**: Detailed error traces and context

### Monitoring Dashboard

View real-time logs and metrics:

```bash
# Tail application logs
tail -f logs/app.log

# Monitor requests
tail -f logs/requests.log

# Check server status
curl http://localhost:8000/api/v1/auth/status
```

## 🧪 Testing

### Quick Test

```bash
# Run all tests
python Test/comprehensive_test.py

# Test authentication
python Test/test_auth.py

# Quick validation
python Test/quick_test.py
```

### Interactive Testing

1. Visit http://localhost:8000/
2. Scroll to "API Testing" section
3. Select API version (V1 or V2)
4. Enter API key: `hackrx_2025_dev_key_123456789`
5. Test with sample data using "Load Sample" button

### Test Coverage

- ✅ Authentication system (7 test scenarios)
- ✅ V1 API endpoints
- ✅ V2 API endpoints with batch processing
- ✅ Document processing pipeline
- ✅ Error handling and validation
- ✅ Performance and caching

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**

   ```bash
   # Set production environment variables
   export GROQ_API_KEY="your_production_groq_key"
   export LANGCHAIN_API_KEY="your_production_langchain_key"
   ```

2. **Run with Production Server**

   ```bash
   # Using Gunicorn for production
   gunicorn Backend.main_api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Docker Deployment** (Optional)
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["python", "main.py"]
   ```

### Performance Optimization

- **CUDA Support**: Automatically detected for PyTorch acceleration
- **Semantic Caching**: FAISS-powered response caching
- **Batch Processing**: V2 API supports parallel document processing
- **Load Balancing**: Ready for horizontal scaling

## 📚 Documentation

### Available Documentation

- **📖 Interactive API Guide**: http://localhost:8000/
- **🔧 Swagger UI**: http://localhost:8000/docs
- **📋 ReDoc**: http://localhost:8000/redoc
- **📁 Component READMEs**: Each folder contains specific documentation

### API Reference

| Component    | Documentation         |
| ------------ | --------------------- |
| 🔧 Backend   | `Backend/README.md`   |
| 🧠 Models    | `Model/README.md`     |
| ⚙️ Config    | `Config/README.md`    |
| 🧪 Testing   | `Test/README.md`      |
| 🎨 Templates | `templates/README.md` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**HackRX Development Team**

- Advanced RAG System Implementation
- FastAPI Backend Architecture
- Interactive Web Interface
- Authentication & Security

## 🎯 HackRX Hackathon

Built for the HackRX hackathon, showcasing:

- **🏆 Advanced AI Integration** - Multi-model LLM processing
- **🚀 High Performance** - V2 API with batch processing
- **🔒 Enterprise Security** - Bearer token authentication
- **📊 Production Ready** - Comprehensive logging and monitoring
- **🎨 User Experience** - Interactive web interface with live testing

---

**🌟 Star this repository if you find it helpful!**

**📞 Support**: For issues and questions, please use the GitHub Issues tab.

**🔗 Links**:

- [Repository](https://github.com/vasujunior7/DGX-RAG)
- [API Documentation](http://localhost:8000/)
- [Interactive Testing](http://localhost:8000/)

Test the API using the interactive documentation:

1. Visit http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in the required parameters
4. Execute the request

Or use curl/Python requests as shown in the examples above.

## 📚 Documentation

- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **API Guide**: http://localhost:8000/ (Custom HTML guide)

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY`: API key for Google's Gemini model (optional for development)

### Logging Configuration

Logging settings can be modified in `main.py` and `utils/logging_config.py`.

### Server Configuration

Server settings (host, port, reload) can be modified in `main.py`.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Check the interactive documentation at `/docs`
- Review the API guide at the root URL

## 🏆 HackRX 2025

This project was built for the HackRX 2025 hackathon, showcasing:

- **Advanced AI Integration**: Document processing with LLM models
- **Production-Ready Architecture**: Comprehensive logging, error handling
- **Developer Experience**: Interactive docs, beautiful web interface
- **Scalable Design**: Versioned APIs, modular structure

---

**Built with ❤️ for HackRX 2025**
