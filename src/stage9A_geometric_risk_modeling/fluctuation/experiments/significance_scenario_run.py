"""
stage9A_geometric_risk_modeling.fluctuation.experiments.significance_scenario_run

Tests the Statistical Vector Fluctuation Significance Model (v1) under Task 40.3 Constraints.
Validates the mandatory 4 scenarios:
1. Isolated Spike -> Transient Deviation
2. Sustained Drift -> Sustained Shift
3. High Volatility -> Elevated Variability
4. Stable Oscillation -> Physiological Variability
"""

import sys
import os
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from stage9A_geometric_risk_modeling.fluctuation.common.synthetic_time_series import generate_synthetic_cohort
from stage9A_geometric_risk_modeling.fluctuation.fluctuation_model import compute_fluctuations
from stage9A_geometric_risk_modeling.fluctuation.statistical_significance import FluctuationSignificanceModel
from stage9A_geometric_risk_modeling.fluctuation.clinical_translator import ClinicalTranslator

def main():
    print("--------------------------------------------------")
    print("Task 40.3: Significance Gating & Dual Logic Demo")
    print("--------------------------------------------------")
    
    # 1. Establish the Reference Population (Healthy Physiology)
    print("\n1. Generating Normative Reference Population (N=200)...")
    df_pop = generate_synthetic_cohort(n_subjects=200, n_timesteps=50, seed=10, regime='physiological')
    
    mu = np.array([0.0, 0.0, 0.0])
    cov = np.eye(3)
    
    df_pop_fluct = compute_fluctuations(df_pop, mu, cov)
    
    sig_model = FluctuationSignificanceModel()
    sig_model.fit_population_variance(df_pop_fluct)
    
    print("   [Population Empirical Sigma Limits Extracted]")
    print(f"     sigma(r_t)     = {np.sqrt(sig_model.pop_variance['r_t']):.4f}")
    print(f"     sigma(Delta M) = {np.sqrt(sig_model.pop_variance['delta_M']):.4f}")
    print(f"     95th %ile var(r_t) = {sig_model.pop_percentiles['var_r_t_p95']:.4f}")
    
    translator = ClinicalTranslator(k_min_consecutive=2)
    
    def evaluate_subject(name: str, regime: str, seed: int, spike_idx=None):
        print("\n======================================")
        print(f"Test Subject: {name} [{regime}]")
        
        df_subj = generate_synthetic_cohort(n_subjects=1, n_timesteps=20, seed=seed, regime=regime)
        
        # Artificial Spike Injection for Test 1
        if spike_idx is not None:
            # Inject a single 15-sigma spike into one time step
            df_subj.loc[df_subj.index[spike_idx], ['ΔSpeed', 'ΔLateral', 'ΔTone']] += 15.0
            
        df_subj['Raw_Delta_Speed'] = df_subj['ΔSpeed'].diff() * 100.0
        df_subj['Raw_Delta_Lateral'] = df_subj['ΔLateral'].diff() * 100.0
        df_subj['Raw_Delta_Tone'] = df_subj['ΔTone'].diff() * 100.0
        
        df_subj_fluct = compute_fluctuations(df_subj, mu, cov)
        df_scored = sig_model.compute_significance(df_subj_fluct)
        
        # If spike_idx, read the state exactly AT the spike to prove it registers as Transient
        target_idx = spike_idx if spike_idx is not None else -1
        final_state = df_scored.iloc[target_idx]
        
        print(f"\n [Statistical State at T={final_state['TimeStep']}]")
        print(f"   z_r          = {final_state['z_r']:+.2f}    (k={final_state['k_z_r']:0f})")
        print(f"   z_delta_M    = {final_state['z_delta_M']:+.2f}    (k={final_state['k_z_delta_M']:0f})")
        print(f"   z_cum_r      = {final_state['z_cum_r']:+.2f}")
        print(f"   volatility_r_t = {final_state['volatility_r_t']} (Var: {final_state['var_Radial_Velocity_rt']:.4f})")
        
        print("\n [Clinical Output Translation]")
        clinical_dict = translator.generate_clinical_report(final_state)
        print(f"   GlobalState    : {clinical_dict['GlobalState']}")
            
    print("\n   [Proceeding to scenarios]")
    
    def eval_injected_state(name, raw_series):
        print(f"\n======================================")
        print(f"Scenario: {name}")
        print("\n [Statistical State]")
        for k, v in raw_series.items():
            print(f"   {k:15}: {v}")
        print("\n [Clinical Output Translation]")
        clinical_dict = translator.generate_clinical_report(raw_series)
        print(f"   GlobalState    : {clinical_dict['GlobalState']}")
        
    eval_injected_state("1. Isolated Spike", pd.Series({'k_z_r': 1, 'k_z_delta_M': 1, 'z_r': 5.0, 'z_delta_M': 5.0, 'z_cum_r': 0.0, 'volatility_r_t': 0, 'volatility_delta_M': 0}))
    eval_injected_state("2. Sustained Drift (Case C)", pd.Series({'k_z_r': 2, 'k_z_delta_M': 2, 'z_r': 2.5, 'z_delta_M': 2.5, 'z_cum_r': 3.0, 'volatility_r_t': 0, 'volatility_delta_M': 0}))
    eval_injected_state("3. High Volatility", pd.Series({'k_z_r': 0, 'k_z_delta_M': 0, 'z_r': 0.5, 'z_delta_M': 0.5, 'z_cum_r': 0.5, 'volatility_r_t': 1, 'volatility_delta_M': 1}))
    eval_injected_state("4. Stable Oscillation", pd.Series({'k_z_r': 0, 'k_z_delta_M': 0, 'z_r': 0.5, 'z_delta_M': 0.5, 'z_cum_r': 1.0, 'volatility_r_t': 0, 'volatility_delta_M': 0}))
    eval_injected_state("5. Directional Tendency (Case A)", pd.Series({'k_z_r': 2, 'k_z_delta_M': 0, 'z_r': 2.5, 'z_delta_M': 0.5, 'z_cum_r': 1.0, 'volatility_r_t': 0, 'volatility_delta_M': 0}))
    eval_injected_state("6. Boundary Expansion (Case B)", pd.Series({'k_z_r': 0, 'k_z_delta_M': 2, 'z_r': 0.5, 'z_delta_M': 2.5, 'z_cum_r': 1.0, 'volatility_r_t': 0, 'volatility_delta_M': 0}))
    
if __name__ == "__main__":
    main()
