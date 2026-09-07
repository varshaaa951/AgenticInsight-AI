from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    # User Inputs
    target_repo_url: str
    user_query: str
    
    # Internal Task Breakdown
    tasks: List[str]
    
    # Tool & Agent Outputs
    code_analysis_results: Optional[Dict[str, Any]]
    web_research_results: Optional[List[Dict[str, Any]]]
    
    # Security & Controls
    is_approved: bool
    status: str
    
    # Final Output Report
    final_report: Optional[str]