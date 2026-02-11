"""
c3x_exploratory.multimodality

This module implements the Multimodality Detection exploratory procedure.
Follows Task 5 Specification and Task 8 Implementation requirements.
"""

import datetime
import numpy as np
from scipy import stats, signal
from typing import List, Optional

from src.shared.artifacts import DistributionStructureResult


PROCEDURE_VERSION = "1.1.0"


class MultimodalityDetection:
    """
    Implementation of the Multimodality Detection exploratory procedure.
    """

    def __init__(
        self,
        bandwidth: str | float = "scott",
        prominence_ratio: float = 0.05,
        n_grid: int = 100
    ):
        """
        Initialization of the procedure with fixed parameters.
        
        Args:
            bandwidth: KDE smoothing parameter ('scott', 'silverman', or float).
            prominence_ratio: Peak detection prominence relative to max density.
            n_grid: Number of points for the density grid.
        """
        self.goal = "Identify structural deviations from unimodality in RT or components."
        self.parameters = {
            "bandwidth": bandwidth,
            "prominence_ratio": prominence_ratio,
            "n_grid": n_grid,
        }
        self.reproducibility_notes = "KDE and peak detection are deterministic for fixed data."

    def execute(self, data: np.ndarray, seed: int) -> DistributionStructureResult:
        """
        Executes multimodality detection on the provided distribution.
        
        Args:
            data: Uni-dimensional input data points.
            seed: Seed for the original data generation (if synthetic).
            
        Returns:
            DistributionStructureResult: Formal artifact containing identified structure.
        """
        # 1. Compute Kernel Density Estimate
        # Deterministic Gaussian KDE
        kde = stats.gaussian_kde(data, bw_method=self.parameters["bandwidth"])
        
        # Define grid for evaluation
        grid_min, grid_max = np.min(data), np.max(data)
        # Pad grid to capture tails
        grid_pad = (grid_max - grid_min) * 0.1
        grid = np.linspace(grid_min - grid_pad, grid_max + grid_pad, self.parameters["n_grid"])
        
        density = kde.evaluate(grid)
        
        # 2. Local Maxima Detection
        # Finds indices of local peaks in the density curve.
        # Use explicit prominence threshold relative to the max density.
        max_density = np.max(density)
        peak_indices, _ = signal.find_peaks(
            density,
            prominence=max_density * self.parameters["prominence_ratio"]
        )
        
        # Map indices to data values
        detected_peaks = grid[peak_indices].tolist()
        
        # 3. Mode Count
        number_of_modes = len(detected_peaks)
        
        # 4. Create Result Artifact
        result = DistributionStructureResult(
            procedure_version=PROCEDURE_VERSION,
            number_of_modes=number_of_modes,
            density_curve=density.tolist(),
            density_grid=grid.tolist(),
            detected_peaks=detected_peaks,
            input_parameters=self.parameters,
            seed=seed,
            timestamp=datetime.datetime.now().isoformat()
        )
        
        return result

    @property
    def non_interpretation_clause(self) -> str:
        """Mandatory architectural clause."""
        return (
            "This procedure is exploratory and descriptive. It identifies structural "
            "features of distributions and does not imply interpretation, "
            "diagnosis, or evaluation."
        )
