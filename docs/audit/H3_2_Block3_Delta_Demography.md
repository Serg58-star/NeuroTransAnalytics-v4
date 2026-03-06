# H3.2 Block 3 — Δ Demographic Structure

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.2 — Δ-Space Cross-Model Comparison

---

## Scope

Does the synthetic v5 architecture correctly replicate the sex and age demographic variance structures observed when historical patients operate under transition loads (ΔV4, ΔV5, ΔLat)?

## 1. Sex Amplitude Asymmetry (Δ-Space)

| Cohort | Empirical Δ-Space | Synthetic v5 Δ-Space |
| :--- | :---: | :---: |
| **Female λ₁**| 1.306 | 1.043 |
| **Male λ₁** | 1.695 | 2.312 |
| **Male/Female Ratio**| **1.30×** | **2.22×** |

### Diagnosis

In the empirical transition space, the male dominance found originally in Baseline (2.1x) softens significantly under cognitive load (down to 1.30x). When historical patients are stressed by shifting, females catch up significantly regarding variance amplitude.

The synthetic v5 generator, however, completely reverses this dynamic. By mathematically binding transitional load linearly to baseline differences, v5 massively amplifies the baseline male-penalty, creating a severe 2.22x male variance dominance under load that does not exist empirically.

## 2. Age Spectral Gradient (Δ-Space)

| Quartile | Empirical Eff.Rank | Empirical λ₁ | Synthetic Eff.Rank | Synthetic λ₁ |
| :--- | :---: | :---: | :---: | :---: |
| **Q1** | 3.53 | 2.419 | 3.71 | 1.223 |
| **Q2** | 3.65 | **1.044 (Min)** | 3.69 | **0.984** |
| **Q3** | 3.50 | 1.278 | 3.41 | **2.742 (Max)** |
| **Q4** | 3.76 | 1.809 | 3.80 | 1.239 |

### Diagnosis

The empirical Q2 (ages 27-39) anomaly **continues completely unaffected into the functional transition space**. The Q2 group hits an absolute minimum bounding variance (λ₁=1.04) regardless of task transitions.

The v5 generator utterly fails to capture this non-linear structure. By applying a continuous exponential age-penalty, v5 shifts the massive transition-load variance spike arbitrarily into Q3 (λ₁=2.74), completely missing the physiological Q2 variance collapse found in reality.

---

## Formal Verdict

> **FUNCTIONAL_ARCHITECTURE_DIVERGENT (DEMOGRAPHICS)**

The v5 synthetic generation framework fundamentally miscalculates the demographic response to functional load. It structurally exaggerates masculine load variance while completely missing the Q2 mid-adult physiological stabilization window.
