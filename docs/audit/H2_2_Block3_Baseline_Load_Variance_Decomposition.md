# H2.2 Block 3 — Baseline / Load / Lat Variance Separation

**Date**: 2026-03-03  
**Status**: COMPLETED  
**Basis**: Stage H2.2 — Baseline-Adjusted Empirical Geometry Audit

---

## Scope

Decomposition of total population variance into three analytical domains:

1. **Baseline** (Trait state, absolute speed)
2. **Load** (Delta transitions)
3. **Lateralization** (Spatial asymmetry indices)

---

## 1. Standardized Variance Proportions (12D Space)

When measured in standardized coordinates (Z-scores to equal-weight the channels), the 12 total dimensions sum to 12.0 variance units. The distribution is mathematically forced by scaling, but reflects the conceptual architecture weight:

| Domain | Channels | Share of Standardized Variance |
| :--- | :---: | :---: |
| **Baseline (F1)** | 3 (L, C, R) | 25.00% |
| **Load (ΔV4, ΔV5)** | 6 (L, C, R) | 50.00% |
| **Lateralization** | 3 (L-index) | 25.00% |

## 2. Raw Variance Amplitude (Before Standardization)

A critically important metric is the absolute raw Sum of Squares (SS) in the original RT space. This shows where the actual millisecond variations are located:

| Domain | Raw SS (Approximation) | Note |
| :--- | :--- | :--- |
| **Baseline (F1)** | 6,174 | Absolute Trait baseline variance is large. |
| **Load (ΔV4, ΔV5)** | 17,630 | The load effect (State Dynamics) generates **nearly 3×** the variance of the baseline. |
| *Lateralization* | *(Tiny scale)* | Normalized coefficients (-1 to 1 range), cannot be directly summed with RT raw variance. |

---

## Formal Conclusion

State Dynamics (Load transitions) contain the absolute majority of subject variance when measured in raw milliseconds (approx. 74% of the combined Base+Load RT variance).

Because F2 and F3 variance is driven heavily by the F1 baseline *plus* the large Load variance, aggregating them in historical Stage 7 mathematically forced PC1 to represent the combined sum, thereby artificially crushing the apparent dimensionality.

Baseline and Load are distinct variance reservoirs and must remain analytically separated (justifying the Dual-Layer architecture logic proposed in Task 63).
