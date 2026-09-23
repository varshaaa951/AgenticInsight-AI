from src.state import AgentState

def synthesizer_agent(state: AgentState) -> dict:
    """
    Synthesizes code analysis data and web research results 
    into a structured technical report.
    """
    print("\n[Synthesizer Agent] Building final technical report...")
    
    code_data = state.get("code_analysis_results") or {}
    web_data = state.get("web_research_results") or []
    query = state.get("user_query", "N/A")
    repo = state.get("target_repo_url", "N/A")

    # Format code analysis section
    code_summary = (
        f"- **Files Parsed**: {code_data.get('total_python_files', 0)}\n"
        f"- **Lines of Code**: {code_data.get('total_lines_of_code', 0)}\n"
        f"- **Functions Count**: {code_data.get('total_functions', 0)}\n"
        f"- **Classes Count**: {code_data.get('total_classes', 0)}\n"
    )

    # Format web research section
    web_summary = ""
    for idx, item in enumerate(web_data, start=1):
        web_summary += f"{idx}. [{item.get('title')}]({item.get('url')})\n   - {item.get('content')[:150]}...\n"

    if not web_summary:
        web_summary = "No web research data retrieved.\n"

    # Assemble final markdown output
    report = (
        f"# AgenticInsight AI Technical Audit\n\n"
        f"**Target Repository**: `{repo}`\n"
        f"**Audit Query**: {query}\n\n"
        f"## 1. Codebase Architecture Metrics\n{code_summary}\n"
        f"## 2. Web Research & Industry Context\n{web_summary}\n"
        f"---\n"
        f"*Report generated automatically via AgenticInsight Multi-Agent System.*"
    )

    return {
        "final_report": report,
        "status": "COMPLETED"
    }