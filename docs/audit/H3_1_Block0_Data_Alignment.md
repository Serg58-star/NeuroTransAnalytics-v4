# H3.1 Block 0 — Data Alignment

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.1 — F1 Cross-Model Comparison

---

## Scope

Preparation of strictly comparable physiological baseline data by completely stripping away dynamic load, syntax sequences, koniocellular paths, and severity scalings from both empirical and synthetic data sources.

## Data Alignment Parameters

| Parameter | Empirical Dataset | Synthetic v5 Generator |
| :--- | :--- | :--- |
| **Cohort** | First-Visit Deduplicated | Synthetic Match |
| **N Subjects** | 1482 | 1482 |
| **Variables** | `tst1_L`, `tst1_C`, `tst1_R` medians | `F1_L`, `F1_C`, `F1_R` lognormal samples |
| **Conio Included?** | No (Tst1 uses Parvo path) | No (Disabled P-path) |
| **Load (ΔV4) Included?** | No (Tst1 is baseline) | No (Disabled P2 phase) |
| **PSI Included?**| No (Median aggregates only) | No (No sequential generation) |
| **Age / Sex Config** | Historical true | Sampled perfectly to match empirical matrix |

## Confirmation

Data alignment was successful. We now have two pure 3D spacial matrices (Left, Center, Right channels) representing the baseline V1 cortical physiological delay, one empirical and one synthetic, ready for direct cross-model structural comparison without confounding dynamic layers.
