# Task 6 Stage L2 — Legacy Data Pattern Verification (Execution Start)

## Goal Description

The objective of this task is to execute the first phase of legacy data pattern verification (Stage L2) using the actual dataset `neuro_data.db` (the converted Boxbase). The goal is to run a primary statistical inspection to confirm baseline hypotheses formulated in Stage L: overall RT distribution, variability profiling, lateral asymmetry, PSI effects, dynamic fatigue windows, and error distributions.

## User Review Required
>
> [!IMPORTANT]
> **Data Access Governance Approval Needed**
> In accordance with the `no-real-data-until-approved` and `mandatory-implementation-plan-approval-gate` rules, I am explicitly requesting approval to connect to and query `neuro_data.db`. Operations on the database will be strictly read-only (`SELECT`, `PRAGMA table_info`) to extract the essential schemas and summary statistics defined in the `Legacy Boxbase Analysis Protocol.md`.
> **Please reply with "Approved for implementation" to authorize database inspection and statistical extraction.**

## Proposed Changes

No Python or Delphi source code modules will be created or modified in this task. Our output will be a comprehensive Markdown report.

### Analytical Report

#### [NEW] `docs/audit_legacy/Stage L/Task 6_Stage L2_Report.md`

This report will document the findings of our database inspection and subsequent statistical tests. It will contain:

1. **Database Structure**: Actual table names and field definitions derived from `.tables` and `PRAGMA table_info`.
2. **Adapted SQL Queries**: The 15 draft queries from the Boxbase Analysis Protocol mapped to the real DB schema.
3. **Primary Statistical Results**: Summary metrics (mean, median, MAD, counts, grouping by field/PSI/index) proving or disproving the baseline operational hypotheses.
4. **Brief Interpretations**: Observations regarding RT distribution shapes, lateral asymmetry, temporal sensitivity (PSI), and error clustering.

## Verification Plan

### Manual Verification

1. I will query `neuro_data.db` using the `sqlite3` CLI via the terminal to read the schema.
2. I will map the logical columns (`reaction_time`, `field`, `psi`, etc.) to the retrieved schema.
3. I will execute the refined SQL queries against the database using the same CLI.
4. I will transcribe the results into `Task 6_Stage L2_Report.md` for user review. No complex modeling (C3.4) or C4 interpretations will be performed at this stage.
