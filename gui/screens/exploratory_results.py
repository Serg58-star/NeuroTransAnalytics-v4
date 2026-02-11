"""
gui.screens.exploratory_results

This module implements the Exploratory Results screen (C3.5).
It provides a read-only interface for browsing and viewing C3.x artifacts.
"""

import os
from typing import List, Optional
from src.c3x_exploratory.persistence import load_artifact, ARTIFACT_ROOT
from src.shared.artifacts import DistributionStructureResult, TemporalStructureResult
from src.c35_visualization.exploratory_adapters import get_distribution_plot_data, get_temporal_plot_data


class ExploratoryResultsController:
    """
    Passive controller for the Exploratory Results screen.
    Strictly read-only.
    """

    def __init__(self, root_dir: str = ARTIFACT_ROOT):
        self.root_dir = root_dir

    def list_procedures(self) -> List[str]:
        """Lists available procedures based on existing artifact directories."""
        if not os.path.exists(self.root_dir):
            return []
        return [d for d in os.listdir(self.root_dir) if os.path.isdir(os.path.join(self.root_dir, d))]

    def list_artifacts(self, procedure_name: str) -> List[str]:
        """Lists available JSON artifacts for a specific procedure, newest first."""
        proc_path = os.path.join(self.root_dir, procedure_name)
        if not os.path.exists(proc_path):
            return []
        files = [f for f in os.listdir(proc_path) if f.endswith(".json")]
        # Sort by filename (which starts with ISO timestamp)
        return sorted(files, reverse=True)

    def load_result(self, procedure_name: str, filename: str) -> Optional[object]:
        """Loads a specific artifact via the persistence layer."""
        path = os.path.join(self.root_dir, procedure_name, filename)
        try:
            return load_artifact(path)
        except Exception as e:
            print(f"Error loading artifact: {e}")
            return None


class ExploratoryResultsView:
    """
    Mock View class demonstrating how the GUI layout interacts with the adapters.
    Following Task 6 and Task 11 specifications.
    """

    def __init__(self, controller: ExploratoryResultsController):
        self.controller = controller
        self.current_artifact = None

    def display_artifact(self, procedure_name: str, filename: str):
        """
        Simulates the logic for displaying an artifact on screen.
        """
        artifact = self.controller.load_result(procedure_name, filename)
        if not artifact:
            return

        print(f"\n--- DISPLAYING ARTIFACT: {filename} ---")
        
        # 1. Provenance Panel Logic
        print(f"[PROVENANCE PANEL]")
        print(f"  Procedure: {artifact.procedure_name} (v{artifact.procedure_version})")
        print(f"  Timestamp: {artifact.timestamp}")
        print(f"  Parameters: {artifact.input_parameters}")
        print(f"  CLAUSE: {artifact.non_interpretation_clause}")

        # 2. Visualization Panel Logic (Adapter Call)
        print(f"\n[VISUALIZATION PANEL]")
        if isinstance(artifact, DistributionStructureResult):
            plot_data = get_distribution_plot_data(artifact)
            print(f"  Mode: Distribution Histogram (rendered from {len(plot_data['x_grid'])} points)")
            print(f"  Highlights: {len(plot_data['peaks_x'])} detected peaks.")
            
        elif isinstance(artifact, TemporalStructureResult):
            plot_data = get_temporal_plot_data(artifact)
            print(f"  Mode: Time-Series Statistic (rendered from {len(plot_data['indices'])} points)")
            print(f"  Highlights: {len(plot_data['change_points_x'])} detected change points.")
        
        print(f"--- END DISPLAY ---\n")
