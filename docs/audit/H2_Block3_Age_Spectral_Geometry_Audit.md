# H2 Block 3 — Extended Age Spectral Geometry Audit

**Date**: 2026-03-03  
**Status**: COMPLETED  
**Basis**: Stage H2 — Empirical & Synthetic Consistency Audit

---

## Scope

Spectral geometry analysis stratified by age quartile.  
N=1482, quartile boundaries derived from empirical distribution.  
No demographic corrections applied.

---

## Age-Quartile Spectral Metrics

| Quartile | N | Age Range | PC1% | Eff. Rank | PR | λ₁ | λ₃ | Aniso (λ₁/λ₃) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Q1 (Young)** | 400 | ≤26 | 86.62% | 1.59 | 1.31 | 3.915 | 0.141 | **27.746** |
| **Q2 (Middle-Low)** | 343 | 27–39 | 68.81% | 2.28 | 1.90 | 0.607 | 0.101 | **6.038** |
| **Q3 (Middle-High)** | 398 | 40–54 | 85.82% | 1.64 | 1.34 | 2.338 | 0.106 | **21.983** |
| **Q4 (Older)** | 341 | ≥55 | 76.79% | 2.01 | 1.62 | 2.142 | 0.250 | **8.558** |

---

## Summary of Spectral Changes

| Property | Observation |
| :--- | :--- |
| **PC1% across quartiles** | Range: 68.8% (Q2) – 86.6% (Q1); non-monotonic |
| **Effective Rank** | Range: 1.59 (Q1) – 2.28 (Q2); Q2 uniquely multidimensional |
| **PR** | Range: 1.31 (Q1) – 1.90 (Q2); consistent with Eff. Rank |
| **λ₁ (dominant eigenvalue)** | Q1=3.92, Q2=0.61, Q3=2.34, Q4=2.14; Q2 dramatically lower |
| **Anisotropy** | Q1=27.75 (extreme), Q2=6.04 (lowest), Q3=21.98 (high), Q4=8.56 |

**Critical structural observation**: Q2 (ages 27–39) is a distinct geometric outlier:  

- Lowest PC1% (68.8%)  
- Highest Effective Rank (2.28)  
- Lowest λ₁ (0.607) — 6.4× lower than Q1  
- Lowest anisotropy (6.04) — 4.6× lower than Q1  

This indicates that the mid-adult cohort (27–39) has a markedly more distributed, lower-anisotropy geometry compared to the young and older quartiles.

Stage 7 (`AGE_INVARIANT_CONTINUUM`) confirmed that cluster topology is age-invariant. This block confirms that **spectral geometry (eigenvalue amplitude, anisotropy) is NOT age-invariant**.

---

## Formal Verdict

> **AGE_GRADIENT_GEOMETRY**

Spectral properties (λ₁, anisotropy, Effective Rank) vary substantially across age quartiles. The population does not form discrete clusters, but the eigenvalue structure is age-differentiated. The Q2 (middle-low) quartile shows a distinct spectral regime.
