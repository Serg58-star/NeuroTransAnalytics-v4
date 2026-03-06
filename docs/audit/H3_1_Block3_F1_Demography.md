# H3.1 Block 3 — Demographic Structure in F1

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.1 — F1 Cross-Model Comparison

---

## Scope

Assessment of how well the synthetic v5 generator replicates the structural asymmetries (Sex Lambda-1 Dominance) and anomalies (Age Q2 Diffusion) found intrinsically within the empirical F1 Baseline space.

## 1. Sex Amplitude Asymmetry

| Cohort | Empirical F1 (λ₁) | Synthetic v5 F1 (λ₁) |
| :--- | :---: | :---: |
| **Female (N=884)** | 4,167 | 5,883 |
| **Male (N=598)** | 8,767 | 7,744 |
| **Male / Female Ratio**| **2.10×** | **1.32×** |

### Observation

The empirical F1 space contains a massive structural sex divergence, with Male baseline variance (λ₁=8767) more than double the Female variance (λ₁=4167). The v5 generator (which applied a flat sigma-shift based on older architectural assumptions) captured only a fraction of this effect (ratio 1.32× vs 2.10×).

## 2. Age Spectral Gradient (Q2 Anomaly)

| Quartile | Empirical Eff.Rank | Empirical λ₁ | Synthetic Eff.Rank | Synthetic λ₁ |
| :--- | :---: | :---: | :---: | :---: |
| **Q1 (Young)** | 1.25 | 5,712 | 2.92 | 6,722 |
| **Q2 (Mid-Low)** | 1.53 | **1,614** | 2.90 | **5,900** |
| **Q3 (Mid-High)**| 1.16 | 9,324 | 2.91 | 5,949 |
| **Q4 (Older)** | 1.38 | 5,547 | 2.88 | 7,927 |

### Observation

The Q2 (ages 27–39) spectral anomaly (massive collapse in primary variance amplitude) is a defining feature of the empirical F1 spatial baseline (dropping from λ₁≈5700 in Q1 to just λ₁=1614 in Q2).

The synthetic v5 generator, utilizing a smooth exponential age-slowing curve, completely misses this cohort-specific structural collapse, producing a smooth transition (6722 → 5900 → 5949 → 7927). Moreover, the v5 generator fails to replicate the severe 1D-dominant geometry of the empirical space across all age groups.

---

## Formal Verdict

> **F1_DEMOGRAPHY_DIVERGENT**

The structural geometry of the core V1 baseline is highly dependent on demographic factors in reality, exhibiting massive non-linear shifts in Q2 and >2x scale differences between sexes. The v5 synthetic architecture generates a structurally invariant, multi-dimensional, overly-smoothed demographic representation.
