"""
System Routes
Health checks and system information
"""

from fastapi import APIRouter, HTTPException
import logging
import os

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import HealthResponse

router = APIRouter(prefix="/system", tags=["System"])
logger = logging.getLogger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check system health and component status.
    """
    try:
        # Check if Groq API key is configured
        groq_key = os.getenv("GROQ_API_KEY")
        groq_status = "healthy" if groq_key and groq_key != "your_groq_api_key_here" else "unhealthy"
        
        # List of available tools
        available_tools = [
            "calculator",
            "weather", 
            "web_search",
            "notes",
            "datetime"
        ]
        
        response = HealthResponse(
            status="healthy" if groq_status == "healthy" else "degraded",
            version=os.getenv("APP_VERSION", "1.0.0"),
            groq_api_status=groq_status,
            available_tools=available_tools,
            database_status="healthy"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            version=os.getenv("APP_VERSION", "1.0.0"),
            groq_api_status="unknown",
            available_tools=[],
            database_status="unknown"
        )


@router.get("/info")
async def get_system_info():
    """
    Get detailed system information.
    """
    try:
        return {
            "app_name": os.getenv("APP_NAME", "AI Agent Toolbox"),
            "version": os.getenv("APP_VERSION", "1.0.0"),
            "model": os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
            "max_iterations": int(os.getenv("MAX_ITERATIONS", "10")),
            "features": {
                "calculator": "Math operations and currency conversion",
                "weather": "Real-time weather information",
                "web_search": "Search the internet (Tavily/SerpAPI)",
                "notes": "Save and retrieve notes",
                "datetime": "Time and date utilities"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get system info: {str(e)}"
        )