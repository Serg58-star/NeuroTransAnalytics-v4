# Task 51 — Implementation Plan (Severity Calibration v5)

**Version:** v1
**Date:** 2026-03-01

## 1. Goal Description

To calibrate the v5 Severity Index utilizing the geometrically locked $Z$-Space Population coordinates. This involves replacing standard mean vectors with a **Robust Centroid (MCD)** and calculating the corresponding Mahalanobis distance ($D_M$). We will then map these distances into 5 Radial Zones (Core, Stable Norm, Extended Norm, Peripheral Deviation, Extreme Deviation) and extensively stress-test the model against heavy-tail variance injections and synthetic physiological bursts.

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule, **explicit written approval** is required before execution of this calibration plan.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 51 v1"**

## 3. Proposed Changes

### [NEW] `src/stage9A_v5_architecture/validation/task_51_severity_calibration.py`

#### 1. Robust Centroid & Covariance Mapping

- Extract synthetic $Z$-space coordinates ($N \ge 300$) using `generate_z_space_population()`.
- Implement Minimum Covariance Determinant (MCD) via `sklearn.covariance.MinCovDet`.
- Export $\mu_{MCD}$ (Center of Norm) and $\Sigma_{MCD}$ (Robust Covariance Matrix).

#### 2. Mahalanobis Distance (Severity Index)

- Calculate the robust Mahalanobis Distance for every subject in the generated population.
- $D_M = \sqrt{(Z - \mu_{MCD})^T \Sigma_{MCD}^{-1} (Z - \mu_{MCD})}$

#### 3. Radial Zone Stratification

- Stratify the $D_M$ distribution into empirical percentiles:
  - **Zone A** (Core): $\le 50th\%$
  - **Zone B** (Stable Norm): $50-75th\%$
  - **Zone C** (Extended Norm): $75-90th\%$
  - **Zone D** (Peripheral Deviation): $90-95th\%$
  - **Zone E** (Extreme Deviation): $>95th\%$

#### 4. Heavy-Tail Stress Test & Bootstrap Envelope

- **Bootstrap (k=1000):** Resample $Z$-space to map standard deviation ranges for $\mu_{MCD}$ and zone boundaries. Rule: $\le 5\%$ drift.
- **Heavy-Tail Stress:** Inject a highly skewed dataset (20% extreme tail, 30% frequency burst).
- Calculate proportional shift in established radial zones when subjected to stress.

#### 5. Continuum Preservation

- Re-run Silhouette $k$-means tests specifically tracking the spatial clustering of the 5 mapping zones.

### [NEW] `docs/v5/Task_51_Severity_Calibration_v5_Report.md`

- The script will export a fully formatted technical markdown report detailing the vector structures of $\mu_{MCD}$, zone boundaries, and the results of the stress tests.
- Status labeled as `LOCKED (Synthetic)` if all Failure Criteria are avoided.

## 4. Verification Plan

1. Create and execute `task_51_severity_calibration.py`.
2. Inspect the terminal log for the calculated centroid dimensions and the Zone boundaries.
3. Assert that when the heavy-tail injection hits the matrix, the Minimum Covariance Determinant effectively shields the geometric center defined by $\mu_{MCD}$, maintaining less than 10% structural deformation.
4. Verify the formal Markdown report for architectural clearance.
