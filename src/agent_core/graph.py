from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from src.agent_core.nodes import retrieval_node, reasoning_node, hypothesis_node
from src.formalizer.critic import critique_node

class ResearchState(TypedDict):
    """
    State schema for the Research Agent workflow.
    """
    topic: str
    context: List[str]
    reasoning_trace: str
    hypothesis: str
    feedback: str
    is_satisfactory: bool
    revision_count: int

def build_graph():
    """
    Constructs the Research Agent Graph.
    
    Workflow:
    1. Retrieve - Fetch papers from ArXiv and store in ChromaDB
    2. Reason - Plan the research approach
    3. Hypothesize - Generate novel hypothesis
    4. Critique - Evaluate and provide feedback
    """
    workflow = StateGraph(ResearchState)

    # Add Nodes
    workflow.add_node("retrieve", retrieval_node)
    workflow.add_node("reason", reasoning_node)
    workflow.add_node("hypothesize", hypothesis_node)
    workflow.add_node("critique", critique_node)

    # Define Edges
    workflow.set_entry_point("retrieve")
    
    workflow.add_edge("retrieve", "reason")
    workflow.add_edge("reason", "hypothesize")
    workflow.add_edge("hypothesize", "critique")
    workflow.add_edge("critique", END)

    # Compile
    app = workflow.compile()
    return app
