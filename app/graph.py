"""
LangGraph Orchestration

Defines the multi-agent workflow graph: A1 → A2 → A3 → A4
"""

from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

from app.agents.a1_sampling import run_sampling_agent, validate_sampling_output
from app.agents.a2_wetlab import run_wetlab_agent, validate_wetlab_output
from app.agents.a3_bioinfo import run_bioinfo_agent, validate_bioinfo_output
from app.agents.a4_analysis import run_analysis_agent, validate_analysis_output


# State schema for the workflow
class WorkflowState(TypedDict):
    """State passed between agents in the graph."""
    user_query: str
    a1_output: Dict[str, Any]
    a2_output: Dict[str, Any]
    a3_output: Dict[str, Any]
    a4_output: Dict[str, Any]
    validation_reports: Dict[str, Any]
    status: str
    error: str


# Agent node functions
def node_a1_sampling(state: WorkflowState) -> WorkflowState:
    """Execute A1 Sampling Agent."""
    print("🔬 Running A1: Sampling Design Agent...")
    
    try:
        output = run_sampling_agent(state["user_query"])
        validation = validate_sampling_output(output)
        
        state["a1_output"] = output
        state["validation_reports"]["a1"] = validation
        
        # Only set error if there's NO output at all
        if not output.get("raw_output"):
            state["status"] = "error"
            state["error"] = "A1 produced no output"
        elif not validation["valid"]:
            # Validation failed but we have output - continue with warning
            state["status"] = "warning"
            print(f"⚠ A1 validation warnings: {validation.get('errors', [])}")
        
        print(f"✓ A1 complete (status: {output['status']})")
    
    except Exception as e:
        print(f"✗ A1 failed: {e}")
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        state["status"] = "error"
        state["error"] = str(e)
    
    return state


def node_a2_wetlab(state: WorkflowState) -> WorkflowState:
    """Execute A2 Wet-Lab Agent."""
    print("🧪 Running A2: Wet-Lab Protocol Agent...")
    
    if state.get("status") == "error":
        print("⚠ Skipping A2 due to previous error")
        return state
    
    try:
        output = run_wetlab_agent(state["a1_output"])
        validation = validate_wetlab_output(output)
        
        state["a2_output"] = output
        state["validation_reports"]["a2"] = validation
        
        if not validation["valid"]:
            state["status"] = "error"
            state["error"] = f"A2 validation failed: {validation['errors']}"
        
        print(f"✓ A2 complete (status: {output['status']})")
    
    except Exception as e:
        print(f"✗ A2 failed: {e}")
        state["status"] = "error"
        state["error"] = str(e)
    
    return state


def node_a3_bioinfo(state: WorkflowState) -> WorkflowState:
    """Execute A3 Bioinformatics Agent."""
    print("💻 Running A3: Bioinformatics Pipeline Agent...")
    
    if state.get("status") == "error":
        print("⚠ Skipping A3 due to previous error")
        return state
    
    try:
        output = run_bioinfo_agent(state["a2_output"])
        validation = validate_bioinfo_output(output)
        
        state["a3_output"] = output
        state["validation_reports"]["a3"] = validation
        
        if not validation["valid"]:
            state["status"] = "error"
            state["error"] = f"A3 validation failed: {validation['errors']}"
        
        print(f"✓ A3 complete (status: {output['status']})")
    
    except Exception as e:
        print(f"✗ A3 failed: {e}")
        state["status"] = "error"
        state["error"] = str(e)
    
    return state


def node_a4_analysis(state: WorkflowState) -> WorkflowState:
    """Execute A4 Analysis Agent."""
    print("📊 Running A4: Statistical Analysis Agent...")
    
    if state.get("status") == "error":
        print("⚠ Skipping A4 due to previous error")
        return state
    
    try:
        output = run_analysis_agent(state["a3_output"])
        validation = validate_analysis_output(output)
        
        state["a4_output"] = output
        state["validation_reports"]["a4"] = validation
        
        if not validation["valid"]:
            state["status"] = "warning"  # A4 is terminal, so warning not error
        else:
            state["status"] = "complete"
        
        print(f"✓ A4 complete (status: {output['status']})")
    
    except Exception as e:
        print(f"✗ A4 failed: {e}")
        state["status"] = "error"
        state["error"] = str(e)
    
    return state


# Build the graph
def create_workflow_graph():
    """
    Create the LangGraph workflow.
    
    Returns:
        Compiled LangGraph
    """
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("a1_sampling", node_a1_sampling)
    workflow.add_node("a2_wetlab", node_a2_wetlab)
    workflow.add_node("a3_bioinfo", node_a3_bioinfo)
    workflow.add_node("a4_analysis", node_a4_analysis)
    
    # Define edges (sequential flow)
    workflow.set_entry_point("a1_sampling")
    workflow.add_edge("a1_sampling", "a2_wetlab")
    workflow.add_edge("a2_wetlab", "a3_bioinfo")
    workflow.add_edge("a3_bioinfo", "a4_analysis")
    workflow.add_edge("a4_analysis", END)
    
    # Compile
    return workflow.compile()


# Main execution function
def run_workflow(user_query: str) -> Dict[str, Any]:
    """
    Execute the full multi-agent workflow.
    
    Args:
        user_query: User's research question or study description
        
    Returns:
        Final state dict with all agent outputs
    """
    # Initialize state
    initial_state: WorkflowState = {
        "user_query": user_query,
        "a1_output": {},
        "a2_output": {},
        "a3_output": {},
        "a4_output": {},
        "validation_reports": {},
        "status": "running",
        "error": ""
    }
    
    # Create and run graph
    graph = create_workflow_graph()
    
    print("=" * 60)
    print("🚀 Starting ARG Surveillance Multi-Agent Workflow")
    print("=" * 60)
    print(f"User Query: {user_query[:100]}...")
    print()
    
    final_state = graph.invoke(initial_state)
    
    print()
    print("=" * 60)
    print(f"✓ Workflow completed with status: {final_state['status']}")
    print("=" * 60)
    
    return final_state


# Optional: Add conditional routing for error handling
def should_continue(state: WorkflowState) -> str:
    """
    Conditional routing based on state.
    
    Args:
        state: Current workflow state
        
    Returns:
        Next node name or "end"
    """
    if state.get("status") == "error":
        return "end"
    return "continue"

