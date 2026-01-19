"""
A1 Sampling Design Agent - User Prompt

"""

TEXT = """<<<Sampling Design Agent - User Prompt

## Task
Transform the user's research question into a **structured, testable sampling design** for ARG surveillance. Output a comprehensive JSON that guides the Wet-Lab Protocol Agent.

---

## Step 1: Parse User Query

Extract the following information:

### Research Objective
- **Primary goal:** Detection | Quantification | Tracking | Intervention assessment | Mechanistic understanding
- **Target analytes:** ARGs | ARB (resistant bacteria) | MGEs | Microbiome composition | Pathogens
- **Study type:** Observational | Experimental | Longitudinal | Cross-sectional

### Study System
- **Environment:** Wastewater treatment | Hospital | Agricultural | Aquatic | Soil | Air | Built environment
- **Scale:** Lab/pilot/full-scale | Local/regional/global
- **Context:** Urban vs. rural | Clinical vs. environmental | One Health surveillance

### Comparisons of Interest
- **Spatial:** Treatment stages | Geographic locations | Environmental compartments
- **Temporal:** Seasonal | Before-after intervention | Event-driven (e.g., storm, antibiotic pulse)
- **Categorical:** Technology types | Host populations | Treatment vs. control

### Constraints (if mentioned)
- Budget limitations
- Access restrictions
- Timeline constraints
- Available analytical methods

---

## Step 2: Generate Hypotheses

Formulate **testable hypotheses** addressing one or more of:

1. **Prevalence/abundance differences:** Across spatial or temporal gradients
2. **Associations:** Between ARGs/ARB and environmental parameters, co-selection factors (metals, disinfectants, antibiotics)
3. **Intervention effectiveness:** Treatment processes, stewardship programs, source control measures
4. **Fate and transport:** Persistence, transfer through environmental compartments
5. **Host-pathogen-environment interactions:** Resistance dissemination pathways

**Format:**
- **H₀ (Null Hypothesis):** "There is no difference in ARG abundance between influent and effluent"
- **H₁ (Alternative Hypothesis):** "ARG abundance is reduced in effluent compared to influent due to biological treatment"

---

## Step 3: Design Sampling Scheme

### Spatial Structure
Explicitly list sampling locations/compartments with justification:

**Example:**
```json
"spatial_design": {
  "framework": "Spatial gradient (wastewater treatment process)",
  "sampling_points": [
    {
      "location": "Influent",
      "justification": "Captures incoming ARG load from community wastewater",
      "n_biological_replicates": 5
    },
    {
      "location": "Activated Sludge Tank",
      "justification": "Assesses ARG dynamics during biological treatment",
      "n_biological_replicates": 5
    },
    {
      "location": "Effluent",
      "justification": "Measures treatment removal efficiency",
      "n_biological_replicates": 5
    },
    {
      "location": "Receiving River (downstream 500m)",
      "justification": "Tracks environmental discharge impact",
      "n_biological_replicates": 5
    }
  ]
}
```

### Temporal Structure
Specify frequency and duration with system-dynamics consideration:

**Example:**
```json
"temporal_design": {
  "framework": "Time-series with seasonal coverage",
  "sampling_frequency": "Monthly",
  "duration": "12 months",
  "justification": "Captures seasonal variation in antibiotic use (higher in winter) and temperature effects on treatment efficiency",
  "total_sampling_events": 12
}
```

### Sample Specifications
Match sample types/volumes to downstream analytical methods:

**Example:**
```json
"sample_specifications": [
  {
    "matrix": "Wastewater (liquid)",
    "volume": "1 L per replicate",
    "purpose": "Filtration (0.22 µm) → DNA extraction → qPCR + shotgun metagenomics"
  },
  {
    "matrix": "Activated sludge",
    "volume": "10 mL per replicate",
    "purpose": "Direct DNA extraction → ARG annotation"
  },
  {
    "matrix": "Wastewater (for cultivation)",
    "volume": "50 mL per replicate",
    "purpose": "Selective plating for phenotypic ARB isolation (optional)"
  }
]
```

### Replication Strategy
Clarify biological vs. technical replicates:

**Example:**
```json
"replication": {
  "biological_replicates": 5,
  "biological_definition": "Independent samples collected from the same location on the same day",
  "technical_replicates": 2,
  "technical_definition": "Duplicate DNA extractions from each biological replicate",
  "total_samples": 80,
  "calculation": "(4 locations) × (5 bio reps) × (12 months) + controls"
}
```

### Stratification (if applicable)
Identify stratifying factors:

**Example:** Multi-site study stratified by treatment technology (conventional activated sludge, MBR, constructed wetlands)

---

## Step 4: Specify Metadata Requirements

### Critical Metadata (MUST collect)
**Always include:**
- GPS coordinates or site ID
- Date and time of sampling
- Temperature (°C)
- pH

**System-specific critical metadata:**

| System | Critical Parameters |
|--------|---------------------|
| Wastewater | Flow rate, HRT, SRT, treatment technology, disinfection method, served population |
| Hospital | Ward type, patient census, cleaning protocols, antibiotic prescribing rate |
| Agricultural | Animal type/density, antibiotic usage (kg/year), manure management |
| Aquatic | Distance from pollution source, DO, BOD, COD, nutrients (N/P) |
| Soil | Land use history, texture, moisture, organic matter content |

### Supplementary Metadata (SHOULD collect if feasible)
- Antibiotic consumption data (DDD per 1000 inhabitants)
- Additional environmental parameters (redox, turbidity, suspended solids)
- Process performance metrics (BOD/COD removal %)

### Gold Standard (OPTIONAL but highly valuable)
- **Antibiotic concentrations** (LC-MS/MS): Enables dose-response analysis with ARG abundance

---

## Step 5: Define Quality Control Strategy

### Controls
```json
"qc_controls": {
  "negative_controls": [
    {
      "type": "Extraction blank",
      "description": "Sterile water processed alongside samples",
      "frequency": "1 per 10 samples"
    },
    {
      "type": "PCR no-template control",
      "description": "Water instead of DNA template",
      "frequency": "1 per qPCR plate"
    }
  ],
  "positive_controls": [
    {
      "type": "Mock community",
      "description": "ZymoBIOMICS standard for sequencing",
      "frequency": "1 per sequencing run"
    },
    {
      "type": "Reference strain",
      "description": "E. coli with known ARGs for qPCR validation",
      "frequency": "Standard curve per assay"
    }
  ],
  "method_validation": [
    "Compare fresh vs. -80°C frozen samples (n=5 pairs) to validate preservation",
    "Process high-biomass and low-biomass samples separately to prevent cross-contamination"
  ]
}
```

### Sample-Type Specific QC

**For low-biomass samples** (drinking water, air):
- Increase extraction blank frequency (1 per 5 samples)
- Include filter blanks (unused filters processed as samples)
- Consider larger sample volumes

**For longitudinal studies:**
- Include stable reference site (negative control location)
- Standardize time-of-day for sampling (minimize diurnal variation)

**For multi-site studies:**
- Standardize SOPs across all sites
- Include split samples between labs for inter-lab QC (10% of samples)
- Use field blanks at each site

---

## Step 6: Calculate Sample Size & Statistical Power

```json
"statistical_considerations": {
  "effect_size_assumed": "Medium (Cohen's d = 0.5)",
  "power": 0.8,
  "alpha": 0.05,
  "minimum_n_per_group": 5,
  "justification": "Based on power analysis for two-group comparison (t-test/Wilcoxon)",
  "actual_n_per_group": 5,
  "recommended_tests": ["Kruskal-Wallis for multi-group comparisons", "Spearman correlation for ARG-environment associations", "PERMANOVA for community composition"]
}
```

If constraints force n < 5:
```json
"constraints_and_tradeoffs": {
  "limitation": "Budget allows only n=3 per group",
  "impact": "Statistical power reduced to ~0.6; may miss subtle effects",
  "mitigation": "Prioritize effect size estimation over hypothesis testing; use non-parametric tests; report as pilot study"
}
```

---

## Step 7: Handoff to Wet-Lab Agent

Provide specifications the Wet-Lab Agent needs to design protocols:

```json
"handoff_to_wetlab": {
  "sample_types": [
    {
      "matrix": "Wastewater (liquid)",
      "expected_biomass": "High (10⁷-10⁹ cells/mL)",
      "preservation": "Process within 6 hours OR freeze at -80°C",
      "biosafety_level": "BSL-2",
      "special_handling": "Contains human pathogens; use appropriate PPE"
    },
    {
      "matrix": "Activated sludge",
      "expected_biomass": "Very high (10⁹-10¹⁰ cells/g)",
      "preservation": "-80°C stable for >1 year",
      "biosafety_level": "BSL-2",
      "special_handling": "Viscous; requires bead-beating for cell lysis"
    }
  ],
  "analytical_targets": [
    "DNA extraction for shotgun metagenomics (Illumina PE150, target 10 Gb/sample)",
    "qPCR for ARG quantification (target genes: sul1, tetW, blaCTX-M, ermB, 16S rRNA)",
    "Optional: Cultivation on selective media for phenotypic characterization"
  ],
  "critical_assumptions": [
    "Samples contain sufficient DNA for sequencing (>100 ng total)",
    "qPCR detection limit: 10³ gene copies/mL"
  ],
  "total_samples_to_process": 80
}
```

---

## Step 8: Generate Complete JSON Output

**Output Schema:**

```json
{
  "study_metadata": {
    "research_question": "[User's original question]",
    "primary_objective": "[Detection/Quantification/etc.]",
    "study_system": "[Wastewater/Hospital/etc.]",
    "scale": "[Local/Regional/Global]"
  },
  
  "hypothesis_framework": {
    "null_hypothesis": "[H₀ statement]",
    "alternative_hypothesis": "[H₁ statement]",
    "secondary_hypotheses": ["[Optional H₂]", "[Optional H₃]"]
  },
  
  "study_design": {
    "framework_type": "[Spatial/Temporal/Comparative/Nested/Hybrid]",
    "justification": "[Why this design best tests the hypothesis]",
    "spatial_design": { ... },
    "temporal_design": { ... }
  },
  
  "sampling_scheme": {
    "sample_specifications": [ ... ],
    "replication": { ... },
    "stratification": { ... },
    "total_samples": 80
  },
  
  "metadata_requirements": {
    "critical_metadata": [ ... ],
    "supplementary_metadata": [ ... ],
    "gold_standard_optional": [ ... ]
  },
  
  "qc_strategy": {
    "qc_controls": { ... },
    "sample_type_specific_qc": [ ... ]
  },
  
  "statistical_considerations": {
    "effect_size_assumed": "Medium (d=0.5)",
    "power": 0.8,
    "minimum_n_per_group": 5,
    "recommended_tests": [ ... ]
  },
  
  "constraints_and_tradeoffs": {
    "acknowledged_limitations": [ ... ],
    "trade_offs_made": [ ... ],
    "implications_for_interpretation": [ ... ]
  },
  
  "handoff_to_wetlab": {
    "sample_types": [ ... ],
    "analytical_targets": [ ... ],
    "critical_assumptions": [ ... ],
    "total_samples_to_process": 80
  }
}
```

---

## Adaptive Logic: Alternative Scenarios

If critical information is missing from user query, provide **2-3 alternative scenarios**:

**Example:** User doesn't specify if cultivation is needed

```json
"alternative_scenarios": {
  "scenario_A_metagenomics_only": {
    "description": "DNA-only workflow, no cultivation",
    "sample_volume": "1 L wastewater",
    "analytical_methods": ["DNA extraction", "qPCR", "Shotgun metagenomics"],
    "advantages": "Faster, lower cost, captures non-culturable organisms",
    "limitations": "No phenotypic data, cannot confirm viability"
  },
  "scenario_B_cultivation_plus_metagenomics": {
    "description": "Hybrid approach with cultivation for phenotypic validation",
    "sample_volume": "1 L wastewater (split: 900 mL for DNA, 100 mL for cultivation)",
    "analytical_methods": ["DNA extraction", "qPCR", "Metagenomics", "Selective plating", "AST"],
    "advantages": "Phenotypic confirmation, isolate collection for mechanistic studies",
    "limitations": "Higher cost, cultivation bias toward fast-growing organisms"
  }
}
```

---

## Adaptive Reasoning Rules

| User mentions... | Adjust design to include... |
|------------------|----------------------------|
| "Pathogens" or "clinical isolates" | Cultivation on selective media, BSL-2 considerations, species identification |
| "Plasmids" or "mobile genetic elements" | Larger sample volumes (MGEs may be rare), long-read sequencing (Nanopore/PacBio), epicPCR for host-ARG linkage |
| "Risk assessment" | Absolute quantification (qPCR/ddPCR with standard curves), cultivation for dose-response, MIC determination |
| "Source tracking" | Include upstream sources (hospital effluent, farm runoff, WWTP discharge points) alongside environmental samples |
| "Seasonal variation" | Minimum 12-month sampling, monthly frequency, capture temperature extremes |
| "Intervention study" | Before-after design: 3+ baseline timepoints, intervention period, 6+ follow-up timepoints, control site |
| "Pilot study" or "exploratory" | Prioritize spatial/temporal breadth over deep replication (n=3 acceptable), focus on method development |

---

## Final Validation Checklist

Before submitting output, verify:

- [ ] Hypothesis is testable and specific
- [ ] Sample size ≥ n=3 biological replicates per group (or limitation explicitly stated)
- [ ] Critical metadata identified for study system
- [ ] QC controls specified (negative and positive)
- [ ] Handoff section provides clear specifications for Wet-Lab Agent
- [ ] Trade-offs and limitations acknowledged if constraints present
- [ ] JSON is complete and well-formatted
- [ ] Alternative scenarios provided if user query is ambiguous

---

## Example Output Summary

For a user asking: *"How effective is wastewater treatment at removing antibiotic resistance genes?"*

**Output includes:**
- H₀: No difference in ARG abundance between influent and effluent
- Spatial design: Influent → Activated Sludge → Effluent (n=5 each)
- Temporal design: Monthly sampling × 12 months (capture seasonal variation)
- Sample specs: 1L wastewater per replicate, 0.22 µm filtration
- Critical metadata: Flow rate, HRT, SRT, temperature, treatment technology
- QC: Extraction blanks (1 per 10), mock community (1 per run)
- Handoff: BSL-2 samples, expected high biomass, DNA for metagenomics + qPCR
- Statistical power: n=5 provides 80% power to detect 50% reduction in ARGs (Cohen's d=0.5)

**Total samples:** (3 locations) × (5 reps) × (12 months) = 180 + 18 controls = **198 samples**>>>

Based on the user's research question, generate a complete sampling design.
User Query: ###USER_QUERY###

Return a JSON with the following sections:
- hypotheses
- sampling_design (spatial, temporal, replication)
- metadata_requirements
- qc_strategy
- statistical_considerations
- handoff_to_wetlab
"""

