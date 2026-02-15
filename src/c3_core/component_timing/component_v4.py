"""
c3_core.component_timing.component_v4

Implementation of the C3.2 Component Timing Computation layer for model v4.
Version: component_v4.0.0
Strictly read-only, deterministic, non-interpretative, and non-aggregative.
"""

import pandas as pd
import numpy as np

class ComponentTimingV4:
    """
    Component Timing Computation for NeuroTransAnalytics-v4.
    Calculates ΔV1, ΔV4, and ΔV5/MT based on EventFrame.
    """
    
    def __init__(self):
        pass

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes the component timing computation.
        
        Args:
            df: EventFrame from C3.1 ETL.
            
        Returns:
            ComponentFrame (DataFrame) with added ΔV1, ΔV4, and ΔV5_MT columns.
        """
        # Ensure we don't modify the input DataFrame
        res = df.copy()
        
        # 1. Create a baseline lookup for Tst1 within each session
        # We need rt_ms for each (session_id, stimulus_index) where test_type == 'Tst1'
        tst1_baseline = res[res['test_type'] == 'Tst1'][['session_id', 'stimulus_index', 'rt_ms']].copy()
        tst1_baseline = tst1_baseline.rename(columns={'rt_ms': 'delta_v1_base'})
        
        # 2. Merge baseline into the main result dataframe
        res = pd.merge(res, tst1_baseline, on=['session_id', 'stimulus_index'], how='left')
        
        # 3. Calculate ΔV1
        # By protocol v4, ΔV1 is the baseline RT from Tst1 (regardless of the current row's test_type)
        res['ΔV1'] = res['delta_v1_base']
        
        # 4. Calculate ΔV4 (Color)
        # Only for Tst2: ΔV4 = RT(Tst2) - ΔV1
        res['ΔV4'] = np.nan
        mask_tst2 = res['test_type'] == 'Tst2'
        res.loc[mask_tst2, 'ΔV4'] = res.loc[mask_tst2, 'rt_ms'] - res.loc[mask_tst2, 'ΔV1']
        
        # 5. Calculate ΔV5/MT (Motion)
        # Only for Tst3: ΔV5_MT = RT(Tst3) - ΔV1
        res['ΔV5_MT'] = np.nan
        mask_tst3 = res['test_type'] == 'Tst3'
        res.loc[mask_tst3, 'ΔV5_MT'] = res.loc[mask_tst3, 'rt_ms'] - res.loc[mask_tst3, 'ΔV1']
        
        # Clean up temporary columns
        res = res.drop(columns=['delta_v1_base'])
        
        return res
