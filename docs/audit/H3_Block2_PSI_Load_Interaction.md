# H3 Block 2 — PSI vs Load-Only Geometry

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3 — PSI Structural Contribution Audit

---

## Scope

Does the heavily anisotropic, dynamic "Load" response (Stage 9 state transitions: ΔV4, ΔV5) change its fundamental structure when the sequential PSI components are mathematically regressed out?

## 1. Load-Space Geometry Comparison

| Metric | Original 8D Load | Residual 8D Load (PSI removed) |
| :--- | :---: | :---: |
| **Effective Rank** | 4.86 | 5.05 |
| **PC1% Variance** | 40.35% | 37.79% |
| **Hopkins Statistic** | 1.0000 | 1.0000 |

## 2. Structural Observations

Regressing the 12 PSI sequence dimensions completely out of the Load-space matrix yields almost no change regarding topology. The Effective Rank increases trivially (4.86 → 5.05), and extreme spatial inhomogeneity (Hopkins = 1.0) is perfectly conserved.

## Formal Verdict

The structural properties of the state dynamics (Load transitions) are mathematically decoupled from the intra-test sequential PSI responses. Removing the PSI effect does not homogenize the load space.
