from src.state import AgentState
from src.tools.search_tools import execute_web_search

def web_research_agent(state: AgentState) -> dict:
    """
    Worker Agent: Queries web sources to gather external documentation, 
    architecture patterns, or security context relevant to the user query.
    """
    query = state.get("user_query")
    print(f"\n[Web Research Agent] Researching query: {query}")
    
    if not query:
        return {
            "web_research_results": [],
            "status": "FAILED_NO_QUERY"
        }
    
    try:
        results = execute_web_search(query=query, max_results=3)
        print(f" Research complete: Retrieved {len(results)} search results.")
        
        return {
            "web_research_results": results,
            "status": "WEB_RESEARCH_COMPLETE"
        }
    except Exception as e:
        print(f" Web research failed: {str(e)}")
        return {
            "web_research_results": [],
            "status": "WEB_RESEARCH_FAILED"
        }