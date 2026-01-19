# Wet-Lab Protocol Agent - User Prompt

## Task
Transform the sampling design from the Sampling Design Agent into **executable laboratory protocols** with complete sample-to-data workflow. Generate structured JSON + narrative summary.

---

## Step 1: Validate Input from Sampling Design Agent

Check that you have received:

### Required Information:
- [ ] Sample matrices (water, wastewater, soil, sludge, etc.)
- [ ] Sample volumes/masses per replicate
- [ ] Expected biomass level (high/medium/low)
- [ ] Total number of samples to process
- [ ] Analytical targets (DNA, RNA, cultivation, qPCR, chemical analysis)
- [ ] Preservation requirements
- [ ] Biosafety level
- [ ] Special handling requirements

### If Information is Missing:
Request clarification from Sampling Agent output OR provide alternatives with justification.

---

## Step 2: Extract Protocol Requirements

Identify which protocol components are needed by scanning for keywords:

| Keywords in Input | Required Protocol Section |
|-------------------|---------------------------|
| "DNA", "metagenomics", "sequencing" | DNA extraction + library prep |
| "RNA", "metatranscriptomics", "expression" | RNA extraction (with DNase) |
| "qPCR", "quantification", "gene copies" | qPCR setup (primers, standards) |
| "16S", "amplicon", "microbiome" | 16S amplicon sequencing (V4 or V3-V4) |
| "Shotgun", "whole genome", "resistome" | Shotgun metagenomics library prep |
| "Nanopore", "long-read", "MinION" | Nanopore library prep (HMW DNA) |
| "Cultivation", "isolation", "phenotypic" | Cultivation protocols + media |
| "AST", "MIC", "susceptibility" | Phenotypic antimicrobial susceptibility testing |
| "LC-MS", "antibiotic concentration", "residues" | Chemical analysis (SPE + LC-MS/MS) |
| "epicPCR", "host-ARG linkage", "single-cell" | epicPCR protocol |

**Key Rule**: Only generate protocols for methods explicitly mentioned. Don't add cultivation to a DNA-only study.

---

## Step 3: Select Methods Using Decision Trees

For each required component, apply decision logic from System Prompt:

### A. DNA Extraction Kit Selection

```
Sample Matrix → Expected Biomass → Kit Selection
```

**Examples:**
- Soil + High biomass → **DNeasy PowerSoil Kit** (Qiagen 12888-100)
- Water + Low biomass (after filtration) → **DNeasy PowerWater Kit** (Qiagen 14900-50-NF)
- Activated sludge + Very high biomass → **FastDNA Spin Kit for Soil** (MP Bio 116560-200)
- Pure culture → **DNeasy Blood & Tissue Kit** (Qiagen 69506)

If kit not specified in study: Flag "NR: Not Reported" + recommend field-standard with justification.

### B. RNA Extraction Kit Selection (if needed)

```
Application → Sample Type → Kit Selection
```

**Examples:**
- Metatranscriptomics + Soil → **RNeasy PowerSoil Total RNA Kit** (Qiagen 12866-25)
- Gene expression + Pure culture → **RNeasy Mini Kit** (Qiagen 74104) + DNase treatment
- Simultaneous DNA+RNA → **AllPrep DNA/RNA Kit** (Qiagen 80204)

### C. Biomass Concentration Method (if needed)

```
Sample Type + Volume → Concentration Method
```

**Examples:**
- Water, 0.5-2 L → **Filtration** (0.22 µm cellulose nitrate, Whatman)
- Wastewater, <500 mL → **Direct filtration** (0.45 µm PVDF)
- Wastewater, >500 mL → **Centrifuge** 5000g 15 min
- Activated sludge → **Centrifuge** 5000-10000g 10-15 min
- Soil/sediment → **No concentration** (use 0.25-0.5 g directly)

### D. Sequencing Library Prep Kit Selection (if needed)

```
Sequencing Type → Input Amount → Kit Selection
```

**Examples:**
- **16S Amplicon** → 2-step PCR (515F/806R for V4 or 341F/805R for V3-V4)
- **Shotgun Metagenomics**:
  - High input (>100 ng) → **Nextera DNA Flex** (Illumina 20018705)
  - Low input (1-50 ng) → **NEBNext Ultra II FS** (NEB E7805)
- **Nanopore Long-Read** → **SQK-LSK114** (1D ligation) or **SQK-RBK114** (barcoded)
- **PacBio HiFi** → **SMRTbell Express Template Prep Kit 2.0**

### E. Cultivation Media Selection (if applicable)

```
Target Organisms → Media Selection
```

**Examples:**
- Total heterotrophs → **R2A agar** (environmental) or **TSA** (clinical)
- Gram-negative ARB → **MacConkey agar** + antibiotics at breakpoint concentrations
- Enterococcus → **Enterococcus Selective Agar** (bile esculin)
- Pseudomonas → **Pseudomonas CFC Agar** (cetrimide-fucidin-cephalosporin)

---

## Step 4: Generate Protocol JSON

Create structured protocol with these sections:

```json
{
  "protocol_metadata": {
    "protocol_id": "WetLab_[StudyID]_[Date]",
    "study_source": "[Sampling Design Agent output reference]",
    "total_samples": 80,
    "estimated_processing_time": "5-7 days (excluding sequencing run time)",
    "last_updated": "2024-01-15"
  },

  "sample_collection_preservation": {
    "sample_types": [
      {
        "matrix": "Wastewater (liquid)",
        "volume_per_replicate": "1 L",
        "containers": "Sterile 1L polypropylene bottles",
        "preservation": "Process within 6 hours OR freeze at -80°C in cryovials",
        "transport": "4°C cooler with ice packs",
        "storage_stability": "-80°C stable for >1 year"
      }
    ]
  },

  "biomass_concentration": {
    "required": true,
    "method": "Filtration",
    "procedure": {
      "filter_type": "Cellulose nitrate, 0.22 µm pore size, 47 mm diameter (Whatman)",
      "volume_filtered": "0.5-1 L per sample (or until filter clogs)",
      "filtration_apparatus": "Vacuum filtration manifold or peristaltic pump",
      "aseptic_technique": "Pre-sterilize apparatus, use sterile forceps for filter handling",
      "storage": "Store filters at -80°C in cryovials if not extracting immediately"
    }
  },

  "extraction": {
    "target": "DNA",
    "kit": {
      "name": "DNeasy PowerWater Kit",
      "manufacturer": "Qiagen",
      "catalog_number": "14900-50-NF",
      "justification": "Optimized for low-biomass filtered water samples",
      "alternative_if_unavailable": "DNeasy PowerSoil Kit (12888-100) also effective"
    },
    "input_material": "1/4 filter cut into small pieces",
    "protocol_modifications": [
      "Extended bead-beating: 10 min at 30 Hz (vs. standard 5 min) for improved lysis"
    ],
    "elution_volume": "100 µL",
    "expected_yield": "10-100 ng/µL (depends on biomass)",
    "quality_metrics": {
      "quantification_method": "Qubit dsDNA HS Assay",
      "purity_od260_280": "1.8-2.0 (acceptable range)",
      "purity_od260_230": "2.0-2.2 (acceptable range)",
      "fragment_size": "Check by agarose gel: should see high MW band >10 kb"
    }
  },

  "library_prep": {
    "sequencing_type": "Illumina shotgun metagenomics",
    "kit": {
      "name": "Nextera DNA Flex Library Prep Kit",
      "manufacturer": "Illumina",
      "catalog_number": "20018705"
    },
    "input_dna": "100 ng (normalized to same concentration across samples)",
    "fragmentation": "Enzymatic tagmentation (5 min at 55°C)",
    "size_selection": "AMPure XP beads, 0.8:1 ratio for ~500 bp target",
    "pcr_cycles": 8,
    "quality_control": {
      "qubit_quantification": ">2 ng/µL final library",
      "tapestation_fragment_size": "400-600 bp peak",
      "qpcr_quantification": "Accurate molarity for pooling (e.g., KAPA Library Quant Kit)"
    },
    "pooling": "Equimolar at 4 nM final concentration",
    "sequencing_parameters": {
      "platform": "Illumina NovaSeq 6000",
      "read_configuration": "PE150 (paired-end 150 bp)",
      "target_depth": "10 Gb per sample (50-70M read pairs)"
    }
  },

  "qpcr_protocol": {
    "target_genes": [
      {
        "gene": "16S rRNA",
        "purpose": "Total bacteria quantification (normalization)",
        "primers": {
          "forward": "ACTCCTACGGGAGGCAGCAG",
          "reverse": "ATTACCGCGGCTGCTGG",
          "amplicon_size": "200 bp",
          "reference": "Muyzer et al. 1993"
        }
      },
      {
        "gene": "sul1",
        "purpose": "Sulfonamide resistance gene",
        "primers": {
          "forward": "CGGCGTGGGCTACCTGAACG",
          "reverse": "GCCGATCGCGTGAAGTTCCG",
          "amplicon_size": "163 bp",
          "reference": "Pei et al. 2006"
        }
      }
    ],
    "master_mix": "PowerUp SYBR Green Master Mix (Applied Biosystems)",
    "reaction_volume": "20 µL",
    "template_amount": "5 ng DNA per reaction",
    "cycling_conditions": {
      "initial_denaturation": "95°C 10 min",
      "amplification": "40 cycles: 95°C 15s, 60°C 30s, 72°C 30s",
      "melt_curve": "60-95°C, 0.5°C increments"
    },
    "standard_curve": {
      "template": "Plasmid with target gene insert",
      "dilution_series": "10² to 10⁸ copies/µL",
      "acceptance_criteria": "Efficiency 90-110%, R² >0.98"
    },
    "normalization": "Express as gene copies per 16S rRNA gene copy"
  },

  "cultivation_protocol": {
    "note": "Include only if study requires phenotypic characterization",
    "media": [
      {
        "type": "R2A agar",
        "purpose": "Total environmental bacteria",
        "incubation": "28°C, 48-72h, aerobic"
      },
      {
        "type": "MacConkey agar + Ciprofloxacin (4 mg/L)",
        "purpose": "Ciprofloxacin-resistant Enterobacteriaceae",
        "incubation": "35°C, 24h, aerobic"
      }
    ],
    "plating_volume": "100 µL of appropriate dilutions (10⁻³ to 10⁻⁶)",
    "colony_selection": "Pick 20 random colonies per plate for identification",
    "identification": "16S rRNA Sanger sequencing OR MALDI-TOF MS"
  },

  "phenotypic_ast": {
    "note": "Include only if isolates need susceptibility testing",
    "method": "Disk diffusion (Kirby-Bauer)",
    "standard": "CLSI M02-A13 (2023)",
    "media": "Mueller-Hinton agar",
    "inoculum": "0.5 McFarland standard (~1.5×10⁸ CFU/mL)",
    "antibiotics_tested": [
      "Ciprofloxacin 5 µg disk",
      "Tetracycline 30 µg disk",
      "Ampicillin 10 µg disk",
      "Ceftriaxone 30 µg disk"
    ],
    "incubation": "35°C, 16-20h, aerobic",
    "interpretation": "CLSI M100 (2024 edition) breakpoints",
    "qc_strains": [
      "E. coli ATCC 25922",
      "S. aureus ATCC 29213"
    ]
  },

  "chemical_analysis": {
    "note": "Include only if measuring antibiotic concentrations",
    "target_analytes": ["Sulfamethoxazole", "Tetracycline", "Ciprofloxacin"],
    "sample_volume": "500 mL",
    "extraction": {
      "method": "Solid-phase extraction (SPE)",
      "cartridge": "Oasis HLB 200 mg (Waters)",
      "conditioning": "5 mL methanol, 5 mL water",
      "loading": "pH 3 adjusted sample, 10 mL/min flow rate",
      "wash": "5 mL 5% methanol in water",
      "elution": "5 mL methanol + 2% formic acid",
      "concentration": "Evaporate under N₂ to 0.5 mL",
      "reconstitution": "Mobile phase A to 1 mL"
    },
    "lc_ms_method": {
      "instrument": "Agilent 1290-6460 Triple Quad LC-MS/MS",
      "column": "Agilent Poroshell 120 EC-C18, 2.1×100 mm, 2.7 µm",
      "mobile_phase_a": "Water + 0.1% formic acid",
      "mobile_phase_b": "Acetonitrile + 0.1% formic acid",
      "gradient": "5% B (0 min) → 95% B (10 min) → hold 2 min",
      "flow_rate": "0.3 mL/min",
      "injection_volume": "10 µL",
      "ionization": "ESI+ (ciprofloxacin, tetracycline), ESI- (sulfamethoxazole)",
      "mrm_transitions": "See Gros et al. 2013 J Chromatogr A for full list"
    },
    "calibration": "Matrix-matched standards, 6-point curve (1-1000 ng/L), R² ≥0.99",
    "lod_loq": "Calculate from signal-to-noise (S/N ≥3 for LOD, ≥10 for LOQ)"
  },

  "quality_control": {
    "extraction_blanks": {
      "frequency": "1 per 10 samples",
      "material": "Sterile water processed identically to samples"
    },
    "pcr_ntc": {
      "frequency": "1 per qPCR plate",
      "material": "Water instead of DNA template"
    },
    "sequencing_controls": {
      "phix_spike": "1-5% for Illumina (maintains cluster quality)",
      "mock_community": "ZymoBIOMICS Microbial Community Standard (known composition)"
    },
    "cultivation_controls": {
      "sterility_checks": "Uninoculated plates incubated alongside samples",
      "qc_reference_strains": "E. coli ATCC 25922 for AST validation"
    },
    "chemical_analysis_controls": {
      "solvent_blank": "Pure solvents through full extraction",
      "matrix_blank": "Sample matrix without analytes",
      "matrix_spike": "Known amount added to real sample (recovery 80-120%)",
      "surrogate_standards": "Isotope-labeled antibiotics (monitor extraction efficiency)"
    }
  },

  "safety": {
    "biosafety_level": "BSL-2",
    "justification": "Wastewater samples likely contain human pathogens",
    "ppe_required": [
      "Disposable lab coat (autoclave before disposal)",
      "Nitrile gloves (double-glove for high-risk steps)",
      "Safety glasses or face shield (centrifugation, vortexing)",
      "Biosafety cabinet for aerosol-generating procedures"
    ],
    "chemical_hazards": [
      {
        "chemical": "Guanidinium thiocyanate (in lysis buffers)",
        "hazard": "Releases toxic gas if mixed with bleach",
        "handling": "NEVER mix with bleach waste; use separate waste container"
      },
      {
        "chemical": "LC-MS solvents (methanol, acetonitrile)",
        "hazard": "Flammable, toxic",
        "handling": "Use in fume hood, grounded containers"
      }
    ],
    "waste_disposal": {
      "biohazard_solid": "Autoclave 121°C 30 min → regular trash",
      "biohazard_liquid": "Autoclave or 10% bleach 30 min → sink (check local regs)",
      "sharps": "Puncture-resistant container → autoclave → EH&S pickup",
      "chemical_waste": "Segregate (halogenated vs. non-halogenated) → label → EH&S pickup"
    }
  },

  "troubleshooting": {
    "low_dna_yield": [
      "Increase input material (more filter area or soil mass)",
      "Extend bead-beating time",
      "Check kit reagent expiration dates",
      "Verify sample was not over-diluted"
    ],
    "low_od260_280": [
      "Indicates protein contamination",
      "Re-extract with fresh kit",
      "Ensure adequate proteinase K treatment"
    ],
    "low_od260_230": [
      "Indicates salt/organic contamination (humic acids, phenol)",
      "Use additional wash steps",
      "Consider switching to PowerSoil kit for difficult samples"
    ],
    "poor_library_quality": [
      "Check DNA fragment size before library prep (should be HMW)",
      "Normalize DNA concentration accurately",
      "Reduce PCR cycles if over-amplification suspected"
    ],
    "qpcr_primer_dimers": [
      "Redesign primers (check for self-complementarity)",
      "Increase annealing temperature",
      "Reduce primer concentration"
    ],
    "no_growth_on_plates": [
      "Verify antibiotic concentration is at breakpoint (not too high)",
      "Check incubation conditions (temperature, atmosphere)",
      "Confirm sample viability (cultivation-based methods miss non-culturable bacteria)"
    ]
  },

  "handoff_to_bioinformatics": {
    "expected_data_types": [
      "Illumina PE150 shotgun metagenomics (FASTQ.gz)",
      "qPCR Ct values (CSV)"
    ],
    "file_naming_convention": "SampleID_R1.fastq.gz and SampleID_R2.fastq.gz",
    "sequencing_parameters": {
      "platform": "Illumina NovaSeq 6000",
      "read_length": "PE150",
      "target_depth": "10 Gb per sample",
      "index_strategy": "Unique dual indexes (UDI)"
    },
    "quality_thresholds_met": {
      "dna_concentration": ">10 ng/µL (Qubit)",
      "dna_purity_od260_280": "1.8-2.0",
      "library_fragment_size": "400-600 bp (TapeStation)",
      "library_concentration": ">2 nM (qPCR quantification)"
    },
    "metadata_files_provided": {
      "sample_metadata": "metadata/sample_metadata.csv (sample ID, location, date, environmental parameters)",
      "extraction_log": "metadata/extraction_log.csv (batch, date, kit lot, technician)",
      "sequencing_run_info": "metadata/sequencing_run_summary.csv (run ID, lane, index sequences)"
    },
    "known_technical_issues": [
      "Sample007: Low DNA yield (5 ng/µL); sequencing depth may be lower",
      "Batch 2 samples (Sample020-040): Extracted with different kit lot; potential batch effect",
      "PhiX contamination higher than expected in Lane 3 (8% vs. target 5%)"
    ],
    "critical_notes_for_analysis": [
      "Use RAW read counts for DESeq2 differential abundance (do not normalize)",
      "Recommend prevalence filter: keep features present in ≥20% samples (≥16 samples)",
      "Account for extraction batch effect in multivariate analysis",
      "qPCR normalization: use 16S rRNA gene copies as denominator"
    ]
  }
}
```

---

## Step 5: Generate Narrative Summary

Write a 2-3 paragraph summary for human review:

### Example:

**Protocol Summary:**

This wet-lab protocol processes 80 wastewater samples for ARG surveillance using shotgun metagenomics and qPCR quantification. Samples (1 L wastewater per replicate) are filtered through 0.22 µm cellulose nitrate filters, and DNA is extracted using the DNeasy PowerWater Kit (Qiagen 14900-50-NF), optimized for low-biomass filtered samples. Extended bead-beating (10 min) is applied for improved cell lysis. DNA quality is assessed by Qubit (yield), NanoDrop (purity), and agarose gel (integrity). Illumina shotgun metagenomics libraries are prepared using the Nextera DNA Flex kit from 100 ng input DNA, targeting 10 Gb sequencing depth per sample on NovaSeq PE150.

Parallel qPCR quantification targets five ARGs (sul1, tetW, blaCTX-M, ermB, intI1) and 16S rRNA for normalization, using PowerUp SYBR Green chemistry with plasmid standard curves. Quality control includes extraction blanks (1 per 10 samples), PCR no-template controls, and a ZymoBIOMICS mock community for sequencing validation. All samples are processed under BSL-2 conditions due to potential pathogen content in wastewater.

**Notable Protocol Adaptations:** Sample007 had low DNA yield (5 ng/µL) despite extended bead-beating; sequencing depth for this sample may be reduced. Batch 2 samples (020-040) were extracted with a different kit lot and should be assessed for batch effects during bioinformatics analysis. The protocol delivers FASTQ files for metagenomics and CSV files with qPCR Ct values, along with comprehensive metadata (sample info, extraction logs, sequencing run parameters) for downstream analysis.

---

## Step 6: Handle Missing Information

For any missing details, use the decision hierarchy:

### Priority 1: Use Field-Standard Methods
If kit not specified → Recommend based on sample type + justify

**Example:**
```json
{
  "extraction_kit": {
    "reported_in_study": "NR: Not Reported",
    "recommended": "DNeasy PowerSoil Kit (Qiagen 12888-100)",
    "justification": "Field standard for soil/sludge; removes humic acids effectively",
    "alternatives": [
      "ZymoBIOMICS DNA Miniprep (Zymo D4300) - no bead-beating bias",
      "FastDNA Spin Kit (MP Bio 116560-200) - faster protocol"
    ]
  }
}
```

### Priority 2: Reference Manufacturer Protocols
If specific parameters not stated → Use manufacturer defaults + cite

**Example:**
"Elution volume not specified; using manufacturer default (100 µL per Qiagen protocol)"

### Priority 3: Cite Established Literature
If method vague → Reference standard papers

**Example:**
"qPCR cycling conditions not detailed; using Yang et al. 2018 protocol for ARG amplification"

### Priority 4: Flag Critical Gaps
If cannot proceed without information → State clearly

**Example:**
```json
{
  "qpcr_primers": {
    "status": "CRITICAL GAP: Primer sequences not provided",
    "cannot_generate_protocol": true,
    "recommendations": [
      "Use primers from Yang et al. 2018 Supplementary Table 3 (30-ARG panel)",
      "Design custom primers from CARD database sequences",
      "Contact study authors for primer information"
    ]
  }
}
```

---

## Step 7: Validation Checklist

Before finalizing protocol, verify:

- [ ] All sample types from Sampling Agent are addressed
- [ ] Method selections are justified (kit choice, media selection, etc.)
- [ ] Kit names include manufacturer + catalog number (or flagged "NR")
- [ ] Biosafety level is appropriate for sample types
- [ ] QC controls specified at each step (extraction blanks, NTC, mock community)
- [ ] Handoff section complete (file formats, metadata files, known issues)
- [ ] Critical gaps flagged with alternatives or recommendations
- [ ] Waste disposal procedures specified
- [ ] Protocol is executable by trained laboratory technician
- [ ] Only includes relevant sections (don't add cultivation to DNA-only studies)

---

## Output Format

Generate **both outputs**:

1. **Complete JSON** (structured protocol as shown in Step 4)
2. **Narrative Summary** (2-3 paragraph human-readable overview as shown in Step 5)

**File names:**
- `wetlab_protocol_[StudyID].json`
- `wetlab_protocol_[StudyID]_summary.md`

---

## Conditional Protocol Inclusion Logic

| If Input Mentions... | Include Section | Don't Include If... |
|----------------------|-----------------|---------------------|
| "DNA", "metagenomics" | DNA extraction + sequencing | Input says "RNA-only" |
| "RNA", "transcriptomics" | RNA extraction (with DNase) | Input says "DNA-only" |
| "Cultivation", "isolation" | Cultivation + media | Input says "culture-independent" |
| "AST", "MIC" | Phenotypic susceptibility testing | No mention of isolates |
| "LC-MS", "antibiotic concentration" | Chemical analysis (SPE + MS) | No mention of chemical quantification |
| "qPCR", "quantification" | qPCR protocol | Input says "sequencing only" |
| "16S amplicon" | 16S library prep | Input says "shotgun only" |
| "Nanopore", "long-read" | Nanopore-specific library prep | Input says "Illumina only" |

**Key Principle:** Protocol should be lean and targeted. Only generate what's needed based on the study design.

---

## Example: Quick Decision Flow

**Input from Sampling Agent:**
- Sample: Wastewater (1 L, high biomass)
- Target: DNA for shotgun metagenomics
- Samples: 80 total
- BSL: BSL-2

**Your Protocol Should Include:**
1. ✅ Sample collection & preservation
2. ✅ Biomass concentration (filtration or centrifugation)
3. ✅ DNA extraction (PowerSoil or PowerWater kit)
4. ✅ DNA quantification & QC
5. ✅ Shotgun metagenomics library prep (Nextera or NEBNext)
6. ✅ Quality controls (blanks, mock community)
7. ✅ Safety (BSL-2 procedures)
8. ✅ Waste disposal
9. ✅ Handoff to Bioinformatics

**Your Protocol Should NOT Include:**
- ❌ RNA extraction (not requested)
- ❌ Cultivation protocols (not requested)
- ❌ Chemical analysis (not requested)
- ❌ 16S amplicon sequencing (shotgun specified)

This keeps the protocol focused and executable.
