# Task 48.2 — Implementation Plan (Extended Microdynamics)

## Расширение микродинамического анализа (нелинейность, взаимодействия, межсубъектная вариативность)

**Version:** v1
**Date:** 2026-02-25

### 1. Goal Description

The objective of Task 48.2 is to deepen the microdynamic analysis of the historical `neuro_data.db` dataset by exploring non-linear recovery effects, non-linear intra-block fatigue, PSI × Position interactions, and inter-subject slope variability (via Mixed-Effects modeling and Clustering). This will determine if there are distinct sub-populations of attention dynamics within the historical cohort.

### 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule and Task 48.2 instructions, **explicit written approval** is required before execution.
> Execution will maintain strict adherence to the `synthetic-data-first` and `no-real-data-until-approved` skills.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 48.2 v1"**

### 3. Proposed Changes & Methodology

To comply with architectural guardrails, implementation is strictly divided into Synthetic and Real phases.

#### Phase 1: Synthetic Data Generation (C3.X Layer)

**[NEW]** `src/c3x_exploratory/synthetic_microdynamics_extended.py`

- Enhance the previous synthetic generator to inject specific advanced Ground Truths:
  - **Interaction**: non-zero coefficient for `log(PSI) × Position`.
  - **Non-Linearity**: inject a quadratic component to Position ($Position^2$) indicating accelerating fatigue.
  - **Mixed-Effects**: subject-specific random intercepts and random slopes (some subjects fatigue faster, some slower).
  - **Clusters**: artificially spawn 2 distinct clusters of subjects (e.g., "fast-fatigue" vs "resilient").

#### Phase 2: Procedure Validation (C3.X Layer)

**[NEW]** `src/c3x_exploratory/microdynamics_extended_validation.py`

- Build the exact advanced models required:
  - Interaction OLS: `RT ~ log(PSI) + Position + log(PSI) × Position` (with HC3 robust errors).
  - Non-linear OLS: `RT ~ log(PSI) + log(PSI)^2` and `RT ~ Position + Position^2`.
  - Mixed-Effects: `RT ~ log(PSI) + Position + (log(PSI) + Position | Subject)` (using `statsmodels.regression.mixed_linear_model.MixedLM`).
  - Clustering: Extract empirical slopes per subject and run `KMeans` with silhouette scoring.
- Assert that these procedures retrieve the generated Ground Truths without false positives on the purely synthetic dataset.

#### Phase 3: Real Data Application

**[NEW]** `src/c3x_exploratory/real_microdynamics_extended.py`

- **Only executed if Phase 2 validation succeeds.**
- Connect to `neuro_data.db`, extract valid trials joining with metadata (similar to Task 48).
- Run the validated advanced models, stratified by Tst1, Tst2, and Tst3.
- Output all numerical arrays, AIC/BIC comparisons, and p-values (adjusted via FDR where comparing multiple conditions).

#### Phase 4: Reporting

**[NEW]** `docs/project_engineering/Microdynamic_Extended_Analysis_Task48_2.md`

- Compile numerical outputs into the finalized report.
- Address whether recovery interacts with fatigue.
- Address whether fatigue accelerates (quadratic) or is purely linear.
- Describe the distinct dynamic profiles (clusters) discovered in the population.
- Deliver the final verdict on whether the micro-level `neuro_data.db` is completely exhausted prior to v5 design.

### 4. Verification Plan

- **Synthetic Recovery Check**: The Advanced scripts must correctly identify non-linear parameters, significant interaction p-values, and recover the 2 injected clusters with high silhouette scores on the synthetic standard.
- **Real Data Execution**: Assert robust standard errors are maintained, and valid AIC/BIC comparisons are explicitly printed for model selection (e.g., Linear vs Quadratic vs Piecewise).
