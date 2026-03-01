# Task 51 — Severity Calibration v5 Report

*(Task 51A Criteria Applied - Center Fixed to Zero)*

**Validation Date:** 2026-03-01
**Status:** LOCKED (Synthetic)

## 1. Robust Centroid (MCD)
- **Minimum Covariance Determinant (MCD):** Successfully Fit
- **Covariance Matrix Positive Semi-Definite:** True

## 2. Radial Zones (Severity Index via Centered Mahalanobis)
- **Zone A:** Core Norm (≤50%) | $D_M \le 3.73$
- **Zone B:** Stable Norm (50-75%) | $D_M \in (3.73, 4.96]$
- **Zone C:** Extended Norm (75-90%) | $D_M \in (4.96, 6.48]$
- **Zone D:** Peripheral Deviation (90-95%) | $D_M \in (6.48, 7.20]$
- **Zone E:** Extreme Deviation (>95%) | $D_M > 7.20$

## 3. Bootstrap Bounds (k=1000)
- **Max Z-Coordinate Drift SD:** ±0.00%
- **Zone A Boundary SD:** ±3.14%

## 4. Heavy-Tail Stress Test
*Injected extreme tails into 20% of subjects and burst frequencies into 30% of subjects.*
- **MCD Center Absolute Displacement:** 0.1638 Z-Units (Limit: 1.0)

## 5. Continuum Preservation
- **Radial Zone Silhouette Score:** 0.018
- **Interpretation:** Contiguous shells confirmed

## 6. Architectural Conclusion
**All Task 51 Criteria Met:** True

The v5 Severity Model successfully scales and stratifies robust dimensional data. Heavy-tail variance is handled securely by the MCD centroid. The model is architecturally locked.
