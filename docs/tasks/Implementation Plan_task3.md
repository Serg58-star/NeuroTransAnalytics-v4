# Implementation Plan

less than a minute ago

Review • 7
Implementation Plan — Task 3: C3 Computation & Pipelines
Perform strictly editorial synchronization of C3-level Computation and Pipeline documentation.

1. Scope
Target Files (ONLY):
docs/12_0_Карта_уровня_C3_Computation_&_Pipelines_v4.md
docs/12_1_C3_1_ETL_Pipeline_v4.md
docs/12_2_C3_2_Component_Timing_Computation_v4.md
docs/12_3_C3_3_QC_and_Aggregation_v4.md
docs/12_4_C3_4_Scenario_Computation_v4.md
Output Directory: docs/current_sqlite/.
2. Objective
Align C3 documentation with the SQLite-centric reality established in Task 1 and ensure strictly mechanical descriptions of the computation layer, free from interpretative (C4) language.

3. Guiding Principles
Mechanical Tone: Describe all processes (ETL, QC, Scenario computation) as deterministic and algorithmic.
Data Access Alignment: Replace Excel/spreadsheet-centric loading descriptions with SQLite-based access.
Boundary Control: Audit for and remove "interpretative" terminology (e.g., "suggests", "indicates", "reveals") that belongs in C4.
Source of Truth: Refer to docs/current_sqlite/ for table mapping and storage invariants.
4. Proposed Changes per File
12_0_Карта_уровня_C3_Computation_&_Pipelines_v4.md
Audit level map for consistency with Task 2's C2 documentation.
Ensure the map emphasizes computation over data persistence (which belongs to C2).
12_1_C3_1_ETL_Pipeline_v4.md
Synchronize ETL stages: focus on extraction from SQLite (trials, users, metadata_*) rather than Excel loading.
Verify that ETL is described as a mechanical transformation.
12_2_C3_2_Component_Timing_Computation_v4.md
Ensure ΔV1, ΔV4, ΔV5 calculation descriptions are strictly algorithmic.
Remove any implicit interpretation of what these timings "mean" in a physical or cognitive sense.
12_3_C3_3_QC_and_Aggregation_v4.md
Update QC descriptions to reflect flagging within SQLite or derived tables.
Ensure QC is presented as a deterministic filter/flag process, not a judgment tool.
12_4_C3_4_Scenario_Computation_v4.md
Align scenario computation with the precomputed results architecture. (No recomputation).
Strictly avoid C4-level "interpretative conclusions" in the scenario output descriptions.
5. Verification & Reporting
Architectural Check: Use architecture-guardian to confirm C3 remains purely computational and descriptive of pipelines.
Editorial Reports: Individual reports for each file confirming:
Specific terminology adjustments.
Confirmation: "No computational logic was altered and no interpretative meaning was introduced."
