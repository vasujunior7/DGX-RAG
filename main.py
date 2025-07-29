import uvicorn
import logging.config
import threading
import time
import os
import sys
import webbrowser
from pathlib import Path
import http.server
import socketserver

from functools import partial

# Logging configuration for uvicorn
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "access": {
            "format": "%(asctime)s - %(levelname)s - %(client_addr)s - %(request_line)s - %(status_code)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/uvicorn.log",
            "maxBytes": 10*1024*1024,  # 10MB
            "backupCount": 5,
        },
        "access": {
            "formatter": "access",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/uvicorn_access.log",
            "maxBytes": 10*1024*1024,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

def run_fastapi_server():
    """Run the FastAPI server"""
    print("🚀 Starting FastAPI server on http://localhost:8000")
    uvicorn.run(
        "Backend.main_api:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,  # Disable reload to work in thread
        log_level="info"
    )

def run_html_server():
    """Run a simple HTTP server for the HTML frontend"""
    print("🌐 Starting HTML frontend server on http://localhost:3000")
    frontend_dir = Path(__file__).parent / "Frontend"
    
    if not frontend_dir.exists():
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Create a simple HTTP server
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(frontend_dir), **kwargs)
        
        def end_headers(self):
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
        
        def do_OPTIONS(self):
            self.send_response(200)
            self.end_headers()
    
    try:
        with socketserver.TCPServer(("", 3000), CustomHTTPRequestHandler) as httpd:
            print("✅ HTML server started successfully")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("🛑 HTML server stopped")
    except Exception as e:
        print(f"❌ Failed to start HTML server: {e}")

def open_browsers():
    """Open browsers after a delay"""
    time.sleep(3)  # Wait for servers to start
    print("🌐 Opening browsers...")
    try:
        webbrowser.open("http://localhost:8000")  # Backend API docs
        time.sleep(1)
        webbrowser.open("http://localhost:3000")  # Frontend React app
    except Exception as e:
        print(f"⚠️  Could not open browsers: {e}")
        print("📋 Manual URLs:")
        print("   Backend API: http://localhost:8000")
        print("   Frontend App: http://localhost:3000")

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 HackRX - Complete Application Launcher")
    print("=" * 60)
    print("Starting FastAPI backend and HTML frontend...")
    print("")
    
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
        print("📁 Created logs directory")
    
    try:
        # Start FastAPI server in a separate thread
        fastapi_thread = threading.Thread(target=run_fastapi_server, daemon=True)
        fastapi_thread.start()
        
        # Wait a moment for FastAPI to start
        time.sleep(3)
        
        print("✅ FastAPI server started successfully")
        print("🌐 API Documentation: http://localhost:8000")
        print("📚 Interactive Docs: http://localhost:8000/docs")
        print("🧪 API Testing: http://localhost:8000 (scroll to API Testing section)")
        print("\n🔑 Available API Keys:")
        print("   Development: hackrx_2025_dev_key_123456789")
        print("   Production:  hackrx_2025_prod_key_987654321")
        print("   Testing:     hackrx_2025_test_key_555666777")
        print("\n⌨️  Press Ctrl+C to stop the server")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("✅ All servers stopped successfully")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error running servers: {e}")
        sys.exit(1)