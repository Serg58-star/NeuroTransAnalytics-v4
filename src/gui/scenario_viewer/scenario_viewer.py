"""
gui.scenario_viewer.scenario_viewer

Loader for pre-computed scenario results.
"""

from pathlib import Path
import pandas as pd
from typing import Optional

# Canonical path resolution
BASE_DIR = Path(__file__).resolve().parents[3]
SCENARIO_ROOT = BASE_DIR / "data" / "derived" / "scenarios"

class ScenarioLoader:
    """
    Handles loading of scenario results from persisted storage.
    Ensures absolute path resolution relative to project root.
    """
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or SCENARIO_ROOT

    def load_scenario(self, scenario_id: str) -> Optional[pd.DataFrame]:
        """
        Loads a specific scenario result by ID (e.g., 'A0.0').
        """
        safe_name = scenario_id.replace(".", "_")
        path = self.data_dir / f"{safe_name}.parquet"
        
        if not path.exists():
            print(f"Scenario file not found: {path}")
            return None
            
        try:
            return pd.read_parquet(path, engine="fastparquet")
        except Exception as e:
            print(f"Error loading scenario {scenario_id}: {e}")
            return None
