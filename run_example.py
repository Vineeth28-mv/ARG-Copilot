#!/usr/bin/env python3
"""
Example script for running the ARG surveillance workflow programmatically.
"""

import os
from pathlib import Path
from app.graph import run_workflow
from app.cli import save_results


def main():
    """Run example workflow."""
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not set")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        return 1
    
    # Load example query
    query_file = Path("example_query.txt")
    if not query_file.exists():
        print(f"❌ Error: {query_file} not found")
        return 1
    
    user_query = query_file.read_text(encoding="utf-8")
    
    print("=" * 60)
    print("Running Example Workflow")
    print("=" * 60)
    print(f"\nQuery:\n{user_query[:200]}...\n")
    
    # Run workflow
    try:
        final_state = run_workflow(user_query)
    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")
        return 1
    
    # Save results
    output_dir = Path("./runs")
    run_dir = save_results(final_state, output_dir)
    
    print(f"\n📂 Results saved to: {run_dir.absolute()}")
    print(f"✅ Workflow completed with status: {final_state['status']}")
    
    return 0


if __name__ == "__main__":
    exit(main())



