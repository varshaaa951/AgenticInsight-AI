from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. Define graph state schema
class HITLState(TypedDict):
    action: str
    human_approved: bool
    status: str

# 2. Define Node 1: Plan Action
def plan_node(state: HITLState) -> dict:
    print("\n[Node 1: Planner] Proposed Action: Execute code snippet.")
    return {"status": "AWAITING_APPROVAL"}

# 3. Define Node 2: Execute Critical Action
def action_node(state: HITLState) -> dict:
    if state.get("human_approved"):
        print("[Node 2: Action Executed] Action successfully run with human approval!")
        return {"status": "EXECUTED_SUCCESSFULLY"}
    else:
        print("[Node 2: Action Blocked] Human denied approval!")
        return {"status": "BLOCKED"}

# 4. Assemble Graph
builder = StateGraph(HITLState)
builder.add_node("plan", plan_node)
builder.add_node("action", action_node)

builder.add_edge(START, "plan")
builder.add_edge("plan", "action")
builder.add_edge("action", END)

# Initialize Checkpointer & Add Interrupt Gate
memory = MemorySaver()
app = builder.compile(
    checkpointer=memory,
    interrupt_before=["action"]  # Intercept execution right before 'action' node runs
)

if __name__ == "__main__":
    # Unique thread identifier for session state
    config = {"configurable": {"thread_id": "session-101"}}

    print("--- 1. Initializing Graph Execution ---")
    initial_input = {"action": "RUN_SCRIPT", "human_approved": False, "status": "STARTED"}
    
    # Run the graph until it hits the interrupt boundary
    for event in app.stream(initial_input, config):
        print(f" Event: {event}")

    # Inspect current state stored in checkpointer
    current_state = app.get_state(config)
    print(f"\n⏸️ Graph Paused! Next node scheduled to run: {current_state.next}")
    print(f" Current State in Checkpointer: {current_state.values}")

    print("\n--- 2. Simulating Human Intervention ---")
    # Prompt simulate decision
    user_decision = input("Approve action? (yes/no): ").strip().lower()
    
    if user_decision == "yes":
        # Inject human approval into the persisted state
        app.update_state(config, {"human_approved": True})
        print(" Human Approval Injected!")
        
        print("\n--- 3. Resuming Graph Execution ---")
        # Resume execution from checkpoint passing None
        for event in app.stream(None, config):
            print(f" Event: {event}")
    else:
        print(" Human Denied Action. Graph cancelled.")