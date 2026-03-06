# H6 Block 3 — PSI Interaction Audit

**Date:** 2026-03-05
**Status:** PASS

## PSI Configuration
- PSI noise scale: 0.2021 (5% of Δ-space SD=4.0427)

## Geometry Stability Under PSI Perturbation

| Metric | Original | With PSI | Change |
|---|---|---|---|
| Effective Rank | 7.878 | 7.914 | 0.46% |
| PC1 Variance | 84.44% | 84.23% | 0.21% |

## PSI → Δ Correlations
| Metric | r | p-value |
|---|---|---|
| Corr(PSI_PC1, ΔPC1) | -0.0007 | 0.9814 |
| Corr(PSI_PC1, ΔPC2) | 0.0146 | 0.6452 |

## PSI → Severity Correlation
| Metric | Value | Expected |
|---|---|---|
| Corr(PSI_magnitude, Severity) | 0.0241 (p=0.4468) | low |

## Interpretation
PSI perturbation at empirical scale (5% of Δ-variance) does not alter the fundamental
Δ-space geometry. PSI is confirmed as a dynamic modifier, not a structural factor.
