"""
Agent API Routes
Endpoints for interacting with the AI agent
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import logging

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import (
    AgentRequest,
    AgentResponse,
    ReasoningStep,
    ToolCall,
    ErrorResponse
)
from app.agent.orchestrator import AgentOrchestrator

router = APIRouter(prefix="/agent", tags=["Agent"])
logger = logging.getLogger(__name__)

# Initialize agent (singleton)
_agent_instance = None


def get_agent() -> AgentOrchestrator:
    """Get or create agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = AgentOrchestrator()
    return _agent_instance


@router.post("/query", response_model=AgentResponse)
async def query_agent(request: AgentRequest):
    """
    Send a query to the AI agent.
    
    The agent will analyze the query, use appropriate tools,
    and return an answer with reasoning steps.
    
    Example:
    ```json
    {
        "query": "What's the weather in Lagos and convert 30 Celsius to Fahrenheit?",
        "include_reasoning": true
    }
    ```
    """
    try:
        logger.info(f"Received query: {request.query}")
        
        # Get agent
        agent = get_agent()
        
        # Process query
        result = agent.process_query(
            query=request.query,
            conversation_id=request.conversation_id,
            include_reasoning=request.include_reasoning
        )
        
        # Convert to response model
        reasoning_steps = [
            ReasoningStep(**step) for step in result.get('reasoning_steps', [])
        ]
        
        tool_calls = [
            ToolCall(**call) for call in result.get('tool_calls', [])
        ]
        
        response = AgentResponse(
            query=result['query'],
            answer=result['answer'],
            reasoning_steps=reasoning_steps,
            tool_calls=tool_calls,
            conversation_id=result['conversation_id'],
            total_execution_time=result['total_execution_time'],
            model_used=result['model_used']
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )


@router.get("/tools")
async def list_available_tools():
    """
    Get list of available tools the agent can use.
    
    Returns information about each tool including name and description.
    """
    try:
        agent = get_agent()
        tools = agent.get_available_tools()
        
        return {
            "tools": tools,
            "total_count": len(tools)
        }
        
    except Exception as e:
        logger.error(f"Error listing tools: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list tools: {str(e)}"
        )


@router.get("/conversation/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """
    Get conversation history for a specific conversation.
    """
    try:
        agent = get_agent()
        history = agent.conversations.get(conversation_id, [])
        
        return {
            "conversation_id": conversation_id,
            "messages": history,
            "message_count": len(history)
        }
        
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversation: {str(e)}"
        )