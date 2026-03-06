# H2 Block 2 — Stage 7 Geometry Replication by Sex

**Date**: 2026-03-03  
**Status**: COMPLETED  
**Basis**: Stage H2 — Empirical & Synthetic Consistency Audit

---

## Scope

Replication of Stage 7 geometry metrics stratified by sex.  
Gender coding: 1=Male (N=598), 0=Female (N=884).  
No demographic corrections applied.

---

## Male (N=598)

| Metric | Value |
| :--- | :---: |
| PC1% | 82.47% |
| Effective Rank | 1.79 |
| PR | 1.44 |
| λ₁ | 3.3344 |
| λ₂ | — |
| λ₃ | 0.2653 |
| Anisotropy (λ₁/λ₃) | 12.567 |
| Hopkins | 0.9968 |
| Gap optimal k | 5 |
| Peak Silhouette | 0.6833 |

---

## Female (N=884)

| Metric | Value |
| :--- | :---: |
| PC1% | 80.90% |
| Effective Rank | 1.85 |
| PR | 1.48 |
| λ₁ | 1.8386 |
| λ₂ | — |
| λ₃ | 0.1698 |
| Anisotropy (λ₁/λ₃) | 10.828 |
| Hopkins | 0.9855 |
| Gap optimal k | 5 |
| Peak Silhouette | 0.5436 |

---

## Comparative Summary

| Metric | Male | Female | Ratio M/F |
| :--- | :---: | :---: | :---: |
| Effective Rank | 1.79 | 1.85 | 0.97 |
| PR | 1.44 | 1.48 | 0.97 |
| **λ₁** | **3.334** | **1.839** | **1.81** |
| Anisotropy | 12.567 | 10.828 | 1.16 |
| Hopkins | 0.9968 | 0.9855 | — |
| Peak Silhouette | 0.6833 | 0.5436 | 1.26 |

**Key structural observation**: Effective Rank and PR are nearly identical (ratio ≈ 0.97). Topological continuity is preserved in both cohorts. However, λ₁ differs by factor 1.81 (Male variance is 81% larger on PC1). Silhouette in Males is notably higher, suggesting stronger density differentiation within the male cohort.

Both cohorts: Hopkins → 1.0 (extreme density inhomogeneity); Gap → k=5 (same optimal k); 3D continuum structure preserved.

---

## Formal Verdict

> **GEOMETRY_STABLE** (topology preserved in both cohorts)  
> With noted **amplitude asymmetry** on PC1: Male λ₁ = 1.81× Female λ₁.
