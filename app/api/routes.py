"""
FastAPI routes for Resume Matcher API.

Provides two endpoints:
- POST /match: Score a resume against a job description
- GET /rankings: Retrieve saved results with optional filtering
"""

import os
import tempfile
import logging
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import JSONResponse

from app.config import Config
from app.factory.pipeline_factory import PipelineFactory

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/match")
async def match_resume(
    resume: UploadFile = File(..., description="Resume PDF file"),
    jd_text: str = Form(..., description="Job description text"),
    role: str = Form(default="backend_engineer", description="Role identifier"),
    parser: Optional[str] = Query(default=None, description="Parser strategy (text/ocr/llm)"),
    scorer: Optional[str] = Query(default=None, description="Scorer strategy (llm/regex)"),
    repository: Optional[str] = Query(default=None, description="Repository strategy (filesystem/sqlite/memory)")
):
    """
    Score a resume against a job description.
    
    Args:
        resume: Uploaded PDF file containing the resume.
        jd_text: Job description text.
        role: Role identifier for loading evaluation rules.
        parser: Optional parser strategy override.
        scorer: Optional scorer strategy override.
        repository: Optional repository strategy override.
        
    Returns:
        JSON response with scoring results or error details.
    """
    temp_file_path = None
    
    try:
        # Validate file type
        if not resume.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await resume.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        logger.info(f"Processing resume: {resume.filename} for role: {role}")
        
        # Get config and validate
        config = Config()
        config.validate()
        
        # Build pipeline with factory
        pipeline = PipelineFactory.build(
            config=config,
            parser=parser,
            scorer=scorer,
            repository=repository
        )
        
        # Execute pipeline
        result = pipeline.execute(
            file_path=temp_file_path,
            jd_text=jd_text,
            role=role,
            resume_name=resume.filename
        )
        
        # Handle result
        if result.success:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "score": result.data.score,
                    "justification": result.data.justification,
                    "gaps": result.data.gaps,
                    "suggestions": result.data.suggestions
                }
            )
        else:
            # Map failed_step to HTTP status code
            status_code_map = {
                "parse": 422,  # Unprocessable Entity
                "load_rules": 404,  # Not Found
                "build_prompt": 500,  # Internal Server Error
                "score": 502,  # Bad Gateway (external service failed)
                "persist": 500,  # Internal Server Error
                "unknown": 500  # Internal Server Error
            }
            
            status_code = status_code_map.get(result.failed_step, 500)
            
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "error": result.error,
                    "failed_step": result.failed_step
                }
            )
            
    except HTTPException:
        raise
    except ValueError as e:
        # Configuration or validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /match endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file: {str(e)}")


@router.get("/rankings")
async def get_rankings(
    role: Optional[str] = Query(default=None, description="Filter by role")
):
    """
    Retrieve saved scoring results.
    
    Args:
        role: Optional role filter.
        
    Returns:
        JSON array of results sorted by score (descending).
    """
    try:
        # Get config
        config = Config()
        
        # Instantiate repository (use default from config)
        from app.strategies.repositories.filesystem_repository import FilesystemRepository
        repository = FilesystemRepository(output_dir=config.RESULTS_DIR)
        
        # Get rankings
        rankings = repository.get_rankings(role=role)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "count": len(rankings),
                "results": rankings
            }
        )
        
    except Exception as e:
        logger.error(f"Error in /rankings endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve rankings: {str(e)}")
