"""
Trial-Level Data Loader for Exploratory Lab

Provides READ-ONLY access to trial-level data from SQLite database.
Architecturally isolated from C3 computation layers.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any


class TrialLevelDataLoader:
    """
    Loads trial-level response events with optional filtering.
    
    This class provides direct access to raw trial data for exploratory analysis,
    bypassing the canonical C3.3 aggregation layer.
    """
    
    def __init__(self, db_path: str = "data/neurotrans.db"):
        """
        Initialize the data loader.
        
        Parameters
        ----------
        db_path : str
            Path to the SQLite database (default: data/neurotrans.db)
        """
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
    
    def load_trials(
        self,
        subject_ids: Optional[List[int]] = None,
        test_types: Optional[List[str]] = None,
        min_sessions: int = 1
    ) -> pd.DataFrame:
        """
        Load trial-level response events with stimulus metadata.
        
        Parameters
        ----------
        subject_ids : list of int, optional
            Filter by specific subject IDs. If None, load all subjects.
        test_types : list of str, optional
            Filter by test types (e.g., ['Tst1', 'Tst2']). If None, load all.
        min_sessions : int, default=1
            Minimum number of valid sessions required for a subject to be included.
        
        Returns
        -------
        pd.DataFrame
            Trial-level data with columns:
            - subject_id
            - session_id
            - test_type
            - stimulus_color
            - stimulus_location (left/center/right)
            - psi (pre-stimulus interval, ms)
            - rt (reaction time, ms)
            - is_correct
            - is_outlier
        """
        conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
        
        try:
            query = """
            SELECT 
                r.subject_id,
                r.session_id,
                s.test_type,
                s.color AS stimulus_color,
                s.location AS stimulus_location,
                s.psi,
                r.rt,
                r.is_correct,
                r.is_outlier
            FROM response_events r
            INNER JOIN stimulus_events s 
                ON r.stimulus_event_id = s.id
            WHERE s.role = 'test'
            """
            
            params = []
            
            if subject_ids is not None:
                placeholders = ','.join('?' * len(subject_ids))
                query += f" AND r.subject_id IN ({placeholders})"
                params.extend(subject_ids)
            
            if test_types is not None:
                placeholders = ','.join('?' * len(test_types))
                query += f" AND s.test_type IN ({placeholders})"
                params.extend(test_types)
            
            query += " ORDER BY r.subject_id, r.session_id, s.position_in_test"
            
            df = pd.read_sql_query(query, conn, params=params if params else None)
            
            # Filter by minimum sessions
            if min_sessions > 1:
                session_counts = df.groupby('subject_id')['session_id'].nunique()
                valid_subjects = session_counts[session_counts >= min_sessions].index
                df = df[df['subject_id'].isin(valid_subjects)]
            
            return df
            
        finally:
            conn.close()
    
    def load_subject_metadata(self) -> pd.DataFrame:
        """
        Load subject demographic metadata.
        
        Returns
        -------
        pd.DataFrame
            Subject metadata with columns: subject_id, birth_date, gender (if available)
        """
        conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
        
        try:
            query = "SELECT id AS subject_id, birth_date FROM subjects"
            df = pd.read_sql_query(query, conn)
            return df
        finally:
            conn.close()
