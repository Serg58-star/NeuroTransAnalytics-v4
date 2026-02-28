import numpy as np
import pandas as pd

def generate_extended_synthetic_data(
    n_subjects: int = 50,
    fatigue_slope_linear: float = 2.0,
    fatigue_slope_quad: float = 0.05,       # Accelerating fatigue
    recovery_factor_lin: float = 25.0,
    recovery_factor_quad: float = -5.0,     # Curving recovery
    interaction_coef: float = 0.5,          # log(PSI) * Position
    noise_std: float = 30.0,
    scenario: str = "FULL",                 # "FULL", "ZERO_INTERACTION", "ZERO_NONLINEARITY"
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates synthetic trial-level data with advanced microdynamic effects.
    Supports Negative Controls for FPR evaluation.
    """
    np.random.seed(seed)
    
    # Negative Control Overrides
    if scenario == "ZERO_INTERACTION":
        interaction_coef = 0.0
    elif scenario == "ZERO_NONLINEARITY":
        fatigue_slope_quad = 0.0
        recovery_factor_quad = 0.0
        
    records = []
    tests = ['Tst1', 'Tst2', 'Tst3']
    
    # 2 Subpopulations (Clusters): 
    # Cluster 0: "Resilient" (lower base RT, lower fatigue, high recovery)
    # Cluster 1: "Fast-Fatigue" (higher base RT, steep fatigue)
    subject_clusters = np.random.choice([0, 1], size=n_subjects, p=[0.6, 0.4])
    
    for subject_id in range(1, n_subjects + 1):
        cluster = subject_clusters[subject_id - 1]
        
        # Mixed-Effects: Subject Random Intercept
        subj_intercept = np.random.normal(300 if cluster == 0 else 400, 20)
        
        # Mixed-Effects: Subject Random Slopes
        subj_fatigue_mod = np.random.normal(0, 0.5) + (0 if cluster == 0 else 1.5)
        
        for test in tests:
            test_shifter = 0 if test == 'Tst1' else (20 if test == 'Tst2' else 40)
            
            for position in range(1, 37):
                psi = np.random.uniform(1000, 3000)
                log_psi = np.log10(psi / 1000.0) # 0 to ~0.477
                
                # Base
                trial_base = subj_intercept + test_shifter
                
                # Recovery (B1) with possible nonlinearity
                psi_effect = (-recovery_factor_lin * log_psi) + (recovery_factor_quad * (log_psi**2))
                
                # Fatigue (A2) with possible nonlinearity
                # Add subject-specific random slope to linear term
                pos_linear = (fatigue_slope_linear + subj_fatigue_mod) * position
                pos_quad = fatigue_slope_quad * (position**2)
                position_effect = pos_linear + pos_quad
                
                # Interaction
                interaction_effect = interaction_coef * (log_psi * position)
                
                # Noise
                noise = np.random.normal(0, noise_std)
                
                rt = trial_base + psi_effect + position_effect + interaction_effect + noise
                rt = max(150.0, rt)
                
                records.append({
                    'SubjectID': subject_id,
                    'TestBlock': test,
                    'Cluster_GT': cluster,
                    'Position': position,
                    'PSI': psi,
                    'log_PSI': log_psi,
                    'RT': rt
                })
                
    return pd.DataFrame(records)

if __name__ == "__main__":
    df_full = generate_extended_synthetic_data(scenario="FULL")
    print(f"Generated {len(df_full)} FULL rows.")
    df_zero_int = generate_extended_synthetic_data(scenario="ZERO_INTERACTION")
    print(f"Generated {len(df_zero_int)} ZERO_INTERACTION rows.")
    df_zero_nl = generate_extended_synthetic_data(scenario="ZERO_NONLINEARITY")
    print(f"Generated {len(df_zero_nl)} ZERO_NONLINEARITY rows.")
