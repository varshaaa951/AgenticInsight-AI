from src.state import AgentState
from src.tools.git_tools import clone_and_analyze_repo

def code_analyst_agent(state: AgentState) -> dict:
    """
    Worker Agent: Clones the target GitHub repository and performs 
    static code analysis using Abstract Syntax Trees (AST).
    """
    repo_url = state.get("target_repo_url")
    print(f"\n[Code Analyst Agent] Starting analysis for: {repo_url}")
    
    if not repo_url:
        print(" Error: No repo URL provided.")
        return {
            "code_analysis_results": {"error": "Missing repository URL"},
            "status": "FAILED_NO_REPO"
        }
    
    try:
        # Run static AST analysis
        results = clone_and_analyze_repo(repo_url)
        print(f" Analysis complete: Parsed {results['total_python_files']} Python files ({results['total_lines_of_code']} lines).")
        
        return {
            "code_analysis_results": results,
            "status": "CODE_ANALYSIS_COMPLETE"
        }
    except Exception as e:
        print(f" Analysis failed: {str(e)}")
        return {
            "code_analysis_results": {"error": str(e)},
            "status": "CODE_ANALYSIS_FAILED"
        }