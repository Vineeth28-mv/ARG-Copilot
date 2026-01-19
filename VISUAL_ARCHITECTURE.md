# Multi-Agent ARG Surveillance Framework
## Visual Architecture & Prompt Flow Diagrams

---

## 📊 **System Overview**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    USER RESEARCH QUESTION                            │
│  "Design a 6-month ARG surveillance study in hospital wastewater"   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AGENT 1: SAMPLING DESIGN                                           │
│  ┌────────────────┐                                                 │
│  │ System Prompt  │  Role: Epidemiologist                           │
│  │ (Who am I?)    │  Framework: 7-step reasoning                    │
│  └────────────────┘  Decision Trees: Study type, sample size        │
│  ┌────────────────┐                                                 │
│  │ User Prompt    │  Task: Generate sampling strategy               │
│  │ (What to do?)  │  Output: JSON (hypotheses, design, QC)          │
│  └────────────────┘                                                 │
│                                                                       │
│  OUTPUT: sampling_design.json                                       │
│  {                                                                   │
│    "spatial_design": "3 hospitals",                                 │
│    "temporal_design": "Monthly for 6 months",                       │
│    "replication": "n=5",                                            │
│    "total_samples": 90                                              │
│  }                                                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │ ✓ Validation: JSON parsed
                             │ ✓ Validation: Required keys present
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AGENT 2: WET-LAB PROTOCOL                                          │
│  ┌────────────────┐                                                 │
│  │ System Prompt  │  Role: Lab Specialist                           │
│  │ (Who am I?)    │  Framework: Input validation → Method selection │
│  └────────────────┘  Decision Trees: Extraction, library prep       │
│  ┌────────────────┐                                                 │
│  │ User Prompt    │  Task: Generate protocol recommendations        │
│  │ (What to do?)  │  Input: ###SAMPLING_OUTPUT### (JSON from A1)    │
│  └────────────────┘  Output: JSON (protocols, citations)            │
│                                                                       │
│  OUTPUT: wetlab_protocol.json                                       │
│  {                                                                   │
│    "extraction": "DNeasy PowerWater Kit",                           │
│    "sequencing": "Illumina NovaSeq PE150",                          │
│    "qc_checkpoints": [...]                                          │
│  }                                                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │ ✓ Validation: JSON parsed
                             │ ⚠ Guardrail: Check for actionable content
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AGENT 3: BIOINFORMATICS PIPELINE                                   │
│  ┌────────────────┐                                                 │
│  │ System Prompt  │  Role: Bioinformatician                         │
│  │ (Who am I?)    │  Framework: Pipeline architecture               │
│  └────────────────┘  Decision Trees: Assembly, taxonomy, ARG DB     │
│  ┌────────────────┐                                                 │
│  │ User Prompt    │  Task: Generate pipeline scripts                │
│  │ (What to do?)  │  Input: ###WETLAB_OUTPUT### (JSON from A2)      │
│  └────────────────┘  Output: Bash scripts + YAML configs            │
│                                                                       │
│  OUTPUT:                                                             │
│  - pipeline.sh (main script)                                        │
│  - config.yaml (parameters)                                         │
│  - setup_databases.sh (database setup)                              │
│  - data_handoff.yaml (for A4)                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │ ✓ Validation: Scripts generated
                             │ ⚠ Guardrail: Check for execution commands
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AGENT 4: STATISTICAL ANALYSIS                                      │
│  ┌────────────────┐                                                 │
│  │ System Prompt  │  Role: Statistician                             │
│  │ (Who am I?)    │  Framework: Assumption checking → Test selection│
│  └────────────────┘  Decision Trees: Parametric/non-parametric      │
│  ┌────────────────┐                                                 │
│  │ User Prompt    │  Task: Generate R analysis workflow             │
│  │ (What to do?)  │  Input: ###BIOINFO_OUTPUT### (YAML from A3)     │
│  └────────────────┘  Output: R Markdown + helper functions          │
│                                                                       │
│  OUTPUT:                                                             │
│  - analysis.Rmd (main workflow)                                     │
│  - helpers.R (utility functions)                                    │
│  - README.md (execution guide)                                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │ ✓ Validation: Scripts generated
                             │ ✓ Guardrail: No system calls
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    COMPLETE RESEARCH PLAN                            │
│  - Sampling Strategy (JSON)                                         │
│  - Wet-Lab Protocols (JSON)                                         │
│  - Bioinformatics Pipeline (Bash/YAML)                              │
│  - Statistical Analysis (R/Rmd)                                      │
│                                                                       │
│  Saved to: runs/TIMESTAMP/                                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 **Prompt Structure: Two-Prompt System**

```
┌────────────────────────────────────────────────────────────┐
│  SYSTEM PROMPT (Persistent Identity)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ WHO AM I?                                            │  │
│  │  - Role definition (e.g., "You are an epidemiologist")│ │
│  │  - Domain expertise                                  │  │
│  │  - Core principles                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ HOW DO I THINK?                                      │  │
│  │  - Reasoning framework (7-step process)             │  │
│  │  - Decision trees                                    │  │
│  │  - Quality standards                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ WHAT ARE MY CONSTRAINTS?                             │  │
│  │  - Output format (JSON schema)                       │  │
│  │  - Required sections                                 │  │
│  │  - Don'ts (what to avoid)                            │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                            +
┌────────────────────────────────────────────────────────────┐
│  USER PROMPT (Task-Specific Instructions)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ WHAT IS MY TASK?                                     │  │
│  │  - Specific goal (e.g., "Generate sampling design")  │  │
│  │  - Input data (###USER_QUERY### or previous output)  │  │
│  │  - Context                                           │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ HOW TO EXECUTE?                                      │  │
│  │  - Step 1: Parse input                               │  │
│  │  - Step 2: Apply decision trees                      │  │
│  │  - Step 3: Generate output                           │  │
│  │  - Step 4: Validate                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ EXAMPLES                                             │  │
│  │  - Example 1: Hospital wastewater                    │  │
│  │  - Example 2: Agricultural runoff                    │  │
│  │  - Example 3: Clinical isolates                      │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ OUTPUT TEMPLATE                                      │  │
│  │  {                                                   │  │
│  │    "hypotheses": {...},                             │  │
│  │    "sampling_design": {...}                         │  │
│  │  }                                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                            ↓
                     LLM (GPT-4o)
                            ↓
                    STRUCTURED OUTPUT
```

---

## 🌳 **Decision Tree Example: A2 DNA Extraction**

```
                    START: DNA Extraction Method Selection
                                    ↓
                    ┌───────────────────────────────┐
                    │  What is the sample type?     │
                    └───────────────┬───────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ↓                       ↓                       ↓
    ┌──────────────┐        ┌──────────────┐      ┌──────────────┐
    │ Wastewater   │        │    Soil      │      │    Fecal     │
    └──────┬───────┘        └──────┬───────┘      └──────┬───────┘
           │                       │                      │
           ↓                       ↓                      ↓
    ┌──────────────┐        ┌──────────────┐      ┌──────────────┐
    │ Biomass high?│        │ Organic high?│      │ Host DNA?    │
    └──────┬───────┘        └──────┬───────┘      └──────┬───────┘
           │                       │                      │
    ┌──────┴──────┐         ┌──────┴──────┐       ┌──────┴──────┐
    ↓             ↓         ↓             ↓       ↓             ↓
  YES            NO        YES           NO       YES           NO
    │             │         │             │       │             │
    ↓             ↓         ↓             ↓       ↓             ↓
DNeasy      DNeasy    DNeasy      MagMAX   QIAamp      MagMAX
PowerWater  PowerWater PowerSoil   Microb.  Stool      Pathogen
  Pro        (basic)     Pro       DNA Kit   Kit          Kit
    │             │         │             │       │             │
    └─────────────┴─────────┴─────────────┴───────┴─────────────┘
                                    ↓
                        OUTPUT: Recommended Kit + Rationale
```

---

## 🔗 **Data Flow & Handoff Mechanism**

```
A1: Sampling Design
         │
         │ Generates
         ↓
    sampling_design.json
    ┌────────────────────────────────────────┐
    │ {                                      │
    │   "study_system": "hospital_ww",       │
    │   "sample_types": ["wastewater"],      │
    │   "biomass": "high",                   │
    │   "target_analyte": "DNA",             │
    │   "safety_level": "BSL-2",             │
    │   "temporal_design": {                 │
    │     "duration": "6 months",            │
    │     "frequency": "monthly"             │
    │   }                                    │
    │ }                                      │
    └────────────┬───────────────────────────┘
                 │
                 │ String Injection:
                 │ USER_PROMPT.replace("###SAMPLING_OUTPUT###", json_str)
                 ↓
A2: Wet-Lab Protocol
         │
         │ Reads and interprets
         ↓
    "study_system" = "hospital_ww" → BSL-2 protocols
    "sample_types" = ["wastewater"] → Centrifugation
    "biomass" = "high" → PowerWater Pro Kit
    "target_analyte" = "DNA" → Metagenomic sequencing
         │
         │ Generates
         ↓
    wetlab_protocol.json
    ┌────────────────────────────────────────┐
    │ {                                      │
    │   "extraction": {                      │
    │     "kit": "DNeasy PowerWater Pro",    │
    │     "rationale": "High biomass..."     │
    │   },                                   │
    │   "sequencing": {                      │
    │     "platform": "Illumina",            │
    │     "chemistry": "PE150",              │
    │     "depth": "10M reads"               │
    │   }                                    │
    │ }                                      │
    └────────────┬───────────────────────────┘
                 │
                 │ String Injection:
                 │ USER_PROMPT.replace("###WETLAB_OUTPUT###", json_str)
                 ↓
A3: Bioinformatics Pipeline
         │
         │ Reads and configures
         ↓
    "platform" = "Illumina" → Use Trimmomatic, MEGAHIT
    "chemistry" = "PE150" → Set read length parameters
    "depth" = "10M" → Adjust assembly parameters
         │
         │ Generates
         ↓
    pipeline.sh + config.yaml + data_handoff.yaml
    ┌────────────────────────────────────────┐
    │ data_handoff.yaml:                     │
    │   input_files:                         │
    │     arg_abundance: "results/arg.tsv"   │
    │     taxonomy: "results/taxa.tsv"       │
    │     metadata: "metadata.csv"           │
    │   format:                              │
    │     arg_abundance:                     │
    │       rows: samples                    │
    │       cols: ARG genes                  │
    │       values: TPM-normalized counts    │
    │   normalization: "TPM"                 │
    └────────────┬───────────────────────────┘
                 │
                 │ String Injection:
                 │ USER_PROMPT.replace("###BIOINFO_OUTPUT###", yaml_str)
                 ↓
A4: Statistical Analysis
         │
         │ Reads and adapts
         ↓
    "arg_abundance" file = "results/arg.tsv"
    "normalization" = "TPM" → Use DESeq2 with TPM input
    "rows" = "samples" → Transpose if needed
         │
         │ Generates
         ↓
    analysis.Rmd + helpers.R
    ┌────────────────────────────────────────┐
    │ # Load data                            │
    │ arg_data <- read.table(                │
    │   "results/arg.tsv",                   │
    │   header=TRUE, row.names=1)            │
    │                                        │
    │ # Check assumptions                    │
    │ assumptions <- check_assumptions(      │
    │   arg_data)                            │
    │                                        │
    │ # Select test                          │
    │ if (assumptions$normal) {              │
    │   test <- "ANOVA"                      │
    │ } else {                               │
    │   test <- "Kruskal-Wallis"             │
    │ }                                      │
    └────────────────────────────────────────┘
```

---

## 🛡️ **Validation & Quality Control**

```
┌─────────────────────────────────────────────────────────────┐
│                    MULTI-STAGE VALIDATION                    │
└─────────────────────────────────────────────────────────────┘

Stage 1: INPUT VALIDATION
    ↓
┌─────────────────────────────────────┐
│  A1: Check user query completeness  │
│   ✓ Study system mentioned?         │
│   ✓ Duration specified?              │
│   ✓ Objective clear?                 │
└─────────────┬───────────────────────┘
              │ If incomplete → Generate alternatives
              ↓
Stage 2: OUTPUT VALIDATION
    ↓
┌─────────────────────────────────────┐
│  A1: Validate own output             │
│   ✓ JSON parseable?                  │
│   ✓ Required keys present?           │
│   ✓ Sample size justified?           │
└─────────────┬───────────────────────┘
              │
              ↓
Stage 3: INTER-AGENT VALIDATION
    ↓
┌─────────────────────────────────────┐
│  A2: Validate A1 output              │
│   ✓ Sample types defined?            │
│   ✓ Study system specified?          │
│   ✓ Safety level indicated?          │
└─────────────┬───────────────────────┘
              │ If invalid → Error, stop workflow
              ↓
Stage 4: GUARDRAIL CHECKS
    ↓
┌─────────────────────────────────────┐
│  A2: Check for policy violations    │
│   ✓ No specific temperatures?        │
│   ✓ No specific volumes?             │
│   ✓ No step-by-step instructions?    │
│                                      │
│  Risk Level:                         │
│   🟢 Low   (0 violations)            │
│   🟡 Medium (1-2 violations)         │
│   🔴 High  (3+ violations)           │
└─────────────┬───────────────────────┘
              │ Continue with warning
              ↓
[Repeat Stages 3-4 for A3, A4]
              ↓
Stage 5: FINAL VALIDATION
    ↓
┌─────────────────────────────────────┐
│  System: Check workflow status       │
│   ✓ All agents completed?            │
│   ✓ All outputs generated?           │
│   ✓ Validation reports clean?        │
│                                      │
│  Final Status:                       │
│   ✅ complete (all passed)           │
│   ⚠️ warning  (minor issues)         │
│   ❌ error    (critical failure)     │
└─────────────────────────────────────┘
```

---

## 🔧 **Technical Stack**

```
┌────────────────────────────────────────────────────────────┐
│                     SYSTEM ARCHITECTURE                     │
└────────────────────────────────────────────────────────────┘

User Interface Layer
├─ CLI (app/cli.py)
│   └─ Command: python -m app.cli "query"
└─ REST API (app/api.py)
    └─ Endpoint: POST /workflow/run
        ↓
Orchestration Layer
├─ LangGraph (app/graph.py)
│   ├─ State Machine: WorkflowState
│   ├─ Nodes: node_a1_sampling, node_a2_wetlab, ...
│   └─ Edges: A1 → A2 → A3 → A4
        ↓
Agent Layer
├─ app/agents/
│   ├─ a1_sampling.py    (run_sampling_agent, validate_output)
│   ├─ a2_wetlab.py      (run_wetlab_agent, validate_output)
│   ├─ a3_bioinfo.py     (run_bioinfo_agent, validate_output)
│   └─ a4_analysis.py    (run_analysis_agent, validate_output)
        ↓
Prompt Layer
├─ app/prompts/
│   ├─ a1_sampling_system_prompt.py
│   ├─ a1_sampling_user_prompt.py
│   ├─ a2_wetlab_system_prompt.py
│   ├─ a2_wetlab_user_prompt.py
│   ├─ ... (8 files total)
        ↓
LLM Layer
├─ app/llm.py
│   └─ call_llm(system_prompt, user_prompt, temperature, max_tokens)
        ↓
External Service
└─ OpenAI API
    └─ Model: GPT-4o

Validation Layer (Parallel)
├─ app/guards.py
│   ├─ check_wetlab_guardrails(response)
│   ├─ check_bioinfo_guardrails(response)
│   └─ check_analysis_guardrails(response)

Output Layer
└─ runs/TIMESTAMP/
    ├─ A1.json, A1.md
    ├─ A2.json, A2.md, A2_guardrails.json
    ├─ A3.json, A3.md, A3_guardrails.json
    ├─ A4.json, A4.md
    ├─ full_state.json
    ├─ validation_reports.json
    └─ SUMMARY.md
```

---

## 📊 **Execution Timeline**

```
Time     Agent    Activity                    Output
─────────────────────────────────────────────────────────────
00:00    -        User submits query          
00:01    A1       Parse query                 
00:15    A1       Generate sampling design    
00:25    A1       Validate output             sampling_design.json
00:26    A2       Read A1 output              
00:30    A2       Select protocols            
00:50    A2       Validate output             wetlab_protocol.json
00:51    A2       Run guardrails              A2_guardrails.json (⚠️ HIGH)
00:52    A3       Read A2 output              
01:00    A3       Generate pipeline scripts   
01:35    A3       Validate output             pipeline.sh, config.yaml
01:36    A3       Run guardrails              A3_guardrails.json (⚠️ MEDIUM)
01:37    A4       Read A3 output              
01:45    A4       Generate R workflow         
02:20    A4       Validate output             analysis.Rmd, helpers.R
02:21    A4       Run guardrails              A4_guardrails.json (✅ LOW)
02:22    -        Save results                runs/TIMESTAMP/
02:23    -        Generate summary            SUMMARY.md
─────────────────────────────────────────────────────────────
Total: ~2.5 minutes (depends on LLM API latency)
```

---

## 🎯 **Key Design Principles**

```
┌─────────────────────────────────────────────────────────────┐
│  1. MODULARITY                                              │
│     Each agent is independent and replaceable              │
│                                                             │
│  2. DOMAIN EXPERTISE                                        │
│     Agents embed specialized knowledge from their field    │
│                                                             │
│  3. STRUCTURED COMMUNICATION                                │
│     JSON/YAML handoffs (no ambiguity)                      │
│                                                             │
│  4. MULTI-STAGE VALIDATION                                  │
│     Catch errors early in the pipeline                     │
│                                                             │
│  5. HUMAN-IN-THE-LOOP                                       │
│     Save outputs at each stage for review                  │
│                                                             │
│  6. PLANNING NOT EXECUTION                                  │
│     Generate recommendations, not automated execution      │
│                                                             │
│  7. REPRODUCIBILITY                                         │
│     Complete audit trail (prompts, outputs, logs)          │
│                                                             │
│  8. EXTENSIBILITY                                           │
│     Easy to add new agents or modify existing ones         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 **For Presentation**

**Suggested Slide Flow:**

1. **Problem Statement** (1 slide)
   - ARG surveillance is complex (4+ domains)
   - Current methods: time-consuming, error-prone

2. **Solution Overview** (1 slide)
   - Multi-agent framework
   - Show the 4-agent chain diagram

3. **Architecture** (2 slides)
   - Prompt structure (System + User)
   - Data flow & handoffs

4. **Example Walkthrough** (2 slides)
   - Input: "Design hospital wastewater study"
   - Show outputs from A1, A2, A3, A4

5. **Quality Assurance** (1 slide)
   - Multi-stage validation
   - Guardrails diagram

6. **Results & Impact** (1 slide)
   - Execution time: ~3 minutes
   - Complete research plan generated
   - Reduces errors via staged validation

7. **Future Work** (1 slide)
   - Additional agents (literature review, ethics)
   - Extension to other domains

**Total: 9 slides, 15-minute presentation**

---

**Prepared by:** [Your Name]  
**Date:** October 9, 2025
