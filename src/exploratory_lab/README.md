# Exploratory Lab

**Independent research layer for advanced multivariate analysis of NeuroTransAnalytics-v4 data.**

---

# Overview

The Exploratory Lab is an architecturally isolated research sandbox
for investigating latent multivariate structure
within the NeuroTransAnalytics dataset.

It provides experimental statistical tools
without affecting the validated C3-Core.

---

# Validated Core Status (v4.0-core-validated)

As of Stages 1–8.5:

- Latent space confirmed as **3D Continuous Density-Gradient Manifold**
- No stable discrete clusters detected
- Trait–State decomposition validated (ICC analysis)
- Dynamics follow Markovian Random Walk (H ≈ 0.5)
- Mathematical Norm Envelope defined (MCD + Mahalanobis)
- Core geometry noise-robust and demographically invariant

Clustering routines remain available
for stress-testing and falsification,
not as assumed natural structure.

---

# Architecture

src/exploratory_lab/
├── data_loader.py
├── feature_engineering/
├── geometry/
├── pipelines/


The lab is:

- READ-ONLY with respect to neuro_data.db
- Architecturally isolated from core modules
- Designed for hypothesis testing and falsification

---

# Capabilities

## Correlation & Multicollinearity

- Pearson & Spearman correlations
- VIF analysis
- Dominant axis detection

## Dimensionality

- PCA
- UMAP (optional)

## Structure Stress-Testing

- Hopkins statistic
- Silhouette analysis
- DBSCAN
- Density inspection

These tools are used to challenge the geometry,
not to impose clustering assumptions.

---

# Output

Results are saved to:

data/exploratory/


Artifacts include:

- Feature matrices
- Correlation tables
- PCA embeddings
- Density statistics
- Structural reports

---

# Design Principles

1. Architectural isolation
2. Reproducibility
3. Statistical rigor
4. Null results are valid
5. No implicit typologization

---

# Role in v4+

The Exploratory Lab remains a sandbox for:

- Stress-testing the core geometry
- Testing alternative embeddings
- Evaluating structural robustness
- Prototyping new analytical approaches

It does not redefine validated Core geometry.
