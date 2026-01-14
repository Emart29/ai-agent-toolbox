"""
Agent Orchestrator
LangChain-based AI agent that coordinates multiple tools

This is the brain that decides which tools to use and how to use them.
"""

import os
import time
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain_core.tools import Tool
from langchain_groq import ChatGroq
from typing import Optional, List, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.calculator import CalculatorTool
from tools.weather import WeatherTool
from tools.web_search import WebSearchTool
from tools.notes import NotesTool
from tools.datetime_tool import DateTimeTool
from agent.prompts import AGENT_SYSTEM_PROMPT, REACT_PROMPT_TEMPLATE

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Removed custom GroqLLM class in favor of official ChatGroq implementation


class AgentOrchestrator:
    """
    Main agent orchestrator using LangChain.
    
    Coordinates multiple tools to answer user queries.
    """
    
    def __init__(self):
        """Initialize agent with LLM and tools"""
        
        logger.info("Initializing AgentOrchestrator...")
        
        # Initialize LLM
        self.llm = self._init_llm()
        
        # Initialize tools
        self.tools = self._init_tools()
        
        # Create agent
        self.agent = self._create_agent()
        
        # Conversation storage (in-memory)
        self.conversations = {}
        
        logger.info(f"AgentOrchestrator initialized with {len(self.tools)} tools")
    
    def _init_llm(self) -> ChatGroq:
        """
        Initialize Groq LLM using LangChain's official ChatGroq.
        
        Returns:
            ChatGroq instance
        """
        api_key = os.getenv("GROQ_API_KEY")
        model_name = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        temperature = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
        
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY not configured")
        
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=int(os.getenv("AGENT_MAX_TOKENS", "2000")),
            # Use proxy=None to avoid the 'proxies' unexpected keyword argument issue in httpx 0.28+
            # Although ChatGroq handles this better, being explicit helps.
        )
        
        logger.info(f"Initialized ChatGroq: {model_name}")
        return llm
    
    def _init_tools(self) -> List[Tool]:
        """
        Initialize all available tools.
        
        Returns:
            List of LangChain Tool objects
        """
        tools = []
        
        # Calculator Tool
        try:
            calculator = CalculatorTool()
            calc_tool = Tool(
                name="calculator",
                func=lambda expr: calculator.calculate(expr)['explanation'],
                description="Useful for mathematical calculations and currency conversions. "
                           "Input should be a math expression like '2+2' or a currency conversion like '100 USD to EUR'."
            )
            tools.append(calc_tool)
            logger.info("✅ Calculator tool loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load calculator tool: {str(e)}")
        
        # Weather Tool
        try:
            weather = WeatherTool()
            weather_tool = Tool(
                name="weather",
                func=lambda city: weather.get_weather(city.split(',')[0].strip(), 
                                                     city.split(',')[1].strip() if ',' in city else None)['explanation'],
                description="Get current weather information for any city. "
                           "Input should be a city name, optionally with country code like 'Lagos, NG' or just 'London'."
            )
            tools.append(weather_tool)
            logger.info("✅ Weather tool loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load weather tool: {str(e)}")
        
        # Web Search Tool
        try:
            search = WebSearchTool()
            search_tool = Tool(
                name="web_search",
                func=lambda query: search.search(query, max_results=5)['explanation'],
                description="Search the web for current information, news, or any topic. "
                           "Input should be a search query like 'latest Python news' or 'weather in Lagos'."
            )
            tools.append(search_tool)
            logger.info("✅ Web search tool loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load web search tool: {str(e)}")
        
        # Notes Tool
        try:
            notes = NotesTool()
            
            # We'll create a simplified wrapper for the agent
            def notes_func(action_str: str) -> str:
                """Parse action string and call appropriate notes method"""
                try:
                    # Parse action (e.g., "create: title=Test, content=Hello")
                    if ':' in action_str:
                        action, params_str = action_str.split(':', 1)
                        action = action.strip().lower()
                    else:
                        action = action_str.lower()
                        params_str = ""
                    
                    if action == 'list':
                        result = notes.list_notes(limit=10)
                    elif action == 'search' and params_str:
                        result = notes.search_notes(params_str.strip())
                    elif action == 'create' and params_str:
                        # Simple parsing (in production, use better parsing)
                        parts = params_str.split(',')
                        title = parts[0].strip() if len(parts) > 0 else "Untitled"
                        content = parts[1].strip() if len(parts) > 1 else ""
                        result = notes.create_note(title, content)
                    else:
                        result = {'explanation': f'Unknown notes action: {action}'}
                    
                    return result['explanation']
                except Exception as e:
                    return f"Error with notes tool: {str(e)}"
            
            notes_tool = Tool(
                name="notes",
                func=notes_func,
                description="Manage notes - create, list, or search. "
                           "For list: use 'list'. "
                           "For search: use 'search: keyword'. "
                           "For create: use 'create: title, content'."
            )
            tools.append(notes_tool)
            logger.info("✅ Notes tool loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load notes tool: {str(e)}")
        
        # DateTime Tool
        try:
            dt_tool = DateTimeTool()
            
            def datetime_func(action_str: str) -> str:
                """Parse action and call datetime methods"""
                try:
                    parts = action_str.split(':', 1)
                    action = parts[0].strip().lower()
                    params = parts[1].strip() if len(parts) > 1 else None
                    
                    if action == 'current' or action == 'now':
                        tz = params if params else 'UTC'
                        result = dt_tool.get_current_time(tz)
                    elif action == 'add' and params:
                        result = dt_tool.add_time(None, days=int(params))
                    else:
                        result = dt_tool.get_current_time('UTC')
                    
                    return result['explanation']
                except Exception as e:
                    return f"Error with datetime tool: {str(e)}"
            
            datetime_tool = Tool(
                name="datetime",
                func=datetime_func,
                description="Get current time, dates, and perform date calculations. "
                           "For current time: use 'current: timezone' (e.g., 'current: Africa/Lagos'). "
                           "For adding days: use 'add: number' (e.g., 'add: 7')."
            )
            tools.append(datetime_tool)
            logger.info("✅ DateTime tool loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load datetime tool: {str(e)}")
        
        return tools
    
    def _create_agent(self) -> AgentExecutor:
        """
        Create LangChain ReAct agent.
        
        Returns:
            AgentExecutor instance
        """
        # Use initialize_agent for simpler setup with newer LangChain
        agent_executor = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=int(os.getenv("MAX_ITERATIONS", "10")),
            handle_parsing_errors=True,
            return_intermediate_steps=True,
            agent_kwargs={
                'prefix': AGENT_SYSTEM_PROMPT
            }
        )
        
        logger.info("Agent executor created")
        return agent_executor
    
    def process_query(
        self, 
        query: str, 
        conversation_id: Optional[str] = None,
        include_reasoning: bool = True
    ) -> Dict[str, Any]:
        """
        Process user query using the agent.
        
        Args:
            query: User's question/request
            conversation_id: Optional conversation ID for context
            include_reasoning: Whether to include reasoning steps
            
        Returns:
            Dict with answer and metadata
        """
        start_time = time.time()
        
        # Generate conversation ID if not provided
        if not conversation_id:
            conversation_id = f"conv_{uuid.uuid4().hex[:12]}"
        
        logger.info(f"Processing query: {query}")
        logger.info(f"Conversation ID: {conversation_id}")
        
        try:
            # Get conversation history
            history = self.conversations.get(conversation_id, [])
            
            # Add context from history if exists
            if history:
                context = "\n".join([f"User: {h['query']}\nAssistant: {h['answer']}" 
                                    for h in history[-3:]])  # Last 3 exchanges
                enhanced_query = f"Previous conversation:\n{context}\n\nCurrent question: {query}"
            else:
                enhanced_query = query
            
            # Invoke agent
            response = self.agent.invoke({"input": enhanced_query})
            
            # Extract answer and steps
            answer = response.get('output', 'I apologize, but I encountered an issue processing your request.')
            intermediate_steps = response.get('intermediate_steps', [])
            
            # Format reasoning steps
            reasoning_steps = []
            tool_calls = []
            
            if include_reasoning:
                for i, (action, observation) in enumerate(intermediate_steps, 1):
                    # Ensure action_input is a dict
                    action_input = action.tool_input if hasattr(action, 'tool_input') else {}
                    if isinstance(action_input, str):
                        # Convert string to dict format
                        action_input = {'input': action_input}
                    elif not isinstance(action_input, dict):
                        action_input = {}
                    
                    step = {
                        'step_number': i,
                        'thought': str(action.log) if hasattr(action, 'log') else '',
                        'action': action.tool if hasattr(action, 'tool') else '',
                        'action_input': action_input,
                        'observation': str(observation)[:500],  # Limit length
                        'timestamp': datetime.now().isoformat()
                    }
                    reasoning_steps.append(step)
                    
                    # Track tool calls
                    tool_calls.append({
                        'tool_name': action.tool if hasattr(action, 'tool') else 'unknown',
                        'tool_input': action_input,
                        'tool_output': str(observation)[:500],
                        'execution_time': 0.0,  # Not tracked per-tool
                        'success': True
                    })
            
            # Update conversation history
            self.conversations.setdefault(conversation_id, []).append({
                'query': query,
                'answer': answer,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only last 10 exchanges
            if len(self.conversations[conversation_id]) > 10:
                self.conversations[conversation_id] = self.conversations[conversation_id][-10:]
            
            execution_time = time.time() - start_time
            
            result = {
                'query': query,
                'answer': answer,
                'reasoning_steps': reasoning_steps,
                'tool_calls': tool_calls,
                'conversation_id': conversation_id,
                'total_execution_time': round(execution_time, 2),
                'model_used': os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
                'success': True
            }
            
            logger.info(f"Query processed successfully in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            
            execution_time = time.time() - start_time
            
            return {
                'query': query,
                'answer': f"I apologize, but I encountered an error: {str(e)}",
                'reasoning_steps': [],
                'tool_calls': [],
                'conversation_id': conversation_id,
                'total_execution_time': round(execution_time, 2),
                'model_used': os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
                'success': False,
                'error': str(e)
            }
    
    def get_available_tools(self) -> List[Dict[str, str]]:
        """
        Get list of available tools with descriptions.
        
        Returns:
            List of tool info dicts
        """
        return [
            {
                'name': tool.name,
                'description': tool.description
            }
            for tool in self.tools
        ]


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Agent Orchestrator\n")
    
    try:
        # Initialize agent
        agent = AgentOrchestrator()
        
        print(f"✅ Agent initialized with {len(agent.tools)} tools\n")
        
        # Test 1: Simple calculation
        print("1️⃣ Test: Simple calculation")
        result = agent.process_query("What is 25% of 80?")
        print(f"Answer: {result['answer']}\n")
        
        # Test 2: Weather query
        print("2️⃣ Test: Weather query")
        result = agent.process_query("What's the weather in Lagos?")
        print(f"Answer: {result['answer']}\n")
        
        # Test 3: Multi-tool query
        print("3️⃣ Test: Multi-tool query")
        result = agent.process_query("What's the weather in London and convert 20 Celsius to Fahrenheit?")
        print(f"Answer: {result['answer']}\n")
        print(f"Tools used: {[tc['tool_name'] for tc in result['tool_calls']]}\n")
        
        print("✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")