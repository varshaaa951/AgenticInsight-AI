import os
from typing import List, Dict, Any
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def execute_web_search(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Executes a real-time web search query using Tavily API.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or api_key == "tvly-YOUR_ACTUAL_API_KEY_HERE":
        print(" Warning: TAVILY_API_KEY not found in environment. Returning mock search results.")
        return [
            {
                "title": f"Mock Search Result for {query}",
                "url": "https://example.com/mock",
                "content": f"Simulated content for research query: '{query}'."
            }
        ]

    client = TavilyClient(api_key=api_key)
    response = client.search(query=query, max_results=max_results)
    
    clean_results = []
    for result in response.get("results", []):
        clean_results.append({
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content")
        })
        
    return clean_results