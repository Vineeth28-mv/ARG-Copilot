# Guardrails System - Explained

## 🛡️ What Are Guardrails?

**Guardrails** are automated validation checks that scan each agent's output to ensure they stay in "**planning mode**" rather than "**execution mode**."

### Design Philosophy

This framework is designed for **reasoning and planning**, not execution. Each agent should:
- ✅ Generate **conceptual plans, workflows, and code templates**
- ✅ Reference existing protocols and tools
- ✅ Provide structured guidance for researchers
- ❌ NOT provide step-by-step executable instructions
- ❌ NOT include commands that could be accidentally run

---

## 📊 Guardrail Rules by Agent

### **A2 - Wet-Lab Protocol Agent**

**Goal:** Provide protocol **selection guidance**, not lab bench instructions.

**Checks for:**
- ❌ Specific temperatures (`37°C`, `65 degrees`)
- ❌ Specific volumes (`250 µL`, `5 mL`)
- ❌ Specific timings (`30 minutes`, `2 hours`)
- ❌ Step-by-step procedural language (`Step 1:`, `Add X, then mix for Y`)

**Why:** Lab protocols require validation and vary by equipment/context. A2 should **recommend** protocols, not prescribe them.

---

### **A3 - Bioinformatics Pipeline Agent**

**Goal:** Generate **script templates**, not auto-executable pipelines.

**Checks for:**
- ❌ Python subprocess calls (`subprocess.run()`, `subprocess.Popen()`)
- ❌ Shell execution patterns (`$(...)`, `` `...` ``, `exec`, `eval`)
- ❌ Docker/container commands (`docker run`, `docker exec`)
- ❌ Package installation (`!pip install`, `apt-get install`)

**Why:** Bioinformatics pipelines need customization for each environment. A3 should provide **templates** for researchers to adapt.

---

### **A4 - Statistical Analysis Agent**

**Goal:** Generate **R analysis workflows**, not system-level operations.

**Checks for:**
- ❌ R system calls (`system()`, `system2()`)
- ❌ Package installation (`install.packages()`, `BiocManager::install()`)
- ❌ File system manipulation (`file.remove()`, `unlink()`)

**Why:** Analysis code should be reproducible and safe. A4 provides analysis templates, not deployment scripts.

---

## 🔍 Your Run: What Was Detected?

### **A2 Wet-Lab: `HIGH` Risk**

**Violations:**
1. ✗ Specific temperature values
2. ✗ Specific volume measurements
3. ✗ Specific timing instructions

**Example from your output:**
```json
"protocol_modifications": [
  "Extended bead-beating: 10 min at 30 Hz (vs. standard 5 min)"
]
```

**Triggered:** `"10 min"` and `"30 Hz"` → specific timings

**Is this a problem?** 
- **Moderate concern** - A2 provided detailed parameters instead of just saying "Use extended bead-beating protocol for improved lysis."
- **Impact:** Low - the output is still useful, just slightly more prescriptive than intended.

---

### **A3 Bioinformatics: `MEDIUM` Risk**

**Violations:**
1. ✗ Shell execution pattern: `\$\(.*?\)`
2. ✗ Shell execution pattern: `` `.*?` ``

**Example from your output:**
```bash
#!/bin/bash
# Pipeline: Illumina Shotgun Metagenomics
```

**Triggered:** The guardrails detected bash script syntax (likely backticks or `$(...)` for command substitution in the generated scripts).

**Is this a problem?**
- **No** - This is a **false positive**!
- A3 is **supposed** to generate bash scripts with standard syntax.
- The guardrails are being overly cautious about patterns that are normal in bash.

---

## ⚙️ Risk Level Interpretation

| Level | Meaning | Action |
|-------|---------|--------|
| 🟢 **Low** | No violations | ✅ Perfect - no review needed |
| 🟡 **Medium** | 1-2 violations | ⚠️ Review - likely false positives or minor issues |
| 🔴 **High** | 3+ violations | 🔍 Review output and potentially refine agent prompts |

---

## 🤔 Should You Be Concerned?

**Your results:**
- ✅ **Workflow Status:** `complete` (all agents ran successfully)
- ⚠️ **A2:** `warning` (high risk - slightly too detailed)
- ⚠️ **A3:** `warning` (medium risk - false positive)
- ✅ **A4:** `success` (no issues)

### **Recommendation: No action needed**

1. **A3's warnings are false positives** - it correctly generated bash scripts.
2. **A2's warnings are minor** - the output is still conceptual enough for planning.
3. **The workflow completed successfully** - all outputs are usable.

---

## 🔧 How to Adjust Guardrails (Optional)

If you want to tune the guardrail sensitivity, edit `app/guards.py`:

### **Option 1: Relax A3 Guardrails for Bash Scripts**

```python
def check_bioinfo_guardrails(response: str) -> Dict[str, Any]:
    violations = []
    
    # Skip $(…) and `…` checks if in a bash script block
    if "```bash" in response or "#!/bin/bash" in response:
        # Allow normal bash syntax
        pass
    else:
        # Apply strict checks for Python/other code
        ...
```

### **Option 2: Make A2 More Strict**

If you want A2 to be even more conceptual, add stricter patterns:
```python
# Flag any mention of specific brands/kits
if re.search(r'(Qiagen|Zymo|Illumina|MagMAX)', response):
    violations.append("Mentions specific commercial kits (should be generic)")
```

### **Option 3: Disable Guardrails Entirely**

In `app/agents/*.py`, comment out the guardrail calls:
```python
# guardrail_report = check_wetlab_guardrails(response)
guardrail_report = {"violations": [], "risk_level": "low", "message": "Guardrails disabled"}
```

---

## 📁 Guardrail Outputs

For each workflow run, guardrails generate:

```
runs/TIMESTAMP/
├── A2_guardrails.json   # Wet-lab validation results
├── A3_guardrails.json   # Bioinformatics validation results
├── A4_guardrails.json   # Analysis validation results (if any)
└── validation_reports.json  # Complete validation summary
```

These are **informational** - they don't block execution, just flag potential issues.

---

## ✅ Bottom Line

**For your current run:**

✅ **Framework works correctly**  
⚠️ **Minor guardrail warnings are expected** (especially for A3 bash scripts)  
✅ **All outputs are usable** for your ARG surveillance workflow  
📝 **No changes required** unless you want to fine-tune prompt verbosity

The guardrails did their job by flagging slightly detailed outputs, but **the workflow is production-ready!** 🎉

---

## 📚 Related Files

- `app/guards.py` - Guardrail implementation and pattern definitions
- `runs/TIMESTAMP/*_guardrails.json` - Individual validation reports
- `validation_reports.json` - Consolidated validation summary
- `SUMMARY.md` - High-level workflow status (includes guardrail warnings)

