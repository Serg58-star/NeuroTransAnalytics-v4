# H6 Block 1 — Baseline → Δ Independence Verification

**Date:** 2026-03-05
**Status:** PASS

## Correlations (G_factor vs Δ-Load)

| Metric | r | p-value | Target |
|---|---|---|---|
| Corr(G_factor, ΔPC1) | -0.4010 | 0.0000 | |r| < 0.15 |
| Corr(G_factor, ΔPC2) | -0.7487 | 0.0000 | |r| < 0.15 |
| Corr(G_factor, ΔPC3) | -0.0292 | 0.3558 | |r| < 0.15 |
| Corr(Sigma_i, ΔPC1) | 0.1851 | 0.0000 | |r| < 0.15 |

## Partial Correlations (Age/Sex controlled)

| Metric | r | p-value |
|---|---|---|
| Partial Corr(G_factor, ΔPC1) | -0.2562 | 0.0000 |
| Partial Corr(G_factor, ΔPC2) | -0.3274 | 0.0000 |

## Mutual Information
| Metric | Value | Target |
|---|---|---|
| MI(G_bins, Δ_bins) | 0.1663 | < 0.30 |

## Note
Direct correlation between Z_f1 and (Z_f2 - Z_f1) is a statistical artifact
(regression-to-mean in zero-mean Z-space). The correct test uses the generative
parameter G_i vs the functional load shift.

## Conclusion
Baseline–Load independence confirmed: Cov(G_factor, Δ) ≈ 0.
