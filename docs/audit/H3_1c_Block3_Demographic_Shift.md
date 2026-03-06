# H3.1c Block 3 — Demographic Shift Evaluation

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.1c — Correlated Motor Layer Simulation Audit

---

## Scope

Does mathematically isolating a "pure Neural" response (by simulating and regressing a severe 80% Motor factor) erase the striking demographic anomalies observed in the raw geometry?

## 1. Sex Amplitude Asymmetry (Neutral Space)

Using the Severe Motor correction (`α` = 0.80, `σ` = 10ms noise):

| Cohort | Original λ₁ Ratio (M/F) | Neural λ₁ Ratio (M/F) | Status |
| :--- | :---: | :---: | :---: |
| **Male vs Female**| 2.10× | **1.56×** | PARTIALLY_SURVIVED |

### Observation

While regressing out general global speeds reduces the Male variance multiplier from 2.10x to 1.56x, a massive structural asymmetry remains in the estimated neural paths. Men exhibit >50% more primary variance amplitude in baseline sensory tracking.

## 2. Age Spectral Gradient (Q2 Anomaly)

| Quartile | Original λ₁ | Neural λ₁ | Neural Eff.Rank |
| :--- | :---: | :---: | :---: |
| **Q1 (Young)** | 5,712 | 596 | 2.36 |
| **Q2 (Mid-Low)** | **1,614** | **352** | **2.48** |
| **Q3 (Mid-High)**| 9,324 | 702 | 2.24 |
| **Q4 (Older)** | 5,547 | 488 | 2.80 |

### Observation

In the isolated Neural space, the fundamental geometry is less anisotropic (Ranks ≈ 2.2—2.8), but the **Q2 spectral anomaly remains exactly where it was**. The Q2 cohort strictly exhibits the absolute lowest structural variance of the population (Neural λ₁ = 352).

## Diagnostic Summary

The demographic structural signatures identified in prior stages (Sex amplitude ratio > 1.5x; Q2 severity collapse) are **true neural-baseline characteristics**. They are partially amplified by global performance (motor) scaling, but their core presence cannot be mathematically erased by removing motor execution assumptions.
