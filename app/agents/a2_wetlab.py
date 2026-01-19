"""
A2 Wet-Lab Protocol Agent

Generates wet-lab protocols based on sampling design.
"""

import json
from typing import Dict, Any

from app.prompts.a2_wetlab_system_prompt import TEXT as SYSTEM_PROMPT
from app.prompts.a2_wetlab_user_prompt import TEXT as USER_PROMPT
from app.llm import call_llm
from app.guards import check_wetlab_guardrails


def run_wetlab_agent(sampling_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute Wet-Lab Protocol Agent.
    
    Args:
        sampling_output: Output from A1 Sampling Agent
        
    Returns:
        Dict containing:
        - raw_output: Full LLM response
        - structured_output: Parsed JSON (if available)
        - guardrail_report: Validation of non-actionable output
        - agent: "A2_WetLab"
    """
    # Format sampling output as JSON string for prompt
    sampling_json = json.dumps(sampling_output.get("structured_output", {}), indent=2)
    
    # Inject sampling output into prompt (using replace to avoid conflicts with JSON braces)
    user_message = USER_PROMPT.replace("###SAMPLING_OUTPUT###", sampling_json)
    
    # Call LLM
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_message,
        temperature=0.3,
        max_tokens=5000
    )
    
    # Try to extract JSON from response
    structured = None
    try:
        text = response
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            json_str = text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            json_str = text[start:end].strip()
        else:
            json_str = text
        
        structured = json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Warning: Could not parse JSON from A2 output: {e}")
    
    # Apply guardrails: enforce non-actionable output
    guardrail_report = check_wetlab_guardrails(response)
    
    return {
        "agent": "A2_WetLab",
        "raw_output": response,
        "structured_output": structured,
        "guardrail_report": guardrail_report,
        "status": "success" if not guardrail_report["violations"] else "warning"
    }


def validate_wetlab_output(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate A2 output structure.
    
    Args:
        output: Agent output dict
        
    Returns:
        Validation result with warnings/errors
    """
    validation = {
        "valid": True,
        "warnings": [],
        "errors": []
    }
    
    structured = output.get("structured_output")
    if not structured:
        validation["valid"] = False
        validation["errors"].append("No structured JSON output found")
        return validation
    
    # Check required keys
    required_keys = [
        "sample_collection_preservation",
        "extraction",
        "library_prep",
        "sequencing",
        "handoff_to_bioinformatics"
    ]
    
    for key in required_keys:
        if key not in structured:
            validation["warnings"].append(f"Missing recommended key: {key}")
    
    # Check guardrail violations
    if output.get("guardrail_report", {}).get("violations"):
        validation["warnings"].append(
            f"Guardrail violations detected: {len(output['guardrail_report']['violations'])} issues"
        )
    
    return validation

