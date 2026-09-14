"""
Main FastAPI application

This is the entry point for the Smart Emergency Routing backend.
All routes, middleware, and configuration are set up here.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="Smart Emergency Routing API",
    description="API for managing emergency vehicle routing and incident tracking",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",  # ReDoc at http://localhost:8000/redoc
    openapi_url="/openapi.json"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows frontend to make requests to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== HEALTH CHECK ENDPOINT =====
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns: {"status": "ok"} if API is running
    """
    return {
        "status": "ok",
        "service": "Smart Emergency Routing API",
        "version": "0.1.0"
    }

# ===== ROOT ENDPOINT =====
@app.get("/", tags=["Info"])
async def root():
    """
    Root endpoint
    
    Returns: Welcome message and API information
    """
    return {
        "message": "Welcome to Smart Emergency Routing API",
        "docs": "Visit http://localhost:8000/docs for interactive documentation",
        "redoc": "Visit http://localhost:8000/redoc for alternative documentation"
    }

# ===== GLOBAL EXCEPTION HANDLER =====
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors
    
    Returns: 500 error with error message
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# ===== STARTUP EVENT =====
@app.on_event("startup")
async def startup_event():
    """
    Runs when FastAPI server starts
    """
    logger.info("🚀 Smart Emergency Routing API starting...")
    logger.info(f"Environment: {settings.ENV}")
    logger.info(f"Debug: {settings.DEBUG}")

# ===== SHUTDOWN EVENT =====
@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when FastAPI server shuts down
    """
    logger.info("🛑 Smart Emergency Routing API shutting down...")

if __name__ == "__main__":
    # Run with: python -m uvicorn app.main:app --reload
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
