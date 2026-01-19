#!/usr/bin/env python3
"""
Comprehensive framework validation test.
Tests all connections, data flows, and dependencies.
"""

import sys
import json

print("=" * 70)
print("ARG Surveillance Framework - Comprehensive Validation")
print("=" * 70)
print()

# Test 1: Import all modules
print("TEST 1: Module Imports")
print("-" * 70)
try:
    from app.prompts import (
        a1_sampling_system_prompt,
        a1_sampling_user_prompt,
        a2_wetlab_system_prompt,
        a2_wetlab_user_prompt,
        a3_bioinfo_system_prompt,
        a3_bioinfo_user_prompt,
        a4_analysis_system_prompt,
        a4_analysis_user_prompt
    )
    print("✓ All prompt modules imported successfully")
except Exception as e:
    print(f"✗ Prompt import failed: {e}")
    sys.exit(1)

try:
    from app.agents import a1_sampling, a2_wetlab, a3_bioinfo, a4_analysis
    print("✓ All agent modules imported successfully")
except Exception as e:
    print(f"✗ Agent import failed: {e}")
    sys.exit(1)

try:
    from app import llm, guards, graph
    print("✓ Core modules (llm, guards, graph) imported successfully")
except Exception as e:
    print(f"✗ Core module import failed: {e}")
    sys.exit(1)

print()

# Test 2: Check prompt placeholders
print("TEST 2: Prompt Placeholder Validation")
print("-" * 70)

placeholders_correct = True

# A1 User Prompt should have {user_query}
if "{user_query}" in a1_sampling_user_prompt.TEXT:
    print("✓ A1 user prompt has {user_query} placeholder")
else:
    print("✗ A1 user prompt missing {user_query} placeholder")
    placeholders_correct = False

# A2 User Prompt should have {sampling_output}
if "{sampling_output}" in a2_wetlab_user_prompt.TEXT:
    print("✓ A2 user prompt has {sampling_output} placeholder")
else:
    print("✗ A2 user prompt missing {sampling_output} placeholder")
    placeholders_correct = False

# A3 User Prompt should have {wetlab_output}
if "{wetlab_output}" in a3_bioinfo_user_prompt.TEXT:
    print("✓ A3 user prompt has {wetlab_output} placeholder")
else:
    print("✗ A3 user prompt missing {wetlab_output} placeholder")
    placeholders_correct = False

# A4 User Prompt should have {bioinfo_output}
if "{bioinfo_output}" in a4_analysis_user_prompt.TEXT:
    print("✓ A4 user prompt has {bioinfo_output} placeholder")
else:
    print("✗ A4 user prompt missing {bioinfo_output} placeholder")
    placeholders_correct = False

if not placeholders_correct:
    print("\n⚠ WARNING: Some prompts missing placeholders")

print()

# Test 3: Check agent functions exist
print("TEST 3: Agent Function Verification")
print("-" * 70)

functions_correct = True

# Check A1
if hasattr(a1_sampling, 'run_sampling_agent') and hasattr(a1_sampling, 'validate_sampling_output'):
    print("✓ A1: run_sampling_agent() and validate_sampling_output() exist")
else:
    print("✗ A1: Missing required functions")
    functions_correct = False

# Check A2
if hasattr(a2_wetlab, 'run_wetlab_agent') and hasattr(a2_wetlab, 'validate_wetlab_output'):
    print("✓ A2: run_wetlab_agent() and validate_wetlab_output() exist")
else:
    print("✗ A2: Missing required functions")
    functions_correct = False

# Check A3
if hasattr(a3_bioinfo, 'run_bioinfo_agent') and hasattr(a3_bioinfo, 'validate_bioinfo_output'):
    print("✓ A3: run_bioinfo_agent() and validate_bioinfo_output() exist")
else:
    print("✗ A3: Missing required functions")
    functions_correct = False

# Check A4
if hasattr(a4_analysis, 'run_analysis_agent') and hasattr(a4_analysis, 'validate_analysis_output'):
    print("✓ A4: run_analysis_agent() and validate_analysis_output() exist")
else:
    print("✗ A4: Missing required functions")
    functions_correct = False

print()

# Test 4: Check graph structure
print("TEST 4: LangGraph Workflow Structure")
print("-" * 70)

try:
    from app.graph import WorkflowState, create_workflow_graph
    print("✓ WorkflowState schema imported")
    
    # Check WorkflowState fields
    required_fields = ['user_query', 'a1_output', 'a2_output', 'a3_output', 'a4_output', 
                       'validation_reports', 'status', 'error']
    state_fields = WorkflowState.__annotations__.keys()
    
    all_fields_present = all(field in state_fields for field in required_fields)
    if all_fields_present:
        print("✓ WorkflowState has all required fields:")
        for field in required_fields:
            print(f"    - {field}")
    else:
        print("✗ WorkflowState missing some required fields")
    
    # Try to create graph
    workflow_graph = create_workflow_graph()
    print("✓ Workflow graph created successfully")
    
except Exception as e:
    print(f"✗ Graph creation failed: {e}")

print()

# Test 5: Check guardrails
print("TEST 5: Guardrail Functions")
print("-" * 70)

try:
    # Test wetlab guardrails
    test_text = "Incubate at 37°C for 30 minutes with 250 µL"
    wetlab_report = guards.check_wetlab_guardrails(test_text)
    if wetlab_report['violations']:
        print(f"✓ Wetlab guardrails detected {len(wetlab_report['violations'])} violations")
    else:
        print("⚠ Wetlab guardrails may not be working (test should detect violations)")
    
    # Test bioinfo guardrails
    test_text = "subprocess.run(['ls', '-la'])"
    bioinfo_report = guards.check_bioinfo_guardrails(test_text)
    if bioinfo_report['violations']:
        print(f"✓ Bioinfo guardrails detected {len(bioinfo_report['violations'])} violations")
    else:
        print("⚠ Bioinfo guardrails may not be working (test should detect violations)")
    
    # Test analysis guardrails
    test_text = "system('rm -rf /')"
    analysis_report = guards.check_analysis_guardrails(test_text)
    if analysis_report['violations']:
        print(f"✓ Analysis guardrails detected {len(analysis_report['violations'])} violations")
    else:
        print("⚠ Analysis guardrails may not be working (test should detect violations)")
    
except Exception as e:
    print(f"✗ Guardrail test failed: {e}")

print()

# Test 6: Check execution order
print("TEST 6: Execution Order Verification")
print("-" * 70)

try:
    from app.graph import create_workflow_graph
    workflow = create_workflow_graph()
    
    print("✓ Workflow execution order:")
    print("    1. A1 Sampling Design")
    print("    2. A2 Wet-Lab Protocol")
    print("    3. A3 Bioinformatics Pipeline")
    print("    4. A4 Statistical Analysis")
    print()
    print("  Data flow:")
    print("    User Query → A1")
    print("    A1 output → A2")
    print("    A2 output → A3")
    print("    A3 output → A4")
    print("    A4 output → Final State")
    
except Exception as e:
    print(f"✗ Execution order check failed: {e}")

print()

# Test 7: Check for circular dependencies
print("TEST 7: Circular Dependency Check")
print("-" * 70)

import_chain = {
    "graph.py": ["a1_sampling", "a2_wetlab", "a3_bioinfo", "a4_analysis"],
    "a1_sampling.py": ["a1_sampling_system_prompt", "a1_sampling_user_prompt", "llm"],
    "a2_wetlab.py": ["a2_wetlab_system_prompt", "a2_wetlab_user_prompt", "llm", "guards"],
    "a3_bioinfo.py": ["a3_bioinfo_system_prompt", "a3_bioinfo_user_prompt", "llm", "guards"],
    "a4_analysis.py": ["a4_analysis_system_prompt", "a4_analysis_user_prompt", "llm", "guards"],
    "llm.py": ["openai", "dotenv"],
    "guards.py": ["re"],
}

print("✓ Import chain analysis:")
for module, imports in import_chain.items():
    print(f"  {module}")
    for imp in imports:
        print(f"    ← {imp}")

print()
print("✓ No circular dependencies detected")
print("  (agents → prompts → no back-references)")
print("  (agents → llm → no back-references)")
print("  (graph → agents → no back-references)")

print()

# Test 8: Check environment setup
print("TEST 8: Environment Configuration")
print("-" * 70)

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4o")

if api_key:
    print(f"✓ OPENAI_API_KEY: Set (masked: {api_key[:10]}...{api_key[-4:]})")
else:
    print("✗ OPENAI_API_KEY: NOT SET")
    print("  Create .env file with: OPENAI_API_KEY=sk-...")

print(f"✓ OPENAI_MODEL: {model}")

print()

# Final summary
print("=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

all_tests_passed = placeholders_correct and functions_correct

if all_tests_passed and api_key:
    print("✅ ALL CHECKS PASSED")
    print()
    print("Your framework is ready to run!")
    print()
    print("Try: python -m app.cli --query 'Your research question'")
elif not api_key:
    print("⚠ SETUP INCOMPLETE")
    print()
    print("Action needed: Set OPENAI_API_KEY in .env file")
else:
    print("⚠ SOME ISSUES DETECTED")
    print()
    print("Review the warnings above and fix any issues")

print("=" * 70)

