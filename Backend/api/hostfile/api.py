from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import sys
import os


# Import logging and auth from utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from utils.logging_config import get_app_logger
from utils.auth import auth_manager

# Create APIRouter instance for v1 endpoints
router = APIRouter()

# Get logger
app_logger = get_app_logger()

# Security scheme
security = HTTPBearer(auto_error=False)

# Pydantic models for request/response

FILE_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'cached_pdfs')


@router.get("/")
def read_root():
    return {"message": "Welcome to the HackRX API!",
            "version": "1.0.0",
            "description": "This is the main API for HackRX project with LLM integration.",
            "work":"Hostfile",
            "endpoints":{
                "list_pdfs": "/api/hostfile/list_cached_pdfs",
                "download_pdf": "/api/hostfile/download_pdf/{filename}"
            }
        }
    
@router.get("/list_cached_pdfs")
def list_cached_pdfs():
    """List all cached PDF files"""
    try:
        files = os.listdir(FILE_DIRECTORY)
        pdf_files = [f for f in files if f.endswith('.pdf')]
        return {"cached_pdfs": pdf_files}
    except Exception as e:
        app_logger.error(f"Error listing cached PDFs: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/download_pdf/{filename}")
def download_pdf(filename: str):
    file_path = os.path.join(FILE_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)