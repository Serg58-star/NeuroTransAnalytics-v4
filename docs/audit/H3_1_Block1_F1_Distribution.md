# H3.1 Block 1 — F1 Distributional Comparison

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.1 — F1 Cross-Model Comparison

---

## Scope

Direct evaluation of the statistical moments (location, scale, shape) of the unaggregated reaction time F1 Baseline to verify functional equivalence.

## Distributional Moments

| Metric | Empirical F1 | Synthetic v5 F1 |
| :--- | :---: | :---: |
| **Mean (ms)** | 262.9 | 299.7 |
| **Standard Deviation**| 44.8 | 47.4 |
| **Coefficient of Var**| 0.171 | 0.158 |
| **Skewness** | **6.06** (Extreme right tail) | **0.70** (Mild lognormal skew) |
| **Kurtosis** | **80.51** (Heavy leaps) | **0.76** (Standard bounds) |

## Channel Correlation Structure

A critical physiological aspect of the F1 spatial representation is how the Left, Center, and Right visual fields co-vary within the same individual on the baseline task:

**Empirical F1 (L, C, R)** Correlation Matrix:

- L vs C: **r = 0.93**
- L vs R: **r = 0.92**
- C vs R: **r = 0.93**

**Synthetic v5 F1 (L, C, R)** Correlation Matrix:

- L vs C: **r = 0.18**
- L vs R: **r = 0.19**
- C vs R: **r = 0.18**

## Structural Diagnosis

While the mean and variance scales are broadly similar (Means ~260-300ms, CVs ~0.16), the internal shape of the spaces is fundamentally broken.

1. The empirical data possesses extreme skew and heavy tails (kurtosis 80) not captured by standard lognormal distributions.
2. The synthetic v5 architectural generator treated Left, Center, and Right processing streams as largely independent samples. In empirical reality, they are almost perfectly locked together (r > 0.92) at the baseline physiological stage, signifying a unified global baseline speed prior to load.

## Formal Verdict

> **DISTRIBUTION_INCOMPATIBLE**

The empirical and synthetic models represent fundamentally different underlying generative shapes regarding spatial correlation and extreme tail behavior.
