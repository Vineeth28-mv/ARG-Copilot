# 7-Step Framework - Quick Reference
## One-Page Cheat Sheet

---

## 🎯 **The 7 Steps in One Sentence Each**

| Step | What It Does | Output |
|------|-------------|--------|
| **1. Hypothesis** | Converts question into testable H₀ and H₁ | "Hospital ≠ Municipal ARGs" |
| **2. Design** | Chooses spatial/temporal/comparative/nested | "Comparative + Temporal" |
| **3. Sample Size** | Calculates n needed for statistical power | "n=5 per site, 180 samples" |
| **4. Metadata** | Lists MUST/SHOULD/NICE-to-have data | "Site, date, temp, pH..." |
| **5. QC** | Specifies controls and replication | "Negative controls, n=3" |
| **6. Constraints** | Identifies limitations and solutions | "Budget: reduce to 3 months" |
| **7. Handoff** | Prepares info for next agent | "BSL-2, high biomass, DNA" |

---

## 📊 **Visual Flow**

```
User Query
    ↓
┌─────────────────────────────────┐
│ STEP 1: Hypothesis              │
│ What are we testing?            │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ STEP 2: Design                  │
│ What type of study?             │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ STEP 3: Sample Size             │
│ How many samples?               │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ STEP 4: Metadata                │
│ What data to collect?           │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ STEP 5: QC                      │
│ How to ensure quality?          │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ STEP 6: Constraints             │
│ What are the limits?            │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ STEP 7: Handoff                 │
│ What does next agent need?      │
└────────────┬────────────────────┘
             ↓
    Complete Sampling Design
```

---

## 💡 **Example: Your Actual Run**

### **Input:**
```
"Design a 6-month ARG surveillance study in hospital wastewater"
```

### **7 Steps Output:**

| Step | Result |
|------|--------|
| 1 | H₁: Hospital has higher ARG diversity than municipal |
| 2 | Comparative (hospital vs. municipal) + Temporal (6 months) |
| 3 | n=5 per site, 3 hospital + 3 municipal = 180 samples |
| 4 | MUST: site ID, date, temp, pH; SHOULD: patient census |
| 5 | Controls: 18 negatives, biological reps: n=5 |
| 6 | Budget: ~$50k, Access: Need IRB approval |
| 7 | To A2: BSL-2, high biomass, DNA, 198 samples |

---

## 🔄 **Each Step Answers a Question**

```
Step 1: WHAT?     What are we testing?
Step 2: HOW?      How do we design it?
Step 3: HOW MANY? How many samples?
Step 4: WHICH?    Which data to collect?
Step 5: QUALITY?  How to ensure quality?
Step 6: LIMITS?   What constraints exist?
Step 7: NEXT?     What comes next?
```

---

## ✅ **Why 7 Steps?**

**It's a checklist** to ensure the AI doesn't forget anything:

- ☑️ Hypothesis (what to test)
- ☑️ Design (how to test)
- ☑️ Sample size (statistical power)
- ☑️ Metadata (data collection)
- ☑️ QC (quality assurance)
- ☑️ Constraints (feasibility)
- ☑️ Handoff (next steps)

---

## 🗣️ **Explain to Your Professor**

**Simple version:**
> "The 7-step framework is a structured checklist embedded in my A1 agent's prompt. It ensures the AI systematically addresses: hypothesis formulation, design selection, sample size calculation, metadata planning, quality control, constraint handling, and handoff preparation—just like an expert epidemiologist would think through a study design."

**One sentence:**
> "It's a systematic reasoning checklist that guides the AI through 7 critical aspects of study design: what, how, how many, which data, quality checks, limitations, and next steps."

---

## 📍 **Where to Learn More**

- **Full explanation:** `7_STEP_FRAMEWORK_EXPLAINED.md`
- **See it in action:** `runs/20251009_140020/A1.json`
- **In the code:** `app/prompts/a1_sampling_system_prompt.py` (lines 13-82)

---

**Bottom line:** 7 steps = 7 questions the AI must answer to create a complete study design! 📝
