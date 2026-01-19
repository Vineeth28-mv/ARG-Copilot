# Multi-Agent ARG Surveillance Framework
## Presentation Summary for Professor

---

## 🎯 **The Problem**

**Research Question:**  
*"How do we design a comprehensive ARG surveillance study?"*

**Current Challenges:**
- ❌ Requires expertise in 4+ domains (epidemiology, lab methods, bioinformatics, statistics)
- ❌ Design decisions are interconnected (sampling affects analysis, analysis affects sampling)
- ❌ Prone to errors (missing controls, underpowered studies, incompatible methods)
- ❌ Time-consuming (weeks of planning and iteration)

---

## 💡 **The Solution**

**Multi-Agent AI Framework** that models the research workflow as a sequence of specialized expert consultants:

```
User Question
    ↓
🔬 A1: Sampling Design (Epidemiologist)
    ↓
🧪 A2: Wet-Lab Protocol (Lab Specialist)
    ↓
💻 A3: Bioinformatics (Bioinformatician)
    ↓
📊 A4: Statistical Analysis (Statistician)
    ↓
Complete Research Plan
```

**Key Insight:** Break complex workflow into **modular expert agents** rather than one monolithic AI.

---

## 🏗️ **Architecture**

### **Each Agent Has:**

1. **System Prompt** (~200 lines)
   - Role definition
   - Reasoning framework
   - Decision trees
   - Quality constraints

2. **User Prompt** (~400-800 lines)
   - Specific task
   - Output templates
   - Examples
   - Edge cases

3. **Validation**
   - Input validation
   - Output validation
   - Guardrails

### **Agent Chain:**

| Agent | Input | Output | Format |
|-------|-------|--------|--------|
| A1 | Research question | Sampling strategy | JSON |
| A2 | A1 JSON | Protocol recommendations | JSON |
| A3 | A2 JSON | Pipeline scripts | Bash/YAML |
| A4 | A3 YAML | Analysis workflow | R/Rmd |

---

## 🧠 **Prompt Engineering Strategy**

### **Core Techniques:**

#### **1. Two-Prompt System**
- **System Prompt:** "Who you are" (persistent identity)
- **User Prompt:** "What you do" (task instructions)

#### **2. Structured Reasoning**
```
Step 1: Parse input
Step 2: Apply decision trees
Step 3: Generate output
Step 4: Validate
Step 5: Handoff to next agent
```

#### **3. Decision Tree Integration**
Example from A2 (DNA extraction):
```
IF sample_type == "wastewater" AND biomass == "high":
  → DNeasy PowerWater Kit
ELIF sample_type == "soil":
  → DNeasy PowerSoil Kit
ELIF sample_type == "fecal":
  → QIAamp DNA Stool Kit
```

#### **4. Output Templates**
Prompts include exact JSON/YAML schemas:
```json
{
  "hypotheses": {
    "primary": "...",
    "statistical_framework": "..."
  },
  "sampling_design": {
    "spatial": "...",
    "temporal": "..."
  }
}
```

#### **5. Adaptive Logic**
Handle incomplete inputs:
```
IF user doesn't specify budget:
  → Generate 3 scenarios (low/medium/high cost)
```

---

## 📊 **Example Run**

### **Input:**
```
"Design a 6-month ARG surveillance study in hospital wastewater"
```

### **Outputs:**

**A1: Sampling Design**
```json
{
  "study_design": "3 hospitals × 5 replicates × 6 months = 90 samples",
  "controls": "18 negative controls",
  "statistical_power": "80% to detect 50% reduction (Cohen's d=0.5)",
  "total_samples": 108
}
```

**A2: Wet-Lab Protocol**
```json
{
  "collection": "Grab sampling, 1L per site",
  "concentration": "Centrifugation (4000g, 15min)",
  "extraction": "DNeasy PowerWater Kit",
  "sequencing": "Illumina NovaSeq PE150, 10M reads/sample"
}
```

**A3: Bioinformatics Pipeline**
```bash
#!/bin/bash
# Stage 1: QC (FastQC + Trimmomatic)
# Stage 2: Assembly (MEGAHIT)
# Stage 3: ARG annotation (CARD + DeepARG)
# Stage 4: Normalization (TPM)
# Output: data_handoff.yaml
```

**A4: Statistical Analysis**
```r
# R Markdown workflow
# 1. Check assumptions (Shapiro-Wilk, Levene)
# 2. Diversity analysis (Shannon, Simpson)
# 3. Ordination (PCoA + PERMANOVA)
# 4. Differential abundance (DESeq2)
# 5. Visualization (ggplot2)
```

**Execution Time:** ~3 minutes  
**Output:** Complete research plan with 4 structured deliverables

---

## 🛡️ **Quality Assurance**

### **1. Inter-Agent Validation**
Each agent validates the previous agent's output:
```python
if "sampling_design" not in a1_output:
    raise ValidationError("A1 missing required field")
```

### **2. Guardrails**
Automated checks ensure design principles:

| Agent | Guardrail | Purpose |
|-------|-----------|---------|
| A2 | No specific measurements | Keep protocols conceptual, not actionable |
| A3 | No execution commands | Generate templates, not auto-run scripts |
| A4 | No system calls | Analysis code only, not deployment |

### **3. Staged Outputs**
Save results after each agent:
```
runs/20251009_140020/
├── A1.json  ← Review & approve before A2
├── A2.json  ← Review & approve before A3
├── A3.md    ← Review & approve before A4
└── A4.md    ← Final deliverable
```

Researchers can **intervene** between stages.

---

## 📐 **Why This Approach Works**

### **Compared to Single-Agent LLM:**

| Aspect | Multi-Agent | Single-Agent |
|--------|------------|--------------|
| **Complexity** | 4 focused agents | 1 giant prompt (3000+ lines) |
| **Expertise** | Domain-specific per agent | Generalist |
| **Validation** | Multi-stage (4 checkpoints) | End-to-end only |
| **Maintenance** | Update one agent | Rewrite entire prompt |
| **Debugging** | Pinpoint which agent failed | Hard to trace |
| **Scalability** | Add new agents easily | Prompt length limit |

### **Compared to Traditional Pipelines:**

| Aspect | Multi-Agent | Traditional Pipeline |
|--------|------------|---------------------|
| **Flexibility** | Adapts to any query | Fixed parameters |
| **User Input** | Natural language | Config files |
| **Expertise Required** | None (AI embedded) | High (expert coding) |
| **Execution** | Planning only | Automated execution |
| **Output** | Recommendations | Processed data |

**Unique Niche:** AI-powered **research planning**, not execution.

---

## 🎓 **Academic Contributions**

### **1. Novel Architecture**
- First multi-agent framework for scientific workflow planning
- Extends LangGraph for domain-specific reasoning

### **2. Prompt Engineering Methodology**
- Two-prompt system (System + User)
- Decision tree integration in prompts
- Adaptive logic for incomplete inputs
- Structured output enforcement

### **3. Domain Expertise Encoding**
- Embedded expert knowledge from 4 domains
- Validated decision trees
- Literature-backed recommendations

### **4. Quality Assurance Framework**
- Inter-agent validation
- Automated guardrails
- Human review points
- Complete audit trail

### **5. Practical Impact**
- Study design time: weeks → minutes
- Reduces design errors
- Makes expertise accessible
- Promotes standardization

---

## 🔬 **Technical Implementation**

### **Stack:**
- **LLM:** OpenAI GPT-4o
- **Orchestration:** LangGraph (state machine)
- **Language:** Python 3.8+
- **Interfaces:** CLI + REST API

### **Code Structure:**
```
app/
├── agents/      # 4 agent modules
├── prompts/     # 8 prompt files (System + User × 4)
├── graph.py     # Workflow orchestration
├── guards.py    # Validation logic
└── api.py       # FastAPI interface
```

### **Execution:**
```python
result = run_workflow(user_query)
# → Runs A1 → A2 → A3 → A4 sequentially
# → Validates at each stage
# → Saves outputs to runs/TIMESTAMP/
```

---

## 🔮 **Future Work**

### **Short-Term:**
1. Add **A0: Literature Review Agent** (search PubMed, summarize papers)
2. Improve **A3 guardrails** (reduce false positives for bash scripts)
3. Add **export to protocol.io** format

### **Medium-Term:**
4. **Interactive mode** (let researchers edit between stages)
5. **Multi-LLM support** (GPT-4, Claude, Gemini for ensemble)
6. **Budget estimation module**

### **Long-Term:**
7. Extend to other domains (microbiome, genomics, ecology)
8. Integration with lab management systems (LIMS)
9. Grant proposal generation

---

## 📊 **Demonstration**

### **Live Demo Available:**

```bash
# CLI Interface
python -m app.cli "Design ARG study in hospital wastewater"

# API Interface
curl -X POST http://localhost:8000/workflow/run \
  -H "Content-Type: application/json" \
  -d '{"query": "Design ARG study in hospital wastewater"}'
```

### **Sample Outputs:**
- See: `runs/20251009_140020/` for complete example
- 4 structured deliverables (JSON + Markdown)
- Validation reports
- Execution logs

---

## 🎯 **Key Takeaways**

### **Innovation:**
✅ Multi-agent architecture for scientific reasoning  
✅ Domain-specific prompt engineering  
✅ Structured inter-agent communication  

### **Quality:**
✅ Multi-stage validation  
✅ Automated guardrails  
✅ Human review points  

### **Impact:**
✅ Accelerates study design (weeks → minutes)  
✅ Reduces errors via staged validation  
✅ Makes expertise accessible  

### **Future:**
✅ Extensible to other research domains  
✅ Integration with lab systems  
✅ Continuous improvement via modular design  

---

## 📚 **Documentation**

1. **Full Strategy:** `STRATEGY_EXPLANATION_FOR_PROF.md` (20 pages)
2. **Architecture:** `STRUCTURE.md`
3. **Guardrails:** `GUARDRAILS_EXPLAINED.md`
4. **Validation:** `VALIDATION_SUMMARY.md`
5. **Sample Run:** `runs/20251009_140020/`

---

## 📞 **Questions?**

**Key Points to Emphasize:**
1. Why multi-agent > single-agent
2. How decision trees embed expertise
3. Validation at every stage
4. Practical impact on research workflow

**Potential Questions:**
- *"Why not execute the pipeline?"* → Planning ≠ Execution (different goals)
- *"How accurate are the recommendations?"* → Based on literature + expert knowledge
- *"Can it handle novel scenarios?"* → Yes, adaptive logic for edge cases
- *"What if an agent makes a mistake?"* → Multi-stage validation catches errors

---

**Prepared by:** [Your Name]  
**Date:** October 9, 2025  
**Duration:** 15-20 minute presentation
