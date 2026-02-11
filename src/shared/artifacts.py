"""
shared.artifacts

This module defines common artifact structures for the NeuroTransAnalytics-v4 project.
These artifacts serve as the formal output of C3 and C3.x procedures.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class DistributionStructureResult:
    """
    Formal output of the Multimodality Detection procedure (Task 8).
    
    Contains structural features of a distribution without any interpretation.
    """
    procedure_version: str
    procedure_name: str = "MultimodalityDetection"
    
    # Core structural data
    number_of_modes: int = 0
    density_curve: List[float] = field(default_factory=list)  # Precomputed KDE values
    density_grid: List[float] = field(default_factory=list)   # Grid points for KDE
    detected_peaks: List[float] = field(default_factory=list) # Indices or values of peaks
    
    # Provenance and reproducibility
    input_parameters: Dict[str, Any] = field(default_factory=dict)
    seed: int = 0
    timestamp: str = ""
    
    # Mandatory Non-Interpretation Clause
    non_interpretation_clause: str = (
        "This procedure is exploratory and descriptive. It identifies structural "
        "features of distributions and does not imply interpretation, "
        "diagnosis, or evaluation."
    )
