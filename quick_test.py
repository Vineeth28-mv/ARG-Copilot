#!/usr/bin/env python3
"""
Quick test of the framework after bug fix.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("Testing ARG Surveillance Framework - Bug Fix Verification")
print("=" * 70)
print()

# Import the workflow
try:
    from app.graph import run_workflow
    print("✓ Successfully imported run_workflow")
except ImportError as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)

# Test query
query = "Design a 6-month ARG surveillance study in hospital wastewater"

print(f"Test Query: {query}")
print()
print("-" * 70)
print()

# Run workflow
try:
    result = run_workflow(query)
    
    print()
    print("=" * 70)
    print(f"Status: {result['status']}")
    print("=" * 70)
    
    if result['status'] == 'error':
        print(f"✗ Workflow failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)
    else:
        print("✓ Workflow completed successfully!")
        print()
        print(f"A1 Output: {'Present' if result['a1_output'] else 'Missing'}")
        print(f"A2 Output: {'Present' if result['a2_output'] else 'Missing'}")
        print(f"A3 Output: {'Present' if result['a3_output'] else 'Missing'}")
        print(f"A4 Output: {'Present' if result['a4_output'] else 'Missing'}")
        
except Exception as e:
    print()
    print("=" * 70)
    print(f"✗ Test failed: {e}")
    print("=" * 70)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print("✅ Test completed successfully!")
print("=" * 70)

