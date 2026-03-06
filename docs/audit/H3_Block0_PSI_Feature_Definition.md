# H3 Block 0 — PSI Feature Definition

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3 — PSI Structural Contribution Audit

---

## Scope

Extraction of quantitative features representing the individual dynamic response to the Pseudo-Random Interval (PSI) stimulus sequence across the 36 trials of each test.

## Feature Engineering

For each valid test (tst1, tst2, tst3) per subject (N=1482 First-Visit pool), the following sequential metrics were extracted directly from the chronological trial stream (`tstX_1` to `tstX_36`):

1. **AR1 (Lag-1 Autocorrelation)**: Measures immediate trial-to-trial memory/adaptation.
2. **Slope**: Linear trend velocity across the 36 trials (quantifying intra-test fatigue or learning).
3. **CV (Coefficient of Variation)**: Relative dispersion width (Standard Deviation / Mean).
4. **PE (Permutation Entropy, order 3)**: A robust measure of sequential volatility and complexity.

This generated 4 PSI features per test × 3 tests = **12 independent PSI dimensions** appended to the subject record, allowing us to explicitly model the structured sequential response separately from the positional spatial medians.
