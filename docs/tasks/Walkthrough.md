Walkthrough — Parquet Restoration & Engine Stabilization (Task 23)
🎯 Goal
Restore Parquet as the canonical derived-data format and resolve environment-specific instability encountered with pyarrow.

🛠️ Root Cause & Solution
1. The pyarrow Crash
Diagnostics revealed that pyarrow 19.0.0 produced a silent process crash on read operations in the current Windows/Python 3.13.5 environment. This made it unsuitable as a stable engine for this project.

2. Stabilization via fastparquet
I identified and verified that fastparquet is stable and efficient in this environment. It was selected as the project's primary Parquet engine.

🚀 Changes Made
1. Engine Standardization
Scenario Engine (C3.4): Reverted export logic from CSV back to Parquet, using engine="fastparquet".
Scenario Loader (C3.5): Reverted load logic from CSV back to Parquet, using engine="fastparquet".
Dependencies: Updated 
requirements.txt
 and documented the decision in 
Dependency_Notes.md
.
2. Fallback Removal
All temporary CSV export and loading code has been removed.
All temporary 
.csv
 files in data/derived/scenarios/ have been deleted.
✅ Verification Results
Row Count Verification
The full pipeline (C3.1 → C3.4) was executed, and the resulting Parquet files were verified via the ScenarioLoader:

A0.0 loaded from Parquet: 1886 rows
System Integrity
No dual-format storage remains.
The GUI correctly renders session data directly from Parquet files.
The project strictly adheres to the canonical src layout.
Status: ARCHITECTURALLY RESTORED The derived data layer now uses the intended Parquet format with a stabilized engine.