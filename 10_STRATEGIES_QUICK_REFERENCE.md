# 10 Prompt Engineering Strategies - Quick Reference
## One-Page Cheat Sheet

---

## 📊 **All 10 Strategies at a Glance**

| # | Strategy | What It Does | Example |
|---|----------|--------------|---------|
| **1** | **Two-Prompt System** | Separate identity from task | System: "You're an epidemiologist" + User: "Design this study" |
| **2** | **7-Step Framework** | Structured reasoning checklist | Hypothesis → Design → Sample Size → Metadata → QC → Constraints → Handoff |
| **3** | **Decision Trees** | IF-THEN logic for choices | IF water+high → PowerWater Kit |
| **4** | **Few-Shot Learning** | 2-3 complete examples | Hospital example + Farm example |
| **5** | **Chain-of-Thought** | Step-by-step reasoning | Step 1 output → used in Step 2 → used in Step 3 |
| **6** | **Output Templates** | Exact JSON/YAML schemas | `{"hypotheses": {...}, "design": {...}}` |
| **7** | **Adaptive Logic** | Handle missing info | "If budget limited: 3 scenarios" |
| **8** | **Constraint Enforcement** | DO/DON'T rules | DON'T: specific temps, volumes |
| **9** | **Inter-Agent Comm** | Structured handoffs | JSON A1 → A2, YAML A3 → A4 |
| **10** | **Guardrails** | Automated validation | Scan for "37°C", "250 µL" |

---

## 🎯 **How They Work Together**

```
USER QUERY
    ↓
┌──────────────────────────────────────┐
│ STRATEGY 1: Two-Prompt System        │
│   System: Who am I? (identity)       │
│   User: What to do? (task)           │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ STRATEGY 2: Structured Framework     │
│   7 steps: H → D → n → M → Q → C → H │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ STRATEGY 3: Decision Trees           │
│   IF-THEN logic: sample → method     │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ STRATEGY 4: Few-Shot Learning        │
│   Example 1 + Example 2 + Example 3  │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ STRATEGY 5: Chain-of-Thought         │
│   Step 1 → Step 2 → Step 3 (linked)  │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ STRATEGY 6: Output Templates         │
│   Exact JSON schema provided         │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ STRATEGY 7: Adaptive Logic           │
│   Missing info? → 3 scenarios        │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ STRATEGY 8: Constraint Enforcement   │
│   Check: DON'T rules violated?       │
└────────────┬─────────────────────────┘
             ↓
    AI GENERATES OUTPUT
             ↓
┌──────────────────────────────────────┐
│ STRATEGY 10: Guardrails              │
│   Scan for violations                │
└────────────┬─────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│ STRATEGY 9: Inter-Agent Comm         │
│   Pass JSON/YAML to next agent       │
└──────────────────────────────────────┘
             ↓
         NEXT AGENT
```

---

## 💡 **Purpose of Each Strategy**

### **STRUCTURE (What to think about)**
- 🏗️ **Strategy 1** (Two-Prompt): Separates "who" from "what"
- 📋 **Strategy 2** (Framework): Ensures completeness
- 🌳 **Strategy 3** (Decision Trees): Guides choices

### **QUALITY (How to think well)**
- 📚 **Strategy 4** (Few-Shot): Shows excellence
- 🔗 **Strategy 5** (Chain-of-Thought): Forces logic
- 📝 **Strategy 6** (Output Templates): Ensures format

### **ROBUSTNESS (Handle edge cases)**
- 🔄 **Strategy 7** (Adaptive Logic): Handles gaps
- 🚫 **Strategy 8** (Constraints): Prevents errors
- 🔗 **Strategy 9** (Inter-Agent): Clear handoffs
- 🛡️ **Strategy 10** (Guardrails): Catches violations

---

## 🗣️ **One-Sentence Explanations**

1. **Two-Prompt System:** One prompt defines identity, another defines task
2. **7-Step Framework:** Checklist ensuring AI covers all aspects systematically
3. **Decision Trees:** Flowcharts showing IF sample=X THEN method=Y
4. **Few-Shot Learning:** 2-3 complete examples demonstrating quality
5. **Chain-of-Thought:** Forces AI to show reasoning step-by-step
6. **Output Templates:** Exact JSON/YAML schemas required in output
7. **Adaptive Logic:** Provides alternatives when info is missing
8. **Constraint Enforcement:** Explicit DO/DON'T rules in prompts
9. **Inter-Agent Communication:** Structured JSON/YAML between agents
10. **Guardrails:** Automated scans checking for policy violations

---

## 📊 **Where Each Strategy Appears**

| Strategy | A1 Sampling | A2 Wet-Lab | A3 Bioinfo | A4 Stats |
|----------|-------------|------------|------------|----------|
| Two-Prompt | ✅ | ✅ | ✅ | ✅ |
| Framework | ✅ (7-step) | ✅ (5-phase) | ✅ (6-stage) | ✅ (5-step) |
| Decision Trees | ⚪ | ✅✅✅ | ✅✅ | ✅ |
| Few-Shot | ✅✅ | ✅ | ✅ | ✅ |
| Chain-of-Thought | ✅✅ | ✅ | ✅ | ✅ |
| Output Templates | ✅ | ✅ | ✅ | ✅ |
| Adaptive Logic | ✅✅ | ✅ | ⚪ | ⚪ |
| Constraints | ✅ | ✅✅ | ✅✅ | ✅ |
| Inter-Agent | ✅ → A2 | ✅ → A3 | ✅ → A4 | - |
| Guardrails | ⚪ | ✅✅ | ✅✅ | ✅ |

✅✅ = Heavy use, ✅ = Standard use, ⚪ = Light/optional use

---

## 🎓 **For Your Professor (30-Second Explanation)**

> "I used 10 prompt engineering strategies in my framework:
> 
> **Structure:** Two-prompt system (identity vs. task), 7-step reasoning framework, and decision trees for method selection.
> 
> **Quality:** Few-shot learning with publication-quality examples, chain-of-thought reasoning, and exact output templates.
> 
> **Robustness:** Adaptive logic for missing data, explicit constraints, structured inter-agent communication, and automated guardrails.
> 
> Together, these create expert-level, transparent, and policy-compliant AI reasoning."

---

## 📖 **Deep Dive Document**

For complete explanations with examples from your actual run:
📄 **Read: `PROMPT_ENGINEERING_STRATEGIES.md`**

---

## 🎯 **Key Innovation**

**It's not just using these strategies—it's how they COMBINE:**

```
Framework (WHAT to think about)
    +
Decision Trees (HOW to decide)
    +
Few-Shot (WHAT good looks like)
    +
Constraints + Guardrails (WHAT to avoid)
    =
Expert-level, Safe, Transparent AI
```

---

**All 10 strategies documented in one place! 🎉**

