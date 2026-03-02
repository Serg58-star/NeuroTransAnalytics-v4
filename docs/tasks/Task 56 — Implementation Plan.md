# Stage 9C Task 56 — Implementation Plan (TPF Revalidation)

**Version:** v1
**Date:** 2026-03-02

## 1. Goal Description

Revalidate the Transition Probability Field (TPF) of the Risk Layer using the locked, stabilized longitudinal generator (**κ = 0.08**).

The goal is to confirm that the structural rigidity (absorbing states in Q2) detected during the initial Task 53/54 checks has been successfully eliminated, and that the Field supports ergodic, fluid state transitions.

**Parameters:** N=500, T=10, no bootstrap.

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule, **explicit written approval** is required before execution.
> Please provide: **"Approved for implementation. Reference: Task 56 v1"**

## 3. Proposed Changes

### [NEW] `src/stage9A_v5_architecture/validation/task_56_tpf_revalidation.py`

This script will generate longitudinal data using the locked `generate_longitudinal_population(..., kappa=0.08, ...)` and compute the transition matrix, evaluating the following criteria:

| # | Criterion | Threshold |
|---|---|---|
| 1 | Transition Matrix | No $P_{ii} > 0.95$, rows sum to 1 |
| 2 | Spectral Stability | $\|\lambda_{max}\| = 1$, Gap $\ge 0.15$ |
| 3 | Stationary Distribution | No quadrant $> 50\%$ |
| 4 | Transition Entropy | Mean $H \ge 0.60$, min $H_i \ge 0.10$ |
| 5 | Continuity | Longitudinal Silhouette $< 0.20$ |

**Report output:** `docs/v5/Stage_9C_Task_56_TPF_Revalidation_Report.md`

## 4. Verification Plan

1. Run the script.
2. Verify all TPF metrics pass the required thresholds.
3. Compare the new TPF against the pre-stabilization TPF (which failed due to Q2 absorbing states).
4. If successful, the Risk Layer logic is validated and we can proceed to formalize the Risk Accumulation Index.
