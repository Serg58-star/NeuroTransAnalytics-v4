# Task 8 — Legacy Method Reuse Audit Implementation Plan

## Goal Description

Perform an audit to search, identify, document, and assess the reusability of already implemented analytical models in the NeuroTransAnalytics-v4 project to avoid duplicate work in Stage L4. The four target models are Ex-Gaussian decomposition, PSI sensitivity, Lateralization index, and Intra-series dynamics.

## User Review Required
>
> [!IMPORTANT]
> **Implementation Approval Needed**
> In compliance with project governance (`mandatory-implementation-plan-approval-gate.md`), this implementation plan must be explicitly approved before generation of the final audit report `docs/audit_legacy/Stage L/Task_8_Legacy_Model_Reusability_Audit.md`.
> **Please reply with "Approved for implementation" to authorize the creation of this audit document.**

## Proposed Changes

### Documentation & Reports

#### [NEW] `docs/audit_legacy/Stage L/Task_8_Legacy_Model_Reusability_Audit.md`

This document will contain a structured table of the 4 requested analytical models based on codebase search results:

1. **Ex-Gaussian decomposition RT**: Will reference its implementation located at `src/c3x_exploratory/exgaussian_integration.py` and `src/c3x_exploratory/parametric_modeling.py` (from Stage 6 Task 35.1 and 35.2). Calculates keys parameter `mu`, `sigma`, `tau`.
2. **PSI sensitivity modeling**: Will reference its implementation in `src/exploratory_lab/pipelines/stage4_stimulus_decomposition.py` and microdynamic files `synthetic_microdynamics_*.py`.
3. **Lateralization index**: Will reference the existing metric implemented in `src/exploratory_lab/pipelines/stage2_lateralization.py` and FOV validations (`src/c3x_exploratory/synthetic_microdynamics_fov.py`). Calculates `RT_left`, `RT_center`, `RT_right`.
4. **Intra-series dynamics modeling**: Will reference implementations in `src/c3_core/component_timing/component_v4.py` and extended microdynamics files `src/c3x_exploratory/microdynamics_*.py`, tracking fatigue, adaptation, and auto-correlative oscillatory patterns over `stimulus_index`.

For each model, the report will provide a short description, its exact location, and a reusability flag (`YES` or `NO`) assessing whether the logic can be directly imported and applied to the legacy long-format reaction view in Stage L4.

## Verification Plan

### Automated Tests

- This task strictly generates documentation. No automated analytical tests are required.

### Manual Verification

- Review the `docs/audit_legacy/Stage L/Task_8_Legacy_Model_Reusability_Audit.md` to ensure all four target models are documented in the requested tabular format (`Model | Found | Location | Description | Reusable`).
