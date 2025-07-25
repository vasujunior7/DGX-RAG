from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import sys
import os

# Add the Model directory to the path so we can import SampleModel
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Model'))
from sample_model import SampleModel

# Import logging from utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from utils.logging_config import get_app_logger

# Create APIRouter instance for v1 endpoints
router = APIRouter()

# Get logger
app_logger = get_app_logger()

# Pydantic models for request/response
class HackRXRequest(BaseModel):
    documents: str
    questions: List[str]

class HackRXResponse(BaseModel):
    answers: List[str]

# Initialize the model (you can add proper API key later)
model = SampleModel(api_key="dummy_key")
app_logger.info("SampleModel initialized in v1 API")

# Define a basic GET endpoint
@router.get("/")
def read_root():
    app_logger.info("V1 root endpoint accessed")
    return {"message": "Welcome to HackRX API", "version": "v1"}

# Define a GET endpoint with a parameter
# @router.get("/hello/{name}")
# def say_hello(name: str):
#     return {"message": f"Hello, {name}!", "version": "v1"}

# Define a POST endpoint
# @router.post("/echo/")
# def echo_data(data: dict):
#     return {"you_sent": data, "version": "v1"}

# Main HackRX endpoint
@router.post("/hackrx/run", response_model=HackRXResponse)
def hackrx_run(request: HackRXRequest):
    """
    Process documents and answer questions using the SampleModel
    """
    try:
        app_logger.info(f"HackRX endpoint called with {len(request.questions)} questions")
        app_logger.info(f"Document URL: {request.documents}")
        
        # Load the document using SampleModel
        model.load_document(request.documents)
        app_logger.info("Document loaded successfully")
        
        # Process each question and get answers
        answers = []
        for i, question in enumerate(request.questions):
            app_logger.info(f"Processing question {i+1}/{len(request.questions)}: {question[:50]}...")
            answer = model.inference(question)
            answers.append(answer)
        
        app_logger.info(f"Successfully processed all {len(request.questions)} questions")
        
        # Return the response in the required format
        return HackRXResponse(answers=answers)
        
    except Exception as e:
        app_logger.error(f"Error in hackrx_run: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

