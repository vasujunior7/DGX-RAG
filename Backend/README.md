# 🔧 Backend

This directory contains the core FastAPI application and API implementation for the HackRX project.

## 📁 Structure

```
Backend/
├── main_api.py           # Main FastAPI application
├── __init__.py          # Package initialization
└── api/                 # API version modules
    ├── __init__.py      # API package initialization
    └── v1/              # Version 1 API endpoints
        ├── __init__.py  # V1 package initialization
        └── api.py       # V1 API routes and handlers
```

## 🚀 Components

### `main_api.py`

- **Main FastAPI application instance**
- **Middleware configuration** (request logging)
- **Router inclusion** (API versioning)
- **Template rendering** (HTML guide)
- **Application lifecycle management**

**Key Features:**

- ✅ FastAPI app configuration with metadata
- ✅ Request logging middleware integration
- ✅ Jinja2 template setup for HTML responses
- ✅ API versioning with `/api/v1` prefix
- ✅ Root endpoint serving HTML guide

### `api/v1/api.py`

- **Version 1 API endpoints**
- **Request/response models** (Pydantic)
- **Business logic integration** (Model classes)
- **Error handling and logging**

**Endpoints:**

- `GET /` - V1 welcome message
- `POST /hackrx/run` - Main document processing endpoint

## 🔗 Dependencies

### Internal Dependencies

- `utils.middleware` - Request logging middleware
- `utils.logging_config` - Logging configuration
- `Model.sample_model` - AI model integration

### External Dependencies

- `fastapi` - Web framework
- `pydantic` - Data validation
- `jinja2` - Template rendering

## 📊 API Versioning

The backend implements API versioning to ensure backward compatibility:

- **v1**: Current stable version
- **Future versions**: Can be added as separate modules

### Adding New API Versions

1. Create new version directory: `api/v2/`
2. Implement routes in `api/v2/api.py`
3. Include router in `main_api.py`:
   ```python
   from .api.v2.api import router as v2_router
   app.include_router(v2_router, prefix="/api/v2", tags=["v2"])
   ```

## 🛠️ Request/Response Flow

1. **Request Reception**: FastAPI receives HTTP request
2. **Middleware Processing**: Request logging middleware captures details
3. **Route Matching**: FastAPI routes request to appropriate handler
4. **Model Integration**: Handler calls Model classes for processing
5. **Response Generation**: Pydantic models ensure response format
6. **Logging**: Request completion logged with timing

## 📝 Request Models

### `HackRXRequest`

```python
{
    "documents": "string",      # Document URL or content
    "questions": ["string"]     # List of questions to answer
}
```

### `HackRXResponse`

```python
{
    "answers": ["string"]       # List of AI-generated answers
}
```

## 🔧 Configuration

### Application Settings

- **Title**: "HackRX API"
- **Description**: "API for HackRX project with LLM integration"
- **Version**: "1.0.0"

### Middleware Stack

1. **RequestLoggingMiddleware** - Logs all HTTP requests/responses

### Template Configuration

- **Directory**: `templates/`
- **Engine**: Jinja2

## 🧪 Testing

Test the backend components:

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
