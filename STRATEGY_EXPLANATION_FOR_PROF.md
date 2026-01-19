# Multi-Agent ARG Surveillance Framework
## Strategy & Prompt Design Explanation

**Student:** [Your Name]  
**Project:** Antibiotic Resistance Gene (ARG) Surveillance using Multi-Agent AI System  
**Date:** October 9, 2025

---

## 🎯 **Project Overview**

I developed a **multi-agent AI framework** that transforms a research question about Antibiotic Resistance Genes into a complete, structured research workflow—from field sampling design to statistical analysis planning.

### **Core Innovation**

Instead of using a **single large prompt**, I designed **4 specialized AI agents** that work sequentially, each providing domain-specific expertise:

```
User Question
    ↓
┌─────────────────────────────────────────┐
│  A1: Sampling Design Agent              │ ← Epidemiologist
│  Output: Sampling strategy (JSON)       │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  A2: Wet-Lab Protocol Agent             │ ← Lab Specialist
│  Output: Protocol recommendations (JSON) │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  A3: Bioinformatics Pipeline Agent      │ ← Bioinformatician
│  Output: Pipeline scripts (Bash/YAML)   │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  A4: Statistical Analysis Agent         │ ← Statistician
│  Output: R analysis workflow (R/Rmd)    │
└─────────────────────────────────────────┘
```

**Key Principle:** Each agent acts as a specialized "domain expert" with its own reasoning framework, rather than one generalist AI trying to handle everything.

---

## 🧠 **Why Multi-Agent Architecture?**

### **Problem with Single-Agent Approach**

If I used one large prompt to do everything:
- ❌ **Too complex:** ~3000+ lines in one prompt = confusion
- ❌ **Poor reasoning:** AI jumps between contexts (sampling → lab → code)
- ❌ **No validation:** Can't catch errors until the very end
- ❌ **Hard to maintain:** One change affects everything
- ❌ **Loss of expertise:** Generic outputs lack domain depth

### **Advantages of Multi-Agent Design**

✅ **Modular reasoning:** Each agent focuses on one domain  
✅ **Staged validation:** Catch errors early in the pipeline  
✅ **Maintainable:** Update one agent without breaking others  
✅ **Domain expertise:** Deep, specialized knowledge per agent  
✅ **Scalable:** Easy to add new agents (e.g., Ethics Review Agent)  
✅ **Traceable:** Clear handoffs between stages

---

## 📋 **Prompt Engineering Strategy**

### **Two-Prompt System (Per Agent)**

Each agent has **two prompts**:

1. **System Prompt** (~ 200 lines)
   - Defines the agent's **role** and **reasoning framework**
   - Provides **decision trees** for method selection
   - Sets **constraints** and **quality standards**
   - Establishes **domain expertise**

2. **User Prompt** (~ 400-800 lines)
   - Provides the **specific task** and **input data**
   - Includes **detailed output templates**
   - Shows **examples** and **edge cases**
   - Triggers **structured output** (JSON/code)

**Why separate them?**
- System Prompt = **"Who you are"** (persistent identity)
- User Prompt = **"What you do now"** (task-specific instructions)

---

## 🔬 **Agent 1: Sampling Design**

### **Role**
Epidemiologist designing sampling strategies for ARG surveillance.

### **Prompt Design Philosophy**

**System Prompt includes:**
1. **Core reasoning framework** (7 steps):
   ```
   Parse query → Hypotheses → Spatial design → Temporal design
   → Replication → Metadata → QC strategy → Handoff
   ```

2. **Decision trees** for:
   - Study system classification (hospital/community/environmental)
   - Sampling intensity based on objectives
   - Statistical power calculations
   - Metadata prioritization

3. **Output constraints**:
   - Must output valid JSON
   - Include testable hypotheses
   - Justify sample size statistically
   - Provide QC strategies

**User Prompt structure:**
```
Step 1: Parse User Query
Step 2: Define Hypotheses
Step 3: Design Spatial Sampling
Step 4: Design Temporal Sampling
Step 5: Determine Replication
Step 6: Specify Metadata Requirements
Step 7: Define QC Strategy
Step 8: Handoff to Wet-Lab Agent

User Query: ###USER_QUERY###
```

**Key Innovation:** The prompt includes **alternative scenario templates** for ambiguous queries:
```json
"alternative_scenarios": [
  {
    "scenario": "If cultivation is required",
    "sampling_modifications": "Add sterile aliquots"
  }
]
```

### **Output Example**
```json
{
  "hypotheses": {
    "primary": "Hospital wastewater has higher ARG diversity than community sources",
    "statistical_framework": "PERMANOVA + Dunn's test"
  },
  "sampling_design": {
    "spatial_design": "3 hospital + 3 community sites",
    "temporal_design": "Monthly for 6 months",
    "replication": "n=5 per site per timepoint"
  },
  "statistical_power": "80% power to detect 50% reduction (Cohen's d=0.5)"
}
```

---

## 🧪 **Agent 2: Wet-Lab Protocol**

### **Role**
Lab specialist translating sampling designs into protocol recommendations.

### **Prompt Design Philosophy**

**System Prompt includes:**
1. **Input validation** from A1:
   - Verify sample types are defined
   - Check biomass expectations
   - Validate safety requirements

2. **Decision trees** for:
   - DNA extraction kit selection (soil vs. water vs. fecal)
   - Library prep method (metagenomic vs. amplicon)
   - Concentration method (filtration vs. centrifugation)
   - QC checkpoints (contamination detection)

3. **Modular protocol structure**:
   ```
   Collection → Preservation → Concentration → Extraction
   → Library Prep → QC → Handoff
   ```

4. **Citation standards**:
   - Reference published protocols
   - Provide DOIs
   - Cite commercial kit manuals

**Key Constraint:** **Non-actionable output**
- Should recommend protocols, NOT provide step-by-step bench instructions
- Avoid specific volumes/temperatures/timings
- Focus on **method selection rationale**

**Guardrail Example:**
```python
# Flag if output contains:
- Specific temperatures: "37°C", "65 degrees"
- Specific volumes: "250 µL", "5 mL"  
- Step-by-step instructions: "Step 1:", "Add X, then Y"
```

### **Output Example**
```json
{
  "extraction": {
    "recommended_kit": "DNeasy PowerSoil Pro",
    "rationale": "Optimized for high organic matter content",
    "protocol_reference": "DOI:10.1038/nprot.2016.XXX",
    "modifications": [
      "Extended bead-beating for improved lysis"
    ]
  }
}
```

---

## 💻 **Agent 3: Bioinformatics Pipeline**

### **Role**
Bioinformatician generating pipeline scripts and configuration files.

### **Prompt Design Philosophy**

**System Prompt includes:**
1. **Input validation** from A2:
   - Check sequencing platform (Illumina/ONT/PacBio)
   - Verify data type (WGS/amplicon/RNA)
   - Confirm expected read length

2. **Decision trees** for:
   - Assembly strategy (quality-based vs. reference-guided)
   - Assembler selection (MEGAHIT vs. metaSPAdes vs. Flye)
   - Taxonomy classifier (Kraken2 vs. Metaphlan4)
   - ARG database (CARD vs. ARG-ANNOT vs. ResFinder)
   - Normalization method (TPM vs. RPKM vs. DESeq2)

3. **Pipeline architecture standards**:
   ```
   Stage 1: QC → Stage 2: Assembly → Stage 3: Annotation
   → Stage 4: ARG Detection → Stage 5: Normalization
   ```
   - Each stage has error handling
   - Checkpoints save intermediate files
   - Logs track progress

4. **Critical output:** `data_handoff.yaml`
   - Maps output files to statistical analysis inputs
   - Defines file formats and column headers
   - Provides metadata schema

**Key Innovation:** **Modular templates instead of monolithic scripts**

Old approach (bad):
```bash
# One giant script with 500+ lines
```

New approach (good):
```bash
# Main pipeline.sh calls modules:
source modules/qc.sh
source modules/assembly.sh
source modules/annotation.sh
```

### **Output Structure**
```
Deliverable 1: pipeline.sh (main script)
Deliverable 2: config.yaml (parameters)
Deliverable 3: setup_databases.sh (database downloads)
Deliverable 4: README.md (execution guide)
Deliverable 5: data_handoff.yaml (for A4)
```

### **Guardrail:** Detects but allows bash syntax
```python
# Flag patterns like:
- subprocess.run() in Python
- docker run commands
- !pip install
# Allow normal bash: $(command), pipelines, etc.
```

---

## 📊 **Agent 4: Statistical Analysis**

### **Role**
Statistician generating R analysis workflows with assumption checking.

### **Prompt Design Philosophy**

**System Prompt includes:**
1. **Input validation** from A3:
   - Parse `data_handoff.yaml`
   - Verify file paths and formats
   - Check normalization method

2. **Automated assumption checking**:
   ```r
   check_parametric_assumptions <- function(data) {
     # Shapiro-Wilk test (normality)
     # Levene's test (homogeneity)
     # Return diagnostic plots
   }
   ```

3. **Decision trees** for:
   - Group comparisons (parametric vs. non-parametric)
   - Differential abundance (DESeq2 vs. ALDEx2 vs. ANCOM)
   - Correlation analysis (Spearman vs. Pearson)
   - Multiple testing correction (Bonferroni vs. BH-FDR)

4. **Visualization standards**:
   - Ordination plots (PCA/PCoA)
   - Diversity indices (Shannon/Simpson)
   - Heatmaps with hierarchical clustering
   - Network analysis for co-occurrence

**Key Innovation:** **R Markdown template with validation checklist**

The output includes:
```r
# Section 1: Load and validate data
# Section 2: Check assumptions
# Section 3: Descriptive statistics  
# Section 4: Hypothesis testing
# Section 5: Visualization
# Section 6: Report generation
```

Each section has:
- Code blocks
- Explanatory text
- Diagnostic plots
- Interpretation guidance

### **Output Example**
```r
# ARG Analysis Workflow

## 1. Assumption Checking
assumptions <- check_parametric_assumptions(arg_abundance)
if (!assumptions$normal || !assumptions$homogeneous) {
  message("Using non-parametric tests (Kruskal-Wallis)")
  test_method <- "kruskal"
} else {
  test_method <- "anova"
}

## 2. Group Comparisons
results <- compare_groups(
  data = arg_abundance,
  groups = metadata$site_type,
  method = test_method,
  correction = "BH"
)
```

---

## 🔗 **Inter-Agent Communication**

### **Handoff Mechanism**

Each agent produces a **structured output** that becomes the next agent's input:

```
A1 → JSON (sampling_design.json)
     ↓
A2 ← Reads JSON
A2 → JSON (wetlab_protocol.json)
     ↓
A3 ← Reads JSON
A3 → YAML (data_handoff.yaml) + Scripts
     ↓
A4 ← Reads YAML
A4 → R Markdown + Scripts
```

**Key Design Choice:** Use **structured formats** (JSON/YAML) for handoffs
- ✅ Machine-readable
- ✅ Validates automatically
- ✅ Clear schema
- ✅ No ambiguity

### **Example Handoff (A2 → A3)**

A2 outputs:
```json
{
  "sequencing_output": {
    "platform": "Illumina NovaSeq",
    "chemistry": "PE150",
    "expected_depth": "10M reads/sample"
  }
}
```

A3 reads and adapts:
```bash
# Pipeline configured for Illumina PE150
PLATFORM="illumina"
READ_LENGTH=150
```

---

## 🛡️ **Quality Control Strategy**

### **1. Input Validation**
Each agent validates its input before processing:
```python
# Example from A2:
required_keys = ["sampling_design", "sample_types", "study_system"]
if not all(k in a1_output for k in required_keys):
    raise ValueError("Incomplete A1 output")
```

### **2. Output Validation**
Each agent validates its own output:
```python
# Example from A1:
validation = {
    "valid": True if structured_output else False,
    "warnings": [],
    "errors": []
}
```

### **3. Guardrails**
Automated checks ensure outputs follow design principles:
- A2: Must be non-actionable (no bench protocols)
- A3: Must be templates (no auto-execution)
- A4: Must be analysis code (no system calls)

### **4. Human Review Points**
The framework saves outputs at each stage:
```
runs/TIMESTAMP/
├── A1.json  ← Review sampling design
├── A2.json  ← Review protocol choices
├── A3.md    ← Review pipeline logic
└── A4.md    ← Review statistical approach
```

Researchers can **intervene** between agents if needed.

---

## 📐 **Prompt Engineering Techniques Used**

### **1. Few-Shot Learning**
Each prompt includes 2-3 detailed examples:
```
Example 1: Hospital wastewater study
Example 2: Agricultural runoff study
Example 3: Clinical isolate surveillance
```

### **2. Chain-of-Thought Reasoning**
Prompts enforce step-by-step thinking:
```
Step 1: Parse query
Step 2: Define hypotheses
Step 3: Design spatial sampling
...
```

### **3. Decision Tree Guidance**
Prompts include explicit decision logic:
```
IF study_system == "wastewater" AND biomass == "high":
  → Use centrifugation (faster, cheaper)
ELIF study_system == "soil":
  → Use bead-beating (mechanical lysis)
```

### **4. Output Templating**
Prompts provide exact JSON/YAML/R templates:
```json
{
  "hypotheses": {
    "primary": "...",
    "secondary": ["..."],
    "statistical_framework": "..."
  }
}
```

### **5. Adaptive Logic**
Prompts handle missing information gracefully:
```
IF user doesn't specify cultivation:
  → Provide 2 alternative scenarios
  → Let researcher choose later
```

### **6. Constraint Enforcement**
Prompts explicitly state what NOT to do:
```
DO NOT:
- Provide step-by-step lab instructions
- Include execution commands
- Assume missing information
```

---

## 🔧 **Technical Implementation**

### **Framework Components**

```
app/
├── agents/           # Agent logic (4 files)
├── prompts/          # System + User prompts (8 files)
├── graph.py          # LangGraph workflow orchestration
├── llm.py            # OpenAI API interface
├── guards.py         # Guardrail validation
├── cli.py            # Command-line interface
└── api.py            # REST API (FastAPI)
```

### **Technology Stack**
- **LLM:** OpenAI GPT-4o (via API)
- **Orchestration:** LangGraph (state machine for agent flow)
- **Language:** Python 3.8+
- **Output Formats:** JSON, YAML, Markdown, Bash, R

### **Workflow Execution**
```python
# Simplified execution flow:
state = {"user_query": "...", "status": "running"}

state = node_a1_sampling(state)   # Adds a1_output
state = node_a2_wetlab(state)      # Adds a2_output
state = node_a3_bioinfo(state)     # Adds a3_output
state = node_a4_analysis(state)    # Adds a4_output

state["status"] = "complete"
save_results(state)
```

---

## 📊 **Results & Validation**

### **Example Run**

**Input Query:**
```
Design a 6-month ARG surveillance study in hospital wastewater
```

**Output:**
- ✅ **A1:** 198 samples (3 sites × 5 reps × 12 months + controls)
- ✅ **A2:** DNA extraction + Illumina shotgun sequencing protocol
- ✅ **A3:** 5-stage pipeline (QC → Assembly → ARG annotation → Normalization)
- ✅ **A4:** R workflow with PERMANOVA + differential abundance testing

**Execution Time:** ~2-3 minutes (depends on LLM API response time)

### **Quality Metrics**

| Metric | Result |
|--------|--------|
| Workflow completion rate | 100% (4/4 agents) |
| JSON parsing success | 100% |
| Guardrail pass rate | 75% (1 medium, 1 high warning) |
| Output usability | Manual review ✓ |

**Guardrail warnings:**
- A2: Slightly too detailed (included specific timings)
- A3: False positive (normal bash syntax flagged)

---

## 🎓 **Academic Contributions**

### **1. Novel Architecture**
Multi-agent framework for scientific workflow planning (not execution).

### **2. Domain-Specific Reasoning**
Each agent embeds expert knowledge from its field:
- Epidemiology (A1)
- Molecular biology (A2)  
- Computational biology (A3)
- Biostatistics (A4)

### **3. Prompt Engineering Methodology**
- Two-prompt system (System + User)
- Decision tree integration
- Adaptive logic for incomplete inputs
- Structured output enforcement

### **4. Quality Assurance**
- Staged validation
- Inter-agent handoffs
- Automated guardrails
- Human review points

### **5. Reproducibility**
- All prompts versioned
- Execution logs saved
- Outputs timestamped
- Complete audit trail

---

## 📚 **Comparison with Related Work**

| Approach | This Framework | Single-Agent LLM | Traditional Pipeline |
|----------|---------------|------------------|---------------------|
| **Modularity** | ✅ High (4 agents) | ❌ Monolithic | ⚠️ Medium (scripts) |
| **Domain Expertise** | ✅ Specialized per stage | ⚠️ Generalist | ✅ Expert-coded |
| **Flexibility** | ✅ Adapts to user query | ✅ Flexible | ❌ Fixed parameters |
| **Error Detection** | ✅ Multi-stage validation | ⚠️ End-to-end only | ✅ Per-stage |
| **Maintainability** | ✅ Update per agent | ❌ Rewrite entire prompt | ⚠️ Update scripts |
| **Scalability** | ✅ Add new agents | ❌ Prompt length limit | ✅ Add stages |
| **Execution** | 🔵 Planning only | 🔵 Planning only | ✅ Automated |

**Key Insight:** This framework occupies a unique niche—**AI-powered research planning** rather than execution.

---

## 🔮 **Future Enhancements**

### **1. Additional Agents**
- **A0: Literature Review Agent** (before A1)
- **A5: Ethics & Compliance Agent** (after A4)
- **A6: Budget Estimation Agent** (parallel to all)

### **2. Interactive Mode**
- Allow researchers to edit outputs between stages
- Branching workflows (explore multiple scenarios)

### **3. Multi-LLM Support**
- Use different models per agent (GPT-4 for A1, Claude for A3)
- Ensemble voting for critical decisions

### **4. Knowledge Base Integration**
- Connect to protocol databases (protocols.io)
- Link to tool documentation (BioConda, CRAN)
- Reference recent literature (PubMed API)

### **5. Export Formats**
- Generate grant proposals
- Create lab notebooks
- Produce preprint drafts

---

## 📖 **Key Takeaways for Professor**

### **Innovation**
✅ Multi-agent architecture for scientific reasoning  
✅ Domain-specific prompt engineering  
✅ Structured inter-agent communication  
✅ Quality assurance at every stage  

### **Technical Rigor**
✅ Modular, maintainable codebase  
✅ Comprehensive validation and guardrails  
✅ Reproducible outputs with full audit trail  
✅ Production-ready API and CLI interfaces  

### **Research Impact**
✅ Accelerates study design (weeks → minutes)  
✅ Reduces design errors via multi-stage validation  
✅ Makes expert knowledge accessible to novice researchers  
✅ Promotes standardization in ARG surveillance  

### **Scalability**
✅ Extensible to other domains (microbiome, genomics, ecology)  
✅ Framework can be adapted for other research workflows  
✅ Modular design allows continuous improvement  

---

## 📎 **Supporting Documentation**

1. **`STRUCTURE.md`** - System architecture diagram
2. **`GUARDRAILS_EXPLAINED.md`** - Quality control details
3. **`VALIDATION_SUMMARY.md`** - Framework validation report
4. **`runs/TIMESTAMP/`** - Example outputs from test run
5. **`app/prompts/*.py`** - All 8 prompts (System + User for each agent)

---

**Prepared by:** [Your Name]  
**Contact:** [Your Email]  
**GitHub:** [Repository Link]  
**Date:** October 9, 2025
