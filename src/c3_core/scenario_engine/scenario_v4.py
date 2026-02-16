"""
c3_core.scenario_engine.scenario_v4

Implementation of the C3.4 Scenario Computation layer for model v4.
Version: scenario_v4.0.0
Initiates A0 baseline scenarios based on AggregatedFrame data.
"""

import pandas as pd
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
            
        # 2. Map fields to scenario structure
        res = tst1[[
            'subject_id', 'session_id', 'count_valid'
        ]].copy()
        
        res['baseline_median'] = tst1['median_ΔV1']
        res['baseline_mad'] = tst1['mad_ΔV1']
        res['baseline_iqr'] = tst1['iqr_ΔV1']
        
        return res

    def run_a0_1(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        A0.1 — ΔV1 Variability Profile.
        Focuses on the variability metrics of the V1 component.
        """
        # 1. Select Tst1 only
        tst1 = df[df['test_type'] == 'Tst1'].copy()
        
        if tst1.empty:
            return pd.DataFrame()
            
        # 2. Map fields to scenario structure
        res = tst1[[
            'subject_id', 'session_id'
        ]].copy()
        
        res['variability_mad'] = tst1['mad_ΔV1']
        res['variability_iqr'] = tst1['iqr_ΔV1']
        
        return res

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

        # 3. Add Metadata from centralized registry
        sub_stats['scenario_code'] = "A0.2"
        sub_stats['scenario_version'] = PIPELINE_VERSIONS['scenario_version']
        sub_stats['etl_version'] = PIPELINE_VERSIONS['etl_version']
        sub_stats['component_algo_version'] = PIPELINE_VERSIONS['component_algo_version']
        sub_stats['qc_version'] = PIPELINE_VERSIONS['qc_version']

        # 4. Deterministic sorting (architectural requirement)
        sub_stats = sub_stats.sort_values(by='subject_id').reset_index(drop=True)

        return sub_stats

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
