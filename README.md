# ARG Surveillance AI Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991.svg)](https://openai.com/)

A production-grade multi-agent system for automating antibiotic resistance gene (ARG) surveillance study design. Built with LangGraph and OpenAI GPT-4, this framework orchestrates four specialized AI agents to generate complete research workflows from natural language queries.

---

## Problem Statement

Designing ARG surveillance studies requires expertise across multiple domains (epidemiology, molecular biology, bioinformatics, statistics) and typically takes 3-4 weeks of iterative planning. This creates bottlenecks in research initiation, particularly for labs without access to multi-disciplinary expertise.

**Current challenges:**
- Time-intensive: 3-4 weeks for study design
- Resource-intensive: Requires 4+ domain experts
- Error-prone: 30-40% of studies have design flaws
- Costly: $5,000-15,000 in consultant fees

## Solution

This framework automates the end-to-end study design process through a sequential multi-agent architecture. Each agent represents a domain expert and produces structured outputs that feed into the next stage of the workflow.


---




**Deployment**
- Docker containerization
- CI/CD pipeline (GitHub Actions)
- REST API + CLI interfaces
- Production-ready error handling

---

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip package manager

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/arg-surveillance-framework.git
cd arg-surveillance-framework

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Docker Setup

```bash
# Build image
docker build -t arg-framework .

# Run API server
docker run -e OPENAI_API_KEY=your-key -p 8000:8000 arg-framework

# Or use docker-compose
docker-compose up
```

---

## Usage

### Command Line Interface

**Direct execution:**
```bash
python -m app.cli "Design a 6-month ARG surveillance study in hospital wastewater"
```

**Interactive mode:**
```bash
python -m app.cli
# Enter query when prompted, Ctrl+D when done
```

**Custom output directory:**
```bash
python -m app.cli --query "..." --output ./results
```

### REST API

**Start server:**
```bash
python -m app.api
# Server runs on http://localhost:8000
```

**Execute workflow:**
```bash
curl -X POST http://localhost:8000/workflow/run \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Design sampling strategy for agricultural ARG monitoring",
    "save_results": true
  }'
```

**Response format:**
```json
{
  "status": "complete",
  "run_id": "20240119_143025",
  "output_path": "/path/to/runs/20240119_143025",
  "a1_status": "success",
  "a2_status": "success",
  "a3_status": "success",
  "a4_status": "success"
}
```

### Programmatic Usage

```python
from app.graph import run_workflow

result = run_workflow(
    user_query="Design a study to monitor ARG dynamics in hospital wastewater"
)

# Access outputs
sampling_design = result["a1_output"]["structured_output"]
lab_protocols = result["a2_output"]["structured_output"]
pipeline_code = result["a3_output"]["structured_output"]
analysis_workflow = result["a4_output"]["structured_output"]
```

---

## Technical Details

### Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Core Language | Python | 3.8+ |
| LLM Provider | OpenAI GPT-4o | API |
| Orchestration | LangGraph | 0.0.30+ |
| API Framework | FastAPI | 0.109+ |
| Validation | Pydantic | 2.0+ |
| Containerization | Docker | 20.10+ |

### Project Structure

```
arg-surveillance-framework/
├── app/
│   ├── agents/           # Agent implementations
│   ├── prompts/          # Prompt templates (8 files)
│   ├── graph.py          # State machine orchestration
│   ├── llm.py            # OpenAI interface
│   ├── guards.py         # Validation logic
│   ├── cli.py            # Command-line interface
│   └── api.py            # REST API
├── runs/                 # Output directory (timestamped)
├── tests/                # Test suite
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

### Agent Details

**A1: Sampling Design Agent**
- Input: Natural language query
- Framework: 7-step reasoning process
- Output: JSON with hypotheses, design, power analysis
- Validation: Schema validation, statistical checks

**A2: Wet-Lab Protocol Agent**
- Input: A1 JSON output
- Framework: 5-phase protocol assembly
- Output: JSON with methods, protocols, citations
- Validation: Guardrails (non-actionable content)

**A3: Bioinformatics Pipeline Agent**
- Input: A2 JSON output
- Framework: 6-stage pipeline generation
- Output: Bash scripts, YAML configs, setup files
- Validation: Guardrails (no execution commands)

**A4: Statistical Analysis Agent**
- Input: A3 YAML output
- Framework: 5-step analysis workflow
- Output: R Markdown, helper functions
- Validation: Guardrails (no system calls)

### Validation & Quality Control

**Multi-stage validation:**
1. Input validation (each agent)
2. Output schema validation
3. Automated guardrails (policy enforcement)
4. Cross-agent compatibility checks

**Guardrails implementation:**
- A2: Flags specific measurements (temperatures, volumes, timings)
- A3: Flags execution commands (subprocess, docker, pip)
- A4: Flags system calls (system(), install.packages())

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key |
| `OPENAI_MODEL` | No | gpt-4o | Model identifier |
| `LOG_LEVEL` | No | INFO | Logging verbosity |

### Advanced Configuration

Modify agent parameters in `app/agents/*.py`:

```python
# Adjust temperature for creativity/determinism
response = call_llm(
    system_prompt=SYSTEM_PROMPT,
    user_prompt=user_message,
    temperature=0.3,    # 0=deterministic, 2=creative
    max_tokens=4000
)
```

---

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest

# Check code quality
black app/
ruff check app/
mypy app/
```

### Running Tests

```bash
# Full test suite
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_agents.py

# Verbose output
pytest -v
```

### Adding New Agents

1. Create agent module: `app/agents/a5_newagent.py`
2. Define prompts: `app/prompts/a5_newagent_*_prompt.py`
3. Register in workflow: `app/graph.py`
4. Add validation logic
5. Write tests

Example:
```python
# app/agents/a5_newagent.py
def run_newagent(input_data: Dict[str, Any]) -> Dict[str, Any]:
    # Implementation
    pass

# app/graph.py
def node_a5_newagent(state: WorkflowState) -> WorkflowState:
    output = run_newagent(state["a4_output"])
    state["a5_output"] = output
    return state

workflow.add_node("a5_newagent", node_a5_newagent)
workflow.add_edge("a4_analysis", "a5_newagent")
```

---

## API Reference

### REST Endpoints

**Health Check**
```
GET /health
```

**Run Workflow (Synchronous)**
```
POST /workflow/run
Content-Type: application/json

{
  "query": "string",
  "save_results": boolean,
  "output_dir": "string"
}
```

**Run Workflow (Asynchronous)**
```
POST /workflow/run-async
```

**Check Status**
```
GET /workflow/status/{run_id}
```

**Get Agent Output**
```
GET /agent/{run_id}/{agent_id}
```

### Python SDK

```python
from app.graph import run_workflow
from app.cli import save_results

# Execute workflow
result = run_workflow("Your research question")

# Save results
save_results(result, output_dir="./runs")
```

---

## Performance



## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/name`)
3. Follow code style guidelines (Black, Ruff)
4. Add tests for new features
5. Update documentation
6. Submit pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Testing

The framework includes comprehensive test coverage:

- Unit tests for each agent
- Integration tests for workflow
- API endpoint tests
- Validation logic tests

Run tests with:
```bash
pytest tests/ -v --cov=app
```

---



## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---



---


