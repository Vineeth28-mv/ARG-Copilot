"""
FastAPI Entry Point

REST API for running the ARG surveillance workflow.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import uvicorn

from app.graph import run_workflow
from app.cli import save_results


# Create FastAPI app
app = FastAPI(
    title="ARG Surveillance Multi-Agent API",
    description="REST API for orchestrating ARG surveillance research workflows",
    version="0.1.0"
)


# Request/Response models
class WorkflowRequest(BaseModel):
    """Request schema for workflow execution."""
    query: str = Field(
        ...,
        description="Research question or study description",
        example="Design a sampling strategy to monitor ARG dynamics in hospital wastewater over 6 months"
    )
    save_results: bool = Field(
        default=True,
        description="Whether to save results to disk"
    )
    output_dir: Optional[str] = Field(
        default="./runs",
        description="Output directory for results"
    )


class WorkflowResponse(BaseModel):
    """Response schema for workflow execution."""
    status: str = Field(
        description="Workflow status: 'complete', 'warning', 'error', or 'running'"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if workflow failed"
    )
    run_id: str = Field(
        description="Timestamp-based run identifier"
    )
    output_path: Optional[str] = Field(
        default=None,
        description="Path to saved results (if save_results=True)"
    )
    a1_status: Optional[str] = None
    a2_status: Optional[str] = None
    a3_status: Optional[str] = None
    a4_status: Optional[str] = None


class AgentOutputResponse(BaseModel):
    """Response schema for individual agent output."""
    agent: str
    status: str
    raw_output: str
    structured_output: Optional[Dict[str, Any]] = None
    guardrail_report: Optional[Dict[str, Any]] = None
    validation: Optional[Dict[str, Any]] = None


# In-memory storage for async runs (in production, use a database)
workflow_runs: Dict[str, Dict[str, Any]] = {}


# API endpoints
@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "ARG Surveillance Multi-Agent API",
        "version": "0.1.0",
        "endpoints": {
            "POST /workflow/run": "Execute the full workflow synchronously",
            "POST /workflow/run-async": "Execute the full workflow asynchronously",
            "GET /workflow/status/{run_id}": "Get status of an async workflow run",
            "GET /workflow/output/{run_id}": "Get full output of a completed workflow",
            "GET /agent/{run_id}/{agent}": "Get specific agent output"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "openai_key_set": bool(os.getenv("OPENAI_API_KEY"))
    }


@app.post("/workflow/run", response_model=WorkflowResponse)
def run_workflow_sync(request: WorkflowRequest):
    """
    Execute the full workflow synchronously.
    
    This will run A1 → A2 → A3 → A4 and return results when complete.
    """
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY environment variable not set"
        )
    
    # Generate run ID
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Run workflow
        final_state = run_workflow(request.query)
        
        # Save results if requested
        output_path = None
        if request.save_results:
            output_dir = Path(request.output_dir)
            run_dir = save_results(final_state, output_dir)
            output_path = str(run_dir.absolute())
        
        # Store in memory
        workflow_runs[run_id] = final_state
        
        # Build response
        response = WorkflowResponse(
            status=final_state.get("status", "unknown"),
            error=final_state.get("error"),
            run_id=run_id,
            output_path=output_path,
            a1_status=final_state.get("a1_output", {}).get("status"),
            a2_status=final_state.get("a2_output", {}).get("status"),
            a3_status=final_state.get("a3_output", {}).get("status"),
            a4_status=final_state.get("a4_output", {}).get("status")
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflow/run-async", response_model=Dict[str, str])
def run_workflow_async(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """
    Execute the full workflow asynchronously.
    
    Returns immediately with a run_id. Use /workflow/status/{run_id} to check progress.
    """
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY environment variable not set"
        )
    
    # Generate run ID
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    # Initialize status
    workflow_runs[run_id] = {
        "status": "running",
        "query": request.query,
        "started_at": datetime.now().isoformat()
    }
    
    # Add background task
    def run_in_background():
        try:
            final_state = run_workflow(request.query)
            
            if request.save_results:
                output_dir = Path(request.output_dir)
                run_dir = save_results(final_state, output_dir)
                final_state["output_path"] = str(run_dir.absolute())
            
            workflow_runs[run_id] = final_state
            workflow_runs[run_id]["completed_at"] = datetime.now().isoformat()
        
        except Exception as e:
            workflow_runs[run_id] = {
                "status": "error",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            }
    
    background_tasks.add_task(run_in_background)
    
    return {
        "run_id": run_id,
        "status": "running",
        "message": f"Workflow started. Check status at /workflow/status/{run_id}"
    }


@app.get("/workflow/status/{run_id}")
def get_workflow_status(run_id: str):
    """Get the current status of a workflow run."""
    if run_id not in workflow_runs:
        raise HTTPException(status_code=404, detail=f"Run ID {run_id} not found")
    
    state = workflow_runs[run_id]
    
    return {
        "run_id": run_id,
        "status": state.get("status", "unknown"),
        "error": state.get("error"),
        "a1_complete": "a1_output" in state,
        "a2_complete": "a2_output" in state,
        "a3_complete": "a3_output" in state,
        "a4_complete": "a4_output" in state
    }


@app.get("/workflow/output/{run_id}")
def get_workflow_output(run_id: str):
    """Get the full output of a completed workflow."""
    if run_id not in workflow_runs:
        raise HTTPException(status_code=404, detail=f"Run ID {run_id} not found")
    
    state = workflow_runs[run_id]
    
    if state.get("status") == "running":
        raise HTTPException(
            status_code=202,
            detail="Workflow still running. Check /workflow/status/{run_id}"
        )
    
    # Return compact version (without raw outputs)
    compact_state = {k: v for k, v in state.items() if k not in ["user_query"]}
    for agent_key in ["a1_output", "a2_output", "a3_output", "a4_output"]:
        if agent_key in compact_state:
            # Include only metadata, not full raw text
            compact_state[agent_key] = {
                "agent": compact_state[agent_key].get("agent"),
                "status": compact_state[agent_key].get("status"),
                "has_structured_output": bool(compact_state[agent_key].get("structured_output")),
                "guardrail_violations": len(
                    compact_state[agent_key].get("guardrail_report", {}).get("violations", [])
                )
            }
    
    return {
        "run_id": run_id,
        "state": compact_state
    }


@app.get("/agent/{run_id}/{agent}", response_model=AgentOutputResponse)
def get_agent_output(run_id: str, agent: str):
    """
    Get the output of a specific agent.
    
    Args:
        run_id: Workflow run ID
        agent: Agent name (a1, a2, a3, or a4)
    """
    if run_id not in workflow_runs:
        raise HTTPException(status_code=404, detail=f"Run ID {run_id} not found")
    
    if agent not in ["a1", "a2", "a3", "a4"]:
        raise HTTPException(status_code=400, detail="Agent must be a1, a2, a3, or a4")
    
    state = workflow_runs[run_id]
    agent_key = f"{agent}_output"
    
    if agent_key not in state:
        raise HTTPException(
            status_code=404,
            detail=f"Agent {agent} output not found (workflow may not have reached this agent)"
        )
    
    agent_output = state[agent_key]
    validation_reports = state.get("validation_reports", {})
    
    return AgentOutputResponse(
        agent=agent_output.get("agent", agent),
        status=agent_output.get("status", "unknown"),
        raw_output=agent_output.get("raw_output", ""),
        structured_output=agent_output.get("structured_output"),
        guardrail_report=agent_output.get("guardrail_report"),
        validation=validation_reports.get(agent)
    )


# Run server
def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the FastAPI server."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()

