import pandas as pd
from src.c3_core.etl.etl_v4 import ETLPipeline
from src.c3_core.component_timing.component_v4 import ComponentTimingV4
from src.c3_core.qc_aggregation.qc_aggregation_v4 import QCAggregationV4
from src.c3_core.scenario_engine.scenario_v4 import ScenarioEngineV4

def verify_c3_4():
    print("--- Verifying C3.4 Scenario Computation (A0) ---")
    
    # 1. Pipeline Execution
    etl = ETLPipeline(db_path="neuro_data.db")
    event_frame = etl.run()
    
    comp = ComponentTimingV4()
    component_frame = comp.run(event_frame)
    
    qc_agg = QCAggregationV4()
    aggregated_frame = qc_agg.run(component_frame)
    
    engine = ScenarioEngineV4()
    scenarios = engine.run(aggregated_frame)
    
    print(f"Loaded AggregatedFrame: {len(aggregated_frame)} rows")
    print(f"Scenarios computed: {list(scenarios.keys())}")
    
    # 2. Verification of A0.0
    a0_0 = scenarios["A0.0"]
    print(f"\nA0.0 (Baseline Stability): {len(a0_0)} rows")
    expected_a0_0_cols = ['subject_id', 'session_id', 'count_valid', 'baseline_median', 'baseline_mad', 'baseline_iqr']
    for col in expected_a0_0_cols:
        assert col in a0_0.columns, f"Missing column in A0.0: {col}"
    
    # Row count should match Tst1 sessions
    tst1_count = len(aggregated_frame[aggregated_frame['test_type'] == 'Tst1'])
    assert len(a0_0) == tst1_count, f"A0.0 row count mismatch: {len(a0_0)} != {tst1_count}"
    
    # 3. Verification of A0.1
    a0_1 = scenarios["A0.1"]
    print(f"A0.1 (Variability Profile): {len(a0_1)} rows")
    expected_a0_1_cols = ['subject_id', 'session_id', 'variability_mad', 'variability_iqr']
    for col in expected_a0_1_cols:
        assert col in a0_1.columns, f"Missing column in A0.1: {col}"
    
    assert len(a0_1) == tst1_count, f"A0.1 row count mismatch: {len(a0_1)} != {tst1_count}"
    
    # 4. Data Mapping Verification
    if not a0_0.empty:
        sample_sid = a0_0['session_id'].iloc[0]
        agg_row = aggregated_frame[(aggregated_frame['session_id'] == sample_sid) & (aggregated_frame['test_type'] == 'Tst1')].iloc[0]
        a0_row = a0_0[a0_0['session_id'] == sample_sid].iloc[0]
        
        assert a0_row['baseline_median'] == agg_row['median_ΔV1']
        assert a0_row['baseline_mad'] == agg_row['mad_ΔV1']
        print(f"\nMapping Check (Session {sample_sid}): median_ΔV1={agg_row['median_ΔV1']} -> baseline_median={a0_row['baseline_median']} : OK")

    print("\n--- All architectural and mapping checks for C3.4 PASSED ---")
    
    print("\nSample A0.0 Baseline Stability:")
    print(a0_0.head())

if __name__ == "__main__":
    verify_c3_4()
