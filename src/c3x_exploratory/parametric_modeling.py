"""
c3x_exploratory.parametric_modeling

This module implements the Parametric Distribution Modeling exploratory procedure 
(Task 35.1, Stage 6 extension).
"""

import numpy as np
import scipy.stats as stats
from typing import Dict, Any, Tuple

class ParametricModelingAnalysis:
    """
    Implementation of the Task 35.1 Parametric Distribution Modeling exploratory procedure.
    Fits theoretical distributions to empirical RT data and evaluates fit quality.
    """
    
    def __init__(self):
        self.procedure_name = "Task 35.1 Parametric Distribution Modeling"
        self.goal = "To compute structural fit metrics (AIC, BIC, Log-likelihood) across 5 generative distribution families."
        
        self.parameters = {
            "distributions_tested": ["normal", "lognormal", "gamma", "weibull", "exgaussian"]
        }
        self.reproducibility_notes = "Deterministic Maximum Likelihood Estimation algorithms via SciPy."
        
    @property
    def non_interpretation_clause(self) -> str:
        """Mandatory architectural clause."""
        return (
            "This procedure is exploratory and descriptive. "
            "It produces structural representations only and does not imply interpretation, "
            "inference, or evaluation."
        )

    def _safe_fit(self, rt_series: np.ndarray, dist_name: str) -> Dict[str, Any]:
        """Safely fits a distribution and computes metrics."""
        n = len(rt_series)
        
        if n < 5:
             # Too few points to fit reliably
             return {"ll": np.nan, "aic": np.nan, "bic": np.nan, "ks_stat": np.nan, "ks_p": np.nan, "params": ()}
             
        try:
            if dist_name == "normal":
                dist = stats.norm
                params = dist.fit(rt_series)
            elif dist_name == "lognormal":
                dist = stats.lognorm
                params = dist.fit(rt_series, floc=0) # Fix loc to 0 for strict lognormality
            elif dist_name == "gamma":
                dist = stats.gamma
                params = dist.fit(rt_series, floc=0) # Fix loc to 0
            elif dist_name == "weibull":
                dist = stats.weibull_min
                params = dist.fit(rt_series, floc=0) # Fix loc to 0
            elif dist_name == "exgaussian":
                dist = stats.exponnorm
                params = dist.fit(rt_series)
            else:
                raise ValueError(f"Unknown distribution: {dist_name}")
                
            # Log likelihood
            ll = np.sum(dist.logpdf(rt_series, *params))
            k = len(params)
            
            # AIC / BIC
            aic = 2 * k - 2 * ll
            bic = k * np.log(n) - 2 * ll
            
            # KS test against fitted distribution
            ks_stat, ks_p = stats.kstest(rt_series, dist.cdf, args=params)
            
            return {
                "ll": float(ll),
                "aic": float(aic),
                "bic": float(bic),
                "ks_stat": float(ks_stat),
                "ks_p": float(ks_p),
                "params": params
            }
        except Exception:
            # Fallback for convergence failures
            return {"ll": np.nan, "aic": np.nan, "bic": np.nan, "ks_stat": np.nan, "ks_p": np.nan, "params": ()}

    def execute(self, data: np.ndarray) -> Dict[str, Any]:
        """
        Executes the parametric fitting sequence.
        
        Args:
            data: Trial-level RT sequence (1D numpy array, ideally 36 items).
            
        Returns:
            Dict containing structural fit representation metrics for all tested models.
        """
        results = {}
        best_aic = float('inf')
        best_bic = float('inf')
        best_model_aic = None
        best_model_bic = None
        
        for dist_name in self.parameters["distributions_tested"]:
            fit_metrics = self._safe_fit(data, dist_name)
            results[dist_name] = fit_metrics
            
            if not np.isnan(fit_metrics["aic"]) and fit_metrics["aic"] < best_aic:
                best_aic = fit_metrics["aic"]
                best_model_aic = dist_name
                
            if not np.isnan(fit_metrics["bic"]) and fit_metrics["bic"] < best_bic:
                best_bic = fit_metrics["bic"]
                best_model_bic = dist_name

        results["best_fit_aic"] = best_model_aic
        results["best_fit_bic"] = best_model_bic
        
        return {
            "procedure_name": self.procedure_name,
            "non_interpretation_clause": self.non_interpretation_clause,
            "parameters": self.parameters,
            "fits": results
        }
