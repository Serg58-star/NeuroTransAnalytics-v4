Implementation Plan — Task 16: C3.1 Real SQLite ETL Initialization

Review
Implementation Plan — Task 16: C3.1 Real SQLite ETL Initialization
Implement a deterministic ETL pipeline (C3.1) that extracts data from the canonical SQLite database (neuro_data.db), normalizes reaction data into a vertical EventFrame, and performs technical integrity checks.

User Review Required
IMPORTANT

Database File Missing: I have not found neuro_data.db in the current workspace. Project documentation (
README.md
, 
ETL_Pipeline_v4.md
) states it is the "ONLY" and "canonical" source of data. I am proceeding with the implementation assuming the database will be located at data/neuro_data.db. Please confirm if this is correct or if I should create it from legacy files.

NOTE

The ETL will be strictly deterministic and will NOT perform any computations (ΔV1, ΔV4, etc.) or analytical QC.

Proposed Changes
[C3.1 ETL Component]
[NEW] 
etl_v4.py
This is the main ETL module. It will contain:

load_sqlite(path): Context manager for SQLite connection.
extract_data(conn): Extraction of users, trials, and metadata_* tables.
build_event_frame(trials_df, metadata_dfs): The core transformation logic.
Unpivots tst1_1...tst1_36, tst2_1...tst2_36, tst3_1...tst3_36.
Maps metadata (PSI, color, position) from metadata_simple, metadata_color_red, metadata_shift based on stimulus_index.
validate_integrity(event_frame): Technical QC flags:
technical_qc_flag = False if RT < 135 ms.
technical_qc_flag = False if session doesn't have 36 reactions.
technical_qc_flag = False if metadata is missing for a stimulus index.
[NEW] 
init
.py
Exports the main ETL entry point.

Verification Plan
Automated Tests
I will create a temporary test script tests/test_etl_v4.py that mocks a SQLite database with the required schema and verifies:
Correct row count: sessions * 3 tests * 36 reactions.
Correct mapping of PSI from metadata.
Correct technical QC flags for RT < 135 ms.
Exclusion of warmup data.
Manual Verification
Run the ETL against the "real" neuro_data.db (if available) and inspect the resulting DataFrame:
df.head() and df.info().
Check if stimulus_index is 1-36.
Check if technical_qc_flag is correctly set.