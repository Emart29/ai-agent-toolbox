"""
Main FastAPI Application
AI Agent Toolbox Backend

Entry point for the FastAPI server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.routers import agent, system

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=os.getenv("APP_NAME", "AI Agent Toolbox API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="""
    🤖 AI Agent with Multiple Tools
    
    An intelligent AI agent that can:
    - 🧮 Perform calculations and currency conversions
    - 🌤️ Get real-time weather information
    - 🔍 Search the web for current information
    - 📝 Save and retrieve notes
    - 🕐 Handle time and date operations
    
    The agent intelligently decides which tools to use based on your query
    and can chain multiple tools together to solve complex tasks.
    
    Built with: FastAPI, LangChain, Groq (Llama 3.1 70B)
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router)
app.include_router(system.router)


@app.get("/")
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "message": "🤖 AI Agent Toolbox API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "status": "running",
        "docs": "/docs",
        "health": "/system/health",
        "endpoints": {
            "agent": {
                "query": "POST /agent/query",
                "tools": "GET /agent/tools",
                "conversation": "GET /agent/conversation/{conversation_id}"
            },
            "system": {
                "health": "GET /system/health",
                "info": "GET /system/info"
            }
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG", "False") == "True" else "An unexpected error occurred"
        }
    )


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.
    """
    logger.info("=" * 60)
    logger.info("🚀 Starting AI Agent Toolbox API")
    logger.info(f"   Version: {os.getenv('APP_VERSION', '1.0.0')}")
    logger.info(f"   Environment: {'Development' if os.getenv('DEBUG') == 'True' else 'Production'}")
    logger.info("=" * 60)
    
    # Check Groq API key
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "your_groq_api_key_here":
        logger.warning("⚠️  GROQ_API_KEY not configured!")
    else:
        logger.info("✅ Groq API key configured")
    
    logger.info("=" * 60)
    logger.info("🎯 API is ready to accept requests!")
    logger.info(f"   📚 Docs: http://localhost:8000/docs")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown.
    """
    logger.info("=" * 60)
    logger.info("🛑 Shutting down AI Agent Toolbox API")
    logger.info("=" * 60)


# For testing purposes
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("DEBUG", "False") == "True"
    )