import time
import json
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from utils.logging_config import get_request_logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all incoming requests and responses
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = get_request_logger()
    
    async def dispatch(self, request: Request, call_next):
        # Start time
        start_time = time.time()
        
        # Get request details
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        url = str(request.url)
        headers = dict(request.headers)
        
        # Read request body for POST requests
        request_body = None
        if method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    request_body = body.decode('utf-8')
            except Exception as e:
                request_body = f"Error reading body: {str(e)}"
        
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log request details
        log_data = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "client_ip": client_ip,
            "method": method,
            "url": url,
            "status_code": response.status_code,
            "process_time": round(process_time, 4),
            "user_agent": headers.get("user-agent", "unknown"),
            "content_type": headers.get("content-type", "unknown"),
            "authorization": "Bearer ***" if headers.get("authorization") else None,
            "request_body": request_body if request_body and len(request_body) < 1000 else "Body too large or empty"
        }
        
        # Log the request
        self.logger.info(f"REQUEST: {json.dumps(log_data, indent=2)}")
        
        return response
