"""
A1 Sampling Design Agent

Generates sampling strategies for ARG surveillance studies.
"""

import json
from typing import Dict, Any

from app.prompts.a1_sampling_system_prompt import TEXT as SYSTEM_PROMPT
from app.prompts.a1_sampling_user_prompt import TEXT as USER_PROMPT
from app.llm import call_llm


def run_sampling_agent(user_query: str) -> Dict[str, Any]:
    """
    Execute Sampling Design Agent.
    
    Args:
        user_query: User's research question or study description
        
    Returns:
        Dict containing:
        - raw_output: Full LLM response
        - structured_output: Parsed JSON (if available)
        - agent: "A1_Sampling"
    """
    # Inject user query into prompt (using replace to avoid conflicts with JSON braces)
    user_message = USER_PROMPT.replace("###USER_QUERY###", user_query)
    
    # Call LLM
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_message,
        temperature=0.3,  # Lower temperature for structured output
        max_tokens=4000
    )
    
    # Try to extract JSON from response
    structured = None
    try:
        # Look for JSON in response (may be wrapped in markdown code blocks)
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
            json_str = text.strip()
        
        structured = json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Warning: Could not parse JSON from A1 output: {e}")
        print(f"  First 200 chars of response: {response[:200]}")
        print(f"  Attempted to parse: {json_str[:200] if len(json_str) > 200 else json_str}")
        # Don't raise, just log and continue with structured=None
    
    return {
        "agent": "A1_Sampling",
        "raw_output": response,
        "structured_output": structured,
        "status": "success" if structured else "warning"
    }


def validate_sampling_output(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate A1 output structure.
    
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
        "hypotheses",
        "sampling_design",
        "metadata_requirements",
        "qc_strategy",
        "handoff_to_wetlab"
    ]
    
    for key in required_keys:
        if key not in structured:
            validation["warnings"].append(f"Missing recommended key: {key}")
    
    # Check sampling_design structure
    if "sampling_design" in structured:
        design = structured["sampling_design"]
        if not any(k in design for k in ["spatial_design", "temporal_design"]):
            validation["warnings"].append(
                "sampling_design should include spatial_design or temporal_design"
            )
    
    return validation

