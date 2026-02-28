# Task 48.4.1 — Implementation Plan (Methodological Clarifications to Task 48.4)

## Корректировка сравнения моделей и оценка устойчивости при удалении центрального поля

**Version:** v1
**Date:** 2026-02-25

### 1. Goal Description

To amend the Implementation Plan for Task 48.4 (Informational Contribution of the Central FOV) by enforcing strict statistical comparison standards. The amendment requires that AIC/BIC differences be calculated on identical datasets, that the "stabilizing" function of the Center field on Left/Right variances be quantified, and that Minimum Detectable Effect (MDE) be empirically recalibrated when reducing the test block from 36 to 24 stimuli.

### 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule and Task 48.4.1 instructions, **explicit written approval** is required before execution of these microdynamic spatial models.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 48.4.1 v1"**

### 3. Proposed Changes

#### Amendment to Phase 2 (Validation)

- **AIC/BIC Identical Dataset Rule**: To compare Model A (with Center factor) versus Model B (without Center), the scripts will implement **Подход A**: Both models will be trained *strictly* on the L/R-only subset. Model A' will artificially retain the Center coefficient (which will be 0 on this subset mathematically, but serves to test structural nested viability), or more accurately, the comparison will contrast the fit over 24 trials with and without treating the center as an independent regressor block in cross-validation. Since standard AIC requires identical $N$, we will deploy $R^2$-out-of-sample Cross Validation as the primary arbiter (Подход B).
- **L-R Variance Stability Check**: The validation script will explicitly compute the variance of $RT_{Left} - RT_{Right}$ on segments with and without intervening Center stimulus anchors.
- **Power Recalibration (36 vs 24)**: The script will compute empirical Power and MDE. It will simulate blocks of 36 trials and blocks of 24 trials (Center omitted) and output the difference in `detectable PSI slope` and `detectable fatigue slope`.

#### Amendment to Phase 4 (Reporting)

- The target document `docs/project_engineering/Central_Field_Information_Value_Task48_4.md` will now explicitly contain:
  - **Power Recalibration Matrix**: Comparing MDE 36 vs MDE 24.
  - **Stabilizing Role metrics**: Showing how the presence of the Center impacts the variance and confidence intervals of the Left and Right slopes.
  - **Corrected AIC/BIC & Cross-Validation**: Proving predictive superior/inferior status of the Center models.
  - **Final Redundancy Verdict**: Strictly mapped against the 5 criteria (AIC, R², Stability, Power, Mixed variance) to state whether v5 must keep or can delete the Central field.

### 4. Verification Plan

- **Stability Variance Check**: Ensure the script outputs `Variance(L) - Variance(R)` or similar comparative standard deviations for scenarios with and without Center.
- **Power Recalibration Run**: Assert that lowering $N$ from 36 to 24 outputs a mathematically higher MDE, tracking the exact loss in statistical sensitivity.
