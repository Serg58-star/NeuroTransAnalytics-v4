"""
src.c35_visualization.exploratory_controller

This module implements the ExploratoryController, which serves as the single
bridge between the GUI layer and the C3.x exploratory computation layer.
"""

import numpy as np
from typing import Dict, Any

from src.c3x_exploratory.multimodality import MultimodalityDetection
from src.c3x_exploratory.change_point import ChangePointDetection
from src.c3x_exploratory.synthetic_generators import (
    generate_mixture_distribution, 
    generate_time_series_with_shifts
)
from src.c3x_exploratory.persistence import save_artifact


class ExploratoryController:
    """
    Orchestrates the execution of exploratory procedures.
    Ensures architectural boundaries are respected.
    """

    def run_multimodality(self, params: Dict[str, Any]) -> str:
        """
        Executes Multimodality Detection with provided parameters.
        Uses synthetic data generation for now (Synthetic First policy).
        """
        # 1. Extract and validate common params
        # Note: In real scenarios, n_samples/modes would come from data selection.
        # For now, we use defaults or extracted params.
        seed = params.get("seed", 42)
        n_samples = params.get("n_samples", 500)
        modes = params.get("modes", 2)
        separation = params.get("separation", 3.0)
        
        # 2. Generate Data (Synthetic First)
        data = generate_mixture_distribution(n_samples, modes, separation, seed)
        
        # 3. Initialize Procedure
        procedure = MultimodalityDetection(
            bandwidth=params.get("bandwidth", "scott"),
            prominence_ratio=params.get("prominence_ratio", 0.05),
            n_grid=params.get("n_grid", 100)
        )
        
        # 4. Execute
        artifact = procedure.execute(data, seed)
        
        # 5. Persist
        filepath = save_artifact(artifact)
        return filepath

    def run_change_point(self, params: Dict[str, Any]) -> str:
        """
        Executes Change-Point Detection with provided parameters.
        """
        seed = params.get("seed", 42)
        n_samples = params.get("n_samples", 200)
        shifts = params.get("shifts", 1)
        magnitude = params.get("magnitude", 2.0)
        
        # 1. Generate Data (Synthetic First)
        data = generate_time_series_with_shifts(n_samples, shifts, magnitude, seed)
        
        # 2. Initialize Procedure
        procedure = ChangePointDetection(
            window_size=params.get("window_size", 10),
            threshold=params.get("threshold", 1.0),
            normalize=params.get("normalize", False),
            search_radius=params.get("search_radius")
        )
        
        # 3. Execute
        artifact = procedure.execute(data, seed)
        
        # 4. Persist
        filepath = save_artifact(artifact)
        return filepath
