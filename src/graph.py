from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.state import AgentState
from src.agents.orchestrator import orchestrator_agent
from src.agents.code_analyst import code_analyst_agent
from src.agents.web_research import web_research_agent
from src.agents.synthesizer import synthesizer_agent

def create_agentic_graph():
    builder = StateGraph(AgentState)

    # 1. Add Nodes
    builder.add_node("orchestrator", orchestrator_agent)
    builder.add_node("code_analyst", code_analyst_agent)
    builder.add_node("web_research", web_research_agent)
    builder.add_node("synthesizer", synthesizer_agent)

    # 2. Define Execution Flow
    builder.add_edge(START, "orchestrator")
    
    # Run Code Analyst and Web Research sequentially from Orchestrator
    builder.add_edge("orchestrator", "code_analyst")
    builder.add_edge("code_analyst", "web_research")
    
    # Gate before Synthesizer
    builder.add_edge("web_research", "synthesizer")
    builder.add_edge("synthesizer", END)

    # 3. Checkpointer for HITL
    memory = MemorySaver()
    
    # Interrupt right before final report synthesis for human sign-off
    app = builder.compile(
        checkpointer=memory,
        interrupt_before=["synthesizer"]
    )
    return app

app = create_agentic_graph()