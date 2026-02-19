"""
c3_core.scenario_engine.scenario_v4

Implementation of the C3.4 Scenario Computation layer for model v4.
Version: scenario_v4.0.0
Initiates A0 baseline scenarios based on AggregatedFrame data.
"""

import pandas as pd
import numpy as np
from typing import Dict
from src.c3_core.pipeline_config import PIPELINE_VERSIONS

class ScenarioEngineV4:
    """
    Scenario Engine for NeuroTransAnalytics-v4.
    Processes AggregatedFrame into scenario-specific outputs.
    """
    
    def __init__(self):
        pass

    def run(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Executes all active scenarios.
        
        Args:
            df: AggregatedFrame from C3.3.
            
        Returns:
            Dictionary with scenario IDs as keys and DataFrames as values.
        """
        results = {}
        
        # Scenario A0.0
        results["A0.0"] = self.run_a0_0(df)
        
        # Scenario A0.1
        results["A0.1"] = self.run_a0_1(df)

        # Scenario A0.2
        results["A0.2"] = self.run_a0_2(df)

        # Scenario A0.3
        results["A0.3"] = self.run_a0_3(df)
        
        return results

    def run_a0_0(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        A0.0 — ΔV1 Baseline Stability.
        Uses Tst1 data to establish the baseline stability of the V1 component.
        """
        # 1. Select Tst1 only
        tst1 = df[df['test_type'] == 'Tst1'].copy()
        
        if tst1.empty:
            return pd.DataFrame()
            
        # 2. Fail-fast: Spatial dimension and triad check (v4.0.3)
        if 'stimulus_location' not in tst1.columns:
            raise ValueError("Spatial dimension missing in AggregatedFrame (v4.0.1+ required)")
            
        # Verify triad for each session
        for (sid, sess), group in tst1.groupby(['subject_id', 'session_id']):
            if set(group['stimulus_location']) != {'left', 'center', 'right'}:
                raise ValueError(f"Incomplete location triad for Subject {sid}, Session {sess}: {set(group['stimulus_location'])}")

        # 3. Pivot to wide format with strict mapping
        pivot = tst1.pivot(index=['subject_id', 'session_id'], columns='stimulus_location', 
                            values=['count_valid', 'median_ΔV1', 'mad_ΔV1', 'iqr_ΔV1'])
        
        mapping = {
            ('count_valid', 'left'): 'count_valid_left',
            ('count_valid', 'center'): 'count_valid_center',
            ('count_valid', 'right'): 'count_valid_right',
            ('median_ΔV1', 'left'): 'median_left',
            ('median_ΔV1', 'center'): 'median_center',
            ('median_ΔV1', 'right'): 'median_right',
            ('mad_ΔV1', 'left'): 'mad_left',
            ('mad_ΔV1', 'center'): 'mad_center',
            ('mad_ΔV1', 'right'): 'mad_right',
            ('iqr_ΔV1', 'left'): 'iqr_left',
            ('iqr_ΔV1', 'center'): 'iqr_center',
            ('iqr_ΔV1', 'right'): 'iqr_right'
        }
        
        res_cols = {}
        for (metric, loc), col_name in mapping.items():
            if (metric, loc) in pivot.columns:
                res_cols[col_name] = pivot[(metric, loc)]
            else:
                res_cols[col_name] = np.nan
        
        res = pd.DataFrame(res_cols, index=pivot.index).reset_index()
        
        return res.sort_values(by=['subject_id', 'session_id']).reset_index(drop=True)

    def run_a0_1(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        A0.1 — ΔV1 Variability Profile.
        Focuses on the variability metrics of the V1 component.
        """
        # 1. Select Tst1 only
        tst1 = df[df['test_type'] == 'Tst1'].copy()
        
        if tst1.empty:
            return pd.DataFrame()
            
        # 2. Fail-fast: Spatial dimension and triad check (v4.0.3)
        if 'stimulus_location' not in tst1.columns:
            raise ValueError("Spatial dimension missing in AggregatedFrame (v4.0.1+ required)")
            
        for (sid, sess), group in tst1.groupby(['subject_id', 'session_id']):
            if set(group['stimulus_location']) != {'left', 'center', 'right'}:
                raise ValueError(f"Incomplete location triad for Subject {sid}, Session {sess}: {set(group['stimulus_location'])}")

        # 3. Pivot to wide format with strict mapping
        pivot = tst1.pivot(index=['subject_id', 'session_id'], columns='stimulus_location', 
                            values=['mad_ΔV1', 'iqr_ΔV1'])
        
        mapping = {
            ('mad_ΔV1', 'left'): 'variability_mad_left',
            ('mad_ΔV1', 'center'): 'variability_mad_center',
            ('mad_ΔV1', 'right'): 'variability_mad_right',
            ('iqr_ΔV1', 'left'): 'variability_iqr_left',
            ('iqr_ΔV1', 'center'): 'variability_iqr_center',
            ('iqr_ΔV1', 'right'): 'variability_iqr_right'
        }
        
        res_cols = {}
        for (metric, loc), col_name in mapping.items():
            if (metric, loc) in pivot.columns:
                res_cols[col_name] = pivot[(metric, loc)]
            else:
                res_cols[col_name] = np.nan
        
        res = pd.DataFrame(res_cols, index=pivot.index).reset_index()
        
        return res.sort_values(by=['subject_id', 'session_id']).reset_index(drop=True)

    def run_a0_2(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        A0.2 — Population Structures of ΔV1.
        Aggregates session-level ΔV1 stats to subject-level structural profile.
        """
        # 1. Select Tst1 only
        tst1 = df[df['test_type'] == 'Tst1'].copy()
        if tst1.empty:
            return pd.DataFrame()

        # 2. Robust subject-level aggregation
        # We group by subject_id and take median/mad/iqr of the session medians
        def mad(x):
            m = x.median()
            return (x - m).abs().median()

        def iqr(x):
            return x.quantile(0.75) - x.quantile(0.25)

        grouped = tst1.groupby('subject_id')
        
        sub_stats = grouped['median_ΔV1'].agg(['median', mad, iqr, 'count']).reset_index()
        sub_stats.columns = ['subject_id', 'median_delta_v1_subject', 'mad_delta_v1_subject', 'iqr_delta_v1_subject', 'n_sessions']

        # 3. Deterministic sorting (architectural requirement)
        sub_stats = sub_stats.sort_values(by='subject_id').reset_index(drop=True)

        return sub_stats

    def run_a0_3(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        A0.3 — Architectural Symmetry (ΔV1).
        Analyzes differences in ΔV1 across left, center, and right fields.
        """
        # 1. Select Tst1 only
        tst1 = df[df['test_type'] == 'Tst1'].copy()
        if tst1.empty:
            return pd.DataFrame()

        # 2. Extract mediation metrics per location
        # Columns in agg frame are median_ΔV1, mad_ΔV1, iqr_ΔV1
        # Each row is (subject, session, location)
        
        # We first aggregate to subject-location level (median across sessions)
        grouped = tst1.groupby(['subject_id', 'stimulus_location'])
        stats = grouped[['median_ΔV1', 'mad_ΔV1', 'iqr_ΔV1']].median().reset_index()

        # 3. Pivot to wide format with strict mapping
        # Columns in 'stats' are subject_id, stimulus_location, median_ΔV1, mad_ΔV1, iqr_ΔV1
        pivot = stats.pivot(index='subject_id', columns='stimulus_location', 
                            values=['median_ΔV1', 'mad_ΔV1', 'iqr_ΔV1'])
        
        # Strict MultiIndex mapping (Task 25.2)
        mapping = {
            ('median_ΔV1', 'left'): 'median_left',
            ('median_ΔV1', 'center'): 'median_center',
            ('median_ΔV1', 'right'): 'median_right',
            ('mad_ΔV1', 'left'): 'mad_left',
            ('mad_ΔV1', 'center'): 'mad_center',
            ('mad_ΔV1', 'right'): 'mad_right',
            ('iqr_ΔV1', 'left'): 'iqr_left',
            ('iqr_ΔV1', 'center'): 'iqr_center',
            ('iqr_ΔV1', 'right'): 'iqr_right'
        }
        
        # Create new DataFrame from mapping to avoid MultiIndex flattening fragility
        res_cols = {}
        for (metric, loc), col_name in mapping.items():
            if (metric, loc) in pivot.columns:
                res_cols[col_name] = pivot[(metric, loc)]
            else:
                # Keep as NaN if missing (Task 25.2)
                res_cols[col_name] = np.nan
        
        pivot_final = pd.DataFrame(res_cols, index=pivot.index).reset_index()

        # 4. Calculate Differences
        pivot_final['diff_left_right'] = pivot_final['median_left'] - pivot_final['median_right']
        pivot_final['diff_left_center'] = pivot_final['median_left'] - pivot_final['median_center']
        pivot_final['diff_right_center'] = pivot_final['median_right'] - pivot_final['median_center']

        # 5. Unit-Check: Symmetry Collapse Safeguard
        valid_diffs = pivot_final[['diff_left_right', 'diff_left_center', 'diff_right_center']].dropna()
        if not valid_diffs.empty:
            if (valid_diffs == 0).all().all():
                raise ValueError("A0.3 symmetry collapse: all diffs are zero. Check pivot mapping.")

        # 6. Deterministic sorting
        pivot_final = pivot_final.sort_values(by='subject_id').reset_index(drop=True)

        return pivot_final

    def export_results(self, results: Dict[str, pd.DataFrame], output_dir: str):
        """
        Exports scenario results to Parquet files using fastparquet.
        """
        import os
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        for name, df in results.items():
            if not df.empty:
                # Sanitize name for filename (e.g. A0.0 -> A0_0)
                safe_name = name.replace(".", "_")
                path = os.path.join(output_dir, f"{safe_name}.parquet")
                df.to_parquet(path, engine="fastparquet", index=False)
                print(f"Exported Scenario {name} to {path}")
