"""
gui.adapters.exploratory_adapters

This module contains visualization adapters for C3.x exploratory artifacts.
Specifically relocated for the GUI layer.
"""

from typing import Any, Dict
import numpy as np
from src.shared.artifacts import DistributionStructureResult, TemporalStructureResult


def get_distribution_plot_data(artifact: DistributionStructureResult) -> Dict[str, Any]:
    """
    Prepares data for plotting a distribution structure (Task 8/13).
    """
    return {
        "x_values": np.array(artifact.density_grid),
        "density_values": np.array(artifact.density_curve),
        "peak_positions": np.array(artifact.detected_peaks),
    }


def get_temporal_plot_data(artifact: TemporalStructureResult) -> Dict[str, Any]:
    """
    Prepares data for plotting a temporal structure (Task 9/13).
    """
    indices = np.arange(len(artifact.statistic_curve))
    return {
        "time_index": indices,
        "signal_values": np.array(artifact.statistic_curve),
        "change_points": np.array(artifact.detected_change_points),
    }
