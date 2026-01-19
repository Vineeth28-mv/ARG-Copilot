# Quick Start Guide

## 1. Setup (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your-key-here'

# Or create .env file
cp .env.example .env
# Edit .env and add your key
```

## 2. Replace Placeholder Prompts

**CRITICAL STEP**: You must replace the placeholder prompts with your actual prompts.

Open each file in `app/prompts/` and replace the placeholder text between `"""..."""`:

| File to Edit | Source Markdown File |
|-------------|---------------------|
| `app/prompts/a1_sampling_system_prompt.py` | `Sampling Design Agent_System Prompt.md` |
| `app/prompts/a1_sampling_user_prompt.py` | `Sampling Design Agent_User_Prompt.md` |
| `app/prompts/a2_wetlab_system_prompt.py` | `Wet-Lab Protocol Agent_System_Prompt.md` |
| `app/prompts/a2_wetlab_user_prompt.py` | `Wet-Lab Protocol Agent_User_Prompt.md` |
| `app/prompts/a3_bioinfo_system_prompt.py` | `bioinformatics_Agent_System_Prompt.md` |
| `app/prompts/a3_bioinfo_user_prompt.py` | `bioinformatics_Agent_User_Prompt.md` |
| `app/prompts/a4_analysis_system_prompt.py` | `Statistical Analysis & Visualization Agent_System_Prompt.md` |
| `app/prompts/a4_analysis_user_prompt.py` | `Statistical Analysis & Visualization Agent_User_Prompt.md` |

**Example:**

Before (placeholder):
```python
TEXT = """<<<PASTE A1 SYSTEM PROMPT HERE>>>

You are the Sampling Design Agent...
"""
```

After (with your prompt):
```python
TEXT = """# Sampling Design Agent - System Prompt

## Role
You are a specialized agent for designing sampling strategies...

[... rest of your actual prompt ...]
"""
```

## 3. Run Your First Workflow

### Option A: CLI

```bash
# Interactive mode
python -m app.cli

# Direct query
python -m app.cli --query "Design a study to monitor ARG in hospital wastewater"
```

### Option B: API

```bash
# Start server
python -m app.api

# In another terminal, send a request
curl -X POST http://localhost:8000/workflow/run \
  -H "Content-Type: application/json" \
  -d '{"query": "Design ARG surveillance study"}'
```

### Option C: Example Script

```bash
python run_example.py
```

## 4. Check Results

Results are saved in `runs/<timestamp>/`:

```
runs/20250109_143025/
├── A1.md                 # Sampling design (Markdown)
├── A1.json               # Sampling design (JSON)
├── A2.md                 # Wet-lab protocols
├── A2.json
├── A3.md                 # Bioinformatics pipeline
├── A3.json
├── A4.md                 # Statistical analysis
├── A4.json
├── SUMMARY.md            # Human-readable summary
└── full_state.json       # Complete workflow state
```

## Troubleshooting

### "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY='sk-...'
```

### "No module named 'langgraph'"
```bash
pip install -r requirements.txt
```

### Prompts are still placeholders
Open each file in `app/prompts/` and paste your actual prompts.

### Workflow hangs
- Check your OpenAI API quota
- Reduce `max_tokens` in `app/llm.py` if needed

## Next Steps

- Customize agent behavior in `app/agents/`
- Adjust guardrails in `app/guards.py`
- Add more agents by following the pattern in `app/graph.py`
- Deploy as a web service using Docker (coming soon)

## Support

See `README.md` for full documentation.

