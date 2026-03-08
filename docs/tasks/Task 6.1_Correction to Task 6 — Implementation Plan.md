# Task 6.1 — Correction to Task 6 Stage L2 (Error Classification Logic)

## Goal Description

Task 6.1 requires correcting a methodological error introduced in `Task 6_Stage L2_Report.md`. Specifically, the artificial threshold used for proxy error detection (`150 ms` to `1000 ms`) is invalid because the legacy SZR system explicitly dictates valid reaction bounds as `135 ms` to `2000 ms`. Furthermore, the legacy system stores precalculated error frequencies (e.g., `tst1_premature` and `tst1_late`) and dynamically repeats out-of-bounds trials, making RT-based proxy detection unnecessary and inaccurate.

## User Review Required
>
> [!IMPORTANT]
> **Implementation Approval Needed**
> In compliance with project governance (`mandatory-implementation-plan-approval-gate`), this plan must be explicitly approved before modifying the analysis script.
> **Please reply with "Approved for implementation" to authorize these corrections.**

## Proposed Changes

### Python Runner Script

#### [MODIFY] `tmp_run_l2.py`

We will rewrite the CTE used to extract the `reactions` and `errors_cte` datasets.

1. The synthetic `rt > 1000 OR rt < 150` condition will be completely removed.
2. The error counts will be derived directly from the canonical legacy counters stored at the trial level (`tst_premature` and `tst_late`) instead of applying arbitrary thresholds to the RT vector.
3. If specific queries such as "Error vs Field" (Query 5) require trial-level error flags, we will document that errors in the Boxbase paradigm are not strictly bound to the final 36-item RT vector. Query 5 and Query 6 will be adapted to reflect the canonical legacy metrics.

### Analytical Report

#### [MODIFY] `docs/audit_legacy/Stage L/Task 6_Stage L2_Report.md`

1. Re-run `tmp_run_l2.py` to regenerate the report output.
2. Update the report explanations under "2. Адаптированные SQL-запросы" to reflect the proper use of canonical protocol limits (135–2000 ms) and the explicit counters.

## Verification Plan

### Manual Verification

1. Review the generated `Task 6_Stage L2_Report.md` to ensure the SQL snippets correctly use `135` and `2000` (if classifying RTs) or query the direct legacy counter fields.
2. Ensure the generated statistics reflect the updated SQL logic without crashing the Python script.
