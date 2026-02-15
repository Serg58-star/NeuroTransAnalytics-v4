"""
c3_core.qc_aggregation.qc_aggregation_v4

Implementation of the C3.3 QC & Aggregation layer for model v4.
Version: qc_aggregation_v4.0.0
Robust statistical aggregation using Median, MAD, and IQR.
"""

import pandas as pd
import numpy as np

class QCAggregationV4:
    """
    QC and Robust Aggregation for NeuroTransAnalytics-v4.
    Processes ComponentFrame into AggregatedFrame.
    """
    
    def __init__(self):
        pass

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes QC filtering and robust aggregation.
        
        Args:
            df: ComponentFrame from C3.2.
            
        Returns:
            AggregatedFrame (DataFrame) with robust stats per session/test.
        """
        # 1. Apply QC filter (only keep valid events for computation)
        # Note: We do NOT delete rows from the input, we just filter for aggregation
        valid_df = df[df['technical_qc_flag'] == True].copy()
        
        if valid_df.empty:
            # Return empty structure if no valid data
            return self._create_empty_aggregated_frame()
            
        # 2. Define robust aggregation functions
        def mad(x):
            m = x.median()
            return (x - m).abs().median()

        def iqr(x):
            return x.quantile(0.75) - x.quantile(0.25)

        # 3. Grouping
        # subject_id and session_id are usually enough, but test_type is critical
        group_cols = ['subject_id', 'session_id', 'test_type']
        val_cols = ['rt_ms', 'ΔV1', 'ΔV4', 'ΔV5_MT']
        
        # 4. Aggregate
        grouped = valid_df.groupby(group_cols)
        
        # Count valid responses per group
        counts = grouped.size().reset_index(name='count_valid')
        
        # Calculate Medians
        medians = grouped[val_cols].median().reset_index()
        medians = medians.rename(columns={c: f"median_{c}" for c in val_cols})
        
        # Calculate MADs
        mads = grouped[val_cols].agg(mad).reset_index()
        mads = mads.rename(columns={c: f"mad_{c}" for c in val_cols})
        
        # Calculate IQRs
        iqrs = grouped[val_cols].agg(iqr).reset_index()
        iqrs = iqrs.rename(columns={c: f"iqr_{c}" for c in val_cols})
        
        # 5. Merge all metrics
        agg_frame = pd.merge(counts, medians, on=group_cols)
        agg_frame = pd.merge(agg_frame, mads, on=group_cols)
        agg_frame = pd.merge(agg_frame, iqrs, on=group_cols)
        
        # Add basic subject metadata (age, sex) back to the aggregated frame
        # These are constant per subject/session, so we can just grab the first value
        metadata = valid_df.groupby(['subject_id', 'session_id']).agg({
            'age': 'first',
            'sex': 'first'
        }).reset_index()
        
        agg_frame = pd.merge(agg_frame, metadata, on=['subject_id', 'session_id'], how='left')
        
        # Final column reordering for readability
        ordered_cols = [
            'subject_id', 'session_id', 'age', 'sex', 'test_type', 'count_valid',
            'median_rt_ms', 'mad_rt_ms', 'iqr_rt_ms',
            'median_ΔV1', 'mad_ΔV1', 'iqr_ΔV1',
            'median_ΔV4', 'mad_ΔV4', 'iqr_ΔV4',
            'median_ΔV5_MT', 'mad_ΔV5_MT', 'iqr_ΔV5_MT'
        ]
        
        # Handle cases where some ΔV columns might be all NaN (e.g. if Tst1 baseline was missing)
        present_cols = [c for c in ordered_cols if c in agg_frame.columns]
        
        return agg_frame[present_cols]

    def _create_empty_aggregated_frame(self) -> pd.DataFrame:
        cols = [
            'subject_id', 'session_id', 'age', 'sex', 'test_type', 'count_valid',
            'median_rt_ms', 'mad_rt_ms', 'iqr_rt_ms',
            'median_ΔV1', 'mad_ΔV1', 'iqr_ΔV1',
            'median_ΔV4', 'mad_ΔV4', 'iqr_ΔV4',
            'median_ΔV5_MT', 'mad_ΔV5_MT', 'iqr_ΔV5_MT'
        ]
        return pd.DataFrame(columns=cols)
