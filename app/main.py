"""
FastAPI application entry point for Resume Matcher.

Creates the FastAPI app, configures middleware, and includes API routes.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.routes import router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Resume Matcher API",
    description="Score resumes against job descriptions using LLM evaluation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="", tags=["matching"])


@app.get("/")
async def root():
    """
    Root endpoint for health check.
    
    Returns:
        Status information.
    """
    return {
        "status": "running",
        "service": "resume_matcher",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """
    Health check endpoint.
    
    Returns:
        Health status.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
