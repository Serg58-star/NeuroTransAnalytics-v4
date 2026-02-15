import pandas as pd
import numpy as np
from src.c3_core.etl.etl_v4 import ETLPipeline
from src.c3_core.component_timing.component_v4 import ComponentTimingV4

def verify_c3_2():
    print("--- Verifying C3.2 Component Timing Computation ---")
    
    # 1. Load Data using C3.1 ETL
    etl = ETLPipeline(db_path="neuro_data.db")
    event_frame = etl.run()
    print(f"Loaded EventFrame with {len(event_frame)} rows.")
    
    # 2. Run C3.2 Computation
    comp = ComponentTimingV4()
    component_frame = comp.run(event_frame)
    print(f"Generated ComponentFrame with {len(component_frame)} rows.")
    
    # 3. Assertions
    # A. Row count must be identical
    assert len(event_frame) == len(component_frame), "Row count mismatch!"
    
    # B. Presence of ΔV columns
    for col in ['ΔV1', 'ΔV4', 'ΔV5_MT']:
        assert col in component_frame.columns, f"Missing column {col}"
    
    # C. Verification of ΔV1
    # For Tst1 rows, ΔV1 must equal rt_ms
    tst1_sample = component_frame[component_frame['test_type'] == 'Tst1']
    np.testing.assert_array_almost_equal(tst1_sample['ΔV1'], tst1_sample['rt_ms'], err_msg="ΔV1 does not match RT for Tst1!")
    
    # D. Verification of ΔV4 for Tst2
    # Pick a session and stimulus index
    sample_session = component_frame['session_id'].iloc[0]
    sample_index = component_frame['stimulus_index'].iloc[0]
    
    row_tst1 = component_frame[(component_frame['session_id'] == sample_session) & 
                               (component_frame['stimulus_index'] == sample_index) & 
                               (component_frame['test_type'] == 'Tst1')]
    row_tst2 = component_frame[(component_frame['session_id'] == sample_session) & 
                               (component_frame['stimulus_index'] == sample_index) & 
                               (component_frame['test_type'] == 'Tst2')]
    
    if not row_tst1.empty and not row_tst2.empty:
        v1 = row_tst1['rt_ms'].iloc[0]
        rt2 = row_tst2['rt_ms'].iloc[0]
        dv4 = row_tst2['ΔV4'].iloc[0]
        assert np.isclose(dv4, rt2 - v1), f"ΔV4 calculation error: {dv4} != {rt2} - {v1}"
        print(f"Sample Session {sample_session}, Index {sample_index}: ΔV1={v1}, RT(Tst2)={rt2}, ΔV4={dv4} -> OK")

    # E. Verify NaN distribution
    assert component_frame[component_frame['test_type'] == 'Tst1']['ΔV4'].isna().all(), "ΔV4 should be NaN for Tst1"
    assert component_frame[component_frame['test_type'] == 'Tst1']['ΔV5_MT'].isna().all(), "ΔV5_MT should be NaN for Tst1"
    assert component_frame[component_frame['test_type'] == 'Tst2']['ΔV5_MT'].isna().all(), "ΔV5_MT should be NaN for Tst2"
    assert component_frame[component_frame['test_type'] == 'Tst3']['ΔV4'].isna().all(), "ΔV4 should be NaN for Tst3"
    
    # F. Verify preservation of metadata and QC flags
    assert (component_frame['technical_qc_flag'] == event_frame['technical_qc_flag']).all(), "QC flags modified!"
    
    print("\n--- All architectural and arithmetic checks PASSED ---")
    
    # Show sample output
    print("\nSample ComponentFrame output (first 5 rows):")
    print(component_frame[['session_id', 'test_type', 'stimulus_index', 'rt_ms', 'ΔV1', 'ΔV4', 'ΔV5_MT']].head())

if __name__ == "__main__":
    verify_c3_2()
