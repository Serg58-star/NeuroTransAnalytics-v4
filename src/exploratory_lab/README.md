# Exploratory Lab

**Independent research layer for advanced multivariate analysis of NeuroTransAnalytics-v4 data.**

---

## Overview

The Exploratory Lab is an **architecturally isolated** research sandbox designed to explore latent structures in the NeuroTransAnalytics dataset that are not visible in canonical A0/A1 scenarios.

### Key Features

- ✅ Trial-level data access (READ-ONLY)
- ✅ **11 corrected baseline features** (Task 27.1: methodologically validated)
- ✅ Correlation structure validation (VIF, multicollinearity detection)
- ✅ Dimensionality analysis (PCA, UMAP)
- ✅ Cluster detection (Hopkins Statistic, Silhouette, DBSCAN)
- ✅ Complete architectural isolation from v4 core

---

## Installation

```bash
# Optional dependencies
pip install -r requirements_exploratory.txt
```

**Note**: If UMAP is not installed, the pipeline will skip UMAP embedding but continue with PCA/Hopkins/Silhouette analysis.

---

## Quick Start

```python
from exploratory_lab.pipelines.exp_pipeline_v0 import ExploratoryPipeline

# Initialize
pipeline = ExploratoryPipeline()

# Run analysis
results = pipeline.run(min_sessions=3)

# Results saved to: data/exploratory/
```

See `examples/exploratory_lab_example.py` for a complete example.

---

## Architecture

```
src/exploratory_lab/
├── data_loader.py              # READ-ONLY trial-level data access
├── feature_engineering/
│   ├── baseline_features.py    # 11 corrected features (Task 27.1)
│   └── correlation_validator.py # Correlation validation
├── geometry/
│   ├── dimensionality.py       # PCA, UMAP
│   └── clustering.py           # Hopkins, Silhouette, DBSCAN
└── pipelines/
    └── exp_pipeline_v0.py      # End-to-end MVP workflow
```

---

## Features Computed (Corrected - Task 27.1)

### Baseline (11 features)

**ΔV1 - Baseline Sensorimotor Speed:**

1. **Median_ΔV1_left** - left visual field
2. **Median_ΔV1_center** - central visual field
3. **Median_ΔV1_right** - right visual field

**Asymmetries (Corrected Formulas):**
4. **Asym_ΔV1_abs** - absolute asymmetry: `|right - left|`
5. **Asym_ΔV1_rel** - relative asymmetry: `(right - left) / ((right + left) / 2)`

**Variability:**
6. **MAD_ΔV1** - phase stability (median absolute deviation)

**ΔV4 - Color Processing (by visual field):**
7. **ΔV4_left** - parvocellular pathway, left field
8. **ΔV4_right** - parvocellular pathway, right field

**ΔV5 - Motion Detection (by visual field):**
9. **ΔV5_left** - magnocellular pathway, left field
10. **ΔV5_right** - magnocellular pathway, right field

**PSI - Cortical Recovery:**
11. **PSI_tau** - exponential recovery time constant `RT(PSI) = RT₀ + β·exp(-PSI/τ)`
12. **PSI_slope_linear** - linear recovery rate (for comparison)

**Methodological Corrections:**

- ❌ Removed center-normalized asymmetry `(right - left) / center`
- ✅ Added absolute and relative asymmetry metrics
- ✅ Separated ΔV4/ΔV5 by visual fields (no premature aggregation)
- ✅ Implemented exponential PSI model with stability checks

---

## Analysis Methods

### Correlation Structure Validation

**Pre-clustering validation (Task 27.1):**

- **Pearson & Spearman correlations**: Detect linear and monotonic relationships
- **VIF (Variance Inflation Factor)**: Identify multicollinearity
  - VIF > 10 → severe multicollinearity
  - VIF > 5 → moderate multicollinearity
- **Dominant axis detection**: Check for general speed factor

### Dimensionality

- **PCA**: Linear dimensionality, scree plot, Kaiser criterion
- **UMAP**: Nonlinear visualization (2D/3D)

### Cluster Detection

- **Hopkins Statistic**: Test for cluster tendency
  - H < 0.5 → gradient structure
  - H > 0.7 → cluster structure
- **Silhouette Analysis**: Evaluate k-means quality
  - Score > 0.35 → real clusters
  - Score < 0.25 → no structure

---

## Output

Results are saved to `data/exploratory/`:

```
data/exploratory/
├── features/
│   └── baseline_features_v0.parquet  # 11 corrected features
├── correlations/                      # NEW (Task 27.1)
│   ├── correlation_pearson.csv
│   ├── correlation_spearman.csv
│   ├── vif_scores.csv
│   └── high_correlations.csv
├── embeddings/
│   ├── pca_results_v0.json
│   └── umap_embedding_v0.parquet
└── reports/
    └── analysis_summary_v0.txt
```

---

## Design Principles

1. **Architectural Isolation**: Zero dependencies on C3.4/C3.5
2. **Data Immutability**: READ-ONLY database access
3. **Reproducibility**: Fixed random seeds, versioned artifacts
4. **Scientific Rigor**: Null results (no structure) are valid outcomes

---

## Future Visualization (GUI Integration)

**Planned additions:**

- RT ~ PSI plot with exponential fit overlay
- Linear vs exponential model comparison
- Asymmetry by visual field bar charts
- Correlation heatmap (interactive)
- VIF scores visualization

---

## References

- Design: `Task_27_0_Exploratory_Lab_Свободное_Проектирование.md`
- Conceptual foundation: `Task_26_6_Возврат_к_Методике_и_Полям_Зрения.md`
