# H3.1c Block 0 — Global Baseline Factor Extraction

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.1c — Correlated Motor Layer Simulation Audit

---

## Scope

Isolation of the primary global speed scalar from the empirical 3D baseline (L, C, R) to serve as the generative factor for latent motor simulation.

## Global Factor (PC1) Extraction

A Principal Component Analysis was run on the deduplicated empirical F1 Baseline space (N=1482).

| Metric | Result |
| :--- | :--- |
| **Eff.Rank of Raw Space** | **1.26** |
| **PC1 % of Total Variance** | **95.07%** |
| **Global Factor Variance (λ₁)**| **6038.8 ms²** |

### Channel Loadings

The correlation between the individual spatial channels and the extracted Global Factor (`G_i`) confirms that the empirical space is overwhelmingly dominated by a single, global speed parameter:

* **Left vs G**: r = 0.978
* **Center vs G**: r = 0.973
* **Right vs G**: r = 0.974

## Conclusion

The extraction of `G` was highly successful, representing the near-perfect fusion of left, center, and right baseline responses into a singular global speed baseline capable of seeding heavily-correlated motor time simulations.
