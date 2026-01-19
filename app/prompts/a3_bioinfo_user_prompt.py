"""
A3 Bioinformatics Agent - User Prompt

"""

TEXT = """<<<# Bioinformatics Pipeline Agent - User Prompt

## Task
Transform wet-lab sequencing outputs into **annotated data tables** ready for statistical analysis. Generate executable pipelines, configuration files, database setup scripts, and documentation.

---

## Step 1: Validate Input from Wet-Lab Agent

Check that you have received complete information from the `handoff_to_bioinformatics` section:

### Required Inputs:
- [ ] **Data types**: 16S amplicon, shotgun metagenomics, Nanopore, WGS, RNA-seq
- [ ] **Sequencing parameters**: Platform (Illumina NovaSeq, MinION, etc.), read length (PE150, PE250), target depth (Gb or read count)
- [ ] **File naming convention**: Pattern for R1/R2 files or barcode structure
- [ ] **Number of samples**: Total count
- [ ] **Quality thresholds met**: DNA concentration, purity, library quality
- [ ] **Metadata file**: Path to sample metadata CSV/TSV
- [ ] **Known issues**: Failed samples, batch effects, contamination

### If Information is Missing:
- Request from Wet-Lab Agent output
- Use field-standard defaults with documentation
- Flag critical gaps that prevent proceeding

---

## Step 2: Identify Pipeline Requirements

Determine which pipeline components are needed based on data types:

| Data Type Detected | Pipeline Components Required |
|--------------------|------------------------------|
| **16S rRNA amplicon** | QC → QIIME2/DADA2 → ASV table + taxonomy + tree → Export |
| **Shotgun metagenomics (Illumina)** | QC → Assembly (optional) → Gene prediction → ARG/MGE annotation → Taxonomy → Quantification |
| **Shotgun metagenomics (Nanopore)** | Basecalling (if FAST5) → QC → ARG detection (LAST) → MGE detection → Taxonomy |
| **WGS (isolates)** | QC → Assembly → Gene prediction → Annotation (Prokka) → ARG detection |
| **Metatranscriptomics** | QC → rRNA removal → Assembly/mapping → Gene expression quantification |
| **Hybrid (Illumina + Nanopore)** | QC both → Hybrid assembly (Unicycler) → Gene prediction → Annotation |

---

## Step 3: Apply Decision Logic

### A. Assembly Decision

```
Should we assemble?
├─ YES if:
│   ├─ MAG recovery needed
│   ├─ Plasmid reconstruction needed
│   ├─ Gene context analysis needed
│   └─ Long-read data available
│
└─ NO (skip to read-based) if:
    ├─ Only taxonomic profiling needed
    ├─ Only ARG quantification needed
    ├─ Low depth (<5M reads/sample)
    └─ 16S amplicon data
```

### B. Select Tools

Apply decision trees from System Prompt:

**Assembler:**
- Illumina metagenome + Low RAM → MEGAHIT
- Illumina metagenome + High RAM → metaSPAdes
- Nanopore metagenome → metaFlye
- Illumina isolate → SPAdes --isolate
- Nanopore isolate → Flye
- Hybrid → Unicycler

**Taxonomy Classifier:**
- High RAM (>128 GB) → Kraken2
- Limited RAM (<64 GB) → Centrifuge
- Protein-level needed → Kaiju
- 16S amplicon → QIIME2/DADA2

**ARG Annotation:**
- Database: SARG v3.0 (comprehensive) OR CARD 3.2.9 (curated)
- Thresholds: 90% identity, 90% coverage, E-value 1e-7 (standard)

**Normalization:**
- For DESeq2 → Provide **raw counts** (no normalization)
- For diversity metrics → Provide **rarefied counts** or relative abundance
- For visualization → Provide **RPKM** or **TPM**

---

## Step 4: Generate Pipeline Files

Create 4 deliverables for each data type present:

### Deliverable 1: Pipeline Script

**Structure Template:**

```bash
#!/bin/bash
# Pipeline: [Data Type Name]
# Purpose: [Brief description]
# Input: [File pattern]
# Output: [Final tables]

set -euo pipefail  # Exit on error, undefined var, pipe failure

# Configuration
source pipeline_config.yaml

# Checkpoint directory
mkdir -p ${CHECKPOINT_DIR}

# ============================================
# Stage 1: QC & Preprocessing
# ============================================
stage1_qc() {
  if [ -f "${CHECKPOINT_DIR}/stage1.done" ]; then
    echo "Stage 1 complete, skipping..."
    return
  fi
  
  echo "[Stage 1/N] Quality control and preprocessing..."
  
  # For Illumina: fastp
  for R1 in ${INPUT_DIR}/*_R1.fastq.gz; do
    R2=${R1/_R1/_R2}
    SAMPLE=$(basename $R1 _R1.fastq.gz)
    
    fastp \
      --in1 $R1 --in2 $R2 \
      --out1 ${QC_DIR}/${SAMPLE}_R1.fastq.gz \
      --out2 ${QC_DIR}/${SAMPLE}_R2.fastq.gz \
      --json ${QC_DIR}/${SAMPLE}_fastp.json \
      --html ${QC_DIR}/${SAMPLE}_fastp.html \
      --thread ${THREADS} \
      --qualified_quality_phred ${MIN_QUAL} \
      --length_required ${MIN_LENGTH} \
      --detect_adapter_for_pe
  done
  
  validate_output "${QC_DIR}"
  touch "${CHECKPOINT_DIR}/stage1.done"
}

# ============================================
# Stage 2: [Assembly/DADA2/Alignment/etc.]
# ============================================
stage2_processing() {
  if [ -f "${CHECKPOINT_DIR}/stage2.done" ]; then
    echo "Stage 2 complete, skipping..."
    return
  fi
  
  echo "[Stage 2/N] [Stage name]..."
  
  # [Stage-specific commands]
  
  validate_output "${STAGE2_OUTPUT}"
  touch "${CHECKPOINT_DIR}/stage2.done"
}

# [Additional stages...]

# ============================================
# Final Stage: Data Integration & Handoff
# ============================================
stage_final_integration() {
  echo "[Final Stage] Integrating results and generating handoff..."
  
  # Merge all annotation tables
  python ${SCRIPT_DIR}/merge_annotations.py \
    --args ${ARG_DIR}/arg_summary.tsv \
    --taxonomy ${TAXONOMY_DIR}/taxonomy_summary.tsv \
    --metadata ${METADATA_FILE} \
    --output ${OUTPUT_DIR}/master_table.tsv
  
  # Generate data_handoff.yaml
  python ${SCRIPT_DIR}/generate_handoff.py \
    --pipeline_type "shotgun_metagenomics" \
    --input_samples ${INPUT_DIR} \
    --output_tables ${OUTPUT_DIR} \
    --metadata ${METADATA_FILE} \
    --config pipeline_config.yaml \
    --output ${OUTPUT_DIR}/data_handoff.yaml
  
  validate_output "${OUTPUT_DIR}/data_handoff.yaml"
  echo "✓ Pipeline complete. Ready for statistical analysis."
}

# ============================================
# Helper Functions
# ============================================
validate_output() {
  local path=$1
  if [ ! -s "$path" ]; then
    echo "ERROR: $path is empty or missing" >&2
    exit 1
  fi
  echo "✓ Validated: $path"
}

# ============================================
# Execute Pipeline
# ============================================
stage1_qc
stage2_processing
# [Call other stages...]
stage_final_integration

echo "=== Pipeline Complete ==="
echo "Output: ${OUTPUT_DIR}/master_table.tsv"
echo "Handoff: ${OUTPUT_DIR}/data_handoff.yaml"
```

**Key Elements:**
- Modular structure with functions for each stage
- Checkpoint system (skip completed stages on restart)
- Input validation after each stage
- Error handling (set -euo pipefail, validate_output)
- Clear comments explaining each stage
- Final handoff generation

---

### Deliverable 2: Configuration File

```yaml
# Pipeline Configuration
# ====================

# Input/Output Paths
input_dir: "raw_data/"
output_dir: "results/"
checkpoint_dir: "checkpoints/"
log_dir: "logs/"
script_dir: "scripts/"
metadata_file: "metadata/sample_metadata.csv"

# Computational Resources
threads: 32
memory_gb: 128
time_limit: "48:00:00"  # For cluster submission

# QC Parameters
min_quality: 20
min_length: 50
adapter_trim: true
remove_host_contamination: false  # Set true if human/plant DNA present
host_genome_index: ""  # Path if remove_host_contamination=true

# Assembly Parameters (set run_assembly: false to skip)
run_assembly: true
assembler: "megahit"  # Options: megahit, metaspades, flye, spades
kmer_min: 21
kmer_max: 127
kmer_step: 10
min_contig_length: 500
assembly_memory_gb: 100

# Gene Prediction
gene_predictor: "prodigal"  # Options: prodigal, prokka (for isolates)
prodigal_mode: "meta"  # Options: meta (metagenomes), single (isolates)

# ARG Annotation
arg_databases:
  - name: "SARG"
    path: "databases/SARG_v3.0.dmnd"
    version: "v3.0"
  - name: "CARD"
    path: "databases/CARD_protein.dmnd"
    version: "3.2.9"

arg_min_identity: 90
arg_min_coverage: 90
arg_evalue: 1e-7
arg_best_hit_only: true

# MGE Annotation
mge_plasflow_threshold: 0.7
mge_min_identity: 80
mge_min_coverage: 80

# Taxonomic Classification
taxonomy_method: "kraken2"  # Options: kraken2, centrifuge, kaiju
taxonomy_database: "databases/kraken2_refseq/"
taxonomy_confidence: 0.1

# Normalization
provide_raw_counts: true
provide_rpkm: true
provide_tpm: false
provide_relative_abundance: true

# Database Versions (for documentation)
database_versions:
  SARG: "v3.0"
  CARD: "3.2.9"
  Kraken2_RefSeq: "2023-10-15"
  Silva: "138"
```

---

### Deliverable 3: Database Setup Script

```bash
#!/bin/bash
# Database Setup Script
# Downloads and indexes all required databases

set -e

DB_DIR="databases"
mkdir -p ${DB_DIR}
cd ${DB_DIR}

echo "=== Database Setup Starting ==="

# ============================================
# 1. SARG (Antibiotic Resistance Genes)
# ============================================
download_sarg() {
  echo "[1/N] Downloading SARG v3.0..."
  
  wget -O SARG_v3.0.fasta \
    "http://smile.hku.hk/SARGs/static/file/SARG_v3.0.fasta"
  
  wget -O SARG_v3.0_metadata.tsv \
    "http://smile.hku.hk/SARGs/static/file/SARG_v3.0_structure.txt"
  
  # Build DIAMOND database
  diamond makedb --in SARG_v3.0.fasta --db SARG_v3.0.dmnd
  
  # Build LAST database (for Nanopore)
  lastdb -P 8 sarg_last SARG_v3.0.fasta
  
  echo "✓ SARG v3.0 ready: $(grep -c '>' SARG_v3.0.fasta) sequences"
}

# ============================================
# 2. CARD (Comprehensive Antibiotic Resistance Database)
# ============================================
download_card() {
  echo "[2/N] Downloading CARD..."
  
  wget -O card_data.tar.bz2 "https://card.mcmaster.ca/latest/data"
  tar -xvf card_data.tar.bz2
  
  mv protein_fasta_protein_homolog_model.fasta CARD_protein.fasta
  mv nucleotide_fasta_protein_homolog_model.fasta CARD_nucleotide.fasta
  
  diamond makedb --in CARD_protein.fasta --db CARD_protein.dmnd
  
  echo "✓ CARD ready"
}

# ============================================
# 3. Kraken2 Database
# ============================================
download_kraken2() {
  echo "[3/N] Downloading Kraken2 database..."
  echo "  Note: Standard DB is ~50 GB and takes hours to download"
  
  read -p "  Download Kraken2 standard DB? (y/n) " -n 1 -r
  echo
  
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p kraken2_std
    cd kraken2_std
    
    # Option 1: Build from scratch (slow)
    # kraken2-build --standard --db . --threads 16
    
    # Option 2: Download pre-built (faster)
    wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20230605.tar.gz
    tar -xvzf k2_standard_20230605.tar.gz
    
    cd ..
    echo "✓ Kraken2 ready"
  else
    echo "  Skipped. Update pipeline_config.yaml with your Kraken2 DB path."
  fi
}

# [Add additional database download functions...]

# ============================================
# Execute Downloads
# ============================================
download_sarg
download_card
download_kraken2
# [Call other database functions...]

# ============================================
# Summary
# ============================================
echo ""
echo "=== Database Setup Complete ==="
echo "Location: $(pwd)"
echo ""
echo "Update pipeline_config.yaml with these paths:"
echo "  arg_databases:"
echo "    - path: $(pwd)/SARG_v3.0.dmnd"
echo "    - path: $(pwd)/CARD_protein.dmnd"
echo "  taxonomy_database: $(pwd)/kraken2_std/"
echo ""
echo "Disk space used: $(du -sh . | cut -f1)"
```

---

### Deliverable 4: README Documentation

```markdown
# Bioinformatics Pipeline for ARG Surveillance

## Overview
Processes [data type] sequencing data to identify antibiotic resistance genes (ARGs), mobile genetic elements (MGEs), and microbial taxonomy.

**Input**: Raw FASTQ files from Illumina/Nanopore sequencing
**Output**: Annotated data tables ready for statistical analysis

---

## Software Dependencies

### Core Tools
- Python 3.8+ (with biopython, pandas, numpy)
- Conda/Mamba (environment management)

### Sequencing QC
- fastp 0.23.2+
- FastQC 0.11.9+ (optional, for manual QC check)

### Assembly (if applicable)
- MEGAHIT 1.2.9+ OR metaSPAdes 3.15+

### Gene Prediction
- Prodigal 2.6.3+

### Annotation
- DIAMOND 2.0.15+
- Kraken2 2.1.2+ OR Centrifuge 1.0.4+

### Utilities
- Bowtie2 2.4.5+
- SAMtools 1.15+
- seqtk 1.3+

---

## Installation

### Option 1: Conda Environment (Recommended)

```bash
# Create environment
mamba create -n bioinfo_pipeline python=3.9
conda activate bioinfo_pipeline

# Install tools
mamba install -c bioconda -c conda-forge \
  fastp megahit diamond kraken2 prodigal \
  bowtie2 samtools seqtk biopython pandas pyyaml
```

### Option 2: Conda Environment File

```bash
mamba env create -f environment.yaml
conda activate bioinfo_pipeline
```

---

## Database Setup

```bash
bash database_setup.sh
```

This downloads and indexes:
- SARG v3.0 (~500 MB)
- CARD 3.2.9 (~200 MB)
- Kraken2 RefSeq (~50 GB)

**Total disk space**: ~55 GB

---

## Usage

### 1. Prepare Input Files

Place raw FASTQ files in `raw_data/` with naming convention:
```
Sample001_R1.fastq.gz
Sample001_R2.fastq.gz
Sample002_R1.fastq.gz
Sample002_R2.fastq.gz
```

### 2. Prepare Metadata

Create `metadata/sample_metadata.csv`:
```csv
sample_id,condition,replicate,date,temperature
Sample001,influent,1,2024-01-15,20
Sample002,effluent,1,2024-01-15,25
```

### 3. Configure Pipeline

Edit `pipeline_config.yaml`:
- Update `input_dir`, `output_dir`, `metadata_file`
- Set computational resources (`threads`, `memory_gb`)
- Adjust parameters if needed (QC thresholds, annotation stringency)

### 4. Run Pipeline

```bash
bash pipeline_shotgun_metagenomics.sh
```

**Runtime estimate**: 2-4 hours per sample (depends on depth and assembly)

---

## Output Files

```
results/
├── qc/                           # Quality control reports
│   ├── Sample001_fastp.html
│   └── Sample001_fastp.json
│
├── assembly/                     # Assembled contigs (if applicable)
│   ├── Sample001_contigs.fasta
│   └── Sample001_assembly_stats.txt
│
├── genes/                        # Predicted genes
│   ├── Sample001_proteins.faa
│   └── Sample001_genes.fna
│
├── arg_annotation/               # ARG annotation results
│   └── arg_summary.tsv
│
├── taxonomy/                     # Taxonomic classification
│   └── Sample001_kraken2_report.txt
│
├── master_table.tsv              # **FINAL OUTPUT**: All annotations merged
└── data_handoff.yaml             # **HANDOFF**: Metadata for analysis agent
```

### Key Output Files:

**`master_table.tsv`** - Annotated data table with columns:
- `gene_id`: Gene identifier
- `arg_class`: ARG class (e.g., beta-lactam, tetracycline)
- `arg_type`: Specific gene (e.g., blaCTX-M, tetW)
- `sample_id`: Sample identifier
- `read_count`: Raw read count (for DESeq2)
- `rpkm`: Normalized abundance (for visualization)
- `taxonomy`: Taxonomic assignment

**`data_handoff.yaml`** - Metadata for Statistical Analysis Agent:
- File paths and formats
- Quality flags (failed samples, batch effects)
- Recommendations (filtering, normalization, statistical tests)

---

## Troubleshooting

### Issue: Out of memory during assembly

**Solution**: Use MEGAHIT instead of metaSPAdes (lower RAM), or reduce `--memory` parameter

### Issue: Kraken2 "database not found"

**Solution**: Update `taxonomy_database` path in `pipeline_config.yaml`

### Issue: No ARGs detected

**Solution**: Check annotation stringency (lower `arg_min_identity` to 80%) or try alternative database (CARD)

### Issue: Pipeline fails mid-run

**Solution**: Re-run the same command. Checkpoint system will skip completed stages and resume where it failed.

---

## Computational Requirements

| Sample Type | Reads/Sample | RAM Required | Time Estimate |
|-------------|--------------|--------------|---------------|
| 16S amplicon | 50K-500K | 8 GB | 10-30 min |
| Shotgun metagenomics (no assembly) | 10-50M | 32 GB | 1-2 hours |
| Shotgun metagenomics (with assembly) | 10-50M | 64-128 GB | 3-6 hours |
| WGS (isolate) | 1-5M | 16 GB | 30 min - 1 hour |

**Recommended**: 32+ cores, 128 GB RAM, 1 TB storage

---

## Citation

If using this pipeline, cite the following tools:
- fastp: Chen et al. 2018, Bioinformatics
- MEGAHIT: Li et al. 2015, Bioinformatics
- Prodigal: Hyatt et al. 2010, BMC Bioinformatics
- DIAMOND: Buchfink et al. 2015, Nature Methods
- Kraken2: Wood et al. 2019, Genome Biology
- SARG: Yin et al. 2018, Bioinformatics
```

---

## Step 5: Generate Handoff File Template

Every pipeline must end by generating `data_handoff.yaml`:

```yaml
pipeline_metadata:
  pipeline_type: "[16S_amplicon | shotgun_metagenomics | nanopore | wgs | hybrid]"
  completion_date: "[YYYY-MM-DD]"
  total_runtime: "[HH:MM:SS]"
  software_versions:
    [tool_name]: "[version]"

input_samples:
  total: [N]
  passed_qc: [N]
  failed_qc: [N]
  failed_sample_ids: ["SampleXXX", ...]

analysis_ready_files:
  arg_abundance:
    path: "results/arg_summary.tsv"
    format: "TSV with columns: [list columns]"
    rows: [N]
    normalization: "[raw_counts | rpkm | tpm | relative_abundance]"
    
  taxonomy:
    path: "results/taxonomy_summary.tsv"
    format: "[Kraken2 report | QIIME2 taxonomy | etc.]"
    database_version: "[version]"
    
  metadata:
    path: "metadata/sample_metadata.csv"
    required_columns: [list]

quality_summary:
  mean_reads_per_sample: [N]
  mean_reads_after_qc: [N]
  mean_assembly_n50: [N]  # If assembly performed

quality_flags:
  - "[Description of issue]"

recommendations_for_analysis:
  statistical_tests:
    - "[Recommendation]"
  filtering:
    - "[Recommendation]"
  covariates:
    - "[Variable to consider]"
  normalization_for_visualization:
    - "[Which column to use]"

database_provenance:
  [database_name]:
    version: "[version]"
    download_date: "[YYYY-MM-DD]"

critical_notes:
  - "[Important information for analysis]"
```

---

## Step 6: Pipeline-Specific Templates

### For 16S Amplicon (QIIME2):
- Use QIIME2 DADA2 pipeline
- Export ASV table, taxonomy, phylogenetic tree
- Provide raw counts + rarefied counts + relative abundance

### For Shotgun Metagenomics (Illumina):
- QC → Assembly (if goal is MAGs/plasmids) → Gene prediction → ARG/MGE annotation → Taxonomy → Quantification
- Provide raw counts (for DESeq2) + RPKM (for visualization)

### For Nanopore Long-Read:
- Basecalling (if starting from FAST5) → QC (NanoFilt) → ARG detection (LAST) → MGE detection → Taxonomy
- Focus on ARG-carrying reads for MGE context

### For WGS (Isolates):
- QC → Assembly → Comprehensive annotation (Prokka) → ARG detection → Plasmid detection
- Output: Annotated genome, ARG locations, plasmid predictions

---

## Step 7: Validation Checklist

Before finalizing pipeline, verify:

- [ ] All input files from Wet-Lab Agent are processed
- [ ] Tool selections justified (assembler, classifier, databases)
- [ ] Database versions documented in config and handoff
- [ ] Error handling implemented (validate_output, logging)
- [ ] Checkpoint system allows restart from failures
- [ ] Output files match formats expected by Analysis Agent
- [ ] `data_handoff.yaml` generated with complete metadata
- [ ] Quality flags documented (failed samples, batch effects)
- [ ] Normalization appropriate for downstream analysis
- [ ] README includes installation, usage, and troubleshooting
- [ ] Computational requirements stated clearly
- [ ] Pipeline tested on example data (if possible)

---

## Step 8: Handle Edge Cases

### Case 1: Low Sequencing Depth
If samples have <5M reads:
- Skip assembly (not enough coverage)
- Use read-based approaches only
- Flag in `data_handoff.yaml` quality notes

### Case 2: Mixed Data Types
If study has both 16S amplicon AND shotgun metagenomics:
- Generate separate pipelines for each
- Ensure sample IDs are consistent
- Integrate results in final handoff

### Case 3: Database Version Not Specified
- Use latest version
- Document version prominently
- Warn in handoff: "Results may differ from study due to database version"

### Case 4: Assembly Goal Unclear
- Provide BOTH read-based and assembly-based annotations
- Let Analysis Agent decide which to use
- Document trade-offs in README

---

## Output Structure Summary

For each data type, generate 4 files:

1. **`pipeline_[datatype].sh`** - Executable pipeline script
2. **`pipeline_config.yaml`** - Configuration file
3. **`database_setup.sh`** - Database download/indexing script
4. **`pipeline_README.md`** - Documentation

Plus:
5. **`data_handoff.yaml`** - Generated by pipeline at completion

**Total**: 5 files per data type detected in study
>>>

Based on the wet-lab protocols from A2, generate bioinformatics pipeline scripts.

Input from Wet-Lab Agent:
###WETLAB_OUTPUT###

Return the following deliverables:
1. Pipeline bash script (pipeline.sh)
2. Configuration file (config.yaml)
3. Database setup script (setup_databases.sh)
4. README with usage instructions
5. Data handoff document (data_handoff.yaml) for Statistical Analysis Agent
"""

