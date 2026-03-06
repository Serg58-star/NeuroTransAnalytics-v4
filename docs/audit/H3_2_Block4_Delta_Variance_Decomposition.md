# H3.2 Block 4 — Variance Decomposition (Δ-Space)

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.2 — Δ-Space Cross-Model Comparison

---

## Scope

Comparison of Total Variance Partitioning (Between vs Within) for the most restrictive and demanding transition: ΔV5 (Shift Load). How much variance is theoretically predictable by demographics?

## Variance Decomposition (ΔV5 Transition)

| Component | Empirical ΔV5 | Synthetic v5 ΔV5 |
| :--- | :---: | :---: |
| **Between-Sex Variance Share** | **0.02%** | **0.14%** |
| **Between-Age Variance Share** | **0.07%** | **2.10%** |
| **Residual Heterogeneity** | > **99.9%** | ~ **97.7%** |

## Structural Diagnosis

In reality (Empirical), predicting how much absolute penalty (in ms) a subject will suffer when integrating cognitive shifts (ΔV5) is **entirely disconnected** from their basic demographic profile (Sex/Age explain < 0.1% of the mean-shift variance). The transition penalty is an intensely individual state-metric (Residual > 99.9%).

The synthetic v5 architecture artificially links Baseline demographic curves to transition scaling, erroneously shifting 2.10% of total variance into age-predictions.

While statistically both systems rely immensely on residual individual differences (>97%), v5 conceptually breaks the functional boundary by embedding demographic baseline differences into functional cognitive load penalties.

---

## Formal Conclusion

The severity metrics for state-transitions (Δ) should not be linearly compounded onto the baseline demographic curve, as empirical Functional Load is 99.9% distinct from age/sex means.
