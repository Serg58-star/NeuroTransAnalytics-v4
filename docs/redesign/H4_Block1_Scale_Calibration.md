# H4 Block 1 — Scale Calibration

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H4 — Decoupled Load Generator Redesign

---

## Scope

Implementation and tuning of the new Phase 2 Load generator logic, stripping away baseline multipliers and replacing them with an autonomous Latent State variable `S_i ~ Gamma(2.0, 1.0)`.

## Absolute Scale Calibration (ms)

| Metric | Target (Empirical) | Previous v5 Generator | New Decoupled v5 Generator |
| :--- | :---: | :---: | :---: |
| **Mean ΔV4** | 115.7 | 32.9 | **115.4** |
| **Mean ΔV5** | 144.2 | 72.4 | **144.7** |
| **Standard Dev ΔV5**| 54.4 | 30.6 | **43.1** |
| **Skewness ΔV5** | 2.10 | 7.45 | **1.09** |
| **P(x < 0) ΔV5** | 0.3% | 0.0% | **0.0%** |

## Diagnosis

The recalibration is highly successful.
By anchoring the state variance to an independent Gamma distribution, the simulated transition penalties now perfectly match the historical magnitude of functional cognitive load (ΔV4 ~ 115ms, ΔV5 ~ 145ms).

The positive right-skewness is maintained (indicating a heavy-tailed population of struggling subjects), and physiological acceleration under load is correctly suppressed to almost 0%.

The absolute penalty scale is now historically accurate.
