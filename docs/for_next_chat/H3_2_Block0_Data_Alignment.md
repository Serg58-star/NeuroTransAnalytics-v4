# H3.2 Block 0 — Data Alignment (Δ-Space)

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.2 — Δ-Space Cross-Model Comparison

---

## Scope

Preparation of the functional relative transition matrices (ΔV4, ΔV5, ΔLat) by restricting the v5 synthetic generator exclusively to Phase 2 Load shifts, omitting explicit clinical/severity mechanics.

## Data Alignment Parameters

| Parameter | Empirical Dataset | Synthetic v5 Generator |
| :--- | :--- | :--- |
| **Cohort** | First-Visit Deduplicated | Synthetic Match |
| **N Subjects** | 1482 | 1482 |
| **ΔV4 Calculation**| `tst2_med - tst1_med` | `P2 Load Generation (V4)` |
| **ΔV5 Calculation**| `tst3_med - tst1_med` | `P2 Load Generation (V5)` |
| **ΔLat Calculation**| Shift in Left/Right Bias | Random Noise around 0 |
| **Baseline Dependency** | Empirical `tst1` | Synthetic normalized baseline |
| **Conio / Severity** | N/A | Explicitly Disabled |

## Confirmation

Data alignment was successful. The generative outputs are direct 4D matrices representing pure execution strain (Load) unpolluted by absolute reaction time or PSI.
