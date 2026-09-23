from src.graph import app
from src.state import AgentState

if __name__ == "__main__":
    thread_config = {"configurable": {"thread_id": "audit-run-001"}}

    initial_state: AgentState = {
        "target_repo_url": "https://github.com/psf/requests",
        "user_query": "Best practices for session pooling and async adapters",
        "tasks": [],
        "code_analysis_results": None,
        "web_research_results": None,
        "is_approved": False,
        "status": "STARTING",
        "final_report": None
    }

    print("--- Starting AgenticInsight AI Pipeline ---")
    
    # 1. Run until hitting the interrupt gate
    for event in app.stream(initial_state, thread_config):
        print(f"Event Step: {list(event.keys())}")

    # 2. Check paused state
    snapshot = app.get_state(thread_config)
    print(f"\n⏸️ Pipeline Paused before node: {snapshot.next}")

    # 3. Request Human Approval
    approval = input("\nApprove synthesis and final report generation? (yes/no): ").strip().lower()

    if approval == "yes":
        print("\n--- Resuming Pipeline ---")
        for event in app.stream(None, thread_config):
            print(f"Event Step: {list(event.keys())}")

        final_state = app.get_state(thread_config).values
        print("\n================ FINAL GENERATED REPORT ================")
        print(final_state.get("final_report"))
    else:
        print("\n Human aborted pipeline execution.")