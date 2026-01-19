# ARG Surveillance Framework - System Architecture

## Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            USER INTERFACE LAYER                              │
├──────────────────────────────────┬──────────────────────────────────────────┤
│          CLI (app/cli.py)         │         API (app/api.py)                 │
│                                   │                                          │
│  • Interactive mode               │  • POST /workflow/run (sync)             │
│  • Direct query mode              │  • POST /workflow/run-async              │
│  • Result saving                  │  • GET /workflow/status/{run_id}         │
│  • Console output                 │  • GET /workflow/output/{run_id}         │
│                                   │  • GET /agent/{run_id}/{agent}           │
└──────────────────────────────────┴──────────────────────────────────────────┘
                                   │
                                   ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATION LAYER (LangGraph)                        │
│                           app/graph.py                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  WorkflowState:                                                              │
│    • user_query: str                                                         │
│    • a1_output, a2_output, a3_output, a4_output: Dict[str, Any]             │
│    • validation_reports: Dict[str, Any]                                      │
│    • status: str ("running" | "complete" | "error" | "warning")             │
│    • error: str                                                              │
│                                                                              │
│  Workflow Graph:                                                             │
│    [START] → node_a1_sampling → node_a2_wetlab →                            │
│              node_a3_bioinfo → node_a4_analysis → [END]                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AGENT EXECUTION LAYER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  A1: Sampling Design Agent (app/agents/a1_sampling.py)           │      │
│  │                                                                   │      │
│  │  Input:  user_query (string)                                     │      │
│  │  Process: → Load prompts (system + user)                         │      │
│  │           → Format user prompt with {user_query}                 │      │
│  │           → Call LLM (temperature=0.3, max_tokens=4000)          │      │
│  │           → Parse JSON response                                  │      │
│  │           → Validate output structure                            │      │
│  │  Output: Dict{raw_output, structured_output, agent, status}      │      │
│  │                                                                   │      │
│  │  Handoff: sampling_design JSON → A2                              │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                   ↓                                          │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  A2: Wet-Lab Protocol Agent (app/agents/a2_wetlab.py)            │      │
│  │                                                                   │      │
│  │  Input:  a1_output (Dict with sampling design)                   │      │
│  │  Process: → Load prompts (system + user)                         │      │
│  │           → Format user prompt with {sampling_output}            │      │
│  │           → Call LLM (temperature=0.3, max_tokens=5000)          │      │
│  │           → Parse JSON response                                  │      │
│  │           → Check guardrails (temps, volumes, timings)           │      │
│  │           → Validate output structure                            │      │
│  │  Output: Dict{raw_output, structured_output, guardrail_report,   │      │
│  │               agent, status}                                      │      │
│  │                                                                   │      │
│  │  Handoff: protocol JSON + handoff_to_bioinformatics → A3         │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                   ↓                                          │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  A3: Bioinformatics Pipeline Agent (app/agents/a3_bioinfo.py)    │      │
│  │                                                                   │      │
│  │  Input:  a2_output (Dict with protocols)                         │      │
│  │  Process: → Load prompts (system + user)                         │      │
│  │           → Format user prompt with {wetlab_output}              │      │
│  │           → Call LLM (temperature=0.2, max_tokens=6000)          │      │
│  │           → Parse code sections (bash, YAML, etc.)               │      │
│  │           → Check guardrails (subprocess, docker, pip)           │      │
│  │           → Validate output structure                            │      │
│  │  Output: Dict{raw_output, structured_output, guardrail_report,   │      │
│  │               agent, status}                                      │      │
│  │                                                                   │      │
│  │  Handoff: pipeline scripts + data_handoff.yaml → A4              │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                   ↓                                          │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  A4: Statistical Analysis Agent (app/agents/a4_analysis.py)      │      │
│  │                                                                   │      │
│  │  Input:  a3_output (Dict with pipeline)                          │      │
│  │  Process: → Load prompts (system + user)                         │      │
│  │           → Format user prompt with {bioinfo_output}             │      │
│  │           → Call LLM (temperature=0.2, max_tokens=6000)          │      │
│  │           → Parse R code sections                                │      │
│  │           → Check guardrails (system calls, install.packages)    │      │
│  │           → Validate output structure                            │      │
│  │  Output: Dict{raw_output, structured_output, guardrail_report,   │      │
│  │               agent, status}                                      │      │
│  │                                                                   │      │
│  │  Handoff: R analysis workflow → [END]                            │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                ↓                  ↓                  ↓
┌──────────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  PROMPT LAYER        │ │   LLM LAYER      │ │ GUARDRAIL LAYER  │
│  app/prompts/        │ │   app/llm.py     │ │  app/guards.py   │
├──────────────────────┤ ├──────────────────┤ ├──────────────────┤
│                      │ │                  │ │                  │
│  System Prompts:     │ │  • load_dotenv() │ │  Wet-Lab:        │
│  • a1_sampling_...   │ │  • OpenAI client │ │  • Temp check    │
│  • a2_wetlab_...     │ │  • call_llm()    │ │  • Volume check  │
│  • a3_bioinfo_...    │ │  • Model: gpt-4o │ │  • Timing check  │
│  • a4_analysis_...   │ │  • Temperature   │ │                  │
│                      │ │  • Max tokens    │ │  Bioinformatics: │
│  User Prompts:       │ │                  │ │  • Subprocess    │
│  • a1_sampling_...   │ │  Environment:    │ │  • Docker        │
│  • a2_wetlab_...     │ │  • OPENAI_API_   │ │  • pip install   │
│  • a3_bioinfo_...    │ │    KEY           │ │                  │
│  • a4_analysis_...   │ │  • OPENAI_MODEL  │ │  Analysis:       │
│                      │ │                  │ │  • system()      │
│  Placeholders:       │ │  From .env file  │ │  • install.      │
│  • {user_query}      │ │                  │ │    packages()    │
│  • {sampling_output} │ │                  │ │                  │
│  • {wetlab_output}   │ │                  │ │  Risk levels:    │
│  • {bioinfo_output}  │ │                  │ │  • low/medium/   │
│                      │ │                  │ │    high          │
└──────────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## Data Flow Sequence

### Step 1: User Input
```
User provides research question
    ↓
CLI or API entry point
    ↓
graph.run_workflow(user_query)
```

### Step 2: State Initialization
```python
initial_state = {
    "user_query": user_query,
    "a1_output": {},
    "a2_output": {},
    "a3_output": {},
    "a4_output": {},
    "validation_reports": {},
    "status": "running",
    "error": ""
}
```

### Step 3: Agent A1 Execution
```
node_a1_sampling(state)
    ↓
run_sampling_agent(state["user_query"])
    ↓
    ├─ Import: a1_sampling_system_prompt.TEXT
    ├─ Import: a1_sampling_user_prompt.TEXT
    ├─ Format: USER_PROMPT.format(user_query=user_query)
    ├─ Call: llm.call_llm(SYSTEM_PROMPT, user_message)
    ├─ Parse: Extract JSON from response
    └─ Validate: check_sampling_output(output)
    ↓
state["a1_output"] = {
    "agent": "A1_Sampling",
    "raw_output": "...",
    "structured_output": {...},
    "status": "success"
}
```

### Step 4: Agent A2 Execution
```
node_a2_wetlab(state)
    ↓
Check: state["status"] != "error"
    ↓
run_wetlab_agent(state["a1_output"])
    ↓
    ├─ Import: a2_wetlab_system_prompt.TEXT
    ├─ Import: a2_wetlab_user_prompt.TEXT
    ├─ Format: USER_PROMPT.format(
    │     sampling_output=json.dumps(a1_output["structured_output"])
    │  )
    ├─ Call: llm.call_llm(SYSTEM_PROMPT, user_message)
    ├─ Parse: Extract JSON from response
    ├─ Guardrail: guards.check_wetlab_guardrails(response)
    └─ Validate: check_wetlab_output(output)
    ↓
state["a2_output"] = {
    "agent": "A2_WetLab",
    "raw_output": "...",
    "structured_output": {...},
    "guardrail_report": {...},
    "status": "success"
}
```

### Step 5: Agent A3 Execution
```
node_a3_bioinfo(state)
    ↓
Check: state["status"] != "error"
    ↓
run_bioinfo_agent(state["a2_output"])
    ↓
    ├─ Import: a3_bioinfo_system_prompt.TEXT
    ├─ Import: a3_bioinfo_user_prompt.TEXT
    ├─ Format: USER_PROMPT.format(
    │     wetlab_output=json.dumps(a2_output["structured_output"])
    │  )
    ├─ Call: llm.call_llm(SYSTEM_PROMPT, user_message)
    ├─ Parse: Extract code sections (bash, YAML, etc.)
    ├─ Guardrail: guards.check_bioinfo_guardrails(response)
    └─ Validate: check_bioinfo_output(output)
    ↓
state["a3_output"] = {
    "agent": "A3_Bioinformatics",
    "raw_output": "...",
    "structured_output": {
        "pipeline_script": "...",
        "config_yaml": "...",
        "setup_script": "...",
        "readme": "...",
        "handoff_yaml": "..."
    },
    "guardrail_report": {...},
    "status": "success"
}
```

### Step 6: Agent A4 Execution
```
node_a4_analysis(state)
    ↓
Check: state["status"] != "error"
    ↓
run_analysis_agent(state["a3_output"])
    ↓
    ├─ Import: a4_analysis_system_prompt.TEXT
    ├─ Import: a4_analysis_user_prompt.TEXT
    ├─ Format: USER_PROMPT.format(
    │     bioinfo_output=json.dumps(a3_output["structured_output"])
    │  )
    ├─ Call: llm.call_llm(SYSTEM_PROMPT, user_message)
    ├─ Parse: Extract R code sections
    ├─ Guardrail: guards.check_analysis_guardrails(response)
    └─ Validate: check_analysis_output(output)
    ↓
state["a4_output"] = {
    "agent": "A4_Analysis",
    "raw_output": "...",
    "structured_output": {
        "rmd_script": "...",
        "helper_functions": "...",
        "workflow_doc": "..."
    },
    "guardrail_report": {...},
    "status": "success"
}
    ↓
state["status"] = "complete" (or "warning" if validation failed)
```

### Step 7: Results Saving
```
save_results(state, output_dir)
    ↓
Create: runs/<timestamp>/
    ├─ A1.md (raw Markdown)
    ├─ A1.json (structured JSON)
    ├─ A2.md
    ├─ A2.json
    ├─ A2_guardrails.json (if violations)
    ├─ A3.md
    ├─ A3.json
    ├─ A3_guardrails.json (if violations)
    ├─ A4.md
    ├─ A4.json
    ├─ A4_guardrails.json (if violations)
    ├─ validation_reports.json
    ├─ full_state.json
    └─ SUMMARY.md
```

---

## Import Dependency Graph

```
app/__init__.py
    │
    ├─ agents/
    │   ├─ a1_sampling.py
    │   │   └─ imports: a1_prompts, llm
    │   ├─ a2_wetlab.py
    │   │   └─ imports: a2_prompts, llm, guards
    │   ├─ a3_bioinfo.py
    │   │   └─ imports: a3_prompts, llm, guards
    │   └─ a4_analysis.py
    │       └─ imports: a4_prompts, llm, guards
    │
    ├─ prompts/
    │   └─ (8 files with TEXT strings, no imports)
    │
    ├─ llm.py
    │   └─ imports: openai, dotenv
    │
    ├─ guards.py
    │   └─ imports: re
    │
    ├─ graph.py
    │   └─ imports: langgraph, all agents
    │
    ├─ cli.py
    │   └─ imports: graph, argparse, pathlib
    │
    └─ api.py
        └─ imports: fastapi, graph, pydantic
```

**✅ No Circular Dependencies**

---

## Error Handling Flow

```
┌─────────────────────────┐
│  Agent Node Execution   │
└───────────┬─────────────┘
            │
            ├─ Check: state["status"] == "error"?
            │  └─ Yes → Skip execution, return state
            │  └─ No → Continue
            │
            ├─ Try:
            │  ├─ run_agent()
            │  ├─ validate_output()
            │  └─ update state
            │
            ├─ Except Exception:
            │  ├─ state["status"] = "error"
            │  ├─ state["error"] = str(e)
            │  └─ print error
            │
            └─ Return state (always)
                │
                ├─ If error: Next node skips
                └─ If success: Next node executes
```

**Benefits:**
- ✅ Graceful degradation
- ✅ Partial results preserved
- ✅ Error messages captured
- ✅ Workflow completes (doesn't crash)

---

## Validation Flow

```
Each Agent Output
    ↓
┌─────────────────────────────────┐
│  validate_X_output(output)      │
├─────────────────────────────────┤
│  1. Check structured_output     │
│     exists                       │
│  2. Check required keys          │
│  3. Check guardrail violations   │
│  4. Return validation dict:      │
│     {                            │
│       "valid": bool,             │
│       "warnings": [...],         │
│       "errors": [...]            │
│     }                            │
└─────────────────────────────────┘
    ↓
Store in state["validation_reports"][agent]
    ↓
If not valid → set state["status"] = "error" (or "warning" for A4)
```

---

## Environment Configuration

```
.env file
    ↓
load_dotenv() in app/llm.py
    ↓
Environment Variables:
    • OPENAI_API_KEY
    • OPENAI_MODEL (default: gpt-4o)
    ↓
Used by:
    • OpenAI client initialization
    • All LLM calls through call_llm()
```

---

## Summary

This architecture provides:

1. **Modularity**: Each agent is independent
2. **Clear Data Flow**: Unidirectional A1→A2→A3→A4
3. **Error Resilience**: Comprehensive error handling
4. **State Management**: Centralized WorkflowState
5. **Validation**: Each agent output validated
6. **Guardrails**: Policy enforcement for A2, A3, A4
7. **Extensibility**: Easy to add new agents
8. **Dual Interface**: CLI and API access

All components verified and working correctly! ✅



