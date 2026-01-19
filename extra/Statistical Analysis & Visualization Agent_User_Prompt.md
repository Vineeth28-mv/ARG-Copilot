# Statistical Analysis & Visualization Agent - User Prompt

## Task
Transform processed bioinformatics data into **statistical results, publication-quality figures, and interpretable findings**. Generate complete R scripts or R Markdown notebooks with analysis workflows.

---

## Step 1: Validate Input from Bioinformatics Agent

Check that you have received complete information from the `data_handoff.yaml`:

### Required Inputs:
- [ ] **Data file paths**: ARG abundance table, taxonomy table, MGE annotations
- [ ] **Column specifications**: Column names and what they contain
- [ ] **Normalization info**: raw_counts, rpkm, tpm, relative_abundance
- [ ] **Sample information**: Total samples, failed samples, sample IDs
- [ ] **Metadata file**: Path with grouping variables
- [ ] **Quality flags**: Batch effects, low-coverage samples, outliers
- [ ] **Recommendations**: Which tests to use, which columns for what analysis

### Validation Steps:

```r
# Load data_handoff.yaml
library(yaml)
handoff <- read_yaml("results/data_handoff.yaml")

# Verify files exist
stopifnot(file.exists(handoff$analysis_ready_files$arg_abundance$path))
stopifnot(file.exists(handoff$analysis_ready_files$metadata$path))

# Load data
args <- read_tsv(handoff$analysis_ready_files$arg_abundance$path)
metadata <- read_csv(handoff$analysis_ready_files$metadata$path)

# Verify sample IDs match
stopifnot(all(unique(args$sample_id) %in% metadata$sample_id))
message("✓ All samples in data match metadata")

# Check for failed samples (exclude from analysis)
failed_samples <- handoff$input_samples$failed_sample_ids
if (length(failed_samples) > 0) {
  message(paste("Excluding", length(failed_samples), "failed samples"))
  args <- args %>% filter(!sample_id %in% failed_samples)
  metadata <- metadata %>% filter(!sample_id %in% failed_samples)
}
```

---

## Step 2: Identify Required Analyses

Based on study design and research questions, determine which analyses are needed:

| Analysis Type | When to Use |
|---------------|-------------|
| **Descriptive Statistics** | Always (summary tables, prevalence) |
| **Alpha Diversity** | If comparing richness/evenness between groups |
| **Beta Diversity + PERMANOVA** | If comparing community composition between groups |
| **Differential Abundance** | If identifying ARGs/taxa that differ between groups |
| **Correlations** | If exploring ARG relationships with environmental variables |
| **Networks** | If investigating co-occurrence patterns |
| **Time Series** | If temporal data (multiple timepoints) |

---

## Step 3: Generate Analysis Workflow

Create an R Markdown file with these sections:

### Section Template:

```r
---
title: "ARG Surveillance Analysis"
author: "Statistical Analysis Agent"
date: "`r Sys.Date()`"
output:
  html_document:
    toc: true
    toc_float: true
    code_folding: show
    theme: flatly
---

# Setup

## Load Packages

```{r setup, message=FALSE, warning=FALSE}
# Set random seed for reproducibility
set.seed(12345)

# Core packages
library(tidyverse)    # Data manipulation and visualization
library(vegan)        # Diversity analysis
library(phyloseq)     # Microbiome data management
library(DESeq2)       # Differential abundance
library(ggplot2)      # Visualization
library(pheatmap)     # Heatmaps
library(corrplot)     # Correlation plots
library(ggpubr)       # Publication-ready plots
library(car)          # Levene's test
library(yaml)         # Read handoff file

# Set theme
theme_set(theme_bw())
```

## Load Data

```{r load-data}
# Load handoff metadata
handoff <- read_yaml("results/data_handoff.yaml")

# Load ARG abundance data
args <- read_tsv(handoff$analysis_ready_files$arg_abundance$path)

# Load sample metadata
metadata <- read_csv(handoff$analysis_ready_files$metadata$path)

# Exclude failed samples
failed_samples <- handoff$input_samples$failed_sample_ids
if (length(failed_samples) > 0) {
  args <- args %>% filter(!sample_id %in% failed_samples)
  metadata <- metadata %>% filter(!sample_id %in% failed_samples)
}

# Display data structure
glimpse(args)
glimpse(metadata)
```

## Data Validation

```{r validate}
# Check sample IDs match
stopifnot(all(unique(args$sample_id) %in% metadata$sample_id))

# Check for missing values
missing_summary <- args %>%
  summarize(across(everything(), ~sum(is.na(.))))
print(missing_summary)

# Check grouping variable
grouping_var <- "condition"  # Adjust based on study
table(metadata[[grouping_var]])
```

---

# Exploratory Data Analysis

## Summary Statistics

```{r summary-stats}
# ARG prevalence by class
prevalence_summary <- args %>%
  group_by(arg_class) %>%
  summarize(
    n_genes = n_distinct(gene_id),
    n_samples_detected = sum(read_count > 0),
    prevalence_pct = (n_samples_detected / n_distinct(args$sample_id)) * 100,
    median_rpkm = median(rpkm[rpkm > 0]),
    iqr_rpkm = IQR(rpkm[rpkm > 0])
  ) %>%
  arrange(desc(prevalence_pct))

write_csv(prevalence_summary, "analysis_results/tables/arg_prevalence_by_class.csv")
knitr::kable(prevalence_summary, digits = 2, caption = "ARG Prevalence by Class")
```

## Distribution Checks

```{r distributions, fig.width=10, fig.height=6}
# Check data distribution (for test selection)
# Example: Total ARG abundance per sample

total_arg_per_sample <- args %>%
  group_by(sample_id) %>%
  summarize(total_rpkm = sum(rpkm)) %>%
  left_join(metadata, by = "sample_id")

# Histogram
p1 <- ggplot(total_arg_per_sample, aes(x = total_rpkm)) +
  geom_histogram(bins = 30, fill = "steelblue", color = "black") +
  labs(title = "Distribution of Total ARG Abundance",
       x = "Total RPKM", y = "Count")

# Q-Q plot
p2 <- ggplot(total_arg_per_sample, aes(sample = total_rpkm)) +
  stat_qq() +
  stat_qq_line(color = "red") +
  labs(title = "Q-Q Plot")

gridExtra::grid.arrange(p1, p2, ncol = 2)

# Shapiro-Wilk test
shapiro_result <- shapiro.test(total_arg_per_sample$total_rpkm)
cat("Shapiro-Wilk test: W =", shapiro_result$statistic, ", P =", shapiro_result$p.value, "\n")

if (shapiro_result$p.value < 0.05) {
  cat("Data are non-normal → Use non-parametric tests\n")
} else {
  cat("Data are normal → Parametric tests appropriate\n")
}
```

---

# Alpha Diversity Analysis

## Calculate Diversity Metrics

```{r alpha-diversity}
# Reshape to wide format (samples × genes)
arg_matrix <- args %>%
  select(sample_id, gene_id, read_count) %>%
  pivot_wider(names_from = gene_id, values_from = read_count, values_fill = 0) %>%
  column_to_rownames("sample_id") %>%
  as.matrix()

# Calculate diversity metrics
alpha_div <- data.frame(
  sample_id = rownames(arg_matrix),
  richness = apply(arg_matrix > 0, 1, sum),  # Number of ARGs detected
  shannon = vegan::diversity(arg_matrix, index = "shannon"),
  simpson = vegan::diversity(arg_matrix, index = "simpson")
) %>%
  left_join(metadata, by = "sample_id")

# Save results
write_csv(alpha_div, "analysis_results/tables/alpha_diversity_metrics.csv")

# Summary by group
alpha_summary <- alpha_div %>%
  group_by(!!sym(grouping_var)) %>%
  summarize(
    n = n(),
    richness_median = median(richness),
    richness_iqr = IQR(richness),
    shannon_median = median(shannon),
    shannon_iqr = IQR(shannon)
  )

knitr::kable(alpha_summary, digits = 2, caption = "Alpha Diversity by Group")
```

## Statistical Test

```{r alpha-stats}
# Check assumptions
assumptions <- check_parametric_assumptions(
  data = alpha_div,
  group_var = grouping_var,
  value_var = "shannon"
)

# Run appropriate test
if (assumptions$test_type == "parametric") {
  if (length(unique(alpha_div[[grouping_var]])) == 2) {
    # Two groups: t-test
    if (assumptions$use_welch) {
      test_result <- t.test(shannon ~ get(grouping_var), data = alpha_div, var.equal = FALSE)
    } else {
      test_result <- t.test(shannon ~ get(grouping_var), data = alpha_div, var.equal = TRUE)
    }
    effect <- effsize::cohen.d(shannon ~ get(grouping_var), data = alpha_div)
  } else {
    # Three+ groups: ANOVA
    test_result <- aov(shannon ~ get(grouping_var), data = alpha_div)
    effect <- effectsize::eta_squared(test_result)
  }
} else {
  if (length(unique(alpha_div[[grouping_var]])) == 2) {
    # Two groups: Wilcoxon
    test_result <- wilcox.test(shannon ~ get(grouping_var), data = alpha_div)
    effect <- effsize::cliff.delta(shannon ~ get(grouping_var), data = alpha_div)
  } else {
    # Three+ groups: Kruskal-Wallis
    test_result <- kruskal.test(shannon ~ get(grouping_var), data = alpha_div)
    # Post-hoc Dunn's test
    posthoc <- FSA::dunnTest(shannon ~ get(grouping_var), data = alpha_div, method = "bh")
  }
}

# Print results
print(test_result)
print(effect)
```

## Visualization

```{r alpha-plot, fig.width=7, fig.height=5}
# Boxplot with statistics
p_alpha <- ggplot(alpha_div, aes(x = get(grouping_var), y = shannon, fill = get(grouping_var))) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width = 0.2, alpha = 0.5, size = 2) +
  stat_compare_means(method = ifelse(assumptions$test_type == "parametric", "t.test", "wilcox.test"),
                     label = "p.format") +
  labs(
    title = "ARG Shannon Diversity by Group",
    x = grouping_var,
    y = "Shannon Index",
    fill = grouping_var
  ) +
  scale_fill_brewer(palette = "Set2") +
  theme_bw() +
  theme(legend.position = "none")

print(p_alpha)

# Save figure
ggsave("analysis_results/figures/alpha_diversity_boxplot.pdf", p_alpha, width = 7, height = 5)
ggsave("analysis_results/figures/alpha_diversity_boxplot.png", p_alpha, width = 7, height = 5, dpi = 300)
```

---

# Beta Diversity Analysis

## Calculate Distance Matrix

```{r beta-diversity}
# Calculate Bray-Curtis dissimilarity
dist_matrix <- vegan::vegdist(arg_matrix, method = "bray")

# Check PERMANOVA assumptions
disp_check <- check_permanova_assumptions(
  dist_matrix = dist_matrix,
  metadata = alpha_div,
  group_var = grouping_var
)
```

## PERMANOVA

```{r permanova}
# Run PERMANOVA
permanova_result <- vegan::adonis2(
  dist_matrix ~ get(grouping_var),
  data = alpha_div,
  permutations = 999,
  method = "bray"
)

print(permanova_result)

# Save results
write.csv(permanova_result, "analysis_results/tables/permanova_results.csv")

# Pairwise PERMANOVA (if >2 groups)
if (length(unique(alpha_div[[grouping_var]])) > 2) {
  pairwise_results <- pairwise.adonis2(
    dist_matrix ~ get(grouping_var),
    data = alpha_div
  )
  write.csv(pairwise_results, "analysis_results/tables/permanova_pairwise.csv")
}
```

## Ordination (PCoA)

```{r pcoa, fig.width=8, fig.height=6}
# Principal Coordinates Analysis
pcoa <- ape::pcoa(dist_matrix)

# Extract axes
pcoa_df <- pcoa$vectors[, 1:2] %>%
  as.data.frame() %>%
  rownames_to_column("sample_id") %>%
  left_join(metadata, by = "sample_id")

# Calculate variance explained
var_explained <- round(pcoa$values$Relative_eig[1:2] * 100, 1)

# Plot
p_pcoa <- ggplot(pcoa_df, aes(x = Axis.1, y = Axis.2, color = get(grouping_var))) +
  geom_point(size = 3, alpha = 0.7) +
  stat_ellipse(level = 0.95, linetype = 2) +
  labs(
    title = "PCoA of ARG Composition (Bray-Curtis)",
    x = paste0("PCoA1 (", var_explained[1], "%)"),
    y = paste0("PCoA2 (", var_explained[2], "%)"),
    color = grouping_var
  ) +
  scale_color_brewer(palette = "Set1") +
  theme_bw()

print(p_pcoa)

# Save figure
ggsave("analysis_results/figures/pcoa_ordination.pdf", p_pcoa, width = 8, height = 6)
ggsave("analysis_results/figures/pcoa_ordination.png", p_pcoa, width = 8, height = 6, dpi = 300)
```

---

# Differential Abundance (DESeq2)

## Prepare Data

```{r deseq2-prep}
# Use raw counts (not normalized)
count_matrix <- args %>%
  select(sample_id, gene_id, read_count) %>%
  pivot_wider(names_from = sample_id, values_from = read_count, values_fill = 0) %>%
  column_to_rownames("gene_id") %>%
  as.matrix()

# Ensure metadata order matches count matrix columns
metadata_ordered <- metadata %>%
  filter(sample_id %in% colnames(count_matrix)) %>%
  arrange(match(sample_id, colnames(count_matrix)))

stopifnot(all(colnames(count_matrix) == metadata_ordered$sample_id))
```

## Run DESeq2

```{r deseq2-analysis}
# Create DESeq2 object
dds <- DESeqDataSetFromMatrix(
  countData = count_matrix,
  colData = metadata_ordered,
  design = as.formula(paste0("~", grouping_var))
)

# Filter low-count genes (optional but recommended)
keep <- rowSums(counts(dds) >= 10) >= 3  # At least 10 reads in 3+ samples
dds <- dds[keep, ]

# Run DESeq2
dds <- DESeq(dds)

# Get results (adjust contrast as needed)
groups <- unique(metadata_ordered[[grouping_var]])
res <- results(dds, contrast = c(grouping_var, groups[2], groups[1]))
res <- as.data.frame(res) %>%
  rownames_to_column("gene_id") %>%
  arrange(padj)

# Add ARG annotations
res <- res %>%
  left_join(args %>% select(gene_id, arg_class, arg_type) %>% distinct(), by = "gene_id")

# Save results
write_csv(res, "analysis_results/tables/deseq2_results.csv")

# Filter significant
sig_genes <- res %>%
  filter(padj < 0.05, abs(log2FoldChange) > 1)

cat("Significant ARGs (padj < 0.05, |log2FC| > 1):", nrow(sig_genes), "\n")
```

## Visualization

```{r deseq2-viz, fig.width=8, fig.height=6}
# Volcano plot
p_volcano <- ggplot(res, aes(x = log2FoldChange, y = -log10(padj))) +
  geom_point(aes(color = padj < 0.05 & abs(log2FoldChange) > 1), alpha = 0.6, size = 2) +
  scale_color_manual(
    values = c("grey70", "red"),
    labels = c("Not significant", "Significant"),
    name = ""
  ) +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed", color = "blue") +
  geom_vline(xintercept = c(-1, 1), linetype = "dashed", color = "blue") +
  labs(
    title = "Differential ARG Abundance",
    x = "log₂ Fold Change",
    y = "-log₁₀ Adjusted P-value"
  ) +
  theme_bw()

print(p_volcano)

ggsave("analysis_results/figures/volcano_plot.pdf", p_volcano, width = 8, height = 6)
ggsave("analysis_results/figures/volcano_plot.png", p_volcano, width = 8, height = 6, dpi = 300)

# Heatmap of top 20 significant ARGs
if (nrow(sig_genes) >= 20) {
  top_genes <- sig_genes %>% slice_head(n = 20) %>% pull(gene_id)
} else {
  top_genes <- sig_genes %>% pull(gene_id)
}

if (length(top_genes) > 0) {
  # Get normalized counts
  norm_counts <- counts(dds, normalized = TRUE)[top_genes, , drop = FALSE]
  
  # Log transform for visualization
  log_counts <- log2(norm_counts + 1)
  
  # Prepare annotation
  annot_col <- metadata_ordered %>%
    select(!!sym(grouping_var)) %>%
    as.data.frame()
  rownames(annot_col) <- metadata_ordered$sample_id
  
  # Heatmap
  pheatmap(
    log_counts,
    annotation_col = annot_col,
    scale = "row",
    clustering_distance_rows = "euclidean",
    clustering_distance_cols = "euclidean",
    color = colorRampPalette(c("blue", "white", "red"))(50),
    filename = "analysis_results/figures/heatmap_top_args.pdf",
    width = 8,
    height = 10
  )
  
  pheatmap(
    log_counts,
    annotation_col = annot_col,
    scale = "row",
    clustering_distance_rows = "euclidean",
    clustering_distance_cols = "euclidean",
    color = colorRampPalette(c("blue", "white", "red"))(50),
    filename = "analysis_results/figures/heatmap_top_args.png",
    width = 8,
    height = 10,
    dpi = 300
  )
}
```

---

# Correlation Analysis

## Correlate ARGs with Environmental Variables

```{r correlations}
# Prepare data: Total ARG abundance per sample + environmental variables
env_vars <- c("temperature", "pH", "doc")  # Adjust based on available metadata

cor_data <- args %>%
  group_by(sample_id) %>%
  summarize(total_arg_rpkm = sum(rpkm)) %>%
  left_join(metadata %>% select(sample_id, all_of(env_vars)), by = "sample_id")

# Calculate Spearman correlations
cor_matrix <- cor(
  cor_data %>% select(-sample_id),
  method = "spearman",
  use = "complete.obs"
)

cor_pvalues <- psych::corr.test(
  cor_data %>% select(-sample_id),
  method = "spearman",
  adjust = "fdr"
)$p

# Save results
write.csv(cor_matrix, "analysis_results/tables/correlation_matrix.csv")
write.csv(cor_pvalues, "analysis_results/tables/correlation_pvalues.csv")

# Visualization
corrplot::corrplot(
  cor_matrix,
  method = "color",
  type = "upper",
  order = "hclust",
  addCoef.col = "black",
  tl.col = "black",
  tl.srt = 45,
  p.mat = cor_pvalues,
  sig.level = 0.05,
  insig = "blank"
)
```

---

# Session Information

```{r session-info}
session_info <- sessionInfo()
print(session_info)

# Save to file
writeLines(capture.output(sessionInfo()), "analysis_results/session_info.txt")
```

---

# Summary of Results

## Key Findings

1. **Alpha Diversity**: [Summarize statistical test results]
2. **Beta Diversity**: [Summarize PERMANOVA results]
3. **Differential Abundance**: [Summarize number of significant ARGs]
4. **Correlations**: [Summarize significant correlations]

## Limitations

- [List any limitations based on data quality flags]
- [Note small sample sizes if applicable]
- [Acknowledge confounding variables if present]

## Data Availability

- Processed data: `analysis_results/data/`
- Results tables: `analysis_results/tables/`
- Figures: `analysis_results/figures/`
- Analysis code: This R Markdown file

```

---

## Step 4: Helper Functions

Include these helper functions at the top of the R Markdown (after loading packages):

```r
# Check parametric assumptions
check_parametric_assumptions <- function(data, group_var, value_var) {
  sample_sizes <- data %>%
    group_by(!!sym(group_var)) %>%
    summarize(n = n())
  
  if (any(sample_sizes$n < 3)) {
    warning("Small sample size detected (n<3)")
  }
  
  normality_tests <- data %>%
    group_by(!!sym(group_var)) %>%
    summarize(shapiro_p = shapiro.test(!!sym(value_var))$p.value)
  
  levene_result <- car::leveneTest(
    as.formula(paste(value_var, "~", group_var)), 
    data = data
  )
  
  all_normal <- all(normality_tests$shapiro_p > 0.05)
  equal_var <- levene_result$`Pr(>F)`[1] > 0.05
  
  if (all_normal & equal_var) {
    message("✓ Parametric assumptions met")
    return(list(test_type = "parametric", use_welch = FALSE))
  } else if (all_normal & !equal_var) {
    message("⚠ Normal but unequal variance")
    return(list(test_type = "parametric", use_welch = TRUE))
  } else {
    message("✗ Non-normal data")
    return(list(test_type = "non-parametric", use_welch = NA))
  }
}

# Check PERMANOVA assumptions
check_permanova_assumptions <- function(dist_matrix, metadata, group_var) {
  bd <- vegan::betadisper(dist_matrix, metadata[[group_var]])
  permutest_result <- permutest(bd, permutations = 999)
  
  if (permutest_result$tab$`Pr(>F)`[1] > 0.05) {
    message("✓ Homogeneous dispersion")
    return(list(valid = TRUE))
  } else {
    message("⚠ Heterogeneous dispersion")
    return(list(valid = FALSE))
  }
}
```

---

## Step 5: Validation Checklist

Before finalizing analysis, verify:

- [ ] All data files loaded successfully
- [ ] Sample IDs match between data and metadata
- [ ] Failed samples excluded from analysis
- [ ] Assumptions checked for all statistical tests
- [ ] Non-parametric tests used when assumptions violated
- [ ] Multiple testing correction applied (FDR)
- [ ] Effect sizes reported alongside P-values
- [ ] Figures use colorblind-friendly palettes
- [ ] Figures exported as PDF + PNG 300dpi
- [ ] All tables saved to `analysis_results/tables/`
- [ ] All figures saved to `analysis_results/figures/`
- [ ] Interpretations acknowledge limitations
- [ ] session_info() saved to file
- [ ] Analysis is reproducible (random seed set)

---

## Step 6: Generate Analysis Report

Render the R Markdown file:

```r
rmarkdown::render("analysis_script.Rmd", output_file = "analysis_report.html")
```

---

## Output Structure

Generate results in this structure:

```
analysis_results/
├── data/
│   └── processed/
│       └── [filtered datasets]
│
├── tables/
│   ├── arg_prevalence_by_class.csv
│   ├── alpha_diversity_metrics.csv
│   ├── permanova_results.csv
│   ├── deseq2_results.csv
│   └── correlation_matrix.csv
│
├── figures/
│   ├── alpha_diversity_boxplot.pdf
│   ├── alpha_diversity_boxplot.png
│   ├── pcoa_ordination.pdf
│   ├── pcoa_ordination.png
│   ├── volcano_plot.pdf
│   ├── volcano_plot.png
│   ├── heatmap_top_args.pdf
│   └── heatmap_top_args.png
│
├── reports/
│   ├── analysis_report.html
│   └── analysis_report.Rmd
│
└── session_info.txt
```

---

## Critical Reminders

### Always:
- ✅ Check assumptions before running tests
- ✅ Use FDR correction for multiple comparisons
- ✅ Report effect sizes, not just P-values
- ✅ Use colorblind-friendly palettes
- ✅ Set random seed for reproducibility
- ✅ Save session_info()

### Never:
- ❌ Use parametric tests without checking normality
- ❌ Report P-values without multiple testing correction
- ❌ Use Pearson correlation on compositional data (use Spearman)
- ❌ Make volcano plots without fold-change threshold
- ❌ Create networks without prevalence filtering
- ❌ Report "P=0.000" (use "P<0.001")
- ❌ Claim causation from correlation

---

## Decision Quick Reference

### Test Selection:
```
Normality?
├─ Yes + 2 groups → t-test (Welch's if unequal variance)
├─ Yes + 3+ groups → ANOVA + Tukey HSD
├─ No + 2 groups → Wilcoxon rank-sum
└─ No + 3+ groups → Kruskal-Wallis + Dunn's test
```

### Differential Abundance:
```
Data type?
├─ Count data + n≥5 → DESeq2
├─ Count data + n<5 → edgeR
├─ Relative abundance → ANCOM
└─ Biomarker discovery → LEfSe
```

### Correlation:
```
Data characteristics?
├─ Non-normal OR ordinal → Spearman (default)
├─ Normal + linear → Pearson
└─ Small sample (n<20) → Kendall's tau
```
