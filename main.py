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
    try:
     uvicorn.run(
        "Backend.main_api:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,  # Disable reload to work in thread
        log_level="info"
    )
    except Exception as e:
        print(f"❌ FastAPI server error: {e}")

def run_html_server():
    """Run a simple HTTP server for the HTML frontend"""
    print("🌐 Starting HTML frontend server on http://localhost:3000")
    
    # Get the project root directory
    project_root = Path(__file__).parent
    frontend_dir = project_root / "Frontend"
    
    if not frontend_dir.exists():
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return
    
    print(f"📁 Serving files from: {frontend_dir}")
    
    # Create a simple HTTP server with custom handler
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(frontend_dir), **kwargs)
        
        def end_headers(self):
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()
        
        def do_OPTIONS(self):
            self.send_response(200)
            self.end_headers()
    
        def do_GET(self):
            # Serve index.html for root path
            if self.path == '/':
                self.path = '/index.html'
            try:
                return super().do_GET()
            except BrokenPipeError:
                # Client disconnected, ignore the error
                pass
            except ConnectionResetError:
                # Client reset connection, ignore the error
                pass
        
        def log_message(self, format, *args):
            # Custom logging for HTTP server - suppress broken pipe errors
            message = format % args
            if "Broken pipe" not in message and "Connection reset" not in message:
                print(f"🌐 Frontend: {message}")
        
        def copyfile(self, source, outputfile):
            # Override copyfile to handle broken pipe gracefully
            try:
                super().copyfile(source, outputfile)
            except BrokenPipeError:
                # Client disconnected while transferring file, ignore
                pass
            except ConnectionResetError:
                # Client reset connection while transferring file, ignore
                pass
    
    try:
        # Allow port reuse
        socketserver.TCPServer.allow_reuse_address = True
        
        with socketserver.TCPServer(("", 3000), CustomHTTPRequestHandler) as httpd:
            print("✅ HTML server started successfully")
            print("📄 Serving index.html from Frontend directory")
            print("🔗 Frontend URL: http://localhost:3000")
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print("❌ Port 3000 is already in use. Please stop any other servers using this port.")
            print("💡 Try running: lsof -ti:3000 | xargs kill -9")
        else:
            print(f"❌ Failed to start HTML server: {e}")
    except KeyboardInterrupt:
        print("🛑 HTML server stopped")
    except Exception as e:
        print(f"❌ HTML server error: {e}")

def open_browsers():
    """Open browsers after a delay"""
    time.sleep(4)  # Wait for servers to start
    print("🌐 Opening browsers...")
    try:
        # Open frontend first (main interface)
        webbrowser.open("http://localhost:3000")
        time.sleep(1)
        # Then API docs (for reference)
        webbrowser.open("http://localhost:8000/docs")
    except Exception as e:
        print(f"⚠️  Could not open browsers: {e}")
        print("📋 Manual URLs:")
        print("   🎨 Frontend App: http://localhost:3000")
        print("   🔧 Backend API: http://localhost:8000")
        print("   📚 API Docs: http://localhost:8000/docs")

def check_port_availability(port):
    """Check if a port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            return True
        except OSError:
            return False

if __name__ == "__main__":
    print("=" * 70)
    print("🎯 HackRX v2.0 - Complete Application Launcher")
    print("=" * 70)
    print("🚀 Starting FastAPI backend and Modern HTML frontend...")
    print("")
    
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
        print("📁 Created logs directory")
    
    # Check port availability
    if not check_port_availability(8000):
        print("❌ Port 8000 is already in use. Please stop any other servers.")
        sys.exit(1)
    
    if not check_port_availability(3000):
        print("❌ Port 3000 is already in use. Please stop any other servers.")
        print("💡 Try running: lsof -ti:3000 | xargs kill -9")
        sys.exit(1)
    
    try:
        # Start FastAPI server in a separate thread
        print("🔧 Starting FastAPI backend...")
        fastapi_thread = threading.Thread(target=run_fastapi_server, daemon=True)
        fastapi_thread.start()
        
        # Start HTML server in a separate thread  
        print("🎨 Starting HTML frontend...")
        html_thread = threading.Thread(target=run_html_server, daemon=True)
        html_thread.start()
        
        # Wait for servers to start
        time.sleep(4)
        
        print("\n" + "=" * 70)
        print("✅ HackRX Platform Started Successfully!")
        print("=" * 70)
        print("🎨 Frontend Application: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 Interactive API Docs: http://localhost:8000/docs")
        print("📖 ReDoc Documentation: http://localhost:8000/redoc")
        print("\n🔑 Available API Keys:")
        print("   Development: hackrx_2025_dev_key_123456789")
        print("   Production:  hackrx_2025_prod_key_987654321")
        print("   Testing:     hackrx_2025_test_key_555666777")
        print("\n🎯 Features:")
        print("   • Modern Glass Morphism UI")
        print("   • Advanced Document Processing")
        print("   • Real-time API Status Monitoring")
        print("   • Export & History Management")
        print("   • Responsive Design")
        print("   • Keyboard Shortcuts (Ctrl+Enter to submit)")
        print("\n⌨️  Press Ctrl+C to stop all servers")
        print("=" * 70)
        
        # Open browsers after a delay
        browser_thread = threading.Thread(target=open_browsers, daemon=True)
        browser_thread.start()
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down all servers...")
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all servers...")
        print("✅ All servers stopped successfully")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error running servers: {e}")
        sys.exit(1)