# H2 Block 4 — Variance Decomposition

**Date**: 2026-03-03  
**Status**: COMPLETED  
**Basis**: Stage H2 — Empirical & Synthetic Consistency Audit

---

## Scope

Partitioning of total variance into sex, age (quartile), and residual components.  
N=1482; 3-channel Z-normalized feature space.  
Method: Sum-of-Squares decomposition (η² effect sizes). No modelling of functional form.

---

## Global Variance Components

| Component | Between-Group SS | η² | % of Total |
| :--- | :---: | :---: | :---: |
| **Between-sex** | 25.36 | 0.0057 | 0.57% |
| **Between-age quartile** | 310.95 | 0.0699 | 6.99% |
| **Residual (within-group)** | — | — | ≈92.44% |
| **Total SS** | 4446.00 | 1.0 | 100% |

---

## Interpretation of Components

| Component | Value | Interpretation |
| :--- | :---: | :--- |
| Sex effect (η²) | 0.0057 | Very small; sex accounts for 0.57% of total variance at population level. Note: this concerns overall variance, not absolute mean position (which may differ — see Block 2: λ₁ asymmetry 1.81×). |
| Age effect (η²) | 0.0699 | Moderate; age quartile accounts for 6.99% of total variance. Consistent with Block 3 showing Q2 as a spectral outlier. |
| Residual | ≈92.44% | Dominant component; reflects true inter-individual heterogeneity within each demographic group. |

---

## Limitations

- η² is computed on Z-normalized data; variance of the absolute RT (ms) distribution may show larger demographic effects.
- Age is treated as quartile category, not continuous — may understate age gradients within quartiles.
- Between-sex SS captures mean position differences between male/female centroids, but does NOT capture scale differences (e.g., Male λ₁ > Female λ₁ by 1.81×, as shown in Block 2).

---

## Formal Output

| Component | η² value |
| :--- | :---: |
| Sex | 0.0057 (0.57%) |
| Age quartile | 0.0699 (6.99%) |
| Residual | ≈0.924 (92.44%) |
