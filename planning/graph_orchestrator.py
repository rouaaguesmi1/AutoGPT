#planning/react_loop.py (Now planning/graph_orchestrator.py)
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents.agent_nodes import planner_node, researcher_node, coder_node, writer_node

class AgentState(TypedDict):
    """
    Defines the shared state between the nodes in the graph.
    """
    objective: str
    plan: str
    research_summary: str
    code: str
    report: str

def should_continue(state: AgentState) -> str:
    """
    A simple router. In a more complex setup, an LLM could make this decision.
    For this example, we follow a fixed path but this is where conditional logic would go. [19]
    """
    # This is a simplified conditional edge. A real implementation could use an LLM
    # to decide if coding is necessary, if debugging is needed, etc. [4, 21]
    if not state.get('research_summary'):
        return "research"
    if not state.get('code'):
        return "code"
    return "write"


def get_workflow():
    """
    Constructs and returns the LangGraph workflow.
    """
    # Define the state graph
    workflow = StateGraph(AgentState)

    # Add the nodes (our "agents")
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("writer", writer_node)

    # Define the edges (the flow of control)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "coder")
    workflow.add_edge("coder", "writer")
    workflow.add_edge("writer", END)
    
    # The conditional router is more advanced and would replace the simple edges above
    # Example of how a conditional router would be added:
    # workflow.add_conditional_edges(
    #     "planner",
    #     should_continue,
    #     {"research": "researcher", "code": "coder", "write": "writer"}
    # )

    # Compile the graph into a runnable app
    app = workflow.compile()
    return app