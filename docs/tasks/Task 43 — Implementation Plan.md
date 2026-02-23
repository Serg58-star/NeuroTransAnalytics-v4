# Task 43 — Implementation Plan for Real Longitudinal Dataset Integration

## Stage 9B Functional Monitoring Framework v1

## NeuroTransAnalytics-v4

**Version**: v1
**Date**: 2026-02-23

---

# 1. Goal Description

This plan outlines the steps to empirically validate the Stage 9B Functional Monitoring Framework v1 by integrating real longitudinal session data from `neuro_data.db`. The goal is to perform an observational evaluation of longitudinal stability classification behaviour, classification distribution, gating behaviour, and noise robustness.

This implementation will strictly adhere to the non-negotiable architectural constraints, including no mutation of C3-Core, no PCA recalculation, and no Stage 9A fluctuation logic modifications.

---

# 2. User Review Required

> [!CAUTION]
> **Governance Rule Enforcement**:
> GoAn requires explicit approval of this specific Implementation Plan ("Approved for implementation. Reference: Task 43 v1") before writing any code or modifying the `src/stage9B_functional_monitoring/` directory for this task.

---

# 3. Proposed Changes

All structural evaluations and logic within the monitoring framework remain untouched (`monitoring_metrics.py`, `deterministic_logic.py`, `clinical_translator.py`). The only changes will be the addition of a new experimental validation script.

### [NEW] `src/stage9B_functional_monitoring/experiments/longitudinal_integration_run.py`

This script will:

- Connect to `neuro_data.db`.
- Query subjects with $\ge 3$ distinct sessions and valid 3D latent coordinates ($M_t, \Delta S_t, \Delta L_t, \Delta T_t$).
- Construct chronological longitudinal sequences.
- Compute the required fluctuation metrics ($r_t, Z(r_t), Z(\Delta M_t), Z_{cum}, Z_{var}$) strictly using the locked normative variance structures inherited from Stage 9A v1. No variance re-estimation, no covariance recalculation, and no threshold adaptation is permitted.
- All fluctuation Z-scores must reference the original frozen normative parameters defined in Stage 9A. The longitudinal subset must not be used to derive or adjust statistical scale parameters.
- Feed sequences into the `MonitoringMetricsEvaluator` and `DeterministicLogicEvaluator`.
- Aggregate distributions across the population (Stable %, Volatile %, Directionally shifting %, Expanding boundary %).
- Perform the required audits: Escalation Frequency, Consecutive Gating verify, and Radial Bias.
- Run a 5% Gaussian noise robustness test and compare identical classification rates.
- Automatically generate the markdown report: `docs/stage9B/Task43_Longitudinal_Integration_Report.md`.

---

# 4. Verification Plan

### Automated Verification

- Run `longitudinal_integration_run.py` to ensure it successfully reads from the SQLite database, processes the data, and writes the `Task43_Longitudinal_Integration_Report.md` file.
- Verify that the synthetic trajectory validation (`trajectory_validation_run.py`) still passes successfully to guarantee no regression occurred.

### Manual Verification

- Review `Task43_Longitudinal_Integration_Report.md` to ensure no diagnostic language is present and that the statistical tests correctly evaluate the empirical limits.
- Ensure the reported metrics strictly match the constraints outlined in Task 43 Specification.
