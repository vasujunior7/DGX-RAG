# 🛠️ Utils

This directory contains utility functions, middleware, and configuration modules that support the core functionality of the HackRX API, with enhanced features for V1/V2 API compatibility.

## 📁 Structure

```
utils/
├── __init__.py              # Package initialization
├── logging_config.py        # Enhanced logging configuration and setup
├── middleware.py            # Custom middleware implementations (V1/V2 compatible)
├── auth.py                  # Authentication and authorization utilities
├── validators.py            # Request/response validation utilities
├── performance.py           # Performance monitoring and metrics
└── __pycache__/            # Python bytecode cache
```

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
```

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
