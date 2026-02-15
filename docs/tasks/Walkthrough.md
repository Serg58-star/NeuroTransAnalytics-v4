Walkthrough — NeuroTransAnalytics-v4 (C3.2 & C3.3)
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
✅ Verification
Dataset: 204,336 rows.
Result: Arithmetic correctness confirmed. ΔV1 matches Tst1; ΔV4/ΔV5 computed per-stimulus.
🎯 Task 18 — C3.3 QC & Aggregation
Implemented robust statistical aggregation with automated QC filtering.

🛠️ Changes
qc_aggregation_v4.py
: Implemented 
QCAggregationV4
.
QC Filter: Uses technical_qc_flag to exclude invalid events from aggregates.
Metrics: Median, MAD (Median Absolute Deviation), and IQR.
Grouping: Segments data by subject_id, session_id, and test_type.
✅ Verification (
verify_c3_3.py
)
Verified on the full real dataset.

Verification Highlights:

Robust Metrics: Formally verified Median, MAD, and IQR against manual calculations for sample sessions.
QC Efficacy: Invalid sessions (total 648 rows in dataset) were correctly filtered out or excluded from aggregation.
Data Integrity: The process generates a new AggregatedFrame without modifying or deleting rows from the source ComponentFrame.
Sample Aggregated Output:

session_id	test_type	count_valid	median_rt_ms	mad_rt_ms	median_ΔV1	median_ΔV4
116	Tst1	36	219.0	8.0	219.0	NaN
116	Tst2	36	304.0	27.5	219.0	85.0
116	Tst3	36	321.5	31.0	219.0	NaN
Status: PASSED All C3.x computation layers implemented so far adhere to the non-interpretative, deterministic architecture of v4.
