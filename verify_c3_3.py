import pandas as pd
import numpy as np
from src.c3_core.etl.etl_v4 import ETLPipeline
from src.c3_core.component_timing.component_v4 import ComponentTimingV4
from src.c3_core.qc_aggregation.qc_aggregation_v4 import QCAggregationV4

def verify_c3_3():
    print("--- Verifying C3.3 QC & Aggregation ---")
    
    # 1. Pipeline Execution
    etl = ETLPipeline(db_path="neuro_data.db")
    event_frame = etl.run()
    
    comp = ComponentTimingV4()
    component_frame = comp.run(event_frame)
    
    qc_agg = QCAggregationV4()
    aggregated_frame = qc_agg.run(component_frame)
    
    print(f"Loaded EventFrame: {len(event_frame)} rows")
    print(f"Generated ComponentFrame: {len(component_frame)} rows")
    print(f"Generated AggregatedFrame: {len(aggregated_frame)} rows")
    
    # 2. Basic Validation
    # AggregatedFrame should have columns for medians, mads, iqrs
    expected_cols = ['subject_id', 'session_id', 'test_type', 'count_valid', 'median_rt_ms', 'mad_rt_ms', 'iqr_rt_ms']
    for col in expected_cols:
        assert col in aggregated_frame.columns, f"Missing column: {col}"
    
    # 3. Validation of Group Counts
    # Each session should have up to 3 test types
    num_sessions = component_frame['session_id'].nunique()
    print(f"Number of sessions: {num_sessions}")
    # aggregated_frame rows should be <= num_sessions * 3
    assert len(aggregated_frame) <= num_sessions * 3
    
    # 4. Manual Verification of Robust Stats for a Sample Group
    # Pick the first valid group
    sample_row = aggregated_frame.iloc[0]
    sid = sample_row['subject_id']
    sess_id = sample_row['session_id']
    ttype = sample_row['test_type']
    
    print(f"\nChecking Sample: Subject {sid}, Session {sess_id}, Test {ttype}")
    
    source_data = component_frame[
        (component_frame['subject_id'] == sid) & 
        (component_frame['session_id'] == sess_id) & 
        (component_frame['test_type'] == ttype) & 
        (component_frame['technical_qc_flag'] == True)
    ]['rt_ms']
    
    calc_median = source_data.median()
    calc_mad = (source_data - calc_median).abs().median()
    calc_iqr = source_data.quantile(0.75) - source_data.quantile(0.25)
    
    print(f"Source responses (count_valid): {len(source_data)}")
    print(f"Expected: Median={calc_median}, MAD={calc_mad}, IQR={calc_iqr}")
    print(f"Actual:   Median={sample_row['median_rt_ms']}, MAD={sample_row['mad_rt_ms']}, IQR={sample_row['iqr_rt_ms']}")
    
    assert np.isclose(sample_row['median_rt_ms'], calc_median)
    assert np.isclose(sample_row['mad_rt_ms'], calc_mad)
    assert np.isclose(sample_row['iqr_rt_ms'], calc_iqr)
    assert sample_row['count_valid'] == len(source_data)
    
    # 5. Check QC Filtering Effectiveness
    # Find a session with some invalid records
    invalid_sessions = component_frame[component_frame['technical_qc_flag'] == False]['session_id'].unique()
    if len(invalid_sessions) > 0:
        inv_sess = invalid_sessions[0]
        agg_inv = aggregated_frame[aggregated_frame['session_id'] == inv_sess]
        comp_inv = component_frame[component_frame['session_id'] == inv_sess]
        
        # All rows for inv_sess in component_frame might be invalid (based on our ETL logic)
        total_rows = len(comp_inv)
        valid_rows = len(comp_inv[comp_inv['technical_qc_flag'] == True])
        
        # If valid_rows is 0, then this session should NOT be in aggregated_frame
        if valid_rows == 0:
            assert len(agg_inv) == 0, f"Session {inv_sess} should be excluded from aggregation as it has 0 valid rows"
            print(f"QC Filter Check: Session {inv_sess} correctly excluded (0/{total_rows} valid).")
        else:
            # If some are valid, count_valid should match
            for _, row in agg_inv.iterrows():
                expected_cv = len(comp_inv[(comp_inv['test_type'] == row['test_type']) & (comp_inv['technical_qc_flag'] == True)])
                assert row['count_valid'] == expected_cv
            print(f"QC Filter Check: Session {inv_sess} correctly filtered.")
    
    # 6. Check ΔV Distribution in AggregatedFrame
    # Tst1 should have median_ΔV1 but NaN for median_ΔV4/ΔV5_MT
    tst1_agg = aggregated_frame[aggregated_frame['test_type'] == 'Tst1']
    assert not tst1_agg['median_ΔV1'].isna().all()
    assert tst1_agg['median_ΔV4'].isna().all()
    assert tst1_agg['median_ΔV5_MT'].isna().all()
    print("ΔV Distribution Check: PASS")

    print("\n--- All architectural and statistical checks PASSED ---")
    
    print("\nSample AggregatedFrame output:")
    print(aggregated_frame[['session_id', 'test_type', 'count_valid', 'median_rt_ms', 'mad_rt_ms', 'median_ΔV1', 'median_ΔV4']].head(10))

if __name__ == "__main__":
    verify_c3_3()
