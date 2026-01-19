"""
CLI Entry Point

Command-line interface for running the ARG surveillance workflow.
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path

from app.graph import run_workflow


def save_results(state: dict, output_dir: Path):
    """
    Save agent outputs to timestamped directory.
    
    Args:
        state: Final workflow state
        output_dir: Base output directory
    """
    # Create timestamped subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_dir / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 Saving results to: {run_dir}")
    
    # Save each agent's output
    agents = ["a1", "a2", "a3", "a4"]
    
    for agent in agents:
        output_key = f"{agent}_output"
        if output_key not in state or not state[output_key]:
            continue
        
        agent_output = state[output_key]
        
        # Save raw markdown output
        raw_output = agent_output.get("raw_output", "")
        if raw_output:
            md_path = run_dir / f"{agent.upper()}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(raw_output)
            print(f"  ✓ {agent.upper()}.md")
        
        # Save structured JSON output
        structured = agent_output.get("structured_output")
        if structured:
            json_path = run_dir / f"{agent.upper()}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(structured, f, indent=2)
            print(f"  ✓ {agent.upper()}.json")
        
        # Save guardrail report if present
        guardrail = agent_output.get("guardrail_report")
        if guardrail and guardrail.get("violations"):
            guard_path = run_dir / f"{agent.upper()}_guardrails.json"
            with open(guard_path, "w", encoding="utf-8") as f:
                json.dump(guardrail, f, indent=2)
            print(f"  ⚠ {agent.upper()}_guardrails.json (violations detected)")
    
    # Save validation reports
    validation_path = run_dir / "validation_reports.json"
    with open(validation_path, "w", encoding="utf-8") as f:
        json.dump(state.get("validation_reports", {}), f, indent=2)
    print(f"  ✓ validation_reports.json")
    
    # Save full state
    state_path = run_dir / "full_state.json"
    with open(state_path, "w", encoding="utf-8") as f:
        # Remove raw outputs (too large)
        compact_state = {k: v for k, v in state.items() if k != "user_query"}
        for agent_key in ["a1_output", "a2_output", "a3_output", "a4_output"]:
            if agent_key in compact_state:
                compact_state[agent_key] = {
                    k: v for k, v in compact_state[agent_key].items() 
                    if k != "raw_output"
                }
        json.dump(compact_state, f, indent=2)
    print(f"  ✓ full_state.json")
    
    # Create summary
    summary_path = run_dir / "SUMMARY.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"# ARG Surveillance Workflow Run\n\n")
        f.write(f"**Timestamp:** {timestamp}\n\n")
        f.write(f"**Status:** {state.get('status', 'unknown')}\n\n")
        
        if state.get("error"):
            f.write(f"**Error:** {state['error']}\n\n")
        
        f.write(f"## User Query\n\n{state['user_query']}\n\n")
        
        f.write(f"## Agent Outputs\n\n")
        for agent in agents:
            output_key = f"{agent}_output"
            if output_key in state and state[output_key]:
                status = state[output_key].get("status", "unknown")
                f.write(f"- **{agent.upper()}**: {status}\n")
        
        f.write(f"\n## Files Generated\n\n")
        for file in run_dir.glob("*"):
            if file.name != "SUMMARY.md":
                f.write(f"- `{file.name}`\n")
    
    print(f"  ✓ SUMMARY.md")
    print(f"\n✅ Results saved successfully!")
    
    return run_dir


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ARG Surveillance Multi-Agent Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python -m app.cli
  
  # Direct query
  python -m app.cli --query "Design a study to monitor ARG dynamics in hospital wastewater"
  
  # Specify output directory
  python -m app.cli --query "..." --output ./my_results
        """
    )
    
    parser.add_argument(
        "--query",
        type=str,
        help="Research question or study description (if not provided, interactive mode)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./runs",
        help="Output directory for results (default: ./runs)"
    )
    
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save results to disk (just print)"
    )
    
    args = parser.parse_args()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY='your-key-here'")
        return 1
    
    # Get user query
    if args.query:
        user_query = args.query
    else:
        print("=" * 60)
        print("ARG Surveillance Multi-Agent Framework - Interactive Mode")
        print("=" * 60)
        print("\nEnter your research question or study description:")
        print("(Press Ctrl+D or Ctrl+Z when done)\n")
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        user_query = "\n".join(lines).strip()
        
        if not user_query:
            print("\n❌ No query provided. Exiting.")
            return 1
    
    print("\n" + "=" * 60)
    print(f"Query: {user_query[:100]}...")
    print("=" * 60 + "\n")
    
    # Run workflow
    try:
        final_state = run_workflow(user_query)
    except Exception as e:
        print(f"\n❌ Workflow failed with error: {e}")
        return 1
    
    # Save results
    if not args.no_save:
        output_dir = Path(args.output)
        run_dir = save_results(final_state, output_dir)
        print(f"\n📂 Results saved to: {run_dir.absolute()}")
    
    # Print final status
    status = final_state.get("status", "unknown")
    if status == "complete":
        print("\n✅ Workflow completed successfully!")
        return 0
    elif status == "warning":
        print("\n⚠ Workflow completed with warnings")
        return 0
    else:
        print(f"\n❌ Workflow failed: {final_state.get('error', 'Unknown error')}")
        return 1


if __name__ == "__main__":
    exit(main())

