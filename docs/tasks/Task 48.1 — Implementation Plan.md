# Task 48.1 — Implementation Plan (Amendment to Task 48)

## Добавление проверки статистической мощности и гетероскедастичности

**Version:** v1
**Date:** 2026-02-25

### 1. Goal Description

To amend the Implementation Plan for Task 48 (Microdynamic Scenarios B1 & A2) by incorporating mandatory statistical rigor layers: Power Analysis on synthetic data and Heteroskedasticity Diagnostics on regression residuals. This ensures sample sizes are sufficient to detect the hypothesized effects and that variance assumptions do not invalidate the findings.

### 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule and Task 48.1 instructions, explicit written approval is required before this amended implementation plan is adopted for execution.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 48.1 v1"**

### 3. Proposed Changes

#### Amendment to Phase 1–2 (Synthetic Validation Layer)

- **Power Estimation on Synthetic Data:**
  - Enhance `src/c3x_exploratory/microdynamics_b1_a2.py` to include a Power Analysis module.
  - Calculate empirical Power (1 - β) for varying signal-to-noise ratios (varying `fatigue_slope` and `recovery_factor`).
  - Calculate the Minimum Detectable Effect (slope) at α = 0.05, N = 50.
  - Assert whether the N=50 historical cohort size is sufficient for intra-block drift detection.

#### Amendment to Phase 2–3 (Regression Validation Layer)

- **Heteroskedasticity Diagnostics:**
  - Enhance the regression extraction pipeline to run the Breusch-Pagan test (and fallback White test) on the residuals of all `RT ~ PSI` and `RT ~ Position` models.
  - If heteroskedasticity is detected (e.g., variance of RT increases with intra-block fatigue), the pipeline must automatically compute and report **HC3 robust standard errors**.

#### Amendment to Phase 4 (Reporting)

- The target document `docs/project_engineering/Microdynamic_Analysis_B1_A2.md` will now explicitly contain:
  - **Power Analysis Section**: Table of detectable slopes and power curves.
  - **Heteroskedasticity Section**: Diagnostics report, Breusch-Pagan p-values, and comparisons of standard vs. robust p-values for main effects.

### 4. Verification Plan

- **Synthetic Power Check:** The scripts must output the minimum `detectable slope` alongside the standard estimations.
- **Residual Diagnostics Check:** Ensure the statistical pipeline logs Breusch-Pagan p-values for every fitted macro-model. Ensure HC3 errors are supplied alongside standard errors when variance inflates.
