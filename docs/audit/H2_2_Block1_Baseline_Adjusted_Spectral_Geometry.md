# H2.2 Block 1 — Rank & Spectral Geometry (Baseline-Adjusted)

**Date**: 2026-03-03  
**Status**: COMPLETED  
**Basis**: Stage H2.2 — Baseline-Adjusted Empirical Geometry Audit

---

## Scope

Reconstruction of the empirical feature space without built-in collinearity (where F2 and F3 historically contained F1).  
The new space explicitly separates:

- **Baseline (F1)**: Left, Center, Right (3D)
- **Load Transitions (ΔV4, ΔV5)**: Left, Center, Right (6D)
- **Normalized Lateralization**: F1, ΔV4, ΔV5 indexes (3D)

Total: 12-dimensional baseline-adjusted empirical space.  
N = 1482 valid subjects.

---

## 1. Spectral Comparison: Aggregated vs Baseline-Adjusted

| Metric | Aggregated Space (Stage 7 / H2 equivalent) | Baseline-Adjusted Space (12D) | Baseline-Adjusted Space (9D, no Lat) |
| :--- | :---: | :---: | :---: |
| **Feature count** | 3 (tst1_L, tst2_L, tst3_L proxy) | 12 | 9 |
| **PC1% variance** | 79.43% | **30.33%** | 40.17% |
| **PC2% variance** | — | 20.87% | 27.72% |
| **PC3% variance** | — | 13.60% | 17.58% |
| **Effective Rank** | 1.91 | **6.49** | 4.65 |
| **Participation Ratio**| — | 5.43 | 3.65 |
| **λ₁** | — | 3.642 | — |

---

## 2. Key Structural Findings

### Collapse of the Strong 1D Dominance

In the aggregated space (Stage 7), PC1 captured ~80% of the variance, leading to an Effective Rank of < 2.
When the artificial collinearity (F2 = F1 + ΔV4) is removed, PC1 variance drops to just 30.3% in the 12D space (and 40.2% in the 9D space without explicit lateralization indexes).

### Expansion of Dimensionality

The Effective Rank of the population expands from **1.91** to **6.49**. The Participation Ratio (PR), measuring how variance is spread across orthogonal axes, expands to **5.43**.

---

## Formal Answer to the H2.2 Key Question

> **Q: Does the empirical space remain low-rank after removing built-in collinearity?**  
> **A: NO. Stage 7 underestimated the true dimensionality due to an incorrect (co-linear) basis.**

The empirical geometry is genuinely multi-dimensional when baseline, load, and spatial position are appropriately separated. The low-rank 1D-dominant geometry of Stage 7 was highly exaggerated by the F1 baseline variance being counted three times (in F1, F2, and F3).
