# 🔧 Backend - FastAPI Multi-Model RAG Architecture

Production-ready FastAPI backend supporting multi-model AI integration with AURA Legal AI, SAM Insurance AI, and comprehensive API versioning for the HackRX RAG system.

## 📁 Architecture Overview

```
Backend/
├── 🚀 Core Application
│   ├── main_api.py              # Main FastAPI app with multi-model routing
│   └── __init__.py              # Package initialization
└── 🔌 API Endpoints
    └── api/                     # Versioned API architecture
        ├── __init__.py          # API package initialization
        ├── v1/                  # Legacy API endpoints
        │   ├── __init__.py      # V1 package init
        │   └── api.py           # V1 standard endpoints
        └── v2/                  # Enhanced API endpoints
            ├── __init__.py      # V2 package init
            └── api.py           # V2 enhanced features with metadata
```

## 🚀 Core Components

### 🎯 **main_api.py** - Central Application Hub

**FastAPI Application Features:**

```python
# Multi-model RAG system with comprehensive features
app = FastAPI(
    title="HackRX Multi-Model RAG API",
    description="Advanced RAG system with AURA Legal AI, SAM Insurance AI",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

**Integrated Systems:**
- ✅ **Multi-Model AI Integration** - Anthropic, OpenAI, Gemini, Groq support
- ✅ **Specialized AI Models** - AURA (Legal), SAM (Insurance)
- ✅ **API Versioning** - V1 (Legacy) and V2 (Enhanced) endpoints
- ✅ **Authentication Middleware** - Bearer token validation
- ✅ **Request Logging** - Comprehensive request/response tracking
- ✅ **Template Rendering** - Jinja2 for interactive documentation
- ✅ **CORS Configuration** - Cross-origin request support
- ✅ **Error Handling** - Production-ready error responses

**Core Endpoints:**
```python
# Interactive documentation
@app.get("/")
async def root() -> HTMLResponse

# API information
@app.get("/help")  
async def help_endpoint()

# Health check
@app.get("/health")
async def health_check()
```

### 🔌 **API v1** - Legacy Standard Processing

**Location:** `api/v1/api.py`

**V1 Features:**
- 🔧 **Standard Processing** - Single document processing
- 🔐 **Basic Authentication** - Bearer token validation  
- 📊 **Simple Logging** - Request/response logging
- 🧠 **Model Integration** - Basic LLM inference

**V1 Endpoints:**
```python
# V1 API status
@v1_router.get("/")
async def v1_welcome()

# Legacy document processing
@v1_router.post("/hackrx/run")  
async def hackrx_run_v1(request: DocumentRequest)
```

### 🚀 **API v2** - Enhanced Multi-Model Processing

**Location:** `api/v2/api.py`

**V2 Enhanced Features:**
- 🔥 **Multi-Model Support** - Anthropic, OpenAI, Gemini, Groq
- ⚖️ **AURA Legal AI** - Specialized legal document processing
- 🛡️ **SAM Insurance AI** - Advanced insurance policy analysis
- � **Enhanced Metadata** - Processing time, model info, performance metrics
- 🎯 **Batch Processing** - Multiple document processing capabilities  
- ⚡ **Parallel Processing** - Concurrent request handling
- � **Fallback Systems** - Automatic model switching for reliability

**V2 Main Endpoints:**
```python  
# V2 API status with features
@v2_router.get("/")
async def v2_welcome()

# Enhanced document processing (current format)
@v2_router.post("/hackrx/run")
async def hackrx_run_v2(request: EnhancedDocumentRequest)

# Batch processing
@v2_router.post("/hackrx/batch") 
async def hackrx_batch_v2(request: BatchDocumentRequest)
```

**V2 Specialized AI Endpoints:**
```python
# AURA Legal AI endpoints
@v2_router.post("/aura/legal-query")
async def aura_legal_query(request: LegalQueryRequest)

@v2_router.post("/aura/case-law")  
async def aura_case_law(request: CaseLawRequest)

# SAM Insurance AI endpoints
@v2_router.post("/sam/policy-analysis")
async def sam_policy_analysis(request: PolicyAnalysisRequest)

@v2_router.post("/sam/claims-processing")
async def sam_claims_processing(request: ClaimsRequest)
```

## 📊 Request/Response Models

### 🎯 **Current V2 API Format** (Production)

**Request Format:**
```json
{
    "documents": "https://example.com/document.pdf",
    "questions": [
        "What is the grace period for premium payment?",
        "What are the waiting periods for pre-existing conditions?", 
        "Does this policy cover maternity expenses?"
    ]
}
```

**Response Format:**
```json
{
    "answers": [
        "The grace period for premium payment is 30 days...",
        "Pre-existing diseases have a waiting period of 24 months...",
        "Maternity expenses are covered after 10 months..."
    ],
    "metadata": {
        "processing_time": "2.3s",
        "model_used": "anthropic-claude-3.5-sonnet",
        "documents_processed": 1,
        "api_version": "v2.1"
    }
}
```

### ⚖️ **AURA Legal AI Format**

**Request:**
```json
{
    "document_url": "https://example.com/contract.pdf",
    "legal_questions": [
        "What are the termination clauses?",
        "Are there any penalty provisions?",
        "What is the governing law?"
    ],
    "analysis_type": "comprehensive"
}
```

### 🛡️ **SAM Insurance AI Format**

**Request:**
```json
{
    "policy_document": "https://example.com/policy.pdf", 
    "analysis_type": "claims_evaluation",
    "questions": [
        "What is the coverage amount?",
        "What are the exclusions?",
        "What is the claim settlement process?"
    ]
}
```

**V1 Endpoints:**

- `GET /api/v1/` - Welcome message
- `GET /api/v1/auth/status` - Authentication status
- `GET /api/v1/auth/validate` - API key validation
- `POST /api/v1/hackrx/run` - Document processing

### `api/v2/api.py` - Enhanced API

**V2 Features:**

- 🔥 **Batch Processing** - Multiple document handling
- 📊 **Enhanced Metadata** - Processing time, model version
- ⚡ **Parallel Processing** - Concurrent document processing
- 🎯 **Advanced Options** - Configurable parameters
- 🧠 **Improved Models** - Enhanced AI processing

**V2 Endpoints:**

- `GET /api/v2/` - Enhanced welcome with features
- `POST /api/v2/hackrx/run` - Enhanced document processing
- `POST /api/v2/hackrx/batch` - Batch processing endpoint

## 🔑 Authentication System

### API Key Management

```python
# Located in utils/auth.py
class AuthManager:
    - validate_api_key()
    - check_permissions()
    - load_configuration()
```

### Permission Levels

- **Read**: Access to GET endpoints and validation
- **Write**: Access to POST endpoints and processing

### Available Keys (Development)

```
Development: hackrx_2025_dev_key_123456789  # read + write
Production:  hackrx_2025_prod_key_987654321 # read + write
Testing:     hackrx_2025_test_key_555666777 # read only
```

## 🔗 Dependencies

### Internal Dependencies

- **utils.middleware** - Request logging and authentication middleware
- **utils.logging_config** - Comprehensive logging setup
- **utils.auth** - Authentication and API key management
- **Model.sample_model** - AI model integration and inference

### External Dependencies

- **fastapi** - Modern web framework for building APIs
- **pydantic** - Data validation and serialization
- **jinja2** - Template engine for HTML responses
- **uvicorn** - ASGI server for production deployment

## 📊 API Versioning Strategy

The backend implements semantic API versioning for backward compatibility:

### Current Versions

- **V1**: Stable API with standard document processing
- **V2**: Enhanced API with batch processing and metadata

### Version Features Comparison

| Feature             | V1  | V2  |
| ------------------- | --- | --- |
| Single Document     | ✅  | ✅  |
| Multiple Documents  | ❌  | ✅  |
| Batch Processing    | ❌  | ✅  |
| Response Metadata   | ❌  | ✅  |
| Processing Options  | ❌  | ✅  |
| Parallel Processing | ❌  | ✅  |

### Adding New Versions

1. Create version directory: `api/v3/`
2. Implement enhanced routes in `api/v3/api.py`
3. Include router in `main_api.py`
4. Update documentation and tests

## 🛠️ Request/Response Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant M as Middleware
    participant R as Router
    participant A as Auth
    participant H as Handler
    participant L as LLM

    C->>M: HTTP Request
    M->>A: Validate API Key
    A-->>M: Auth Status
    M->>R: Route Request
    R->>H: Handler Execution
    H->>L: LLM Processing
    L-->>H: AI Response
    H-->>R: Formatted Response
    R-->>M: HTTP Response
    M-->>C: Final Response
```

## 📝 Request/Response Models

### V1 Models

```python
# V1 Request
class HackRXRequest(BaseModel):
    documents: str              # Single document URL
    questions: List[str]        # Questions list

# V1 Response
class HackRXResponse(BaseModel):
    answers: List[str]          # AI-generated answers
```

### V2 Models

```python
# V2 Request
class HackRXV2Request(BaseModel):
    documents: Union[str, List[str]]  # Single or multiple documents
    questions: List[str]              # Questions list
    options: Optional[Dict]           # Processing options

# V2 Response
class HackRXV2Response(BaseModel):
    answers: List[str]                # AI-generated answers
    metadata: Dict                    # Processing metadata
    sources: List[str]                # Source documents
```

## 🔧 Configuration

### Application Settings

```python
app = FastAPI(
    title="HackRX API",
    description="API for HackRX project with LLM integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

### Middleware Stack

1. **RequestLoggingMiddleware** - HTTP request/response logging
2. **AuthenticationMiddleware** - API key validation
3. **CORSMiddleware** - Cross-origin request handling

### Router Configuration

```python
# V1 API
app.include_router(v1_router, prefix="/api/v1", tags=["v1"])

# V2 API
app.include_router(v2_router, prefix="/api/v2", tags=["v2"])
```

## 🧪 Testing

### Test Backend Components

```bash
# Test V1 endpoints
curl -X GET "http://localhost:8000/api/v1/"

# Test authentication
curl -X GET "http://localhost:8000/api/v1/auth/status"

# Test V2 enhanced endpoints
curl -X GET "http://localhost:8000/api/v2/"

# Test document processing
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
     -H "Authorization: Bearer hackrx_2025_dev_key_123456789" \
     -H "Content-Type: application/json" \
     -d '{"documents": "test.pdf", "questions": ["What is this?"]}'
```

### Performance Testing

```bash
# Load testing with ab
ab -n 100 -c 10 http://localhost:8000/api/v1/

# Stress testing endpoints
python Test/comprehensive_test.py
```

## 🚀 Deployment

### Development

```bash
# Run with auto-reload
python main.py
```

### Production

```bash
# Using Gunicorn with Uvicorn workers
gunicorn Backend.main_api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY Backend/ ./Backend/
COPY utils/ ./utils/
COPY Model/ ./Model/
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "Backend.main_api:app", "-k", "uvicorn.workers.UvicornWorker"]
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Models**: https://pydantic-docs.helpmanual.io/
- **Uvicorn Server**: https://www.uvicorn.org/
- **API Testing**: Use the interactive docs at `/docs`

```bash
# Test main endpoint
curl http://localhost:8000/

# Test v1 API
curl http://localhost:8000/api/v1/

# Test document processing
curl -X POST http://localhost:8000/api/v1/hackrx/run \
     -H "Content-Type: application/json" \
     -d '{"documents": "test.pdf", "questions": ["What is this?"]}'
```

## 📋 Error Handling

The backend implements comprehensive error handling:

- **HTTP 422**: Validation errors (Pydantic)
- **HTTP 500**: Internal server errors
- **Custom exceptions**: Model processing errors

## 🔗 Integration Points

### Model Integration

- Imports `SampleModel` from `Model/` directory
- Initializes model instance with API key
- Calls model methods for document processing

### Logging Integration

- Uses `utils.logging_config` for application logging
- Integrates with `utils.middleware` for request logging

### Template Integration

- Serves HTML templates from `templates/` directory
- Provides interactive API documentation

---

**Part of the HackRX API Backend Architecture**
