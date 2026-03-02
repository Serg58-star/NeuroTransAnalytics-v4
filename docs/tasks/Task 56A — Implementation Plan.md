# Stage 9C Task 56A — Implementation Plan (Anchored TPF Revalidation)

**Version:** v1
**Date:** 2026-03-02

## 1. Goal Description

Revalidate the Transition Probability Field of the locked stabilized generator (κ=0.08), but this time using **anchored quadrant thresholds** ($S_{75}$ and $DII_{75}$) computed exclusively from the baseline unstabilized generator (κ=0).

This methodological correction prevents the phenomenon where dynamic threshold recalculation artificially "dilates" the Q2 boundaries to capture the now-stabilized variance, leading to distorted stationary distributions.

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule, **explicit written approval** is required before execution.
> Please provide: **"Approved for implementation. Reference: Task 56A v1"**

## 3. Proposed Changes

### [MODIFY] `src/stage9A_v5_architecture/validation/task_53_transition_probability_field.py`

Modify `block_1_discrete_transition_matrix()` to accept optional parameters `fixed_S75` and `fixed_DII75`. If provided, the internal percentile calculation is bypassed, strictly adhering to the external anchors.

### [NEW] `src/stage9A_v5_architecture/validation/task_56A_tpf_revalidation_anchored.py`

A new script that:

1. Instantiates a baseline population (κ=0) to compute global $S_{75}$ and $DII_{75}$.
2. Generates the stabilized population (κ=0.08).
3. Evaluates the TPF using the modified Task 53 class, passing the fixed baseline anchors.
4. Checks all 5 ergodic criteria from the original Task 56.
5. Generates `Stage_9C_Task_56A_TPF_Revalidation_Anchored_Report.md`.

## 4. Verification Plan

1. The script will compare the stationary mass of Q2 against the 50% limit.
2. If the criteria are met under anchored thresholds, the generator is definitively locked, and the Risk Layer logic is validated.
