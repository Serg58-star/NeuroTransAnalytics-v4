# H3.1 Block 2 — F1 Spectral Geometry

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.1 — F1 Cross-Model Comparison

---

## Scope

Eigen-decomposition of the raw covariance matrix (measured in actual ms variance, without standard scaling) of the 3D F1 space to quantify the structural dimensionality gap identified in Block 1.

## Raw Covariance Spectral Metrics

| Metric | Empirical F1 Space (3D) | Synthetic v5 F1 Space (3D) |
| :--- | :---: | :---: |
| **Effective Rank** | **1.26** | **2.90** |
| **PC1% Variance** | 95.07% | 45.76% |
| **λ₁ (Primary Amplitude)**| 6038 | 6751 |
| **λ₂** | 175 | 4053 |
| **λ₃** | 137 | 3949 |

## Structural Diagnosis

The divergence is absolute.
Because the historically measured left, center, and right F1 baseline fields are almost perfectly correlated (r = 0.93), the empirical 3D spatial geometry immediately collapses into a **singular 1D axis** (PC1=95%, Eff.Rank=1.26). This primary axis (λ₁≈6000) absorbs nearly all physiological variance.

In contrast, because the v5 generator modelled spatial positions (Left/Right/Center) with independent noise distributions lacking a locked central global driver, its geometry remained highly isotropic and nearly perfectly spherical (λ≈6700, 4000, 3900), utilizing almost all 3 available dimensions (Eff.Rank=2.90).

*(Note: The Effective Ranks seen in Stage H2.2 (≈6.5) were driven entirely by the addition of the Load and Lateralization axes. When looking at Baseline alone, the space is a 1D line).*

---

## Formal Conclusion

At the fundamental baseline level, the architectures do not align structurally. The empirical baseline represents a single global unified physiological speed factor. The synthetic architecture erroneously generates uncorrelated multi-dimensional local channel delays.
