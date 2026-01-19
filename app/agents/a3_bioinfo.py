"""
A3 Bioinformatics Pipeline Agent

Generates bioinformatics pipeline scripts (bash, YAML, setup).
"""

import json
from typing import Dict, Any

from app.prompts.a3_bioinfo_system_prompt import TEXT as SYSTEM_PROMPT
from app.prompts.a3_bioinfo_user_prompt import TEXT as USER_PROMPT
from app.llm import call_llm
from app.guards import check_bioinfo_guardrails


def run_bioinfo_agent(wetlab_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute Bioinformatics Pipeline Agent.
    
    Args:
        wetlab_output: Output from A2 Wet-Lab Agent
        
    Returns:
        Dict containing:
        - raw_output: Full LLM response
        - structured_output: Parsed sections (pipeline, config, etc.)
        - guardrail_report: Check for execution commands
        - agent: "A3_Bioinformatics"
    """
    # Format wetlab output as JSON string
    wetlab_json = json.dumps(wetlab_output.get("structured_output", {}), indent=2)
    
    # Inject wetlab output into prompt (using replace to avoid conflicts with JSON braces)
    user_message = USER_PROMPT.replace("###WETLAB_OUTPUT###", wetlab_json)
    
    # Call LLM
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_message,
        temperature=0.2,  # Lower temperature for code generation
        max_tokens=6000
    )
    
    # Apply guardrails: check for execution commands
    guardrail_report = check_bioinfo_guardrails(response)
    
    # Try to extract structured sections (bash, YAML, etc.)
    structured = extract_bioinfo_sections(response)
    
    return {
        "agent": "A3_Bioinformatics",
        "raw_output": response,
        "structured_output": structured,
        "guardrail_report": guardrail_report,
        "status": "success" if not guardrail_report["violations"] else "warning"
    }


def extract_bioinfo_sections(response: str) -> Dict[str, str]:
    """
    Extract code sections from response (bash, YAML, etc.).
    
    Args:
        response: Raw LLM response
        
    Returns:
        Dict with keys: pipeline_script, config_yaml, setup_script, readme, handoff_yaml
    """
    sections = {}
    
    # Look for code blocks with labels
    import re
    
    # Pattern: ```language\n# Filename or description\ncontent\n```
    code_blocks = re.findall(r'```(\w+)\n(.*?)\n```', response, re.DOTALL)
    
    for lang, content in code_blocks:
        # Try to infer section based on content or filename comments
        lower_content = content.lower()[:200]  # Check first 200 chars
        
        if 'pipeline.sh' in lower_content or 'bash' in lang.lower():
            sections['pipeline_script'] = content.strip()
        elif 'config.yaml' in lower_content or 'yml' in lang.lower() or 'yaml' in lang.lower():
            if 'data_handoff' in lower_content:
                sections['handoff_yaml'] = content.strip()
            else:
                sections['config_yaml'] = content.strip()
        elif 'setup' in lower_content and 'database' in lower_content:
            sections['setup_script'] = content.strip()
        elif 'readme' in lower_content or lang.lower() == 'markdown':
            sections['readme'] = content.strip()
    
    return sections


def validate_bioinfo_output(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate A3 output structure.
    
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
    expected_sections = [
        "pipeline_script",
        "config_yaml",
        "setup_script",
        "readme",
        "handoff_yaml"
    ]
    
    for section in expected_sections:
        if section not in structured or not structured[section]:
            validation["warnings"].append(f"Missing or empty section: {section}")
    
    # Check guardrail violations
    if output.get("guardrail_report", {}).get("violations"):
        validation["warnings"].append(
            f"Guardrail violations detected: {len(output['guardrail_report']['violations'])} issues"
        )
        for violation in output['guardrail_report']['violations'][:3]:  # Show first 3
            validation["warnings"].append(f"  - {violation}")
    
    return validation

