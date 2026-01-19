"""
Guardrail Validators

Check agent outputs for policy violations (execution commands, actionable instructions, etc.).
"""

import re
from typing import Dict, List, Any


def check_wetlab_guardrails(response: str) -> Dict[str, Any]:
    """
    Enforce non-actionable wet-lab output.
    
    A2 should NOT generate specific temperatures, volumes, timings, or step-by-step instructions.
    Flag these patterns.
    
    Args:
        response: Raw LLM response from A2
        
    Returns:
        Dict with:
        - violations: List of detected issues
        - risk_level: "low" | "medium" | "high"
        - message: Summary
    """
    violations = []
    
    # Pattern 1: Specific temperatures (e.g., "37°C", "65 degrees")
    temp_pattern = r'\b\d+\s*[°]?[CF]\b|\b\d+\s+degrees?\b'
    if re.search(temp_pattern, response, re.IGNORECASE):
        violations.append("Contains specific temperature values (should be conceptual only)")
    
    # Pattern 2: Specific volumes (e.g., "250 µL", "5 mL")
    volume_pattern = r'\b\d+\s*[µu]?[LlmM][Ll]?\b'
    if re.search(volume_pattern, response):
        violations.append("Contains specific volume measurements (should be conceptual only)")
    
    # Pattern 3: Specific timings (e.g., "30 minutes", "2 hours")
    timing_pattern = r'\b\d+\s*(min|minutes?|hrs?|hours?|sec|seconds?)\b'
    if re.search(timing_pattern, response, re.IGNORECASE):
        violations.append("Contains specific timing instructions (should be conceptual only)")
    
    # Pattern 4: Step-by-step procedural language
    procedural_patterns = [
        r'\b(step \d+|first,|second,|then,|next,|finally,)\b',
        r'\badd \d+',
        r'\bmix for \d+',
        r'\bincubate (at|for)\b'
    ]
    for pattern in procedural_patterns:
        if re.search(pattern, response, re.IGNORECASE):
            violations.append("Contains step-by-step procedural instructions (should be protocol references only)")
            break
    
    # Determine risk level
    if len(violations) == 0:
        risk_level = "low"
        message = "No guardrail violations detected"
    elif len(violations) <= 2:
        risk_level = "medium"
        message = f"Minor violations detected ({len(violations)} issues)"
    else:
        risk_level = "high"
        message = f"Multiple violations detected ({len(violations)} issues) - output may be too actionable"
    
    return {
        "violations": violations,
        "risk_level": risk_level,
        "message": message
    }


def check_bioinfo_guardrails(response: str) -> Dict[str, Any]:
    """
    Check for execution commands in bioinformatics code.
    
    A3 generates code but should NOT include actual execution (subprocess, docker run, etc.).
    
    Args:
        response: Raw LLM response from A3
        
    Returns:
        Dict with violations and risk level
    """
    violations = []
    
    # Pattern 1: Subprocess execution
    if re.search(r'subprocess\.(run|call|Popen|check_output)', response):
        violations.append("Contains subprocess execution (Python)")
    
    # Pattern 2: Shell execution patterns
    shell_exec_patterns = [
        r'\$\(.*?\)',  # Command substitution $(...)
        r'`.*?`',      # Backtick command substitution
        r'\bexec\s+',  # exec command
        r'\beval\s+',  # eval command
    ]
    for pattern in shell_exec_patterns:
        if re.search(pattern, response):
            violations.append(f"Contains shell execution pattern: {pattern}")
    
    # Pattern 3: Docker/container execution
    if re.search(r'\bdocker (run|exec|start)\b', response):
        violations.append("Contains Docker execution command")
    
    # Pattern 4: Package installation
    install_patterns = [
        r'!pip install',
        r'pip install',
        r'conda install',
        r'apt-get install',
        r'yum install'
    ]
    for pattern in install_patterns:
        if re.search(pattern, response):
            violations.append(f"Contains package installation command: {pattern}")
            break
    
    # Determine risk level
    if len(violations) == 0:
        risk_level = "low"
        message = "No execution commands detected"
    elif len(violations) <= 2:
        risk_level = "medium"
        message = f"Some execution patterns detected ({len(violations)} issues)"
    else:
        risk_level = "high"
        message = f"Multiple execution commands detected ({len(violations)} issues)"
    
    return {
        "violations": violations,
        "risk_level": risk_level,
        "message": message
    }


def check_analysis_guardrails(response: str) -> Dict[str, Any]:
    """
    Check for execution commands in R analysis code.
    
    A4 generates R code but should NOT include system calls or package installation.
    
    Args:
        response: Raw LLM response from A4
        
    Returns:
        Dict with violations and risk level
    """
    violations = []
    
    # Pattern 1: System calls in R
    if re.search(r'\bsystem\(|system2\(', response):
        violations.append("Contains R system() calls")
    
    # Pattern 2: Package installation
    install_patterns = [
        r'install\.packages\(',
        r'BiocManager::install\(',
        r'devtools::install',
        r'remotes::install'
    ]
    for pattern in install_patterns:
        if re.search(pattern, response):
            violations.append("Contains package installation command (R)")
            break
    
    # Pattern 3: File system manipulation (should be read-only)
    dangerous_io = [
        r'\bfile\.remove\(',
        r'\bunlink\(',
        r'\bsystem\.file\(',
    ]
    for pattern in dangerous_io:
        if re.search(pattern, response):
            violations.append(f"Contains file system manipulation: {pattern}")
    
    # Determine risk level
    if len(violations) == 0:
        risk_level = "low"
        message = "No execution commands detected"
    else:
        risk_level = "medium"
        message = f"Execution patterns detected ({len(violations)} issues)"
    
    return {
        "violations": violations,
        "risk_level": risk_level,
        "message": message
    }


def sanitize_output(text: str, guardrail_report: Dict[str, Any]) -> str:
    """
    Optionally sanitize output by removing/commenting out violations.
    
    Args:
        text: Original output
        guardrail_report: Report from guardrail check
        
    Returns:
        Sanitized text (for now, just returns original with warning comments)
    """
    if guardrail_report["risk_level"] == "high":
        warning = (
            "\n\n<!-- WARNING: Guardrail violations detected -->\n"
            f"<!-- {guardrail_report['message']} -->\n"
            f"<!-- Violations: {', '.join(guardrail_report['violations'])} -->\n\n"
        )
        return warning + text
    
    return text

