# Task 11 Stage L5 (Legacy Structural Analysis) Implementation Plan

## Goal Description

Perform deep exploratory analysis of the legacy testing architecture and dataset (`reactions_view`) to identify behavioral patterns versus protocol artifacts. This analysis is structurally divided into five blocks (A: Protocol Order Effects, B: Temporal Dynamics, C: Spatial Structure, D: Reaction Structure & Variability, E: Sequential Dynamics).

## User Review Required
>
> [!IMPORTANT]
> **Implementation Approval Needed**
> In compliance with the governance rule `mandatory-implementation-plan-approval-gate`, this plan must be explicitly approved before any code is written.  
> **Please reply with "Approved for implementation" to authorize the creation of the Stage L5 analytical modules and orchestrator.**

## Proposed Changes

### Data & Analytical Modules

#### [NEW] `analysis/stage_L5_structural_analysis.py`

This module will contain functions for each analytical block:

- **Block A:** `analyze_order_effects` (Comparing 3 tests structurally: test order means/variances, early/late series drift, cross-test correlations).
- **Block B:** `analyze_temporal_dynamics` (Modeling `RT = f(PSI)` via regression, checking predictable Markov biases `RT vs PSI(i-1)`, computing subject-level PSI sensitivity).
- **Block C:** `analyze_spatial_structure` (Lateralization re-evaluation `left vs right`, and interaction `RT = f(PSI * field)` for peripheral degradation).
- **Block D:** `analyze_reaction_structure` (Using models from Stage L4 to track Ex-Gaussian `tau` across tests, compute speed-accuracy models, map variance across PSI/field, and calculate residual metrics).
- **Block E:** `analyze_sequential_dynamics` (Autocorrelation metrics for oscillatory cycles and computing Post-Error Slowing vectors).

#### [NEW] `analysis/run_stage_L5.py`

The orchestrator script. It will load `reactions_view`, invoke all blocks from `stage_L5_structural_analysis.py`, generate diagnostic plots using `matplotlib`/`seaborn`, output CSV tables into `docs/audit_legacy/Stage L/L5_results/`, and automatically compile the comprehensive `Stage_L5_Legacy_Structural_Analysis_Report.md`.

### Documentation Outputs

#### [NEW] `docs/audit_legacy/Stage L/L5_results/*`

Will contain output statistics (CSV tables) and diagnostic `.png` graphs representing findings for Blocks A-E.

#### [NEW] `docs/audit_legacy/Stage L/Stage_L5_Legacy_Structural_Analysis_Report.md`

A descriptive, consolidated report describing methods, results, observed patterns and implications for v5 design for each block.

#### [NEW] `docs/governance/Task_11_Stage_Completion_Audit.md`

Standard stage completion audit verifying architectural constraints (no raw DB queries allowed, strict `reactions_view` usage) and reproducibility of the pipeline.

## Verification Plan

### Automated Tests

- Command terminal execution `python analysis/run_stage_L5.py`. Verification implies that the script processes `reactions_view` continuously across all five analytical blocks without runtime errors, correctly generating CSV datasets and structural visualization plots.

### Manual Verification

- Review generated `L5_results/` for comprehensive metrics.
- Ensure `Stage_L5_Legacy_Structural_Analysis_Report.md` documents insights specifically relevant for the NeuroTransAnalytics v5 design (e.g., whether random test order is required, spatial interaction constraints).
- Verify the `Task_11_Stage_Completion_Audit.md` is strictly filled.
