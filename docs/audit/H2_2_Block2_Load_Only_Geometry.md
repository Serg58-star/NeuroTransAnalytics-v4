# H2.2 Block 2 — Load-Only Geometry

**Date**: 2026-03-03  
**Status**: COMPLETED  
**Basis**: Stage H2.2 — Baseline-Adjusted Empirical Geometry Audit

---

## Scope

Isolation and structural analysis of the pure dynamic response subspace.  
Features (8D):

- ΔV4 Left, Center, Right
- ΔV5 Left, Center, Right
- Normalized Lat(ΔV4), Lat(ΔV5)

N = 1482 subjects.

---

## 1. Load-Space Spectral Metrics

| Metric | Value |
| :--- | :---: |
| **Subspace Dimensionality** | 8 |
| **Effective Rank** | 4.86 |
| **PC1% variance** | 40.34% |
| **λ₁** | 3.229 |
| **λ₂** | 1.647 |
| **λ₃** | 1.275 |

---

## 2. Load-Space Density & Clustering

| Metric | Value | Interpretation |
| :--- | :---: | :--- |
| **Hopkins Statistic** | 1.0000 | Extreme spatial inhomogeneity / density gradients |
| **Peak Silhouette** | 0.2912 | Weak cluster tendency; falls below the 0.35 stable threshold |

---

## 3. Structural Observations

1. **Dimensionality**: The pure load response is distinctly multi-dimensional (Eff.Rank = 4.86 out of 8). It does not collapse into a single universal "fatigue/adaptation" axis. PC1 explains only 40% of the variance.
2. **Topology**: The Peak Silhouette is < 0.30, confirming that the load response (Stage 9 state dynamics) is a **continuum**, not a set of discrete state-transition typologies.
3. **Density**: The Hopkins statistic of 1.00 indicates extreme density variations within that continuum (an "anisotropic cloud", heavily concentrated in certain standard transition zones, with sparse heavy tails).

## Formal Conclusion

The pure Load geometry is a **moderately high-dimensional (Eff.Rank ≈ 4.9), continuous, highly anisotropic manifold** without dominating 1D structure.
