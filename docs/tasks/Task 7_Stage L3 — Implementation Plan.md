# Task 7 Stage L3 — Visual Pattern Exploration Implementation Plan

## Goal Description

The objective of this task is to perform visual exploration of the reaction-time patterns detected during Stage L2. This implies generating specific plots (histograms, boxplots, and line plots) from the legacy `neuro_data.db` database. In accordance with architectural requirements, a canonical SQL adapter (`reactions_view`) will be created to transform the wide-format Boxbase storage into a long format. A visualization script and a stage runner will be implemented to generate the figures and save them to the documentation directory, culminating in a Stage Report and a Stage Completion Audit.

## User Review Required
>
> [!IMPORTANT]
> **Implementation Approval Needed**
> In compliance with project governance (`mandatory-implementation-plan-approval-gate`), this implementation plan must be explicitly approved before modifying the codebase or generating the artifacts.
> **Please reply with "Approved for implementation" to authorize the creation of these scripts and SQL views.**

## Proposed Changes

### SQL Adapter

#### [NEW] `sql/boxbase_reactions_view.sql`

This script will create a view named `reactions_view` in `neuro_data.db`. It will union the 36 trials of the 3 tests (simple, shift, color) and join them with the metadata tables to provide a long-format schema: `trial_id, subject_id, test_type, stimulus_index, rt, field, psi, color`.
Errors will be drawn from the trial-level counters (`tst1_premature`, etc.) via a separate or joined logic as required by the pipeline.

### Python Scripts

#### [NEW] `analysis/stage_L3_visual_patterns.py`

A visualization pipeline using `pandas`, `sqlite3`, `matplotlib`, and `seaborn`. It will connect to the database, read from `reactions_view` (and trial error counters), and generate the 7 required figures:

- `rt_distribution.png`
- `rt_distribution_by_test.png`
- `rt_vs_field.png`
- `rt_vs_index.png`
- `rt_vs_psi.png`
- `rt_vs_test_type.png`
- `errors_by_test_type.png`

#### [NEW] `analysis/run_stage_L3.py`

A stage runner script that orchestrates the execution. It will:

1. Recreate the SQL adapter view by executing `boxbase_reactions_view.sql`.
2. Run `stage_L3_visual_patterns.py` to generate the figures.
3. Automatically build the draft of `docs/audit_legacy/Stage L/Task_7_Stage_L3_Report.md`.

### Documentation & Reports

#### [NEW] `docs/audit_legacy/Stage L/figures/*` (Directory for output figures)

#### [NEW] `docs/audit_legacy/Stage L/Task_7_Stage_L3_Report.md`

A report without interpretative modeling containing descriptions of queries, the generated figures, and short observational notes.

#### [NEW] `docs/governance/Task_7_Stage_Completion_Audit.md`

A filled-out copy of the `STAGE_COMPLETION_AUDIT_TEMPLATE.md` confirming the existence of deliverables and successful runner execution.

## Verification Plan

### Automated Tests

- Execution of `python analysis/run_stage_L3.py` from the terminal. This command will verify that the SQL view is created without errors, data is successfully extracted, and all seven PNG files are saved to `docs/audit_legacy/Stage L/figures/`.

### Manual Verification

- Verify the contents of `docs/audit_legacy/Stage L/Task_7_Stage_L3_Report.md` correctly embed the generated figures.
- Verify the `Task_7_Stage_Completion_Audit.md` has all requirements checked off.
