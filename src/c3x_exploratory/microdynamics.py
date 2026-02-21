"""
c3x_exploratory.microdynamics

This module implements the Stage 5 Microdynamic Architecture exploratory procedure.
Follows Task 34 requirements.
"""

import numpy as np
import scipy.stats as stats
from typing import Dict, Any, Tuple


class MicrodynamicAnalysis:
    """
    Implementation of the Stage 5 Microdynamic Analysis exploratory procedure.
    Analyzes trial-level temporal dynamics within a test sequence.
    """

    def __init__(
        self,
        n_blocks: int = 3,
        acf_lags: int = 5,
        burst_threshold_mad: float = 1.0,
        n_permutations: int = 1000
    ):
        """
        Initialization of the procedure with fixed parameters.
        
        Args:
            n_blocks: Number of temporal blocks for decomposition (Block XX).
            acf_lags: Maximum lag for ACF computation (Block XXI).
            burst_threshold_mad: Threshold in MADs for burst detection (Block XXII).
            n_permutations: Number of shuffles for structural stability check (Block XXIII).
        """
        self.procedure_name = "Stage 5 Microdynamic Analysis"
        self.goal = "To compute structural representations of temporal dynamics within a 36-trial test."
        
        self.parameters = {
            "n_blocks": n_blocks,
            "acf_lags": acf_lags,
            "burst_threshold_mad": burst_threshold_mad,
            "n_permutations": n_permutations
        }
        self.reproducibility_notes = "Deterministic aggregations and deterministic pseudo-random permutations."

    @property
    def non_interpretation_clause(self) -> str:
        """Mandatory architectural clause."""
        return (
            "This procedure is exploratory and descriptive. "
            "It produces structural representations only and does not imply interpretation, "
            "inference, or evaluation."
        )

    def analyze_block_decomposition(self, rt_series: np.ndarray) -> Dict[str, Any]:
        """Block XX: Block decomposition (3x12)."""
        n_blocks = self.parameters["n_blocks"]
        n_trials = len(rt_series)
        
        if n_trials % n_blocks != 0:
            raise ValueError(f"Series length {n_trials} is not divisible by {n_blocks} blocks.")
            
        block_size = n_trials // n_blocks
        
        block_medians = []
        block_mads = []
        
        for i in range(n_blocks):
            block_data = rt_series[i * block_size : (i + 1) * block_size]
            median = np.median(block_data)
            mad = np.median(np.abs(block_data - median))
            block_medians.append(median)
            block_mads.append(mad)
            
        # Linear trend: RT median ~ block index
        block_indices = np.arange(1, n_blocks + 1)
        slope, intercept, r_value, p_value, std_err = stats.linregress(block_indices, block_medians)
        
        return {
            "block_medians": block_medians,
            "block_mads": block_mads,
            "trend_slope": slope,
            "trend_p_value": p_value
        }

    def analyze_autocorrelation(self, rt_series: np.ndarray) -> Dict[str, Any]:
        """Block XXI: Autocorrelation RT (ACF & Ljung-Box)."""
        lags = self.parameters["acf_lags"]
        n = len(rt_series)
        
        mean_rt = np.mean(rt_series)
        var_rt = np.var(rt_series)
        
        acf_values = []
        if var_rt == 0:
            acf_values = [0.0] * lags
            lb_stat = 0.0
            lb_p = 1.0
        else:
            for k in range(1, lags + 1):
                cov = np.sum((rt_series[:-k] - mean_rt) * (rt_series[k:] - mean_rt)) / n
                acf_values.append(cov / var_rt)
                
            # Ljung-Box Test (simple implementation)
            lb_stat = n * (n + 2) * sum((acf_values[k-1]**2) / (n - k) for k in range(1, lags + 1))
            lb_p = stats.chi2.sf(lb_stat, lags)
            
        return {
            "acf_lags": acf_values,
            "acf_lag1": acf_values[0] if lags > 0 else 0.0,
            "ljung_box_stat": lb_stat,
            "ljung_box_p_value": lb_p
        }

    def analyze_bursts(self, rt_series: np.ndarray) -> Dict[str, Any]:
        """Block XXII: Burst-analysis."""
        threshold_factor = self.parameters["burst_threshold_mad"]
        
        global_median = np.median(rt_series)
        global_mad = np.median(np.abs(rt_series - global_median))
        if global_mad == 0:
            global_mad = 1e-6
            
        # fast bursts: < median - mad*factor
        fast_threshold = global_median - global_mad * threshold_factor
        # slow bursts: > median + mad*factor
        slow_threshold = global_median + global_mad * threshold_factor
        
        fast_bursts = []
        slow_bursts = []
        
        current_fast_len = 0
        current_slow_len = 0
        
        for rt in rt_series:
            if rt < fast_threshold:
                current_fast_len += 1
                if current_slow_len >= 3:
                    slow_bursts.append(current_slow_len)
                current_slow_len = 0
            elif rt > slow_threshold:
                current_slow_len += 1
                if current_fast_len >= 3:
                    fast_bursts.append(current_fast_len)
                current_fast_len = 0
            else:
                if current_fast_len >= 3:
                    fast_bursts.append(current_fast_len)
                if current_slow_len >= 3:
                    slow_bursts.append(current_slow_len)
                current_fast_len = 0
                current_slow_len = 0
                
        # Catch tails
        if current_fast_len >= 3:
            fast_bursts.append(current_fast_len)
        if current_slow_len >= 3:
            slow_bursts.append(current_slow_len)
            
        return {
            "fast_burst_count": len(fast_bursts),
            "fast_burst_mean_len": np.mean(fast_bursts) if fast_bursts else 0.0,
            "slow_burst_count": len(slow_bursts),
            "slow_burst_mean_len": np.mean(slow_bursts) if slow_bursts else 0.0,
            "total_burst_frequency": len(fast_bursts) + len(slow_bursts)
        }

    def permutation_test(self, rt_series: np.ndarray, seed: int | None = None) -> Dict[str, Any]:
        """Block XXIII: Permutation test for structural stability."""
        n_permutations = self.parameters["n_permutations"]
        rng = np.random.default_rng(seed)
        
        # Original metrics
        orig_trend = self.analyze_block_decomposition(rt_series)["trend_slope"]
        orig_acf1 = self.analyze_autocorrelation(rt_series)["acf_lag1"]
        orig_bursts = self.analyze_bursts(rt_series)["total_burst_frequency"]
        
        permuted_trends = []
        permuted_acf1s = []
        permuted_bursts = []
        
        rt_copy = rt_series.copy()
        
        for _ in range(n_permutations):
            rng.shuffle(rt_copy)
            
            p_trend = self.analyze_block_decomposition(rt_copy)["trend_slope"]
            p_acf1 = self.analyze_autocorrelation(rt_copy)["acf_lag1"]
            p_bursts = self.analyze_bursts(rt_copy)["total_burst_frequency"]
            
            permuted_trends.append(p_trend)
            permuted_acf1s.append(p_acf1)
            permuted_bursts.append(p_bursts)
            
        # calculate p-values (two-tailed for trend, one-tailed for others usually, but let's do absolute for trend)
        p_val_trend = np.mean(np.abs(permuted_trends) >= np.abs(orig_trend))
        p_val_acf1 = np.mean(np.abs(permuted_acf1s) >= np.abs(orig_acf1))
        # bursts are integer counts
        p_val_bursts = np.mean(np.array(permuted_bursts) >= orig_bursts)
        
        return {
            "orig_trend_slope": orig_trend,
            "perm_p_trend": p_val_trend,
            "orig_acf1": orig_acf1,
            "perm_p_acf1": p_val_acf1,
            "orig_burst_freq": orig_bursts,
            "perm_p_bursts": p_val_bursts
        }

    def execute(self, data: np.ndarray, seed: int | None = None) -> Dict[str, Any]:
        """
        Executes the full microdynamic sequence.
        
        Args:
            data: Trial-level RT sequence (1D numpy array, ideally 36 items).
            seed: RNG seed for permutations.
            
        Returns:
            Dict containing full structural report metrics.
        """
        block_metrics = self.analyze_block_decomposition(data)
        acf_metrics = self.analyze_autocorrelation(data)
        burst_metrics = self.analyze_bursts(data)
        perm_metrics = self.permutation_test(data, seed=seed)
        
        return {
            "procedure_name": self.procedure_name,
            "non_interpretation_clause": self.non_interpretation_clause,
            "parameters": self.parameters,
            "block_decomposition": block_metrics,
            "autocorrelation": acf_metrics,
            "burst_analysis": burst_metrics,
            "permutation_test": perm_metrics
        }
