# 🛠️ Utils - API Key Management System

This directory contains utility functions, middleware, and configuration modules that support the core functionality of the HackRX API, with enhanced features for V1/V2 API compatibility and comprehensive API key management.

## 📁 Structure

```
utils/
├── __init__.py              # Package initialization
├── logging_config.py        # Enhanced logging configuration and setup
├── load_env.py             # 🔑 Comprehensive API key manager (NEW)
├── validate_keys.py        # 🔍 API key validation utility (NEW)
├── demo_keys.py           # 📖 API key usage examples (NEW)
├── auth.py                # 🔐 Authentication utilities
└── README.md             # This documentation
```

---

# 🔑 API Key Management System

This directory contains a comprehensive API key management system for the HackRX project, ensuring secure and organized handling of all API credentials.

## 📁 Files Overview

| File               | Purpose                                             |
| ------------------ | --------------------------------------------------- |
| `load_env.py`      | Main API key manager with comprehensive key loading |
| `validate_keys.py` | Validation utility to test API key functionality    |
| `demo_keys.py`     | Demonstration script showing usage examples         |
| `auth.py`          | Authentication utilities for FastAPI endpoints      |

## 🔑 API Key Manager Features

### Comprehensive Key Loading

- **LLM Providers**: OpenAI, Anthropic, Google/Gemini, Groq, Hugging Face, Cohere, Together AI, Replicate
- **Services**: LangChain, Azure, AWS, Pinecone, Weaviate, Chroma
- **Databases**: PostgreSQL, MongoDB, Redis, SQLite
- **Authentication**: API keys, JWT secrets, encryption keys
- **Monitoring**: Sentry, DataDog, New Relic

### Security Features

- Environment variable loading from `.env` files
- JSON config file support with active/inactive keys
- Masked key display for security
- Legacy compatibility mode

## 🚀 Quick Start

### 1. Setup Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit with your actual API keys
nano .env
```

### 2. Basic Usage

```python
from utils.load_env import api_key_manager

# Get a specific API key
openai_key = api_key_manager.get_key('OPENAI_API_KEY')

# Get all LLM provider keys
llm_keys = api_key_manager.get_llm_keys()

# Validate required keys
required = ['GROQ_API_KEY', 'ANTHROPIC_API_KEY']
validation = api_key_manager.validate_required_keys(required)
```

### 3. Legacy Compatibility

```python
# Old way (still works)
from utils.load_env import env_vars, OPENAI_API_KEY

# New way (recommended)
from utils.load_env import api_key_manager
api_key = api_key_manager.get_key('OPENAI_API_KEY')
```

## 🛠️ Validation & Testing

### Basic Validation

```bash
# Check key status
python utils/demo_keys.py

# Validate key formats
python utils/validate_keys.py

# Test actual API connectivity
python utils/validate_keys.py --test-llm

# Verbose output
python utils/validate_keys.py --verbose

# Save validation report
python utils/validate_keys.py --output validation_report.json
```

### Integration Testing

```python
from utils.validate_keys import APIKeyValidator

validator = APIKeyValidator(verbose=True)
results = validator.validate_all_keys(test_connectivity=True)
validator.print_summary(results)
```

## 📊 Key Categories

### 🤖 LLM Providers

| Provider     | Environment Variable  | Get Key From                             |
| ------------ | --------------------- | ---------------------------------------- |
| OpenAI       | `OPENAI_API_KEY`      | https://platform.openai.com/api-keys     |
| Anthropic    | `ANTHROPIC_API_KEY`   | https://console.anthropic.com/           |
| Google AI    | `GOOGLE_API_KEY`      | https://makersuite.google.com/app/apikey |
| Groq         | `GROQ_API_KEY`        | https://console.groq.com/                |
| Hugging Face | `HUGGINGFACE_API_KEY` | https://huggingface.co/settings/tokens   |

### 🔧 Services

| Service      | Environment Variable   | Purpose                  |
| ------------ | ---------------------- | ------------------------ |
| LangChain    | `LANGCHAIN_API_KEY`    | Tracing and monitoring   |
| Azure OpenAI | `AZURE_OPENAI_API_KEY` | Enterprise OpenAI access |
| AWS          | `AWS_ACCESS_KEY_ID`    | Cloud services           |
| Pinecone     | `PINECONE_API_KEY`     | Vector database          |

### 🗄️ Databases

| Database   | Environment Variable | Example                               |
| ---------- | -------------------- | ------------------------------------- |
| PostgreSQL | `DATABASE_URL`       | `postgresql://user:pass@host:5432/db` |
| MongoDB    | `MONGODB_URI`        | `mongodb://localhost:27017/db`        |
| Redis      | `REDIS_URL`          | `redis://localhost:6379/0`            |

## 🔒 Security Best Practices

### Environment Variables

- Always use `.env` files for local development
- Never commit `.env` files to version control
- Use environment variables in production
- Rotate API keys regularly

### Key Validation

```python
# Always validate keys before use
api_key = api_key_manager.get_key('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not configured")
```

### Error Handling

```python
try:
    # Use API key
    client = SomeAPIClient(api_key=api_key)
except Exception as e:
    logger.error(f"API key validation failed: {e}")
    # Handle gracefully
```

## 🏗️ Integration Examples

### FastAPI Dependency

```python
from utils.load_env import api_key_manager
from fastapi import Depends, HTTPException

def get_openai_client():
    api_key = api_key_manager.get_key('OPENAI_API_KEY')
    if not api_key:
        raise HTTPException(400, "OpenAI API key not configured")
    return OpenAI(api_key=api_key)

@app.post("/generate")
async def generate(client = Depends(get_openai_client)):
    # Use client safely
    pass
```

### LangChain Integration

```python
from utils.load_env import api_key_manager
from langchain_anthropic import ChatAnthropic

def create_llm():
    api_key = api_key_manager.get_key('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("Anthropic API key required")

    return ChatAnthropic(
        anthropic_api_key=api_key,
        model="claude-3-sonnet-20240229"
    )
```

### Startup Validation

```python
from utils.load_env import api_key_manager

def validate_environment():
    """Validate environment at application startup"""
    required_keys = [
        'GROQ_API_KEY',
        'ANTHROPIC_API_KEY',
        'DATABASE_URL'
    ]

    validation = api_key_manager.validate_required_keys(required_keys)
    missing_keys = [k for k, v in validation.items() if not v]

    if missing_keys:
        raise EnvironmentError(
            f"Missing required API keys: {', '.join(missing_keys)}"
        )

    print("✅ Environment validation passed")

# Call during app startup
validate_environment()
```

## 🐛 Troubleshooting

### Common Issues

1. **Keys not loading**

   ```bash
   # Check if .env file exists
   ls -la .env

   # Verify file format
   python utils/demo_keys.py
   ```

2. **API connectivity issues**

   ```bash
   # Test actual API calls
   python utils/validate_keys.py --test-llm
   ```

3. **Permission errors**
   ```bash
   # Check file permissions
   chmod 600 .env
   ```

### Debug Mode

```python
# Enable verbose logging
import os
os.environ['SILENT_LOAD'] = 'false'

from utils.load_env import api_key_manager
api_key_manager.print_key_status()
```

## 📈 Advanced Usage

### Custom Key Validation

```python
def validate_custom_api_key(api_key: str) -> bool:
    """Custom validation logic"""
    if not api_key or len(api_key) < 20:
        return False
    # Add your custom validation
    return True

# Use in your application
api_key = api_key_manager.get_key('CUSTOM_API_KEY')
if not validate_custom_api_key(api_key):
    raise ValueError("Invalid custom API key")
```

### Dynamic Key Loading

```python
# Load keys at runtime
def load_runtime_keys():
    """Load additional keys at runtime"""
    runtime_keys = {
        'RUNTIME_KEY': os.getenv('RUNTIME_KEY'),
        'DYNAMIC_KEY': get_key_from_vault()
    }
    api_key_manager._api_keys.update(runtime_keys)
```

### Health Check Endpoint

```python
@app.get("/health/keys")
async def health_check_keys():
    """Health check for API keys"""
    llm_keys = api_key_manager.get_llm_keys()
    service_keys = api_key_manager.get_service_keys()

    return {
        "llm_providers": len(llm_keys),
        "services": len(service_keys),
        "status": "healthy" if llm_keys else "degraded"
    }
```

## 📚 Reference

### Available Methods

| Method                         | Description                | Returns           |
| ------------------------------ | -------------------------- | ----------------- |
| `get_key(name)`                | Get specific API key       | `Optional[str]`   |
| `get_all_keys()`               | Get all loaded keys        | `Dict[str, Any]`  |
| `get_llm_keys()`               | Get LLM provider keys only | `Dict[str, str]`  |
| `get_service_keys()`           | Get service keys only      | `Dict[str, str]`  |
| `validate_required_keys(keys)` | Validate required keys     | `Dict[str, bool]` |
| `print_key_status()`           | Print status report        | `None`            |

### Environment Variables

See `.env.example` for complete list of supported environment variables.

---

💡 **Pro Tip**: Use `python utils/validate_keys.py --summary` for a quick status overview of all your API keys!

---

# 🛠️ Original Utils Documentation

├── middleware.py # Custom middleware implementations (V1/V2 compatible)
├── auth.py # Authentication and authorization utilities
├── validators.py # Request/response validation utilities
├── performance.py # Performance monitoring and metrics
└── **pycache**/ # Python bytecode cache

````

## 🚀 Components

### `logging_config.py` (Enhanced)

- **Comprehensive logging setup** for the entire V1/V2 API application
- **Multiple log types** with separate files and intelligent rotation
- **Production-ready configuration** with advanced features
- **V2 enhancements**: Batch processing logs, metadata tracking

**Key Functions:**

```python
def setup_logging() -> None:
    """Initialize all loggers with V1/V2 support"""

def get_request_logger() -> logging.Logger:
    """Get request-specific logger with enhanced formatting"""

def get_app_logger() -> logging.Logger:
    """Get application logger with performance tracking"""

def get_performance_logger() -> logging.Logger:
    """Get performance metrics logger (V2 feature)"""

def log_api_metrics(endpoint: str, version: str, duration: float) -> None:
    """Log API performance metrics (V2 enhanced)"""
````

**Enhanced Log Types:**

- 📝 **Request Logs** - HTTP request/response details with V1/V2 differentiation
- 📱 **Application Logs** - Business logic, errors, and V2 batch operations
- 🖥️ **Server Logs** - Uvicorn server events and health monitoring
- 📊 **Performance Logs** - V2 feature: API metrics, response times, throughput
- 🔍 **Debug Logs** - Detailed debugging with V2 batch processing info

### `middleware.py` (V1/V2 Compatible)

- **Enhanced middleware** for V1/V2 request processing
- **Smart request logging** with API version detection
- **Performance monitoring** with enhanced timing data
- **V2 features**: Batch request handling, metadata collection

**Class: `RequestLoggingMiddleware` (Enhanced)**

```python
class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        """Enhanced middleware with V1/V2 support"""
        # V2 features: API version detection, batch request handling
        # Enhanced logging with metadata collection
```

**Features:**

- ✅ **V1/V2 API Detection** - Automatically detects API version
- ✅ **Batch Request Logging** - Special handling for V2 batch operations
- ✅ **Enhanced Timing** - More granular performance metrics
- ✅ **Metadata Collection** - V2 feature: collects processing metadata
- ✅ **Smart Body Logging** - Intelligent request/response body handling
- ✅ **Security Enhanced** - Advanced token masking and sanitization

### `auth.py` (New - V2 Enhanced)

- **Authentication utilities** for V1/V2 API endpoints
- **Permission management** with version-specific access control
- **API key validation** with enhanced security features

**Key Functions:**

```python
def validate_api_key(key: str) -> Dict[str, Any]:
    """Validate API key and return permissions"""

def check_api_version_access(key_permissions: List[str], version: str) -> bool:
    """Check if API key has access to specific version"""

def get_rate_limits(api_key: str) -> Dict[str, int]:
    """Get rate limits for specific API key"""

def mask_sensitive_data(data: str) -> str:
    """Enhanced data masking for logs"""
```

### `validators.py` (New - V2 Enhanced)

- **Request/response validation** for both API versions
- **Schema validation** with V1/V2 specific rules
- **Data sanitization** and security validation

**Key Functions:**

```python
def validate_v1_request(data: Dict) -> bool:
    """Validate V1 API request format"""

def validate_v2_request(data: Dict) -> bool:
    """Validate V2 API request with batch support"""

def sanitize_input(data: Any) -> Any:
    """Sanitize user input for security"""

def validate_response_schema(response: Dict, version: str) -> bool:
    """Validate API response against schema"""
```

### `performance.py` (New - V2 Feature)

- **Performance monitoring** and metrics collection
- **API usage analytics** with V1/V2 comparison
- **Resource usage tracking** for optimization

**Key Functions:**

```python
def track_request_performance(endpoint: str, duration: float, version: str) -> None:
    """Track API request performance"""

def get_performance_metrics() -> Dict[str, Any]:
    """Get comprehensive performance metrics"""

def monitor_resource_usage() -> Dict[str, float]:
    """Monitor CPU, memory, and other resources"""
```

## 📊 Enhanced Logging Configuration

### Log Files (V2 Enhanced)

| File                      | Purpose       | Content                           | V2 Enhancements                                 |
| ------------------------- | ------------- | --------------------------------- | ----------------------------------------------- |
| `logs/requests.log`       | HTTP Requests | Request/response details, timing  | API version tracking, batch request metrics     |
| `logs/app.log`            | Application   | Business logic, errors, events    | V2 batch operation logs, enhanced error context |
| `logs/performance.log`    | Performance   | API metrics, response times       | **NEW**: Detailed performance analytics         |
| `logs/security.log`       | Security      | Authentication, authorization     | **NEW**: Enhanced security event tracking       |
| `logs/uvicorn.log`        | Server        | Server startup, shutdown, reloads | Health monitoring, resource usage               |
| `logs/uvicorn_access.log` | Access        | Server access logs                | Enhanced with API version info                  |

### Enhanced Log Rotation

- **Max File Size**: 10MB per log file (configurable)
- **Backup Count**: 5 backup files retained (configurable)
- **Format**: Enhanced timestamped with API version and request ID
- **Compression**: Automatic compression of rotated logs (V2 feature)
- **Cleanup**: Automatic cleanup of old logs (V2 feature)

### Enhanced Log Levels

- **DEBUG**: Detailed debugging with V2 batch processing details
- **INFO**: Normal operations, requests with enhanced context
- **WARNING**: Potential issues with suggested actions
- **ERROR**: Error conditions with enhanced stack traces
- **CRITICAL**: System failures requiring immediate attention

### V2 Performance Metrics

```json
{
  "timestamp": "2025-07-26T10:30:00Z",
  "api_version": "v2",
  "endpoint": "/api/v2/hackrx/run",
  "request_id": "req-123456",
  "performance": {
    "total_duration": 2.341,
    "model_processing_time": 1.876,
    "document_loading_time": 0.234,
    "response_formatting_time": 0.231
  },
  "resources": {
    "cpu_usage": 45.2,
    "memory_usage": 234.5,
    "gpu_usage": 67.8
  },
  "batch_info": {
    "documents_processed": 3,
    "questions_answered": 5,
    "parallel_processes": 2
  }
}
```

## 🔧 Enhanced Logging Setup

### Basic Setup (V1/V2 Compatible)

```python
from utils.logging_config import setup_logging, get_app_logger, get_performance_logger

# Initialize enhanced logging
setup_logging()

# Get loggers
app_logger = get_app_logger()
perf_logger = get_performance_logger()

# Use loggers with V2 enhancements
app_logger.info("Application started", extra={
    "api_versions": ["v1", "v2"],
    "features_enabled": ["batch_processing", "metadata_tracking"]
})

# Log performance metrics (V2 feature)
perf_logger.info("API performance", extra={
    "endpoint": "/api/v2/hackrx/run",
    "duration": 2.341,
    "version": "v2"
})
```

### Request Logging with V2 Features

```python
from utils.logging_config import get_request_logger

# Get enhanced request logger
request_logger = get_request_logger()

# Log V1 request
request_logger.info("V1 API request", extra={
    "api_version": "v1",
    "endpoint": "/api/v1/hackrx/run",
    "documents": 1,
    "questions": 3
})

# Log V2 batch request
request_logger.info("V2 batch request", extra={
    "api_version": "v2",
    "endpoint": "/api/v2/hackrx/run",
    "documents": 5,
    "questions": 10,
    "batch_size": 5,
    "parallel_processing": True
})
```

### Performance Monitoring (V2 Feature)

```python
from utils.performance import track_request_performance, get_performance_metrics

# Track individual request performance
track_request_performance(
    endpoint="/api/v2/hackrx/run",
    duration=2.341,
    version="v2",
    metadata={
        "documents_processed": 3,
        "batch_size": 3,
        "model_used": "gemini-1.5-flash"
    }
)

# Get comprehensive metrics
metrics = get_performance_metrics()
print(f"Average V2 response time: {metrics['v2']['avg_response_time']}")
print(f"V2 throughput: {metrics['v2']['requests_per_minute']}")
```

## 📋 Middleware Details

### `RequestLoggingMiddleware`

**Features:**

- ✅ **Request Timing** - Measures processing time
- ✅ **Client Information** - IP address, user agent
- ✅ **Request Details** - Method, URL, headers
- ✅ **Body Logging** - POST/PUT request bodies (with size limits)
- ✅ **Security** - Masks authorization tokens
- ✅ **JSON Format** - Structured logging for easy parsing

**Logged Information:**

```json
{
  "timestamp": "2025-07-25 22:37:26",
  "client_ip": "127.0.0.1",
  "method": "POST",
  "url": "http://localhost:8000/api/v1/hackrx/run",
  "status_code": 200,
  "process_time": 0.005,
  "user_agent": "python-requests/2.32.3",
  "content_type": "application/json",
  "authorization": "Bearer ***",
  "request_body": "{\"documents\": \"...\", \"questions\": [...]}"
}
```

### Security Features

- **Token Masking**: Authorization headers are masked as "Bearer \*\*\*"
- **Body Size Limits**: Large request bodies are truncated
- **Sensitive Data**: No sensitive data logged in plain text

## 🔧 Configuration Options

### Logging Configuration

Edit `logging_config.py` to modify:

```python
# File rotation settings
maxBytes=10*1024*1024  # 10MB
backupCount=5          # 5 backup files

# Log format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log levels
logger.setLevel(logging.INFO)
```

### Middleware Configuration

Edit `middleware.py` to modify:

```python
# Request body size limit
if len(request_body) < 1000:  # Log if < 1000 chars
    log_data["request_body"] = request_body
else:
    log_data["request_body"] = "Body too large"
```

## 🚀 Usage in Application

### FastAPI Integration

```python
from fastapi import FastAPI
from utils.middleware import RequestLoggingMiddleware
from utils.logging_config import setup_logging

# Setup logging
setup_logging()

# Create app
app = FastAPI()

# Add middleware
app.add_middleware(RequestLoggingMiddleware)
```

### Manual Logging

```python
from utils.logging_config import get_app_logger

logger = get_app_logger()

def my_function():
    logger.info("Function started")
    try:
        # Some operation
        result = do_something()
        logger.info(f"Operation completed: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in function: {str(e)}")
        raise
```

## 📊 Log Analysis

### Reading Logs

```bash
# View latest requests
tail -f logs/requests.log

# Search for errors
grep "ERROR" logs/app.log

# View server status
tail logs/uvicorn.log
```

### Log Parsing

```python
import json

# Parse request logs
with open('logs/requests.log', 'r') as f:
    for line in f:
        if 'REQUEST:' in line:
            # Extract JSON part
            json_part = line.split('REQUEST: ')[1]
            data = json.loads(json_part)
            print(f"Request: {data['method']} {data['url']}")
```

## 🔄 Adding New Utilities

### Adding New Middleware

1. Create new middleware in `middleware.py`:

```python
class NewMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Your middleware logic
        response = await call_next(request)
        return response
```

2. Add to FastAPI app:

```python
app.add_middleware(NewMiddleware)
```

### Adding New Loggers

1. Modify `logging_config.py`:

```python
def setup_new_logger():
    logger = logging.getLogger("new_logger")
    # Configure logger
    return logger
```

2. Use in application:

```python
from utils.logging_config import setup_new_logger
logger = setup_new_logger()
```

## 🧪 Testing Utilities

### Test Logging

```python
# Test logging setup
python -c "
from utils.logging_config import setup_logging, get_app_logger
setup_logging()
logger = get_app_logger()
logger.info('Test log message')
print('Check logs/app.log for the message')
"
```

### Test Middleware

```python
# Middleware is tested automatically when making requests
# Check logs/requests.log for request logging
curl http://localhost:8000/
```

## 📋 Best Practices

### Logging

- Use appropriate log levels (INFO, WARNING, ERROR)
- Include context in log messages
- Don't log sensitive information
- Use structured logging (JSON) for parsing

### Middleware

- Keep middleware lightweight
- Handle errors gracefully
- Don't modify request/response unless necessary
- Log relevant information for debugging

## 🔒 Security Considerations

- **Sensitive Data**: Never log passwords, full API keys
- **Request Bodies**: Limit size and content of logged bodies
- **File Permissions**: Ensure log files have appropriate permissions
- **Retention**: Consider log retention policies for compliance

---

**Utility Components Supporting the HackRX API**
