"""
gui.scenario_viewer.scenario_viewer

Loader for pre-computed scenario results.
"""

import os
import pandas as pd
from typing import Optional

class ScenarioLoader:
    """
    Handles loading of scenario results from persisted storage.
    """
    def __init__(self, data_dir: str = "data/derived/scenarios"):
        self.data_dir = data_dir

    def load_scenario(self, scenario_id: str) -> Optional[pd.DataFrame]:
        """
        Loads a specific scenario result by ID (e.g., 'A0.0').
        """
        safe_name = scenario_id.replace(".", "_")
        path = os.path.join(self.data_dir, f"{safe_name}.parquet")
        
        if not os.path.exists(path):
            print(f"Scenario file not found: {path}")
            return None
            
        try:
            return pd.read_parquet(path)
        except Exception as e:
            print(f"Error loading scenario {scenario_id}: {e}")
            return None
