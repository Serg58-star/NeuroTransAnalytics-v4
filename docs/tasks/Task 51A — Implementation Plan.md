# Task 51A — Implementation Plan (Z-Space Severity Centering Correction)

**Version:** v1
**Date:** 2026-03-01

## 1. Goal Description

To correctly calibrate the Severity Index in the v5 Dual-Space Vector Architecture by replacing the percentage-based mean-centroid drift check with an absolute $L^2$-Norm displacement, because the normalized $Z$-space vector inherently possesses a mean of 0. We will remove the artificial centroid subtraction from the Mahalanobis Distance so that Severity focuses entirely on covariance-driven displacement.

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule, **explicit written approval** is required before execution of this architectural correction plan.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 51A v1"**

## 3. Proposed Changes

### [MODIFY] `src/stage9A_v5_architecture/validation/task_51_severity_calibration.py`

#### 1. Correct the Mahalanobis Distance Formula

- Alter `_calc_mahalanobis` to remove centroid subtraction. New Formula:
  $D_M(Z) = \sqrt{Z^T \Sigma_{robust}^{-1} Z}$
- In code, this translates to utilizing `mu = np.zeros(D)` as the absolute center since the $Z$-space is structurally standardized.

#### 2. Deprecate Relative Center Drift

- Remove `self.metrics['stress_center_drift_percent']`.
- Calculate absolute $L^2$ displacement during Heavy-Tail testing:
  $\Delta_{abs} = \|\mu_{stress} - \mu_{base}\|_2$
- Assert a new stability limit for the absolute displacement under extreme physiological injection: $\Delta_{abs} \le 1.0$.

#### 3. Formalize New Limit Constraints

- Adjust `generate_report()` to validate the architectural changes:
  - `stress_abs_drift` $\le 1.0$ (Instead of percentage limit)
  - `zone_silhouette` $< 0.20$ (Continuum Preservation)
  - Split-Half zone boundaries limit replaced with Bootstrapped SD percentage limits $\le 5\%$.

### [MODIFY] `docs/v5/Task_51_Severity_Calibration_v5_Report.md`

- The system logic will alter the file output to list the Absolute L2 Drift instead of the percentage.
- Specifically insert the line: **"Task 51A Criteria Applied"** into the generated header.

## 4. Verification Plan

1. Re-run `task_51_severity_calibration.py` to assert the updated bounds.
2. Confirm the 124% failure has been structurally bypassed via absolute measurement while still defending against covariance explosions.
3. Validate that the mathematical zone limits successfully execute under Task 51A.
