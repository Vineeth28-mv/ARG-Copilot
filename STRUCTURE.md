# Project Structure

```
arg-surveillance-framework/
│
├── app/                                    # Main application package
│   ├── __init__.py                        # Package initialization
│   │
│   ├── agents/                            # Agent execution modules
│   │   ├── __init__.py
│   │   ├── a1_sampling.py                 # A1: Sampling Design Agent
│   │   │   └── run_sampling_agent()       #   - Generates sampling strategy
│   │   │   └── validate_sampling_output() #   - Validates output structure
│   │   │
│   │   ├── a2_wetlab.py                   # A2: Wet-Lab Protocol Agent
│   │   │   └── run_wetlab_agent()         #   - Generates protocols
│   │   │   └── validate_wetlab_output()   #   - Checks guardrails
│   │   │
│   │   ├── a3_bioinfo.py                  # A3: Bioinformatics Pipeline Agent
│   │   │   └── run_bioinfo_agent()        #   - Generates bash/YAML
│   │   │   └── validate_bioinfo_output()  #   - Checks for execution commands
│   │   │   └── extract_bioinfo_sections() #   - Parses code blocks
│   │   │
│   │   └── a4_analysis.py                 # A4: Statistical Analysis Agent
│   │       └── run_analysis_agent()       #   - Generates R workflows
│   │       └── validate_analysis_output() #   - Checks for system calls
│   │       └── extract_analysis_sections()#   - Parses R code
│   │
│   ├── prompts/                           # Prompt storage (8 files)
│   │   ├── __init__.py
│   │   │
│   │   ├── a1_sampling_system_prompt.py   # ← PASTE YOUR PROMPTS HERE
│   │   ├── a1_sampling_user_prompt.py     # ← PASTE YOUR PROMPTS HERE
│   │   │
│   │   ├── a2_wetlab_system_prompt.py     # ← PASTE YOUR PROMPTS HERE
│   │   ├── a2_wetlab_user_prompt.py       # ← PASTE YOUR PROMPTS HERE
│   │   │
│   │   ├── a3_bioinfo_system_prompt.py    # ← PASTE YOUR PROMPTS HERE
│   │   ├── a3_bioinfo_user_prompt.py      # ← PASTE YOUR PROMPTS HERE
│   │   │
│   │   ├── a4_analysis_system_prompt.py   # ← PASTE YOUR PROMPTS HERE
│   │   └── a4_analysis_user_prompt.py     # ← PASTE YOUR PROMPTS HERE
│   │
│   ├── graph.py                           # LangGraph orchestration
│   │   └── WorkflowState                  #   - State schema
│   │   └── node_a1_sampling()             #   - A1 graph node
│   │   └── node_a2_wetlab()               #   - A2 graph node
│   │   └── node_a3_bioinfo()              #   - A3 graph node
│   │   └── node_a4_analysis()             #   - A4 graph node
│   │   └── create_workflow_graph()        #   - Build LangGraph
│   │   └── run_workflow()                 #   - Main execution
│   │
│   ├── llm.py                             # OpenAI API interface
│   │   └── call_llm()                     #   - Single LLM call
│   │   └── call_llm_with_history()        #   - Multi-turn conversation
│   │   └── estimate_tokens()              #   - Token estimation
│   │
│   ├── guards.py                          # Guardrail validators
│   │   └── check_wetlab_guardrails()      #   - Detect actionable instructions
│   │   └── check_bioinfo_guardrails()     #   - Detect execution commands
│   │   └── check_analysis_guardrails()    #   - Detect system calls
│   │   └── sanitize_output()              #   - Add warnings to output
│   │
│   ├── cli.py                             # Command-line interface
│   │   └── save_results()                 #   - Save to timestamped directory
│   │   └── main()                         #   - CLI entry point
│   │
│   └── api.py                             # FastAPI REST API
│       └── /workflow/run                  #   - Sync workflow execution
│       └── /workflow/run-async            #   - Async workflow execution
│       └── /workflow/status/{run_id}      #   - Check workflow status
│       └── /workflow/output/{run_id}      #   - Get full output
│       └── /agent/{run_id}/{agent}        #   - Get specific agent output
│
├── runs/                                  # Workflow outputs (gitignored)
│   └── 20250109_143025/                   # Timestamped run directory
│       ├── A1.md                          #   - A1 Markdown output
│       ├── A1.json                        #   - A1 JSON output
│       ├── A2.md                          #   - A2 Markdown output
│       ├── A2.json                        #   - A2 JSON output
│       ├── A2_guardrails.json             #   - A2 violations (if any)
│       ├── A3.md                          #   - A3 Markdown output
│       ├── A3.json                        #   - A3 JSON output
│       ├── A3_guardrails.json             #   - A3 violations (if any)
│       ├── A4.md                          #   - A4 Markdown output
│       ├── A4.json                        #   - A4 JSON output
│       ├── A4_guardrails.json             #   - A4 violations (if any)
│       ├── validation_reports.json        #   - All validation results
│       ├── full_state.json                #   - Complete workflow state
│       └── SUMMARY.md                     #   - Human-readable summary
│
├── requirements.txt                       # Python dependencies
├── .env.example                           # Environment variable template
├── .gitignore                             # Git ignore rules
│
├── README.md                              # Full documentation
├── QUICK_START.md                         # Quick start guide
├── STRUCTURE.md                           # This file
│
├── setup.sh                               # Setup script (Linux/Mac)
├── run_example.py                         # Example workflow script
└── example_query.txt                      # Example research question
```

## Key Files to Modify

### 🔴 **MUST EDIT** (Before First Run)

1. **Prompts** (`app/prompts/*_prompt.py`): Replace all 8 placeholder prompts with your actual prompts from Markdown files

2. **Environment** (`.env`): Add your `OPENAI_API_KEY`

### 🟡 **OPTIONAL** (Customize Behavior)

3. **Agents** (`app/agents/*.py`): Adjust validation logic, parsing, temperature, max_tokens

4. **Guardrails** (`app/guards.py`): Add/remove guardrail patterns, adjust risk thresholds

5. **Graph** (`app/graph.py`): Add new agents, change flow, add conditional routing

6. **LLM** (`app/llm.py`): Change model, adjust defaults, add retry logic

## Data Flow

```
User Query
    ↓
graph.py (LangGraph)
    ↓
┌─────────────────────────────────────────────────┐
│  node_a1_sampling()                             │
│    → a1_sampling.py                             │
│    → prompts/a1_*_prompt.py                     │
│    → llm.py (OpenAI call)                       │
│    → validate_sampling_output()                 │
│    → state["a1_output"] = {...}                 │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│  node_a2_wetlab()                               │
│    → a2_wetlab.py                               │
│    → prompts/a2_*_prompt.py                     │
│    → llm.py (OpenAI call)                       │
│    → guards.py (check_wetlab_guardrails)        │
│    → validate_wetlab_output()                   │
│    → state["a2_output"] = {...}                 │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│  node_a3_bioinfo()                              │
│    → a3_bioinfo.py                              │
│    → prompts/a3_*_prompt.py                     │
│    → llm.py (OpenAI call)                       │
│    → guards.py (check_bioinfo_guardrails)       │
│    → extract_bioinfo_sections()                 │
│    → validate_bioinfo_output()                  │
│    → state["a3_output"] = {...}                 │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│  node_a4_analysis()                             │
│    → a4_analysis.py                             │
│    → prompts/a4_*_prompt.py                     │
│    → llm.py (OpenAI call)                       │
│    → guards.py (check_analysis_guardrails)      │
│    → extract_analysis_sections()                │
│    → validate_analysis_output()                 │
│    → state["a4_output"] = {...}                 │
└─────────────────────────────────────────────────┘
    ↓
Final State → cli.py or api.py
    ↓
save_results() → runs/<timestamp>/
```

## Import Chain

```python
# CLI/API imports graph
from app.graph import run_workflow

# graph imports agents
from app.agents.a1_sampling import run_sampling_agent
from app.agents.a2_wetlab import run_wetlab_agent
from app.agents.a3_bioinfo import run_bioinfo_agent
from app.agents.a4_analysis import run_analysis_agent

# agents import prompts
from app.prompts.a1_sampling_system_prompt import TEXT as SYSTEM_PROMPT
from app.prompts.a1_sampling_user_prompt import TEXT as USER_PROMPT

# agents import llm and guards
from app.llm import call_llm
from app.guards import check_wetlab_guardrails
```

## Module Responsibilities

| Module | Responsibility | Dependencies |
|--------|----------------|--------------|
| `prompts/*.py` | Store prompt text | None |
| `llm.py` | OpenAI API calls | `openai` |
| `guards.py` | Validate outputs | `re` |
| `agents/*.py` | Run agents, parse outputs | `prompts`, `llm`, `guards` |
| `graph.py` | Orchestrate workflow | `langgraph`, `agents` |
| `cli.py` | CLI interface | `graph` |
| `api.py` | REST API interface | `fastapi`, `graph` |

## Extension Points

1. **Add a new agent**: Create `app/agents/a5_myagent.py`, add prompts, register in `graph.py`

2. **Add guardrails**: Add pattern checks in `app/guards.py`

3. **Change LLM provider**: Replace `app/llm.py` with Anthropic, Google, etc.

4. **Add database**: Replace in-memory `workflow_runs` dict in `api.py` with PostgreSQL, Redis, etc.

5. **Add authentication**: Add FastAPI dependencies in `api.py`

6. **Add caching**: Wrap `call_llm()` with LangChain caching

7. **Add human-in-the-loop**: Add approval nodes in `graph.py`

