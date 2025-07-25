# 🛠️ Utils

This directory contains utility functions, middleware, and configuration modules that support the core functionality of the HackRX API.

## 📁 Structure

```
utils/
├── __init__.py              # Package initialization
├── logging_config.py        # Logging configuration and setup
├── middleware.py            # Custom middleware implementations
└── __pycache__/            # Python bytecode cache
```

## 🚀 Components

### `logging_config.py`

- **Comprehensive logging setup** for the entire application
- **Multiple log types** with separate files and rotation
- **Production-ready configuration** with file rotation

**Key Functions:**

- `setup_logging()` - Initialize all loggers
- `get_request_logger()` - Get request-specific logger
- `get_app_logger()` - Get application logger

**Log Types:**

- 📝 **Request Logs** - HTTP request/response details
- 📱 **Application Logs** - Business logic and errors
- 🖥️ **Server Logs** - Uvicorn server events

### `middleware.py`

- **Custom middleware** for request processing
- **Request logging** with detailed information
- **Performance monitoring** with timing data

**Class: `RequestLoggingMiddleware`**

- Logs all incoming HTTP requests
- Captures request body, headers, and timing
- Formats data as structured JSON

## 📊 Logging Configuration

### Log Files

| File                      | Purpose       | Content                           |
| ------------------------- | ------------- | --------------------------------- |
| `logs/requests.log`       | HTTP Requests | Request/response details, timing  |
| `logs/app.log`            | Application   | Business logic, errors, events    |
| `logs/uvicorn.log`        | Server        | Server startup, shutdown, reloads |
| `logs/uvicorn_access.log` | Access        | Server access logs                |

### Log Rotation

- **Max File Size**: 10MB per log file
- **Backup Count**: 5 backup files retained
- **Format**: Timestamped with rotation numbering

### Log Levels

- **INFO**: Normal operations, requests
- **WARNING**: Potential issues
- **ERROR**: Error conditions
- **DEBUG**: Detailed debugging (if enabled)

## 🔧 Logging Setup

### Basic Setup

```python
from utils.logging_config import setup_logging, get_app_logger

# Initialize logging
setup_logging()

# Get logger
logger = get_app_logger()

# Use logger
logger.info("Application started")
logger.error("Something went wrong")
```

### Request Logging

```python
from utils.logging_config import get_request_logger

# Get request logger
request_logger = get_request_logger()

# Log request details
request_logger.info("User accessed endpoint /api/v1/hackrx/run")
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
