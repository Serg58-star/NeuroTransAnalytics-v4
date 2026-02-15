"""
c3_core.etl.etl_v4

Implementation of the C3.1 ETL Pipeline for model v4.
Version: etl_v4.1.2
Strictly read-only, deterministic, and non-interpretative.
"""

import sqlite3
import pandas as pd
import numpy as np
from typing import Optional, List, Union
from pathlib import Path
from datetime import datetime

# Architectural invariants
MIN_RT_MS = 135  # Architectural invariant (MinRedLight, 25.12.2016)

class ETLPipeline:
    """
    ETL Pipeline for extracting and normalizing neurotrans data from SQLite.
    Version: etl_v4.1.2
    """
    
    def __init__(self, db_path: str = "neuro_data.db"):
        self.db_path = db_path

    def run(self) -> pd.DataFrame:
        """
        Executes the full ETL pipeline.
        """
        with sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True) as conn:
            # 1. Extract
            users_df = self._extract_users(conn)
            trials_df = self._extract_trials(conn)
            meta_simple = self._extract_metadata(conn, "metadata_simple")
            meta_color = self._extract_metadata(conn, "metadata_color_red")
            meta_shift = self._extract_metadata(conn, "metadata_shift")
            
            # 2. Transform
            event_frame = self._build_event_frame(
                trials_df, 
                users_df,
                {"simple": meta_simple, "color": meta_color, "shift": meta_shift}
            )
            
            # 3. Validate
            event_frame = self._validate_integrity(event_frame, users_df)
            
            return event_frame

    def _extract_users(self, conn: sqlite3.Connection) -> pd.DataFrame:
        return pd.read_sql_query("SELECT * FROM users", conn)

    def _extract_trials(self, conn: sqlite3.Connection) -> pd.DataFrame:
        return pd.read_sql_query("SELECT * FROM trials", conn)

    def _extract_metadata(self, conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
        return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

    def _calculate_age(self, test_date_str: str, birth_date_str: str) -> Optional[int]:
        """Calculates age from test date and birth date. Returns None on error."""
        try:
            test_date = datetime.strptime(test_date_str, '%Y-%m-%d')
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
            age = test_date.year - birth_date.year - ((test_date.month, test_date.day) < (birth_date.month, birth_date.day))
            return int(age)
        except (ValueError, TypeError):
            return None

    def _build_event_frame(self, trials_df: pd.DataFrame, users_df: pd.DataFrame, meta_dfs: dict) -> pd.DataFrame:
        """
        Normalizes wide trials table into vertical EventFrame and includes subject attributes.
        """
        # Mapping gender to sex (0 -> 'F', 1 -> 'M')
        users_df = users_df.copy()
        users_df['sex'] = users_df['gender'].map({0: 'F', 1: 'M'})
        
        # trial_id is renamed to session_id in EventFrame
        id_vars = ['subject_id', 'trial_id', 'test_date', 'test_time']
        
        test_types = {
            'Tst1': 'simple',
            'Tst2': 'color',
            'Tst3': 'shift'
        }
        
        all_events = []
        
        for t_prefix, meta_key in test_types.items():
            cols = [f"{t_prefix.lower()}_{i}" for i in range(1, 37)]
            
            melted = pd.melt(
                trials_df,
                id_vars=id_vars,
                value_vars=cols,
                var_name='stimulus_raw',
                value_name='rt_ms'
            )
            
            melted['stimulus_index'] = melted['stimulus_raw'].str.extract(r'tst\d+_(\d+)', expand=False).astype(int)
            melted['test_type'] = t_prefix
            
            # Join with metadata
            meta_df = meta_dfs[meta_key].copy()
            meta_df = meta_df.rename(columns={'stimulus_id': 'stimulus_index'})
            
            merged = pd.merge(melted, meta_df, on='stimulus_index', how='left')
            
            # Map metadata fields
            merged['psi_pre_ms'] = merged['psi_ms']
            merged['stimulus_color'] = merged['color']
            merged['stimulus_location'] = merged['position']

            all_events.append(merged)
            
        event_frame = pd.concat(all_events, ignore_index=True)
        
        # Merge with users for age and sex
        event_frame = pd.merge(event_frame, users_df[['subject_id', 'birth_date', 'sex']], on='subject_id', how='left')
        
        # Calculate age
        event_frame['age'] = event_frame.apply(
            lambda x: self._calculate_age(x['test_date'], x['birth_date']), axis=1
        )
        
        # Final Rename and Selection
        event_frame = event_frame.rename(columns={'trial_id': 'session_id'})
        
        keep_cols = [
            'subject_id', 'session_id', 'age', 'sex', 'test_type', 
            'stimulus_index', 'rt_ms', 'psi_pre_ms', 
            'stimulus_color', 'stimulus_location'
        ]
        
        if 'shift_parameter' in event_frame.columns:
            keep_cols.append('shift_parameter')
            
        return event_frame[keep_cols]

    def _validate_integrity(self, df: pd.DataFrame, users_df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs technical QC checks.
        """
        df['technical_qc_flag'] = True
        
        # 1. NaN RT check
        df.loc[df['rt_ms'].isna(), 'technical_qc_flag'] = False
        
        # 2. RT threshold check: RT >= 135 ms
        df.loc[df['rt_ms'] < MIN_RT_MS, 'technical_qc_flag'] = False
        
        # 3. Metadata existence check
        df.loc[df['psi_pre_ms'].isna(), 'technical_qc_flag'] = False
        
        # 4. Session count check (36 reactions per test)
        counts = df.groupby(['session_id', 'test_type']).size().reset_index(name='count')
        invalid_sessions = counts[counts['count'] != 36]['session_id'].unique()
        if len(invalid_sessions) > 0:
            df.loc[df['session_id'].isin(invalid_sessions), 'technical_qc_flag'] = False
            
        # 5. Subject existence check
        valid_subject_ids = users_df['subject_id'].unique()
        df.loc[~df['subject_id'].isin(valid_subject_ids), 'technical_qc_flag'] = False
        
        # 6. Age check (flag None/NaN ages)
        df.loc[df['age'].isna(), 'technical_qc_flag'] = False
            
        return df

    def export_parquet(self, df: pd.DataFrame, output_path: str):
        """
        Optional export to Parquet.
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output_path, index=False)
