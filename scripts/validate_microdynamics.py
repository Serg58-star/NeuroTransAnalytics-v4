"""
scripts.validate_microdynamics

Runs the stage 5 microdynamic analysis against 4 distinct synthetic datasets
to prove that it can distinguish between stationary, trending, autocorrelated,
and bursty sequences.
"""

import sys
sys.path.append('.')

from src.c3x_exploratory.synthetic_microdynamics import (
    generate_stationary_rt,
    generate_trending_rt,
    generate_autocorrelated_rt,
    generate_bursty_rt
)
from src.c3x_exploratory.microdynamics import MicrodynamicAnalysis


def main():
    print("--- Stage 5 Microdynamics Validation ---\n")
    
    analyzer = MicrodynamicAnalysis(n_blocks=3, acf_lags=5, burst_threshold_mad=1.0, n_permutations=1000)
    
    print(analyzer.non_interpretation_clause)
    print("\nParameters used:", analyzer.parameters)
    print("\nExecuting against Synthetic Generators...\n")
    
    datasets = {
        "1. Stationary": generate_stationary_rt(seed=42),
        "2. Trending (Accelerating)": generate_trending_rt(trend_effect=-150, seed=42),
        "3. Autocorrelated (AR1)": generate_autocorrelated_rt(phi=0.7, std=50, seed=42),
        "4. Bursty (Fast)": generate_bursty_rt(burst_type='fast', burst_length=5, burst_magnitude=150, seed=42)
    }
    
    print(f"{'Dataset':<26} | {'Block Trend (p)':<16} | {'ACF Lag1':<8} | {'Burst Freq':<10} | {'Perm p_trend':<12} | {'Perm p_acf1':<11}")
    print("-" * 97)
    
    for name, data in datasets.items():
        res = analyzer.execute(data, seed=42)
        
        b = res["block_decomposition"]
        a = res["autocorrelation"]
        bu = res["burst_analysis"]
        p = res["permutation_test"]
        
        trend = f"{b['trend_slope']:>6.1f} ({b['trend_p_value']:>4.2f})"
        acf1 = f"{a['acf_lag1']:>8.2f}"
        bursts = f"{bu['total_burst_frequency']:>10}"
        p_trend = f"{p['perm_p_trend']:>12.3f}"
        p_acf1 = f"{p['perm_p_acf1']:>11.3f}"
        
        print(f"{name:<26} | {trend:<16} | {acf1:<8} | {bursts:<10} | {p_trend:<12} | {p_acf1:<11}")


if __name__ == '__main__':
    main()
