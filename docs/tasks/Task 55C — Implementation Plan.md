# Stage 9C Task 55C — Implementation Plan (Geometric Preservation Check)

**Version:** v1
**Date:** 2026-03-02

## 1. Goal Description

This is Stage 3/3 of the generator stabilization arc. With **κ = 0.08** locked from Task 55B, we now run the full v5 geometric invariant suite against the stabilized generator to confirm that the Ornstein-Uhlenbeck elastic drift has not damaged the fundamental geometry of the Z-Space.

**Parameters:** N=500, T=10, Bootstrap=500.

**Architectural constraints:** Z-Space, Severity formula, Anchored Projection, MAD standardization, and MCD are all unchanged. Only the longitudinal drift uses κ=0.08.

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule, **explicit written approval** is required before execution.
> Please provide: **"Approved for implementation. Reference: Task 55C v1"**

## 3. Proposed Changes

### [NEW] `src/stage9A_v5_architecture/validation/task_55C_geometric_preservation_check.py`

The script will run the following checks using the **stabilized generator** (κ=0.08) and compare against the **baseline** (κ=0):

| # | Invariant | Threshold |
|---|---|---|
| 1 | Participation Ratio | ≥ 4 |
| 2 | Effective Rank | ≥ 4 |
| 3 | PC1 Variance | ∈ [10%, 25%] |
| 4 | Bootstrap SD of PC1 (k=500) | ≤ 2% |
| 5 | Silhouette Static (at t=0) | < 0.20 |
| 6 | Silhouette Longitudinal (Δ-Z field) | < 0.20 |
| 7 | Condition Number of Covariance | ≤ Baseline × 1.20 |
| 8 | No dominant axis | PC1 < 40% |

**Report output:** `docs/v5/Stage_9C_Task_55C_Geometric_Preservation_Report.md`

**Final status:** `LOCKED` (all criteria met) or `REJECTED` (return to Task 55A).

## 4. Verification Plan

1. Run the script and inspect the generated report.
2. Confirm LOCKED status for all 8 criteria.
3. If all pass → κ=0.08 is the canonical stabilized parameter for all future Stage 9C development.
