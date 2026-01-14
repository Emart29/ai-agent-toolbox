"""
Pydantic Models for AI Agent API
Request/Response validation and serialization
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ToolType(str, Enum):
    """Available tool types"""
    WEB_SEARCH = "web_search"
    CALCULATOR = "calculator"
    WEATHER = "weather"
    NOTES = "notes"
    DATETIME = "datetime"


class AgentRequest(BaseModel):
    """Request to agent for processing"""
    query: str = Field(..., min_length=1, max_length=1000, description="User query")
    conversation_id: Optional[str] = None
    include_reasoning: bool = Field(default=True, description="Include agent reasoning steps")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What's the weather in Lagos and convert 30 celsius to fahrenheit?",
                "conversation_id": "conv_123",
                "include_reasoning": True
            }
        }


class ToolCall(BaseModel):
    """Represents a single tool invocation"""
    tool_name: str
    tool_input: Dict[str, Any]
    tool_output: Any
    execution_time: float
    success: bool
    error: Optional[str] = None


class ReasoningStep(BaseModel):
    """Agent's reasoning at each step"""
    step_number: int
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class AgentResponse(BaseModel):
    """Response from agent"""
    query: str
    answer: str
    reasoning_steps: List[ReasoningStep] = []
    tool_calls: List[ToolCall] = []
    conversation_id: str
    total_execution_time: float
    model_used: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What's 25% of 80?",
                "answer": "25% of 80 is 20",
                "reasoning_steps": [
                    {
                        "step_number": 1,
                        "thought": "I need to calculate 25% of 80",
                        "action": "calculator",
                        "action_input": {"expression": "0.25 * 80"},
                        "observation": "Result: 20"
                    }
                ],
                "tool_calls": [
                    {
                        "tool_name": "calculator",
                        "tool_input": {"expression": "0.25 * 80"},
                        "tool_output": 20,
                        "execution_time": 0.01,
                        "success": True
                    }
                ],
                "conversation_id": "conv_123",
                "total_execution_time": 1.23,
                "model_used": "llama-3.1-70b-versatile"
            }
        }


class WebSearchRequest(BaseModel):
    """Request for web search"""
    query: str = Field(..., min_length=1, max_length=500)
    max_results: int = Field(default=5, ge=1, le=10)


class WebSearchResult(BaseModel):
    """Single web search result"""
    title: str
    url: str
    snippet: str
    source: str = Field(description="tavily or serpapi")


class WebSearchResponse(BaseModel):
    """Response from web search"""
    query: str
    results: List[WebSearchResult]
    total_results: int
    search_provider: str


class CalculatorRequest(BaseModel):
    """Request for calculation"""
    expression: str = Field(..., description="Mathematical expression or currency conversion")
    operation_type: Optional[str] = Field(default="math", description="math or currency")


class CalculatorResponse(BaseModel):
    """Response from calculator"""
    expression: str
    result: Any
    explanation: Optional[str] = None


class WeatherRequest(BaseModel):
    """Request for weather information"""
    city: str = Field(..., min_length=2, max_length=100)
    country_code: Optional[str] = Field(None, max_length=2, description="ISO 3166 country code")


class WeatherResponse(BaseModel):
    """Response with weather data"""
    city: str
    country: str
    temperature: float = Field(description="Temperature in Celsius")
    feels_like: float
    description: str
    humidity: int
    wind_speed: float
    timestamp: datetime = Field(default_factory=datetime.now)


class NoteRequest(BaseModel):
    """Request to create/update note"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=10000)
    tags: Optional[List[str]] = []


class NoteResponse(BaseModel):
    """Response with note data"""
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime


class NotesListResponse(BaseModel):
    """Response with list of notes"""
    notes: List[NoteResponse]
    total_count: int


class ToolInfo(BaseModel):
    """Information about a tool"""
    name: str
    description: str
    parameters: Dict[str, Any]
    enabled: bool = True


class ToolsListResponse(BaseModel):
    """Response with available tools"""
    tools: List[ToolInfo]
    total_count: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    groq_api_status: str
    available_tools: List[str]
    database_status: str


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    error_code: Optional[str] = None