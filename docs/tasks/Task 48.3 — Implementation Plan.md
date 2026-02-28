# Task 48.3 — Implementation Plan (Methodological Corrections to Task 48.2)

## Усиление контроля ложноположительных результатов и вычислительной устойчивости

**Version:** v1
**Date:** 2026-02-25

### 1. Goal Description

To amend the Implementation Plan for Task 48.2 (Extended Microdynamics) by injecting strict methodological safeguards: Negative Control Scenarios to estimate False Positive Rates (FPR), a robust fallback hierarchy for MixedLM non-convergence, and stringent constraints on AIC/BIC model comparisons. This guarantees that complex models do not hallucinate interactions or non-linearities and that the final verdict on the database's micro-level exhaustion is statistically bulletproof.

### 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule and Task 48.3 instructions, **explicit written approval** is required before execution of these microdynamic models.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 48.3 v1"**

### 3. Proposed Changes

#### Amendment to Phase 1 (Synthetic Generator)

- **Negative Controls:** The synthetic generator (`synthetic_microdynamics_extended.py`) must be capable of running two null-hypothesis scenarios:
  - **(A) Zero-Interaction Scenario**: Generator coefficient for `log(PSI) × Position` is strictly 0.
  - **(B) Zero-Nonlinearity Scenario**: Generator coefficients for `Position^2` and `log(PSI)^2` are strictly 0.

#### Amendment to Phase 2 (Validation)

- **FPR Estimation**: The validation script must run 100+ iterations (or a statistically sufficient robust check) of the Negative Controls to empirically calculate the False Positive Rate for detecting interactions and non-linearities. It must assert that `FPR ≈ 5%` (at $\alpha=0.05$) before proceeding.
- **MixedLM Fallback Strategy**: Implement a strict `try-except` fallback hierarchy for statsmodels MixedLM logic:
  1. Full model: `RT ~ log(PSI) + Position + (log(PSI) + Position | Subject)`
  2. Fallback 1: `RT ~ log(PSI) + Position + (Position | Subject)`
  3. Fallback 2: Random Intercept model `RT ~ log(PSI) + Position + (1 | Subject)`
  - The script must log warnings if Fallback 1 or 2 is triggered due to singularity/non-convergence.

#### Amendment to Phase 3 (Real Data Execution)

- **AIC/BIC Constraints**: Enforce a programmatic check ensuring AIC/BIC are only compared across models predicting the exact same dependent variable (`RT`) on the exact same dropped-NaN indices.

#### Amendment to Phase 4 (Reporting)

- The target document `docs/project_engineering/Microdynamic_Extended_Analysis_Task48_2.md` will now explicitly contain:
  - **Synthetic FPR Validation**: Proof that the pipeline does not hallucinate effects.
  - **MixedLM Execution Path**: Documentation of which fallback was triggered if any.
  - **AIC/BIC Tables**: With disclaimers confirming nested/identical-data validity.
  - **Final Exhaustion Assessment**: A non-declarative, numerically justified verdict clearly separating proven effects, absent effects, and methodological walls, answering the ultimate question of whether the `neuro_data.db` micro-layer is exhausted.

### 4. Verification Plan

- **Synthetic Negative Control Check**: Run Negative Control A and B. Assert that the resulting p-values for interaction/non-linearity are uniformly distributed, confirming a ~5% FPR.
- **MixedLM Convergence Check**: Ensure the script successfully downgrades to a simpler random-effects structure if a Singular Matrix error is encountered.
