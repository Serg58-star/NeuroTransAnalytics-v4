Task 25.3 — Spatial Refactor (A0.0, A0.1) - Revised Plan
I have updated the implementation plan based on the mandatory requirements specified in the "Amendment to Implementation Plan — Task 25.3".

Revised Strategy:
Mandatory Spatial Breakdown: A0.0 and A0.1 will now strictly avoid spatial collapsing or averaging. They will provide field-specific analytical columns (Left, Center, Right) per session.
Triad Integrity Verification: Before pivoting, the engine will verify that each session has the complete set of locations (left, center, right). Any missing field will trigger a ValueError.
Complete Metadata Purity: In addition to moving version fields out of Parquet, I will also remove the scenario_code column from all A0.x artifacts.
Internal Versioning: scenario_version will be bumped to v4.0.3 for logging purposes but will not appear in the resulting data.
Please review the updated 
implementation_plan.md
. Once approved, I will proceed with the execution.

Implementation Plan — Task 25.3: Spatial Refactor (A0.0, A0.1)
Refactoring A0.0 and A0.1 to use a spatially-extended structure and enforcing strict field integrity across the A0-block.

User Review Required
IMPORTANT

No Spatial Collapse: A0.0 and A0.1 will now mirror A0.3 by providing per-field columns (Left, Center, Right) instead of session-level averages. Triad Integrity Check: The pipeline will now fail fast (ValueError) if any session lacks a complete triad of visual fields (left, center, right). No zero-filling or averaging allowed. Metadata Removal: The scenario_code column will be removed from all parquet artifacts (A0.0–A0.3).

Proposed Changes
[Scenario Engine (C3.4)]
[MODIFY] 
scenario_v4.py
A0.0 (Baseline Stability):
Add location triad check for each session.
Implement strict pivot mapping for median_ΔV1, mad_ΔV1, iqr_ΔV1, and count_valid.
Columns: median_{left|center|right}, mad_{left|center|right}, etc.
A0.1 (Variability Profile):
Add location triad check for each session.
Implement strict pivot mapping for mad_ΔV1 and iqr_ΔV1.
Columns: variability_mad_{left|center|right}, variability_iqr_{left|center|right}.
A0.2 & A0.3:
Remove scenario_code assignment.
Fail-fast Logic:
Validate stimulus_location presence.
Verify 
set(group['stimulus_location']) == {'left', 'center', 'right'}
 before pivot.
[MODIFY] 
pipeline_config.py
Bump scenario_version to scenario_v4.0.3 (Internal logging only).
[GUI Visualizations (C3.5)]
[MODIFY] 
a0_views.py
Update 
A0BaselineView
 and 
A0VariabilityView
 to display the new spatial columns. Version fields already excluded.
Verification Plan
Automated Tests
Pipeline Execution: Run 
prepare_scenarios.py
.
Triad Validation: Verify it raises ValueError if we manually delete a field from a session.
Parquet Audit:
Confirm NO scenario_code in any A0 file.
Confirm full spatial breakdown in A0_0 and A0_1.
Manual Verification
Open GUI tabs for Baseline and Variability.
Confirm spatial breakdown is correctly displayed in tables.