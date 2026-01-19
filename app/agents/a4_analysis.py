"""
A4 Statistical Analysis & Visualization Agent

Generates R analysis workflows from bioinformatics pipelines.
"""

import json
from typing import Dict, Any

from app.prompts.a4_analysis_system_prompt import TEXT as SYSTEM_PROMPT
from app.prompts.a4_analysis_user_prompt import TEXT as USER_PROMPT
from app.llm import call_llm
from app.guards import check_analysis_guardrails


def run_analysis_agent(bioinfo_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute Statistical Analysis Agent.
    
    Args:
        bioinfo_output: Output from A3 Bioinformatics Agent
        
    Returns:
        Dict containing:
        - raw_output: Full LLM response
        - structured_output: Parsed sections (R scripts, helpers, etc.)
        - guardrail_report: Check for execution commands
        - agent: "A4_Analysis"
    """
    # Format bioinfo output as JSON string
    bioinfo_json = json.dumps(bioinfo_output.get("structured_output", {}), indent=2)
    
    # Inject bioinfo output into prompt (using replace to avoid conflicts with JSON braces)
    user_message = USER_PROMPT.replace("###BIOINFO_OUTPUT###", bioinfo_json)
    
    # Call LLM
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_message,
        temperature=0.2,  # Lower temperature for code generation
        max_tokens=6000
    )
    
    # Apply guardrails: check for execution commands
    guardrail_report = check_analysis_guardrails(response)
    
    # Try to extract structured sections (R scripts, etc.)
    structured = extract_analysis_sections(response)
    
    return {
        "agent": "A4_Analysis",
        "raw_output": response,
        "structured_output": structured,
        "guardrail_report": guardrail_report,
        "status": "success" if not guardrail_report["violations"] else "warning"
    }


def extract_analysis_sections(response: str) -> Dict[str, str]:
    """
    Extract R code sections from response.
    
    Args:
        response: Raw LLM response
        
    Returns:
        Dict with keys: rmd_script, helper_functions, workflow_doc
    """
    sections = {}
    
    # Look for code blocks
    import re
    
    code_blocks = re.findall(r'```(\w+)\n(.*?)\n```', response, re.DOTALL)
    
    for lang, content in code_blocks:
        lower_content = content.lower()[:200]
        
        if 'analysis.rmd' in lower_content or 'rmarkdown' in lang.lower():
            sections['rmd_script'] = content.strip()
        elif 'helpers.r' in lower_content or lang.lower() == 'r':
            if 'rmd_script' not in sections:  # First R block is RMD
                sections['rmd_script'] = content.strip()
            else:
                sections['helper_functions'] = content.strip()
        elif lang.lower() == 'markdown':
            sections['workflow_doc'] = content.strip()
    
    return sections


def validate_analysis_output(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate A4 output structure.
    
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
    
    structured = output.get("structured_output", {})
    
    # Check expected sections
    expected_sections = ["rmd_script", "helper_functions", "workflow_doc"]
    
    for section in expected_sections:
        if section not in structured or not structured[section]:
            validation["warnings"].append(f"Missing or empty section: {section}")
    
    # Check guardrail violations
    if output.get("guardrail_report", {}).get("violations"):
        validation["warnings"].append(
            f"Guardrail violations detected: {len(output['guardrail_report']['violations'])} issues"
        )
    
    return validation

