"""
src.c35_visualization.exploratory_adapters

This module contains visualization adapters for C3.x exploratory artifacts.
It maps structural findings to visual representations in a deterministic,
read-only manner.
"""

from typing import Any, Dict, List
import numpy as np
from src.shared.artifacts import DistributionStructureResult, TemporalStructureResult


def get_distribution_plot_data(artifact: DistributionStructureResult) -> Dict[str, Any]:
    """
    Prepares data for plotting a distribution structure (Task 8).
    
    Returns a dictionary of plot-ready components.
    """
    return {
        "x_grid": np.array(artifact.density_grid),
        "y_density": np.array(artifact.density_curve),
        "peaks_x": np.array(artifact.detected_peaks),
        "peaks_y": [float(np.interp(p, artifact.density_grid, artifact.density_curve)) for p in artifact.detected_peaks],
        "label_x": "Value",
        "label_y": "Density",
        "title": f"Distribution Analysis (Modes: {artifact.number_of_modes})"
    }


def get_temporal_plot_data(artifact: TemporalStructureResult) -> Dict[str, Any]:
    """
    Prepares data for plotting a temporal structure (Task 9).
    
    Returns a dictionary of plot-ready components.
    """
    # Note: The artifact does not store the original raw time-series data
    # (only the detection statistic). In a real case, the GUI would load 
    # the signal separately or the artifact would contain a sample.
    # For now, we visualize the statistic curve and the change points.
    
    indices = np.arange(len(artifact.statistic_curve))
    
    return {
        "indices": indices,
        "statistic": np.array(artifact.statistic_curve),
        "change_points_x": np.array(artifact.detected_change_points),
        "change_points_y": [artifact.statistic_curve[cp] for cp in artifact.detected_change_points],
        "label_x": "Time Index",
        "label_y": "Detection Statistic",
        "title": f"Temporal Analysis (Change Points: {len(artifact.detected_change_points)})"
    }
