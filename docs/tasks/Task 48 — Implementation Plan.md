# Task 48 — Implementation Plan

## Реализация микродинамических сценариев B1 и A2 (PSI Recovery & Temporal Reallocation)

**Version:** v1
**Date:** 2026-02-25

### 1. Goal Description

The objective is to operationalize exploratory scenarios B1 (PSI Recovery Response) and A2 (Temporal Reallocation/Intra-block fatigue) to investigate the microdynamic behavior of Reaction Time (RT) inside individual 36-trial test blocks. This will address the unmined, non-aggregated trial-by-trial data layers of the historical test system.

### 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule and Task 48 instructions, **explicit written approval** is required before execution.
> Additionally, execution will strictly adhere to the `synthetic-data-first` and `no-real-data-until-approved` skills. Real data from `neuro_data.db` will not be touched until the analysis procedures are mathematically verified against synthetic models.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 48 v1"**

### 3. Proposed Changes & Methodology

To comply with the architectural guardrails, implementation is strictly divided into Synthetic and Real phases.

#### Phase 1: Synthetic Data Generation (C3.X Layer)

**[NEW]** `src/c3x_exploratory/synthetic_microdynamics_b1_a2.py`

- Generate mock trial-level data (N subjects = 50, 3 tests * 36 trials).
- Embed known Ground Truth effects:
  - **B1 Effect**: `RT = base_rt - recovery_factor * log(PSI) + noise` (Longer PSI creates faster RT).
  - **A2 Effect**: `RT = base_rt + fatigue_slope * Position + noise` (Slower RT over 36 trials).
  - Include conditional `anti-CV` resets (RT artificially truncated and repeated if CV > 15%).

#### Phase 2: Procedure Validation (C3.X Layer)

**[NEW]** `src/c3x_exploratory/microdynamics_b1_a2.py`

- Build the exact regression models required:
  - Linear/Quadratic models for `RT ~ PSI`.
  - Linear/Piecewise models for `RT ~ Position (1-36)`.
- Apply to the generated synthetic data and verify that the procedures successfully recover the Ground Truth coefficients injected in Phase 1 without false positives.

#### Phase 3: Real Data Application

- **Only executed if Phase 2 validation succeeds.**
- Connect to `neuro_data.db`.
- Extract raw 36-trial sequences for Tst1, Tst2, and Tst3.
- Run the validated `microdynamics_b1_a2.py` models with stratification by color, field of view, and test block.
- Calculate subject-level slopes, p-values, R², and assess anti-CV impact.

#### Phase 4: Reporting

**[NEW]** `docs/project_engineering/Microdynamic_Analysis_B1_A2.md`

- Compile the numerical outputs, coefficient tables, and visual descriptions (if applicable) into the finalized report.
- Assess whether 36 stimuli are sufficient (A2) and the physiological reality of the PSI recovery curve (B1).

### 4. Verification Plan

- **Synthetic Validation Check**: The slopes extracted by the regression model on synthetic data must match the generator's Ground Truth parameters within a 95% Confidence Interval. Output the synthetic recovery metrics.
- **Real Data Integrity Check**: Confirm no aggregation artifacts are present by asserting input vectors always have length exactly 36 (or 36 + anti-CV repeats) prior to model fitting.
