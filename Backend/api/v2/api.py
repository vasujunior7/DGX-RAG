from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading

# Add the Model directory to the path so we can import SampleModel
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Model'))
from sample_model import SampleModel , SampleModelPaller

# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Model', 'GOAT'))
# from GOAT.inference import GOATModel

# Using AURA model again
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Model', 'AURA'))
from AURA.infrance import SampleModelPaller

# Commenting out SimpleModel - back to using AURA
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Model', 'simple_'))
# from sample import SampleModel as SimpleModel

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
class HackRXRequest(BaseModel):
    documents: str
    questions: List[str]

class HackRXResponse(BaseModel):
    answers: List[str]

# Initialize the model (you can add proper API key later)
# model = SampleModel(api_key="dummy_key")
# We'll create model instances dynamically for parallel processing
# model = SampleModelPaller()

# Thread pool for parallel processing
executor = ThreadPoolExecutor(max_workers=10)  # Adjust based on your server capacity

def create_model_instance():
    """Create a new model instance for parallel processing"""
    return SampleModelPaller()

# Authentication dependency
async def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Verify API key from Authorization header"""
    if not auth_manager.is_authentication_enabled():
        app_logger.info("Authentication disabled - allowing request")
        return {"valid": True, "bypass": True}
    
    if not auth_manager.is_api_key_required():
        app_logger.info("API key not required - allowing request")
        return {"valid": True, "bypass": True}
    
    if not credentials:
        app_logger.warning("No authorization header provided")
        raise HTTPException(
            status_code=401,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    api_key = credentials.credentials
    key_info = auth_manager.validate_api_key(api_key)
    
    if not key_info:
        app_logger.warning(f"Invalid API key attempted: {api_key[:10]}...")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    app_logger.info(f"Valid API key used: {key_info.get('name', 'Unknown')}")
    return key_info
app_logger.info("Parallel processing setup completed for HackRX API v2 with AURA Model (Anthropic Claude)")

# Define a basic GET endpoint
@router.get("/")
def read_root():
    app_logger.info("V2 root endpoint accessed")
    return {"message": "Welcome to HackRX API", "version": "v2", "endpoints": {
        "hackrx_run": "/api/v2/hackrx/run",
        "auth_status": "/api/v2/auth/status",
        "validate_key": "/api/v2/auth/validate"
    }}

# Define a GET endpoint with a parameter
# @router.get("/hello/{name}")
# def say_hello(name: str):
#     return {"message": f"Hello, {name}!", "version": "v2"}

# Define a POST endpoint
# @router.post("/echo/")
# def echo_data(data: dict):
#     return {"you_sent": data, "version": "v1"}

# Main HackRX endpoint
@router.post("/hackrx/run", response_model=HackRXResponse)
async def hackrx_run(request: HackRXRequest, auth_info: dict = Depends(verify_api_key)):
    """
    Process documents and answer questions using the SampleModel with parallel processing
    Each request gets its own model instance enabling concurrent processing
    Requires valid API key in Authorization header
    """
    try:
        # Check if user has write permission
        if not auth_manager.has_permission(auth_info, "write"):
            app_logger.warning(f"Insufficient permissions for API key: {auth_info.get('name', 'Unknown')}")
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions. Write access required."
            )
        
        # Log the request with API key info
        key_name = auth_info.get('name', 'Unknown') if not auth_info.get('bypass') else 'Authentication Disabled'
        app_logger.info(f"HackRX endpoint called with {len(request.questions)} questions - API Key: {key_name}")
        app_logger.info(f"Document URL: {request.documents}")
        
        # Create a new model instance for this request (enables parallel processing)
        model = create_model_instance()
        app_logger.info(f"Created new model instance for request - Thread: {threading.current_thread().name}")
        
        # Load the document using the new model instance
        model.load_document(request.documents)
        app_logger.info("Document loaded successfully")
        
        # Process each question and get answers
        answers = None
        question_batch = []
        for i, question in enumerate(request.questions):
            app_logger.info(f"Batching question {i+1}/{len(request.questions)}: {question}")
            question_batch.append(question)

        # Run inference in thread pool to enable parallel processing
        loop = asyncio.get_event_loop()
        answers = await loop.run_in_executor(executor, model.inference, question_batch)
        app_logger.info("Inference completed successfully")
        
        for i, answer in enumerate(answers):
            app_logger.info(f"Answer for question {i+1}: {answer}...")
        
        
        app_logger.info(f"Successfully processed all {len(request.questions)} questions")
        
        # Return the response in the required format
        return HackRXResponse(answers=answers)
        
    except HTTPException:
        # Re-raise HTTP E/exceptions (like authentication errors)
        raise
    except Exception as e:
        app_logger.error(f"Error in hackrx_run: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Authentication status endpoint
@router.get("/auth/status")
def auth_status():
    """Get current autheE/ntication configuration status"""
    return {
        "authentication_enabled": auth_manager.is_authentication_enabled(),
        "api_key_required": auth_manager.is_api_key_required(),
        "total_active_keys": len(auth_manager.api_keys)
    }

# Endpoint to test API key validation
@router.get("/auth/validate")
def validate_key(auth_info: dict = Depends(verify_api_key)):
    """Validate the provided API key and return key information"""
    if auth_info.get('bypass'):
        return {
            "valid": True,
            "message": "Authentication is disabled or not required",
            "key_info": "bypass"
        }
    
    return {
        "valid": True,
        "message": "API key is valid",
        "key_info": {
            "name": auth_info.get('name'),
            "permissions": auth_info.get('permissions', [])
        }
    }

