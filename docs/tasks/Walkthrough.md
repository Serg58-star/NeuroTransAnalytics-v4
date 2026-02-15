Walkthrough — NeuroTransAnalytics-v4 (C3.1 - C3.4)
🎯 Task 17 — C3.2 Component Timing Computation
Implemented the deterministic calculation of reaction time components.

🛠️ Changes
component_v4.py
: Implemented 
ComponentTimingV4
.
ΔV1: Baseline RT from Tst1.
ΔV4: RT(Tst2) - ΔV1.
ΔV5_MT: RT(Tst3) - ΔV1.
🎯 Task 18 — C3.3 QC & Aggregation
Implemented robust statistical aggregation with automated QC filtering.

🛠️ Changes
qc_aggregation_v4.py
: Implemented 
QCAggregationV4
.
QC Filter: Uses technical_qc_flag to exclude invalid events from aggregates.
Metrics: Median, MAD (Median Absolute Deviation), and IQR.
✅ Verification (
verify_c3_3.py
)
Robust Metrics: Formally verified Median, MAD, and IQR against manual calculations.
QC Efficacy: Invalid sessions correctly filtered without row loss in original frame.
🎯 Task 19 — C3.4 Scenario Computation (A0 First)
Implemented the Scenario Engine for structuring results of baseline scenarios.

🛠️ Changes
scenario_v4.py
: Implemented 
ScenarioEngineV4
.
Scenario A0.0 (Baseline Stability): Structures ΔV1 median, MAD, and IQR for Tst1.
Scenario A0.1 (Variability Profile): Structures ΔV1 MAD and IQR for Tst1.
✅ Verification (
verify_c3_4.py
)
Verified on the full dataset (~5.6k aggregated sessions).

Verification Highlights:

Purity: Confirmed no new calculations or thresholds are introduced.
Mapping: 100% accuracy in mapping AggregatedFrame columns to scenario-specific fields.
Structure: Return format is a dictionary of DataFrames, ready for visualization or reporting.
Sample A0.0 Output (Structured):

subject_id	session_id	baseline_median	baseline_mad	baseline_iqr
7	116	219.0	8.0	13.75
7	1325	227.0	13.5	24.25
Status: PASSED The C3 computation pipeline (ETL -> Component -> QC Aggregation -> Scenario) is now fully implemented and verified for A0-level analysis.
