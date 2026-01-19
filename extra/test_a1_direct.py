#!/usr/bin/env python3
"""
Direct test of A1 agent to debug JSON parsing issue.
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 70)
print("A1 Sampling Agent - Direct Test")
print("=" * 70)
print()

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not set!")
    exit(1)

print(f"✓ API Key loaded: {api_key[:10]}...{api_key[-4:]}")
print()

# Test query
test_query = "Design a 6-month ARG surveillance study in hospital wastewater"

print(f"Test Query: {test_query}")
print()

# Import and run A1
print("Running A1 agent...")
print("-" * 70)

from app.agents.a1_sampling import run_sampling_agent

try:
    result = run_sampling_agent(test_query)
    
    print()
    print("=" * 70)
    print("RESULT:")
    print("=" * 70)
    print(f"Agent: {result['agent']}")
    print(f"Status: {result['status']}")
    print()
    
    if result['structured_output']:
        print("✓ Structured output successfully parsed!")
        print(f"  Keys: {list(result['structured_output'].keys())}")
    else:
        print("✗ No structured output (JSON parsing failed)")
    
    print()
    print("RAW OUTPUT (first 1000 chars):")
    print("-" * 70)
    print(result['raw_output'][:1000])
    print()
    
    if len(result['raw_output']) > 1000:
        print(f"... ({len(result['raw_output']) - 1000} more characters)")
        print()
        print("Last 500 chars:")
        print("-" * 70)
        print(result['raw_output'][-500:])
    
    print()
    print("=" * 70)
    
    # Save to file
    with open("test_a1_output.txt", "w", encoding="utf-8") as f:
        f.write(result['raw_output'])
    print("✓ Full output saved to: test_a1_output.txt")
    
    if result['structured_output']:
        import json
        with open("test_a1_structured.json", "w", encoding="utf-8") as f:
            json.dump(result['structured_output'], f, indent=2)
        print("✓ Structured output saved to: test_a1_structured.json")

except Exception as e:
    print()
    print("=" * 70)
    print("❌ ERROR:")
    print("=" * 70)
    print(f"{e}")
    print()
    
    import traceback
    print("Full traceback:")
    print("-" * 70)
    traceback.print_exc()

print()
print("=" * 70)
print("Test complete")
print("=" * 70)

