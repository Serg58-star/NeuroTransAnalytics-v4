# H2.2 Block 4 — Sex & Age Spectral Stability in Adjusted Space

**Date**: 2026-03-03  
**Status**: COMPLETED  
**Basis**: Stage H2.2 — Baseline-Adjusted Empirical Geometry Audit

---

## Scope

Re-evaluation of the demographic spectral metrics identified in Stage H2 Blocks 2 and 3, but now executed in the **baseline-adjusted 12D space** (Baseline, Load, Lateralization) to see if the demographic structural variances survive collinearity removal.

---

## 1. Sex Stability (12D Adjusted Space)

| Cohort | N | Eff. Rank | PC1% | λ₁ |
| :--- | :---: | :---: | :---: | :---: |
| **0 (Female)** | 884 | 6.83 | 29.65% | 3.078 |
| **1 (Male)** | 598 | 5.94 | 32.53% | 4.650 |

### Observation

- The amplitude asymmetry identified in Stage H2 (Male λ₁ > Female λ₁) survives in the baseline-adjusted space.
- Male λ₁ (4.65) vs Female λ₁ (3.08) ratio = **1.51×**.
- However, both spaces are similarly high-rank (Eff.Rank ≈ 6–7), replacing the 1D-dominant geometry of Stage 7.

---

## 2. Age Spectral Gradient (12D Adjusted Space)

| Quartile | N | Eff. Rank | PC1% | λ₁ |
| :--- | :---: | :---: | :---: | :---: |
| **Q1 (Young)** | 400 | 5.15 | 47.42% | 7.167 |
| **Q2 (Middle-Low)** | 343 | **7.14** | **22.47%** | **1.332** |
| **Q3 (Middle-High)**| 398 | 5.39 | 44.86% | 4.856 |
| **Q4 (Older)** | 341 | 6.99 | 24.94% | 3.537 |

### Observation

- The `AGE_GRADIENT_GEOMETRY` flagged in Stage H2 Block 3 survives entirely.
- The Q2 (ages 27–39) mid-adult cohort remains a dramatic spectral outlier:
  - Highest multidimensionality (Eff.Rank = 7.14)
  - Lowest 1D dominance (PC1% = 22.47%)
  - Lowest primary variance amplitude (λ₁ = 1.33 vs Q1=7.17)

## Formal Conclusion

The structural demographic asymmetries (Male amplitude dominance; Q2 age spectral diffusion) found in Stage H2 were **not** artifacts of baseline-collinearity. They represent genuine features of the physiological trait/state manifold that persist when Load and Baseline are properly separated.
