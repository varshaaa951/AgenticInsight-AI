from src.state import AgentState

def orchestrator_agent(state: AgentState) -> dict:
    """
    Analyzes user inputs and generates task assignments for downstream worker agents.
    """
    print("\n[Orchestrator Agent] Planning execution pipeline...")
    
    tasks = []
    if state.get("target_repo_url"):
        tasks.append("ANALYZE_CODEBASE")
    if state.get("user_query"):
        tasks.append("RESEARCH_WEB")
        
    print(f" Planned Tasks: {tasks}")
    return {
        "tasks": tasks,
        "status": "PLANNING_COMPLETE"
    }