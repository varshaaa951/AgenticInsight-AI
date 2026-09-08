import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.code_analyst import code_analyst_agent
from src.agents.web_research import web_research_agent
from src.state import AgentState

if __name__ == "__main__":
    test_state: AgentState = {
        "target_repo_url": "https://github.com/psf/requests",
        "user_query": "Best practices for asynchronous HTTP client session handling in Python",
        "tasks": [],
        "code_analysis_results": None,
        "web_research_results": None,
        "is_approved": False,
        "status": "INIT",
        "final_report": None
    }
    
    print("--- 1. Testing Code Analyst Agent ---")
    analyst_update = code_analyst_agent(test_state)
    print(analyst_update)

    print("\n--- 2. Testing Web Research Agent ---")
    research_update = web_research_agent(test_state)
    print(research_update)