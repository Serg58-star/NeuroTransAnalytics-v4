# Task 49.1A — Implementation Plan (Robust Standardization Amendment)

**Version:** v1.1
**Date:** 2026-03-01

## 1. Goal Description

To implement the **Robust Standardization Amendment (Task 49.1A)** into the existing `v5-dual-space-architecture`. The primary objective is to eliminate scale domination of high-variance channels by formally injecting a **Robust Z-layer** between the Primary Physiological Raw Space (Level I/II) and the Analytical Orthogonal Space (Level III). This transforms the geometric representation into a dimensionless space ($R^{(Z)}$) based on Median and MAD.

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule, **explicit written approval** is required before modifying `dual_space_core.py` to implement these changes.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 49.1A v1.1"**

## 3. Proposed Changes

### [MODIFY] `src/stage9A_v5_architecture/dual_space_core.py`

The space transition logic will be modified to accommodate the new Stage 2.

#### 1. Level II.5: Robust Standardization Layer (NEW)

Introduce `compute_robust_z_layer(robust_space)`:

- Computes $Z_{X,F} = (X_F - \tilde{X}) / MAD_X$
- Where $\tilde{X} = median(X_L, X_C, X_R)$ (the channel median across all fields).
- Handles edge cases where $MAD_X$ might be 0 to prevent division by zero errors.

#### 2. Level III: Analytical Space Modification

Update `compute_analytical_space(z_space)`:

- Previously accepted robust medians in ms. It will now accept the $Z_{X,F}$ scores.
- $Center_X^{(Z)} = (Z_{X,L} + Z_{X,C} + Z_{X,R}) / 3$
- $Lat_{X,L}^{(Z)} = Z_{X,L} - Z_{X,C}$
- $Lat_{X,R}^{(Z)} = Z_{X,R} - Z_{X,C}$

#### 3. Level VI & VII: Modulator and Severity Modifications

Update `compute_global_modulator` and the analytical structure to explicitly document that $G$ and $Severity$ are derived entirely from the dimensionless $Z$-space coordinates.

#### 4. Phase 2 Independent Processing

Update the conceptual pipeline for Phase 2 operator:

- Ensure the code allows independent processing of $F2$ through the entire pipeline: $Raw_{F2} \rightarrow Robust_{F2} \rightarrow Z_{F2}$.
- Refactor `apply_load_operator` to calculate the analytical delta $\Delta Z = Z_{F2} - Z_{F1}$ instead of simply augmenting the Phase 1 base medians.

### [MODIFY] `src/stage9A_v5_architecture/tests/test_v5_dual_space.py`

- Add synthetic assertions demonstrating that `Z-score` eliminates the scale dominance of channels designed with artificially large synthetic variance.
- Test the new independent processing of the Phase 2 simulation.

## 4. Verification Plan

1. **Dimensionality Test:** Assert that all values entering the Analytical step are statistically dimensionless $Z$-scores bounded approximately within $[-3, 3]$ margins for typical non-burst trials.
2. **Phase 2 Invariant:** Run sequential Phase 1 and Phase 2 data and verify that modifying the load ($\lambda$) explicitly expands the $MAD$ dispersion vector, preventing variance collapse.
3. **Execution:** Full clean run of `pytest src/stage9A_v5_architecture/tests/`.
