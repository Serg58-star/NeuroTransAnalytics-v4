# Task 49.1 — Implementation Plan

**Version:** v1
**Date:** 2026-03-01

## 1. Goal Description

To implement the **Dual-Space Vector Architecture** for v5 as specified in `Task_49_1_Dual_Space_Vector_Architecture.md`, ensuring absolute adherence to the defined architectural invariants. The implementation will structurally separate the **Robust Estimation Layer** (Level I) from the **Analytical Orthogonal Space** (Level III) and explicitly model the **Global Modulator**. This plan defines the modules, data pipelines, and logic paths for establishing `v5-dual-space-architecture`.

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule and Task 49.1, **explicit written approval** is required before code execution.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 49.1 v1"**

## 3. Proposed Changes

### Data Structure and Directory Setup

#### [NEW] `src/stage9A_v5_architecture/`

To isolate v5 logic from v4 exploratory models, create a new directory for v5 dual-space logic.

#### [NEW] `src/stage9A_v5_architecture/dual_space_core.py`

Will contain the data classes and computation logic for the vector spaces.

### Level I & II: Robust Estimation Layer & Raw Space

#### [NEW] `compute_robust_layer(trials_df)`

- Implements robust estimation using `median` and `MAD` (Median Absolute Deviation) over 12 trials per visual field (`L`, `C`, `R`).
- Strict mapping for 4 channels: `V1`, `Parvo`, `Magno`, `Koniocellular`.
- Rule Enforcement: No log transformations, no trimming, no mean RT.
- Returns `R_raw` vector $\in \mathbb{R}^{12}$ representing the Primary Physiological Raw Space coordinates.

### Level IV: Local Donders Application

#### [NEW] `apply_local_donders(robust_metrics)`

- Subtraction logic exclusively applied *within* a specified field (e.g., $M_L - V1_L$) without affecting multi-field geometry, eliminating cross-field multicorrelation.

### Level III: Analytical Orthogonal Space

#### [NEW] `compute_analytical_space(robust_layer_output)`

- Geometric Aggregation: `Center_X = (X_L + X_C + X_R) / 3` (applied strictly to robust medians, not raw RTs).
- Lateralization Coordinates: Evaluated as `Lat_X_L = X_L - X_C` and `Lat_X_R = X_R - X_C`.

### Level V & VII: Global Modulator & Phase 2 Operator

#### [NEW] `compute_global_modulator(analytical_vectors, variance_weights)`

- Models the system covariance component explicitly: $G = \alpha_1 V1 + \alpha_2 P + \alpha_3 M + \alpha_4 K$.

#### [NEW] `apply_load_operator(R_F1, lambda_load, d_sensitivity)`

- Implements the Phase 2 State transition as a linear vector operator: $R_{F2} = R_{F1} + \lambda \cdot d$.

## 4. Verification Plan

### Automated Tests (Synthetic Validation)

**[NEW]** `src/stage9A_v5_architecture/tests/test_v5_dual_space.py`

- Setup synthetic datasets strictly enforcing heavy-tail/burst distribution properties to test the logic paths.
- **Execution:** `pytest src/stage9A_v5_architecture/tests/test_v5_dual_space.py`
- **Assertions:**
  1. The Robust Layer yields correct Median/MAD and completely ignores the mean RT of the simulated bursts.
  2. The Physiological vector $R$ is strictly returned as 12-dimensional logic mapping.
  3. `Center_X` matches the mathematical mean of the robust medians.
  4. The Phase 2 transition behaves linearly on the robust coordinates per the $\lambda \cdot d$ operator model.

### Analytical Invariant Check

The test suite will validate that Donders subtractions never bleed across Left, Center, and Right visual fields (`L`, `C`, `R` independently processed), resolving v4 multicollinearity.
