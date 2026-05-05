# Task 9 Stage L4 (Model Integration) Implementation Plan

## Goal Description

Task 9 aims to integrate existing project analytical models with the newly established `reactions_view` from `neuro_data.db`. We will not build new models. We will build a data adapter layer (`stage_L4_model_adapter.py`) to extract arrays (RT vectors, PSI arrays, field groups, sequence indexes) and map them to the inputs of four existing project models: Ex-Gaussian decomposition, PSI sensitivity, Lateralization index, and Intra-series dynamics. A stage runner will orchestrate this data flow, save CSV outputs, and generate an analytical report.

## User Review Required
>
> [!IMPORTANT]
> **Implementation Approval Needed**
> Following the `mandatory-implementation-plan-approval-gate` rule, this architecture and file modification plan must be explicitly approved.
> **Please reply with "Approved for implementation" to authorize building the Stage L4 data adapter and orchestration runners.**

## Proposed Changes

### Adapter Layer

#### [NEW] `analysis/stage_L4_model_adapter.py`

This script acts as the bridge. It connects to `neuro_data.db`, extracts data from `reactions_view`, and structures the DataFrames/NumPy arrays into the expected input formats required by the four target models. It then imports the corresponding model functions from `src/` (identified in Task 8) and executes them, returning the calculated parameters.

### Python Scripts

#### [NEW] `analysis/run_stage_L4.py`

The orchestrator script. It will invoke the adapter to acquire the parameter sets (Ex-Gaussian μ, σ, τ; PSI regressions; Lateralization RTs; Dynamics sequences) and write them as CSV files to `docs/audit_legacy/Stage L/L4_results/`. It will also synthesize the `Task_9_Stage_L4_Report.md` providing contextual tables and descriptions of these parameters.

### Documentation & Reports

#### [NEW] `docs/audit_legacy/Stage L/L4_results/*` (Directory for output files)

Will contain the targeted model results:

- `exgaussian_parameters.csv`
- `psi_sensitivity_model.csv`
- `lateralization_index.csv`
- `intra_series_dynamics.csv`

#### [NEW] `docs/audit_legacy/Stage L/Task_9_Stage_L4_Report.md`

Report structure detailing the structural model integration, showing the resulting parameter sets (tables/CSV values), and demonstrating the model graphs if applicable.

#### [NEW] `docs/governance/Task_9_Stage_Completion_Audit.md`

Filled Stage Completion Audit template for L4 validation.

## Verification Plan

### Automated Tests

- Command terminal execution `python analysis/run_stage_L4.py`. Verification implies that the script successfully reads the legacy DB, routes data through the `src/` modules, correctly calculates parameters without throwing type or shape errors, and saves the `L4_results/` outputs.

### Manual Verification

- Review resulting CSV outputs inside `L4_results` for expected parameter footprints.
- Verify `Task_9_Stage_L4_Report.md` displays the integrated tables.
- Verify `Task_9_Stage_Completion_Audit.md` has all requirements checked off.
