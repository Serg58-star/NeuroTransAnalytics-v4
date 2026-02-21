"""
c3x_exploratory.variability

This module implements the Stage 6 Variability and Tail Geometry exploratory procedure.
Follows Task 35 requirements.
"""

import numpy as np
import scipy.stats as stats
from typing import Dict, Any

class VariabilityAnalysis:
    """
    Implementation of the Stage 6 Variability Geometry exploratory procedure.
    Analyzes trial-level shape parameters independent of temporal order.
    """
    
    def __init__(self, tail_percentile: float = 90.0):
        """
        Initialization of the procedure with fixed parameters.
        
        Args:
            tail_percentile: The high percentile used for Tail Geometry analysis (Block XXV).
        """
        self.procedure_name = "Stage 6 Variability and Tail Geometry"
        self.goal = "To compute structural representations of distribution shapes and tail indices."
        
        self.parameters = {
            "tail_percentile": tail_percentile
        }
        self.reproducibility_notes = "Deterministic statistics on static distribution arrays."
        
    @property
    def non_interpretation_clause(self) -> str:
        """Mandatory architectural clause."""
        return (
            "This procedure is exploratory and descriptive. "
            "It produces structural representations only and does not imply interpretation, "
            "inference, or evaluation."
        )

    def analyze_skew_kurtosis(self, rt_series: np.ndarray) -> Dict[str, Any]:
        """Block XXIV: Skew / Kurtosis Analysis."""
        if len(rt_series) < 3:
            return {
                "skewness": 0.0,
                "kurtosis": 0.0,
                "shapiro_w": 1.0,
                "shapiro_p": 1.0
            }
            
        skew = float(stats.skew(rt_series))
        kurt = float(stats.kurtosis(rt_series)) # Fisher's definition, normal=0
        
        # Shapiro-Wilk can sometimes raise Warnings on perfectly identical inputs, so we catch potential shape issues.
        try:
            w_stat, p_val = stats.shapiro(rt_series)
        except Exception:
            w_stat, p_val = 1.0, 1.0
            
        return {
            "skewness": skew,
            "kurtosis": kurt,
            "shapiro_w": float(w_stat),
            "shapiro_p": float(p_val)
        }

    def analyze_tail_geometry(self, rt_series: np.ndarray) -> Dict[str, Any]:
        """Block XXV: Tail-layer geometry."""
        if len(rt_series) == 0:
            return {
                "tail_absolute": 0.0,
                "tail_normalized": 0.0,
                "tail_to_mad_ratio": 0.0
            }
            
        median = np.median(rt_series)
        mad = np.median(np.abs(rt_series - median))
        
        if mad == 0:
            mad = 1e-6 # avoid div by zero
            
        p90 = np.percentile(rt_series, self.parameters["tail_percentile"])
        
        tail_abs = float(p90 - median)
        
        tail_norm = 0.0
        if median > 0:
            tail_norm = float(tail_abs / median)
            
        tail_mad_ratio = float(tail_abs / mad)
        
        return {
            "tail_absolute": tail_abs,
            "tail_normalized": tail_norm,
            "tail_to_mad_ratio": tail_mad_ratio
        }

    def analyze_variance(self, rt_series: np.ndarray) -> Dict[str, Any]:
        """Block XXVI: MAD and Coefficient of Variation."""
        if len(rt_series) == 0:
            return {
                "mad": 0.0,
                "cv_classical": 0.0,
                "cv_robust": 0.0
            }
            
        median = float(np.median(rt_series))
        mad = float(np.median(np.abs(rt_series - median)))
        mean = float(np.mean(rt_series))
        std = float(np.std(rt_series))
        
        cv_classical = 0.0
        if mean > 0:
            cv_classical = std / mean
            
        cv_robust = 0.0
        if median > 0:
            cv_robust = mad / median
            
        return {
            "mad": mad,
            "cv_classical": cv_classical,
            "cv_robust": cv_robust
        }

    def execute(self, data: np.ndarray) -> Dict[str, Any]:
        """
        Executes the full variability analysis sequence.
        
        Args:
            data: Trial-level RT sequence (1D numpy array, ideally 36 items).
            
        Returns:
            Dict containing full structural report metrics.
        """
        skew_metrics = self.analyze_skew_kurtosis(data)
        tail_metrics = self.analyze_tail_geometry(data)
        var_metrics = self.analyze_variance(data)
        
        return {
            "procedure_name": self.procedure_name,
            "non_interpretation_clause": self.non_interpretation_clause,
            "parameters": self.parameters,
            "skew_kurtosis": skew_metrics,
            "tail_geometry": tail_metrics,
            "variance": var_metrics
        }
