from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from agents import MultiAgentSystem
import uvicorn
import os
from pathlib import Path
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Multi-Agent RAG System")

# Set up templates directory
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Set up static files only if the directory exists
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

class Query(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: Optional[str] = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    original_error: Optional[str] = None
    intermediate_steps: Dict[str, Any]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/ask", response_model=QueryResponse)
async def process_query(query: Query):
    try:
        logger.info(f"Received question: {query.question}")
        
        # Initialize agent system
        logger.info("Initializing agent system...")
        if not hasattr(app, "agent_system"):
            app.agent_system = MultiAgentSystem()
        
        # Process the query
        logger.info("Processing query through agent system...")
        result = app.agent_system.process_query(query.question)
        
        logger.info(f"Processing complete. Result: {result}")
        
        # Handle errors in the result
        if "error" in result:
            logger.error(f"Error in result: {result['error']}")
            error_type = result.get("error_type", "unknown")
            
            # Map error types to appropriate HTTP status codes
            status_codes = {
                "api_quota": status.HTTP_402_PAYMENT_REQUIRED,
                "api_quota_partial": status.HTTP_206_PARTIAL_CONTENT,
                "database": status.HTTP_503_SERVICE_UNAVAILABLE,
                "unknown": status.HTTP_400_BAD_REQUEST
            }
            
            return JSONResponse(
                status_code=status_codes.get(error_type, status.HTTP_400_BAD_REQUEST),
                content={
                    "error": result["error"],
                    "error_type": error_type,
                    "original_error": result.get("original_error"),
                    "intermediate_steps": result.get("intermediate_steps", {})
                }
            )
        
        # Return successful result
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )
            
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        logger.error(f"Full error traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error occurred",
                "error_type": "server_error",
                "original_error": str(e),
                "intermediate_steps": None
            }
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug") 