# H3.1 Block 4 — Variance Decomposition (F1)

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.1 — F1 Cross-Model Comparison

---

## Scope

Total Variance Decomposition (TVD) of the global F1 proxy (`global_med` for empirical, mean-across-channels for synthetic) into demographic components.

## Variance Share Comparison

| Component | Empirical F1 Share | Synthetic v5 F1 Share |
| :--- | :---: | :---: |
| **Between-Sex Variance** | 0.32% | 1.90% |
| **Between-Age(Q) Variance** | 5.77% | 4.31% |
| **Residual Variance** | ~93.9% | ~93.8% |

## Structural Diagnosis

At the population summary level, both systems correctly allocate the vast majority of variance (~94%) to individual-level, non-demographic residual heterogeneity.

However, the v5 synthetic generator mathematically over-weights the linear effect-size of Sex on the absolute mean. The empirical model shows that while Sex creates massive differences in structural **variance/amplitude (λ₁ geometry)**, its impact on predicting the population **absolute mean** is trivial (< 0.5%).

v5 currently misaligns this: it imparts too much predictive mean-shift to gender, and drastically under-represents the volumetric covariance differences detailed in Block 3.

---

## Formal Conclusion

While the total residual share is aligned safely above 90%, the internal allocation of demographic variance between mean-shifts and covariance-shape is misconfigured in the synthetic model relative to empirical baseline reality.
