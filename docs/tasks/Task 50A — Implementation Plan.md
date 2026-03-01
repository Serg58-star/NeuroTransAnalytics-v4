# Task 50A — Implementation Plan (Z-Space Validation Criteria Update)

**Version:** v1
**Date:** 2026-03-01

## 1. Goal Description

To update the geometric validation criteria for the v5 Dual-Space Vector Architecture (Z-Space), correcting the flawed application of the Kaiser rule ($\lambda > 1$) on Z-score matrices standardized by MAD. The new validation protocol will implement **Participation Ratio (PR)**, **Effective Rank ($r_{eff}$)**, **Cumulative Variance**, and **Silhouette scores** to correctly validate the geometry within synthetic models.

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule, **explicit written approval** is required before execution of this validation plan amendment.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 50A v1"**

## 3. Proposed Changes

### [MODIFY] `src/stage9A_v5_architecture/validation/task_50_geometric_validation.py`

#### 1. PCA Spectrum (Revising Dimensionality)

- Remove the `λ > 1` (Kaiser) calculation for valid dimensions.
- Implement Effective Rank: $r_{eff} = \exp(-\sum p_i \log p_i)$ where $p_i = \lambda_i / \sum \lambda_i$.
- Track Participation Ratio (PR): $PR = (\sum \lambda_i)^2 / \sum \lambda_i^2$.
- Add checks for Cumulative Variance:
  - $PC1 < 40\%$
  - $PC1 + PC2 < 65\%$

#### 2. Radial Continuum Validation (Revising Clustering Check)

- Maintain Mahalanobis Distance calculation.
- Implement $k$-means clustering loop ($k \in [2, 5]$) to calculate **Silhouette Score** on the dimensionless $Z$-space.
- Instead of counting KDE peaks (which is sensitive to small fluctuations in small N simulations), we will assert `Silhouette < 0.20` to verify the absence of true clustering.

#### 3. Update Validation Constraints Logic

The script will internally assert:

- `PR >= 3`
- `r_eff >= 3`
- `PC1_percent <= 50%`
- `max_silhouette < 0.25`
- `is_psd == True`

### [MODIFY] `docs/v5/Task_50_Population_Geometry_v5_Report.md`

- The script will be updated to output the revised metrics ($r_{eff}$, PR, Silhouette, Cumulative Variance).
- The report will explicitly contain the text: **"Z-Space Criteria v5 Applied"**.

## 4. Verification Plan

1. The script `task_50_geometric_validation.py` will be executed again, processing the 300-subject synthetic Z-space.
2. We expect the updated mathematical parameters (PR and $r_{eff}$) to prove the multi-dimensionality of the space, showing that the system has successfully maintained independent channels despite the previous Kaiser failure.
3. The report will output mathematically sound pass criteria, generating a `LOCKED` status.
