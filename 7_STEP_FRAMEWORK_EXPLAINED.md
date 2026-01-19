# 7-Step Reasoning Framework Explained
## How A1 Sampling Agent Thinks Through Problems

---

## 🤔 **What is the 7-Step Framework?**

The **7-step reasoning framework** is a structured thinking process that guides the A1 Sampling Design Agent through creating a research study design.

**Think of it like a checklist** that ensures the AI doesn't miss any critical aspects when designing a study.

---

## 📋 **The 7 Steps**

### **Step 1: Hypothesis Formulation**
**Question:** What are we actually testing?

**What the AI does:**
- Converts your research question into testable hypotheses
- Creates null hypothesis (H₀) and alternative hypothesis (H₁)
- Makes sure hypotheses are specific and measurable

**Example:**
```
Your question: "Is hospital wastewater different from municipal wastewater?"

AI creates hypotheses:
- H₀ (Null): "Hospital and municipal wastewater have equal ARG diversity"
- H₁ (Alternative): "Hospital wastewater has higher ARG diversity than municipal"
```

---

### **Step 2: Design Selection**
**Question:** What type of study design do we need?

**What the AI does:**
- Chooses appropriate sampling framework
- Options: Spatial, Temporal, Comparative, Nested, or Hybrid

**Example:**
```
For hospital vs. municipal comparison:
→ Design type: Comparative (comparing two groups)
→ Plus Temporal (over 6 months to account for variation)
→ Result: Hybrid design (Comparative + Temporal)
```

**Design options:**
- **Spatial:** Different locations (upstream/downstream)
- **Temporal:** Over time (daily/weekly/monthly)
- **Comparative:** Different groups (hospital vs. municipal)
- **Nested:** Multiple levels (regions → sites → samples)
- **Hybrid:** Combination of above

---

### **Step 3: Sample Size Estimation**
**Question:** How many samples do we need?

**What the AI does:**
- Calculates minimum samples needed for statistical power
- Uses standard assumptions (80% power, α=0.05)
- Recommends n ≥ 5 replicates per group

**Example:**
```
For hospital vs. municipal comparison:
→ Minimum: n=3 per site (basic)
→ Recommended: n=5 per site (robust)
→ With 3 hospital + 3 municipal sites × 5 reps = 30 samples per timepoint
→ Over 6 months = 180 total samples
```

---

### **Step 4: Metadata Prioritization**
**Question:** What information do we need to collect alongside samples?

**What the AI does:**
- Lists required metadata in 3 categories:
  - **MUST collect** (critical for analysis)
  - **SHOULD collect** (enhances interpretation)
  - **NICE to have** (optional, exploratory)

**Example:**
```
MUST collect:
- Site ID, GPS coordinates
- Date and time
- Temperature, pH
- Sample volume

SHOULD collect:
- Antibiotic usage data (for hospital)
- Patient census
- Weather conditions

NICE to have:
- Antibiotic concentrations (LC-MS/MS)
- Heavy metal concentrations
```

---

### **Step 5: Quality Control Strategy**
**Question:** How do we ensure data quality?

**What the AI does:**
- Specifies controls needed
- Plans replication strategy
- Identifies potential contamination sources

**Example:**
```
Biological replicates: n=5 per site per timepoint
Technical replicates: Duplicate DNA extractions for 10% of samples

Controls:
- Negative controls: Extraction blanks (n=3 per batch)
- Positive controls: Mock community (ZymoBIOMICS)
- Field blanks: Sterile water processed like samples
```

---

### **Step 6: Constraint Assessment**
**Question:** What are the limitations and how do we handle them?

**What the AI does:**
- Identifies potential problems (budget, access, time)
- Proposes solutions or alternatives
- Adjusts design to be realistic

**Example:**
```
Constraint: Budget limited to $20,000
Solution:
- Reduce from 6 months to 3 months
- OR reduce sites from 6 to 4
- OR use amplicon sequencing (cheaper) instead of metagenomics

Constraint: Can't access hospital during COVID
Solution:
- Collect from wastewater treatment plant receiving hospital effluent
- Add metadata on hospital discharge patterns
```

---

### **Step 7: Handoff to Next Agent**
**Question:** What does the Wet-Lab Agent need to know?

**What the AI does:**
- Summarizes key information for next agent
- Specifies sample types, biosafety requirements
- Sets expectations for downstream analysis

**Example:**
```
Handoff to Wet-Lab Agent:
- Sample type: Liquid wastewater
- Biosafety: BSL-2 (hospital samples may contain pathogens)
- Expected biomass: High
- Target: DNA for shotgun metagenomics
- Total samples: 180 + 18 controls = 198
- Downstream: ARG annotation, taxonomy, differential abundance
```

---

## 🔄 **How It Works in Practice**

### **Your Input:**
```
"Design a 6-month ARG surveillance study in hospital wastewater"
```

### **A1 Agent's Thinking Process:**

```
Step 1: Hypothesis Formulation
→ H₁: Hospital wastewater has higher ARG diversity than municipal

Step 2: Design Selection
→ Comparative (hospital vs. municipal) + Temporal (6 months)

Step 3: Sample Size
→ n=5 per site, 3 hospitals + 3 municipal = 30 samples/month
→ 6 months = 180 samples

Step 4: Metadata
→ MUST: site ID, date, temp, pH, patient census
→ SHOULD: antibiotic usage, weather
→ NICE: antibiotic concentrations

Step 5: QC Strategy
→ Biological reps: n=5
→ Negative controls: 3 per batch
→ Positive controls: ZymoBIOMICS

Step 6: Constraints
→ Budget: ~$50k estimated for sequencing
→ Access: Need hospital IRB approval
→ Time: 6 months sampling + 2 months analysis

Step 7: Handoff
→ To Wet-Lab: BSL-2, high biomass, DNA extraction, 198 samples
```

### **A1 Agent's Output:**
```json
{
  "hypotheses": {...},
  "sampling_design": {
    "spatial": "3 hospitals + 3 municipal WWTPs",
    "temporal": "Monthly for 6 months",
    "replication": "n=5 per site"
  },
  "total_samples": 180,
  "controls": 18,
  "metadata_requirements": {...},
  "qc_strategy": {...},
  "handoff_to_wetlab": {...}
}
```

---

## 🎯 **Why 7 Steps?**

### **1. Complete Coverage**
Each step addresses a critical aspect of study design:
- ✅ What are we testing? (Step 1)
- ✅ How do we test it? (Step 2)
- ✅ How many samples? (Step 3)
- ✅ What data to collect? (Step 4)
- ✅ How to ensure quality? (Step 5)
- ✅ What are the limits? (Step 6)
- ✅ What's next? (Step 7)

### **2. Logical Flow**
Each step builds on the previous:
```
Hypothesis → Design → Sample size → Metadata → QC → Constraints → Handoff
```

### **3. Nothing Forgotten**
The framework ensures the AI doesn't miss critical elements that researchers often overlook.

---

## 📊 **Visual Summary**

```
User Question: "Design ARG study in hospital wastewater"
         ↓
┌────────────────────────────────────────────────┐
│  A1 AGENT REASONING (7 STEPS)                  │
│                                                │
│  1. Hypothesis    → H₁: Hospital ≠ Municipal   │
│  2. Design        → Comparative + Temporal     │
│  3. Sample Size   → n=5, 180 samples           │
│  4. Metadata      → Site, date, temp, pH...    │
│  5. QC            → Controls, replicates       │
│  6. Constraints   → Budget, access, time       │
│  7. Handoff       → BSL-2, DNA, 198 samples    │
└────────────────────────────────────────────────┘
         ↓
OUTPUT: Complete sampling design (JSON)
```

---

## 🔍 **See It In Your Actual Run**

From your test run (`runs/20251009_140020/A1.json`):

**Step 1 result:**
```json
{
  "hypotheses": {
    "primary": "Hospital wastewater harbors higher ARG diversity...",
    "statistical_framework": "PERMANOVA + Dunn's test"
  }
}
```

**Step 3 result:**
```json
{
  "sampling_design": {
    "total_samples": 90,
    "replication": {
      "biological_replicates": 5,
      "rationale": "n=5 provides 80% power to detect medium effect (Cohen's d=0.5)"
    }
  }
}
```

**Step 7 result:**
```json
{
  "handoff_to_wetlab": {
    "sample_type": "liquid wastewater",
    "biosafety_level": "BSL-2",
    "expected_biomass": "high",
    "target_molecule": "DNA"
  }
}
```

**The AI followed all 7 steps!**

---

## 🆚 **Compare: With vs Without Framework**

### **Without Framework (Random AI):**
```
User: "Design ARG study in hospital wastewater"
AI: "Collect wastewater samples and sequence them"
```
❌ Vague, no details, unusable

### **With 7-Step Framework:**
```
User: "Design ARG study in hospital wastewater"
AI follows 7 steps:
- Formulates testable hypotheses
- Chooses comparative + temporal design
- Calculates n=5 per site, 180 samples
- Lists required metadata (14 variables)
- Specifies QC controls (3 types)
- Addresses budget constraints
- Hands off to Wet-Lab with clear specs
```
✅ Complete, detailed, actionable

---

## 💡 **Why This is Innovative**

Most AI prompts don't have structured reasoning frameworks. They just say "design a study" and hope for the best.

**Your framework:**
1. ✅ **Enforces systematic thinking** (can't skip steps)
2. ✅ **Ensures completeness** (all aspects covered)
3. ✅ **Mimics expert process** (how real epidemiologists think)
4. ✅ **Provides transparency** (can see which step produced each output)

---

## 🎓 **For Your Professor**

### **Simple Explanation:**
> "The 7-step framework is a structured thinking process I embedded in the A1 agent's system prompt. It guides the AI through: (1) hypothesis formulation, (2) design selection, (3) sample size calculation, (4) metadata planning, (5) quality control, (6) constraint handling, and (7) handoff preparation. This mimics how an expert epidemiologist would systematically approach study design."

### **Why It's Important:**
> "Without this framework, AI outputs are often incomplete—missing controls, underpowered sample sizes, or unclear hypotheses. The framework ensures systematic coverage of all critical aspects, like a checklist that expert researchers follow."

### **The Innovation:**
> "This represents a novel prompt engineering approach where we embed structured reasoning frameworks directly into the system prompt. It's not just 'please design a study'—it's 'follow these 7 specific cognitive steps that experts use.' This makes AI reasoning more reliable and auditable."

---

## 📚 **Other Agents Have Frameworks Too**

### **A2 (Wet-Lab):** 5-phase framework
1. Input validation
2. Method selection (using decision trees)
3. Protocol assembly
4. QC definition
5. Handoff preparation

### **A3 (Bioinformatics):** 6-stage framework
1. Input validation
2. Pipeline architecture
3. Tool selection
4. Database specification
5. Normalization strategy
6. Data handoff

### **A4 (Statistical Analysis):** 5-step framework
1. Data loading
2. Assumption checking
3. Test selection
4. Visualization
5. Interpretation

**Each agent has its own reasoning framework!**

---

## 🎯 **Key Takeaway**

**The 7-step framework = A structured checklist that guides the AI's thinking**

Just like:
- Pilots use checklists before takeoff
- Surgeons use checklists before surgery
- Your AI uses a 7-step framework before designing a study

**It ensures nothing important is forgotten!**

---

**Does this make the 7-step framework clear now?** 😊

It's basically a **to-do list** for the AI that says:
1. ☑️ Create hypotheses
2. ☑️ Choose design
3. ☑️ Calculate sample size
4. ☑️ Plan metadata
5. ☑️ Design QC
6. ☑️ Handle constraints
7. ☑️ Prepare handoff

Simple! 📝
