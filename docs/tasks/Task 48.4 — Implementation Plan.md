# Task 48.4 — Implementation Plan

## Информационный вклад центрального поля зрения (Quantitative Evaluation of Central FOV)

**Version:** v1
**Date:** 2026-02-25

### 1. Goal Description

To quantitatively evaluate whether the Central Field of View (FOV) provides independent, non-redundant information in the microdynamic models (B1, A2, Interaction). The historical architecture dedicated 33% of the stimulus budget (12 out of 36 trials per block) to the center. This task will determine if this 33% allocation is statistically justified or if it can be safely reallocated to Left/Right lateralized measurements in the upcoming v5 design without losing diagnostic power.

### 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule and Task 48.4 instructions, **explicit written approval** is required before execution.
> Execution will maintain strict adherence to the `synthetic-data-first` and `no-real-data-until-approved` skills.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 48.4 v1"**

### 3. Proposed Changes & Methodology

To comply with architectural guardrails, implementation is strictly divided into Synthetic and Real phases.

#### Phase 1: Synthetic Data Generation (C3.X Layer)

**[NEW]** `src/c3x_exploratory/synthetic_microdynamics_fov.py`

- Generate trial-level data with explicit `FieldOfView` metadata (Left, Center, Right).
- Inject Ground Truth spatial biases (e.g., Center yields faster RT than Periphery).
- Produce three parallel sub-datasets reflecting the scenarios:
  - **Scenario A (Full Sequence)**: L, C, R at 33% each.
  - **Scenario B (Center Removed)**: Only L and R trials are retained (simulating a 24-trial test).
  - **Scenario C (Center as Baseline Reference)**: A synthetic structure where L and R are defined as deviations from C.

#### Phase 2: Procedure Validation (C3.X Layer)

**[NEW]** `src/c3x_exploratory/microdynamics_fov_validation.py`

- Construct comparative pipelines:
  - **Model A**: `RT ~ FieldOfView + log(PSI) + Position + (FieldOfView * Position)`
  - **Model B**: Same as A but applied only to the subset where `FieldOfView` is strictly Left or Right.
- Evaluate $\Delta$AIC, $\Delta$BIC, and partial $R^2$ contribution of the `FieldOfView==Center` factor.
- Assess the variance of lateralization ($L - R$) with and without the central stabilization context.
- Assert that the procedure reliably calculates $\Delta$AIC and isolates the center's informational value without crashing or hallucinating.

#### Phase 3: Real Data Application

**[NEW]** `src/c3x_exploratory/real_microdynamics_fov.py`

- **Only executed if Phase 2 validation succeeds.**
- Connect to `neuro_data.db`, extract valid trials joining with metadata.
- Execute Scenarios A, B, and C on the historical cohort (Tst1, Tst2, Tst3).
- Apply robust HC3 errors to account for heteroskedasticity.

#### Phase 4: Reporting

**[NEW]** `docs/project_engineering/Central_Field_Information_Value_Task48_4.md`

- Compile all comparative metrics ($R^2$, AIC/BIC shifts).
- Report on how removing the center impacts the core temporal slopes (PSI recovery and Intra-block fatigue).
- Present the final determination answering:
  - Does the Center act as a necessary baseline anchor?
  - Does the Center possess its own unique deterioration profile?
  - Is the Center entirely redundant (i.e., its removal doesn't meaningfully affect the lateralized components)?
  - **Formal V5 Recommendation**: Must the Center remain, or can its 33% stimulus allocation be distributed to Left/Right?

### 4. Verification Plan

- **Synthetic Delta AIC Check**: The script must correctly compute and print the $\Delta$AIC difference between nested and non-nested structures under Scenarios A and B.
- **Robustness Check**: The analysis must stratify by test type (Tst1 vs Tst2 vs Tst3) as visual fields operate differently across simple vs. complex cognitive loads.
