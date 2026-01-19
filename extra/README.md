# ARG Surveillance Multi-Agent Framework

A LangGraph-based multi-agent system for designing and planning Antibiotic Resistance Gene (ARG) surveillance research workflows using metagenomic data.

## Overview

This framework orchestrates four specialized agents in sequence to model the entire research pipeline—from field sampling to data interpretation:

```
User Query
    ↓
A1: Sampling Design Agent → sampling strategy, metadata requirements
    ↓
A2: Wet-Lab Protocol Agent → protocols, methods, QC measures
    ↓
A3: Bioinformatics Pipeline Agent → bash scripts, YAML configs, database setup
    ↓
A4: Statistical Analysis Agent → R workflows, visualizations, interpretation
```

**Key Features:**
- 🔗 **Sequential orchestration** using LangGraph
- 🤖 **OpenAI-powered** agents with specialized system prompts
- 🛡️ **Guardrails**: A2 enforces non-actionable output; A3/A4 flag execution commands
- 📂 **Structured outputs**: JSON/YAML for inter-agent handoffs
- 💾 **Persistent results**: Timestamped runs with Markdown + JSON outputs
- 🌐 **Dual interfaces**: CLI and FastAPI REST API

---

## Project Structure

```
.
├── app/
│   ├── agents/                  # Agent execution modules
│   │   ├── a1_sampling.py       # A1: Sampling Design Agent
│   │   ├── a2_wetlab.py         # A2: Wet-Lab Protocol Agent
│   │   ├── a3_bioinfo.py        # A3: Bioinformatics Pipeline Agent
│   │   └── a4_analysis.py       # A4: Statistical Analysis Agent
│   │
│   ├── prompts/                 # Prompt storage (placeholders)
│   │   ├── a1_sampling_system_prompt.py
│   │   ├── a1_sampling_user_prompt.py
│   │   ├── a2_wetlab_system_prompt.py
│   │   ├── a2_wetlab_user_prompt.py
│   │   ├── a3_bioinfo_system_prompt.py
│   │   ├── a3_bioinfo_user_prompt.py
│   │   ├── a4_analysis_system_prompt.py
│   │   └── a4_analysis_user_prompt.py
│   │
│   ├── graph.py                 # LangGraph orchestration
│   ├── llm.py                   # OpenAI API interface
│   ├── guards.py                # Guardrail validators
│   ├── cli.py                   # Command-line interface
│   └── api.py                   # FastAPI REST API
│
├── runs/                        # Workflow outputs (timestamped)
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
└── README.md                    # This file
```

---

## Installation

### 1. Clone or Create Project

```bash
mkdir arg-surveillance-framework
cd arg-surveillance-framework
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Or export directly:

```bash
export OPENAI_API_KEY='your-key-here'
export OPENAI_MODEL='gpt-4o'  # Optional, defaults to gpt-4o
```

### 4. Paste Your Prompts

**IMPORTANT:** The placeholder prompts in `app/prompts/*_prompt.py` need to be replaced with your actual prompts.

For each file:
1. Open the corresponding Markdown file (e.g., `Sampling Design Agent_System Prompt.md`)
2. Copy the full content
3. Open the Python prompt file (e.g., `app/prompts/a1_sampling_system_prompt.py`)
4. Replace the placeholder text between the triple quotes with your copied content

**Mapping:**

| Markdown File | Python Prompt File |
|---------------|-------------------|
| `Sampling Design Agent_System Prompt.md` | `app/prompts/a1_sampling_system_prompt.py` |
| `Sampling Design Agent_User_Prompt.md` | `app/prompts/a1_sampling_user_prompt.py` |
| `Wet-Lab Protocol Agent_System_Prompt.md` | `app/prompts/a2_wetlab_system_prompt.py` |
| `Wet-Lab Protocol Agent_User_Prompt.md` | `app/prompts/a2_wetlab_user_prompt.py` |
| `bioinformatics_Agent_System_Prompt.md` | `app/prompts/a3_bioinfo_system_prompt.py` |
| `bioinformatics_Agent_User_Prompt.md` | `app/prompts/a3_bioinfo_user_prompt.py` |
| `Statistical Analysis & Visualization Agent_System_Prompt.md` | `app/prompts/a4_analysis_system_prompt.py` |
| `Statistical Analysis & Visualization Agent_User_Prompt.md` | `app/prompts/a4_analysis_user_prompt.py` |

---

## Usage

### Command-Line Interface (CLI)

#### Interactive Mode

```bash
python -m app.cli
```

You'll be prompted to enter your research question. Press `Ctrl+D` (Linux/Mac) or `Ctrl+Z` (Windows) when done.

#### Direct Query

```bash
python -m app.cli --query "Design a 6-month study to monitor ARG dynamics in hospital wastewater"
```

#### Custom Output Directory

```bash
python -m app.cli --query "..." --output ./my_results
```

#### Don't Save Results

```bash
python -m app.cli --query "..." --no-save
```

---

### REST API

#### Start the Server

```bash
python -m app.api
```

Or with custom host/port:

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

#### API Endpoints

**1. Health Check**

```bash
curl http://localhost:8000/health
```

**2. Run Workflow (Synchronous)**

```bash
curl -X POST http://localhost:8000/workflow/run \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Design a sampling strategy for ARG surveillance in agricultural soil",
    "save_results": true,
    "output_dir": "./runs"
  }'
```

Response:
```json
{
  "status": "complete",
  "run_id": "20250109_143025",
  "output_path": "/path/to/runs/20250109_143025",
  "a1_status": "success",
  "a2_status": "success",
  "a3_status": "success",
  "a4_status": "success"
}
```

**3. Run Workflow (Asynchronous)**

```bash
curl -X POST http://localhost:8000/workflow/run-async \
  -H "Content-Type: application/json" \
  -d '{"query": "..."}'
```

Response:
```json
{
  "run_id": "20250109_143025_123456",
  "status": "running",
  "message": "Workflow started. Check status at /workflow/status/20250109_143025_123456"
}
```

**4. Check Workflow Status**

```bash
curl http://localhost:8000/workflow/status/{run_id}
```

**5. Get Agent Output**

```bash
curl http://localhost:8000/agent/{run_id}/a1
```

---

## Output Structure

Each workflow run creates a timestamped directory under `runs/`:

```
runs/20250109_143025/
├── A1.md                      # A1 raw Markdown output
├── A1.json                    # A1 structured JSON
├── A2.md                      # A2 raw Markdown output
├── A2.json                    # A2 structured JSON
├── A2_guardrails.json         # A2 guardrail violations (if any)
├── A3.md                      # A3 raw Markdown output
├── A3.json                    # A3 structured sections
├── A3_guardrails.json         # A3 guardrail violations (if any)
├── A4.md                      # A4 raw Markdown output
├── A4.json                    # A4 structured sections
├── A4_guardrails.json         # A4 guardrail violations (if any)
├── validation_reports.json    # All validation results
├── full_state.json            # Complete workflow state
└── SUMMARY.md                 # Human-readable summary
```

---

## Guardrails

### A2: Wet-Lab Protocol Agent

**Enforces non-actionable output** by detecting:
- Specific temperatures (e.g., "37°C")
- Specific volumes (e.g., "250 µL")
- Specific timings (e.g., "30 minutes")
- Step-by-step procedural instructions

**Risk levels:**
- `low`: No violations
- `medium`: 1-2 violations
- `high`: 3+ violations

### A3: Bioinformatics Pipeline Agent

**Flags execution commands**:
- Subprocess calls (`subprocess.run`)
- Shell execution (`eval`, `exec`)
- Docker commands (`docker run`)
- Package installation (`pip install`, `conda install`)

### A4: Statistical Analysis Agent

**Flags execution commands**:
- System calls (`system()`, `system2()`)
- Package installation (`install.packages()`)
- File system manipulation (`file.remove()`)

---

## Agent Handoffs

Each agent produces structured output for the next:

```
A1 → A2: JSON with sampling_design, metadata_requirements, qc_strategy, handoff_to_wetlab
A2 → A3: JSON with extraction, library_prep, sequencing, handoff_to_bioinformatics
A3 → A4: YAML with pipeline_metadata, analysis_ready_files, quality_summary, recommendations
```

---

## Development

### Run Tests

```bash
pytest
```

### Format Code

```bash
black app/
ruff check app/
```

### Add New Agent

1. Create `app/agents/a5_myagent.py`
2. Create prompt files:
   - `app/prompts/a5_myagent_system_prompt.py`
   - `app/prompts/a5_myagent_user_prompt.py`
3. Add node to `app/graph.py`:
   ```python
   from app.agents.a5_myagent import run_myagent, validate_myagent_output
   
   def node_a5_myagent(state):
       output = run_myagent(state["a4_output"])
       state["a5_output"] = output
       return state
   
   workflow.add_node("a5_myagent", node_a5_myagent)
   workflow.add_edge("a4_analysis", "a5_myagent")
   workflow.add_edge("a5_myagent", END)
   ```

---

## Troubleshooting

### Issue: `OPENAI_API_KEY not set`

**Solution:** Export the environment variable:
```bash
export OPENAI_API_KEY='your-key-here'
```

### Issue: `ModuleNotFoundError: No module named 'langgraph'`

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Workflow hangs or times out

**Solution:** Check your OpenAI API quota/rate limits. Consider reducing `max_tokens` in `app/llm.py`.

### Issue: Guardrail violations detected

**Solution:** Review the `*_guardrails.json` file in the run directory. Adjust prompts to avoid generating actionable instructions or execution commands.

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (required) | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | Model to use (`gpt-4o`, `gpt-4-turbo`, etc.) |

### Customizing Agent Behavior

Edit the agent modules in `app/agents/` to adjust:
- Temperature (creativity)
- Max tokens (response length)
- Validation logic
- Output parsing

---

## Citation

If you use this framework in your research, please cite:

```bibtex
@software{arg_surveillance_framework,
  title={ARG Surveillance Multi-Agent Framework},
  author={Your Name},
  year={2025},
  url={https://github.com/yourusername/arg-surveillance-framework}
}
```

---

## License

MIT License - see LICENSE file for details

---

## Support

For issues, questions, or contributions, please open an issue on GitHub or contact [your-email@example.com].

---

## Roadmap

- [ ] Add async/parallel agent execution for independent tasks
- [ ] Implement caching for expensive LLM calls
- [ ] Add database persistence for workflow runs
- [ ] Create web UI for visualization
- [ ] Add support for Claude, Gemini, and other LLMs
- [ ] Implement human-in-the-loop approval steps
- [ ] Add unit tests for all agents
- [ ] Create Docker deployment configuration

