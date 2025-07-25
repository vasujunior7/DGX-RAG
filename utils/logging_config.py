import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Setup logging configuration for the application
    """
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Configure request logger
    request_logger = logging.getLogger("request_logger")
    request_logger.setLevel(logging.INFO)
    
    # Request log file handler with rotation
    request_handler = RotatingFileHandler(
        os.path.join(logs_dir, "requests.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Request log formatter
    request_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    request_handler.setFormatter(request_formatter)
    request_logger.addHandler(request_handler)
    
    # Configure uvicorn/server logger
    server_logger = logging.getLogger("uvicorn.access")
    server_handler = RotatingFileHandler(
        os.path.join(logs_dir, "uvicorn.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Server log formatter
    server_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    server_handler.setFormatter(server_formatter)
    server_logger.addHandler(server_handler)
    
    # Configure application logger
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)
    
    app_handler = RotatingFileHandler(
        os.path.join(logs_dir, "app.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    app_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app_handler.setFormatter(app_formatter)
    app_logger.addHandler(app_handler)
    
    return request_logger, app_logger

def get_request_logger():
    """Get the request logger instance"""
    return logging.getLogger("request_logger")

def get_app_logger():
    """Get the application logger instance"""
    return logging.getLogger("app")
