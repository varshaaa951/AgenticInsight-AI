from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define shared graph state
class AgentState(TypedDict):
    query: str
    is_safe: bool
    status: str

# 2. Define Node 1: Guardrail Inspector
def guardrail_node(state: AgentState) -> dict:
    print("\n[Node 1: Guardrail] Inspecting query...")
    query = state["query"]
    
    # Simple security check for risky terms
    if "DROP" in query.upper() or "DELETE" in query.upper():
        print(" Security Risk Detected: Risky command found.")
        return {"is_safe": False, "status": "REJECTED"}
    
    print(" Query passed safety check.")
    return {"is_safe": True, "status": "APPROVED"}

# 3. Define Node 2: Command Executor
def executor_node(state: AgentState) -> dict:
    print("[Node 2: Executor] Executing query...")
    updated_query = state["query"] + " -> Executed successfully!"
    return {"query": updated_query, "status": "COMPLETED"}

# 4. Define Routing Logic
def route_query(state: AgentState) -> str:
    if state["is_safe"]:
        return "executor"
    return END

# 5. Build and Compile the Graph
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("guardrail", guardrail_node)
builder.add_node("executor", executor_node)

# Add edges
builder.add_edge(START, "guardrail")
builder.add_conditional_edges(
    "guardrail",
    route_query,
    {
        "executor": "executor",
        END: END
    }
)
builder.add_edge("executor", END)

# Compile into an executable graph app
app = builder.compile()

# Test Execution
if __name__ == "__main__":
    print("--- Test 1: Safe Query ---")
    safe_input = {"query": "SELECT * FROM users;", "is_safe": False, "status": "PENDING"}
    result_1 = app.invoke(safe_input)
    print(f"Final State: {result_1}")

    print("\n--- Test 2: Unsafe Query ---")
    unsafe_input = {"query": "DROP TABLE users;", "is_safe": False, "status": "PENDING"}
    result_2 = app.invoke(unsafe_input)
    print(f"Final State: {result_2}")