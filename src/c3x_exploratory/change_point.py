"""
c3x_exploratory.change_point

This module implements the Change-Point Detection exploratory procedure.
Follows Task 9 requirements.
"""

import datetime
import numpy as np
from typing import Dict, Any

from src.shared.artifacts import TemporalStructureResult


PROCEDURE_VERSION = "1.1.0"


class ChangePointDetection:
    """
    Implementation of the Change-Point Detection exploratory procedure.
    Uses a deterministic rolling mean difference approach.
    """

    def __init__(
        self,
        window_size: int = 10,
        threshold: float = 1.0,
        minimum_segment_length: int = 10,
        search_radius: int | None = None,
        normalize: bool = False
    ):
        """
        Initialization of the procedure with fixed parameters.
        
        Args:
            window_size: Size of the window for computing local means.
            threshold: Difference threshold for detection.
            minimum_segment_length: Minimum distance between detected points.
            search_radius: Neighborhood for local maxima check (None -> window_size // 2).
            normalize: If True, divides statistic by signal standard deviation.
        """
        self.goal = "Identify structural mean shifts in time-series data."
        
        # Explicit search_radius derivation
        radius = search_radius if search_radius is not None else window_size // 2
        
        self.parameters = {
            "window_size": window_size,
            "threshold": threshold,
            "minimum_segment_length": minimum_segment_length,
            "search_radius": radius,
            "normalize": normalize
        }
        self.reproducibility_notes = "Deterministic rolling mean difference."

    def execute(self, data: np.ndarray, seed: int) -> TemporalStructureResult:
        """
        Executes change-point detection on the provided time-series.
        
        Args:
            data: Uni-dimensional time-series data.
            seed: Seed for the original data generation (if synthetic).
            
        Returns:
            TemporalStructureResult: Formal artifact containing identified structure.
        """
        n = len(data)
        window = self.parameters["window_size"]
        threshold = self.parameters["threshold"]
        min_len = self.parameters["minimum_segment_length"]
        radius = self.parameters["search_radius"]
        
        # 1. Compute Statistic Curve (Absolute mean difference)
        statistic_curve = np.zeros(n)
        for t in range(window, n - window):
            m1 = np.mean(data[t - window : t])
            m2 = np.mean(data[t : t + window])
            statistic_curve[t] = abs(m1 - m2)
            
        # 2. Optional scale normalization
        if self.parameters["normalize"]:
            std_dev = np.std(data)
            if std_dev > 0:
                statistic_curve = statistic_curve / std_dev
        
        # 3. Local Maxima Detection & Filtering
        detected_points = []
        last_cp = -min_len
        
        for t in range(window, n - window):
            if statistic_curve[t] > threshold:
                # Check if it's a local maximum within explicit search_radius
                is_local_max = True
                for neighbor in range(max(window, t - radius), min(n - window, t + radius + 1)):
                    if statistic_curve[neighbor] > statistic_curve[t]:
                        is_local_max = False
                        break
                
                if is_local_max and (t - last_cp >= min_len):
                    detected_points.append(int(t))
                    last_cp = t
                    
        # 4. Create Result Artifact
        result = TemporalStructureResult(
            procedure_version=PROCEDURE_VERSION,
            detected_change_points=detected_points,
            statistic_curve=statistic_curve.tolist(),
            input_parameters=self.parameters,
            seed=seed,
            timestamp=datetime.datetime.now().isoformat()
        )
        
        return result

    @property
    def non_interpretation_clause(self) -> str:
        """Mandatory architectural clause."""
        return (
            "This procedure identifies structural changes in time-series data. "
            "It is exploratory and descriptive, and does not imply interpretation "
            "or evaluation."
        )
