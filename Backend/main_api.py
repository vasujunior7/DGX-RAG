from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.api import router as v1_router
from .api.v2.api import router as v2_router
from .api.hostfile.api import router as hostfile_router
from utils.middleware import RequestLoggingMiddleware
from utils.logging_config import setup_logging, get_app_logger

# Setup logging
setup_logging()
app_logger = get_app_logger()

# Setup templates
templates = Jinja2Templates(directory="templates")

# Create FastAPI app instance
app = FastAPI(
    title="HackRX API",
    description="API for HackRX project with LLM integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including OPTIONS
    allow_headers=["*"],  # Allow all headers
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Include the v1 router with prefix
app.include_router(v1_router, prefix="/api/v1", tags=["v1"])
app.include_router(v2_router, prefix="/api/v2", tags=["v2"])
app.include_router(hostfile_router, prefix="/api/hostfile", tags=["hostfile"])

# Log application startup
app_logger.info("HackRX API application started")

# Root endpoint - Serve HTML guide
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    app_logger.info("Root endpoint accessed - serving HTML guide")
    return templates.TemplateResponse("api_guide.html", {"request": request})

@app.get("/help")
def read_help():
    app_logger.info("Help endpoint accessed")
    return {
        "message": "Welcome to HackRX API",
        "version": "1.0.0",
        "endpoints": {
            "api_v1": "/api/v1",
            "api_v2": "/api/v2",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }