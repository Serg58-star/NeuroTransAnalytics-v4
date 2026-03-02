# Stage 9C Task 55B — Implementation Plan (Full Dynamic Validation)

**Version:** v1
**Date:** 2026-03-02

## 1. Goal Description

Perform full dynamic validation of the three kappa candidates ($\kappa \in \{0.08, 0.09, 0.10\}$) identified by Task 55A (T=10), and select the **minimum sufficient** κ that satisfies all six stability criteria. This is Stage 2 of 3 in the generator stabilization arc.

**Architectural constraints (strictly respected):**

- No changes to Z-Space, Severity formula, Anchored Projection, or MAD standardization
- No bootstrap
- Only the longitudinal drift parameter κ is operative

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule, **explicit written approval** is required before execution.
> Please provide: **"Approved for implementation. Reference: Task 55B v1"**

## 3. Proposed Changes

### [NEW] `src/stage9A_v5_architecture/validation/task_55B_full_dynamic_validation.py`

For each of **κ ∈ {0.08, 0.09, 0.10}**, at **N=400, T=10**, the script will evaluate:

| # | Criterion | Threshold |
|---|---|---|
| 1 | Absorbing states ($P_{ii}$) | All $P_{ii} \le 0.95$ |
| 2 | Spectral Gap ($1 - |\lambda_2|$) | $\ge 0.10$ |
| 3 | Stationary $Q_2$ mass | $\le 50\%$ |
| 4 | Mean System Entropy | $\ge 0.50$ |
| 5 | Saturation Slope ($\Delta S / S$) | $\in [-0.05, 0.02]$ |
| 6 | Longitudinal Silhouette | $< 0.20$ |

**Selection rule:** Choose the **smallest** κ for which all 6 criteria pass.

### Output

`docs/v5/Stage_9C_Task_55B_Full_Dynamic_Validation_Report.md` — containing per-κ table of all 6 metrics, transition matrix, eigenvalues, and the final selected κ.

## 4. Verification Plan

1. Run `task_55B_full_dynamic_validation.py` and inspect all 6 metrics per κ.
2. Confirm the selected κ is the minimum passing value.
3. Ensure no modifications were made to geometry or Severity logic.
4. The selected κ feeds directly into Task 55C (final geometric lock-in).
