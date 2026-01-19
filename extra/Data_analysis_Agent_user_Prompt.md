Statistical Analysis & Visualization Agent - User_prompt
Generate complete statistical analysis workflows from processed bioinformatics data. Transform annotated tables into statistical results and publication-quality figures.
Extract from Study
1. Available Data (from bioinformatics pipeline outputs):

 ARG abundance table (arg_summary.tsv)
 Taxonomy table (feature-table.tsv or taxonomy_summary.tsv)
 MGE annotations (mge_summary.tsv)
 Sample metadata (metadata.tsv)
 Antibiotic concentrations (LC-MS)
 qPCR data
 Phylogenetic tree (for UniFrac)

2. Study Design:

Grouping variable (e.g., TreatmentStage: Influent, Activated Sludge, Effluent)
Sample sizes per group (critical for test selection)
Paired or unpaired comparisons
Research questions/hypotheses

3. Analyses Performed in Study:
Extract which statistical tests and visualizations were used:

Diversity metrics (alpha: richness/Shannon, beta: PERMANOVA/ordination)
Group comparisons (t-tests, ANOVA, Kruskal-Wallis)
Differential abundance (DESeq2, ANCOM, LEfSe)
Correlations (ARGs vs environment/antibiotics)
Networks (co-occurrence)
Visualizations (boxplots, heatmaps, ordinations, volcano plots)

Generate Complete R Script
Create analysis_script.R (or .Rmd) with these sections:
SECTION 1: Setup
set.seed(12345)
library(tidyverse); library(vegan); library(phyloseq); library(DESeq2)
library(ggplot2); library(pheatmap); library(corrplot); library(ggpubr)

# Import data
args <- read_tsv("results/bioinformatics/arg_summary.tsv")
metadata <- read_csv("metadata/sample_metadata.tsv")
# [other data as needed]
set.seed(12345)
library(tidyverse); library(vegan); library(phyloseq); library(DESeq2)
library(ggplot2); library(pheatmap); library(corrplot); library(ggpubr)

# Import data
args <- read_tsv("results/bioinformatics/arg_summary.tsv")
metadata <- read_csv("metadata/sample_metadata.tsv")
# [other data as needed]
Condensed Decision Trees
Test Selection:
Is data normal (Shapiro P>0.05)?
├─ YES → Parametric (t-test, ANOVA)
└─ NO  → Non-parametric (Wilcoxon, Kruskal-Wallis)

How many groups?
├─ 2 groups → t-test or Wilcoxon
├─ 3+ groups → ANOVA/Kruskal + post-hoc
└─ Multivariate → PERMANOVA

Differential Abundance:
Data type?
├─ Sequencing counts → DESeq2 (normalized counts)
├─ Relative abundance → ANCOM (compositional)
└─ Biomarker discovery → LEfSe (LDA scores)

Significance criteria:
├─ Statistical: padj < 0.05 (FDR-corrected)
└─ Biological: |log2FoldChange| > 1 (2-fold)

Visualization:
Analysis type → Figure type
├─ Alpha diversity → Boxplot with stats
├─ Beta diversity → PCoA/NMDS ordination
├─ Differential abundance → Volcano plot + heatmap
├─ Correlations → Scatter plot + matrix heatmap
├─ Network → Force-directed graph
└─ Composition → Stacked barplot

Critical Implementation Notes
Always include:

Data validation: Check sample sizes, missing values, outliers
Assumption checking: Normality (Shapiro-Wilk), equal variance (Levene), dispersion (betadisper)
Multiple testing correction: FDR for all tests involving multiple comparisons
Effect sizes: Not just P-values
Post-hoc tests: If ANOVA/Kruskal significant, specify which pairs differ
Figure annotations: Sample sizes, test statistics, P-values directly on plots
Session info: sessionInfo() saved to file

Never:

Use parametric tests without checking normality
Report P-values without multiple testing correction (when testing multiple hypotheses)
Make volcano plots without fold-change threshold (|LFC|>1)
Create networks without filtering low-prevalence features
Use Pearson correlation on relative abundance (compositional data)
Claim causation from correlation
Report "P=0.000" (use "P<0.001")

Output Structure:
results/
├── tables/
│   ├── arg_prevalence_by_type.csv
│   ├── arg_diversity_metrics.csv
│   ├── deseq2_results.csv
│   ├── permanova_pairwise.csv
│   └── correlations.csv
├── figures/
│   ├── alpha_diversity_boxplots.pdf
│   ├── pcoa_ordination.pdf
│   ├── volcano_plot.pdf
│   ├── heatmap_top_args.pdf
│   └── network_cooccurrence.pdf
└── session_info.txt

This compressed prompt focuses on what to extract, what to generate, and key decision points, removing verbose explanations while retaining all essential technical details.RetryClaude can make mistakes. Please double-check responses.