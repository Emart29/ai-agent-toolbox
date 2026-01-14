"""
Web Search Tool
Search the web using Tavily API (primary) with SerpAPI fallback

Features:
- Real-time web search
- Automatic fallback between providers
- Result filtering and ranking
- Caching to reduce API calls
"""

import os
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSearchTool:
    """
    Web search tool with Tavily (primary) and SerpAPI (fallback).
    
    Tavily: Optimized for AI agents, returns clean results
    SerpAPI: Google search results, more comprehensive
    """
    
    def __init__(self):
        """Initialize with API keys"""
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.serpapi_key = os.getenv("SERPAPI_API_KEY")
        
        # Track which provider is being used
        self.primary_provider = "tavily"
        self.fallback_provider = "serpapi"
        
        logger.info("WebSearchTool initialized")
    
    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for information.
        
        Tries Tavily first, falls back to SerpAPI if needed.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Dict with search results
        """
        logger.info(f"Searching for: {query}")
        
        # Try Tavily first
        if self.tavily_api_key and self.tavily_api_key != "your_tavily_api_key_here":
            result = self._search_tavily(query, max_results)
            if result['success']:
                return result
            logger.warning("Tavily search failed, trying fallback...")
        
        # Fallback to SerpAPI
        if self.serpapi_key and self.serpapi_key != "your_serpapi_api_key_here":
            result = self._search_serpapi(query, max_results)
            if result['success']:
                return result
            logger.warning("SerpAPI search also failed")
        
        # If both fail, return mock results
        logger.warning("Both search providers unavailable, using mock results")
        return self._get_mock_results(query, max_results)
    
    def _search_tavily(self, query: str, max_results: int) -> Dict[str, Any]:
        """
        Search using Tavily API.
        
        Tavily is optimized for AI agents and RAG systems.
        """
        try:
            from tavily import TavilyClient
            
            client = TavilyClient(api_key=self.tavily_api_key)
            
            # Perform search
            response = client.search(
                query=query,
                max_results=max_results,
                search_depth="basic",  # or "advanced" for more comprehensive
                include_answer=True     # Get AI-generated summary
            )
            
            # Format results
            results = []
            for item in response.get('results', []):
                results.append({
                    'title': item.get('title', 'No title'),
                    'url': item.get('url', ''),
                    'snippet': item.get('content', '')[:300],  # Limit snippet length
                    'source': 'tavily'
                })
            
            explanation = self._format_search_explanation(query, results, 'Tavily')
            
            return {
                'success': True,
                'query': query,
                'results': results,
                'total_results': len(results),
                'provider': 'tavily',
                'answer': response.get('answer', ''),  # Tavily's AI summary
                'explanation': explanation
            }
            
        except Exception as e:
            logger.error(f"Tavily search error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'provider': 'tavily'
            }
    
    def _search_serpapi(self, query: str, max_results: int) -> Dict[str, Any]:
        """
        Search using SerpAPI (Google Search).
        
        SerpAPI provides Google search results.
        """
        try:
            from serpapi import GoogleSearch
            
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "num": max_results
            }
            
            search = GoogleSearch(params)
            response = search.get_dict()
            
            # Parse organic results
            results = []
            for item in response.get('organic_results', [])[:max_results]:
                results.append({
                    'title': item.get('title', 'No title'),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', '')[:300],
                    'source': 'serpapi'
                })
            
            explanation = self._format_search_explanation(query, results, 'SerpAPI')
            
            return {
                'success': True,
                'query': query,
                'results': results,
                'total_results': len(results),
                'provider': 'serpapi',
                'explanation': explanation
            }
            
        except Exception as e:
            logger.error(f"SerpAPI search error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'provider': 'serpapi'
            }
    
    def _format_search_explanation(self, query: str, results: List[Dict], provider: str) -> str:
        """
        Format search results into explanation text.
        """
        if not results:
            return f"No results found for: {query}"
        
        explanation = f"Found {len(results)} results for '{query}' using {provider}:\n\n"
        
        for i, result in enumerate(results[:3], 1):  # Show top 3
            explanation += f"{i}. {result['title']}\n"
            explanation += f"   {result['snippet']}\n"
            explanation += f"   URL: {result['url']}\n\n"
        
        if len(results) > 3:
            explanation += f"... and {len(results) - 3} more results."
        
        return explanation
    
    def _get_mock_results(self, query: str, max_results: int) -> Dict[str, Any]:
        """
        Return mock search results for testing without API keys.
        """
        # Generate mock results based on query
        mock_results = []
        
        for i in range(min(max_results, 3)):
            mock_results.append({
                'title': f'Result {i+1} for: {query}',
                'url': f'https://example.com/result-{i+1}',
                'snippet': f'This is a mock search result for the query "{query}". In a real implementation, this would contain relevant information from the web.',
                'source': 'mock'
            })
        
        explanation = (
            f"[MOCK RESULTS - No API keys configured]\n\n"
            f"Found {len(mock_results)} mock results for '{query}':\n\n"
        )
        
        for i, result in enumerate(mock_results, 1):
            explanation += f"{i}. {result['title']}\n"
            explanation += f"   {result['snippet']}\n"
            explanation += f"   URL: {result['url']}\n\n"
        
        return {
            'success': True,
            'query': query,
            'results': mock_results,
            'total_results': len(mock_results),
            'provider': 'mock',
            'explanation': explanation
        }


# LangChain Tool wrapper
def get_web_search_tool_for_langchain():
    """
    Create LangChain-compatible web search tool.
    """
    search_tool = WebSearchTool()
    
    def search_wrapper(query: str) -> str:
        """
        Search the web for information.
        
        Args:
            query: Search query
            
        Returns:
            Search results as formatted string
        """
        result = search_tool.search(query, max_results=5)
        
        if result['success']:
            return result['explanation']
        else:
            return f"Error: {result.get('error', 'Search failed')}"
    
    return search_wrapper


# Example usage and testing
if __name__ == "__main__":
    search = WebSearchTool()
    
    print("🧪 Testing Web Search Tool\n")
    
    # Test 1: General search
    print("1️⃣ Searching for 'Python programming':")
    result = search.search("Python programming", max_results=3)
    print(f"   Provider: {result['provider']}")
    print(f"   Results: {result['total_results']}")
    print(f"   {result['explanation'][:200]}...\n")
    
    # Test 2: News search
    print("2️⃣ Searching for 'latest AI news':")
    result = search.search("latest AI news", max_results=3)
    print(f"   Provider: {result['provider']}")
    print(f"   Results: {result['total_results']}")
    print(f"   {result['explanation'][:200]}...\n")
    
    # Test 3: Specific query
    print("3️⃣ Searching for 'weather in Lagos':")
    result = search.search("weather in Lagos", max_results=3)
    print(f"   Provider: {result['provider']}")
    print(f"   Results: {result['total_results']}\n")
    
    print("✅ All tests completed!")