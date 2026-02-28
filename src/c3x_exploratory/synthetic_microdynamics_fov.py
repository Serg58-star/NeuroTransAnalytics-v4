import numpy as np
import pandas as pd

def generate_fov_synthetic_data(
    n_subjects: int = 50,
    base_rt: int = 350,
    lat_rt_diff: int = 15,    # Right is faster than Left by 15ms
    center_rt_diff: int = -25, # Center is faster than baseline by 25ms
    fatigue_slope: float = 2.0,
    recovery_factor: float = 25.0,
    noise_std: float = 30.0,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates synthetic trial-level data specifically for Central Field Of View (FOV) evaluation.
    Each 36-trial block has exactly 12 Left, 12 Center, 12 Right stimuli evenly distributed.
    """
    np.random.seed(seed)
    records = []
    
    # Pre-generate a balanced sequence of 36 FOVs: 12L, 12C, 12R
    fov_base = ['Left']*12 + ['Center']*12 + ['Right']*12
    
    for subject_id in range(1, n_subjects + 1):
        subj_intercept = np.random.normal(base_rt, 25.0)
        subj_lat_bias = np.random.normal(0, 10.0) # Subject specific lateralization variation
        
        for test in ['Tst1', 'Tst2', 'Tst3']:
            test_shifter = 0 if test == 'Tst1' else (25 if test == 'Tst2' else 50)
            
            # Shuffle FOV sequence to be pseudo-random for each block
            fov_seq = np.random.permutation(fov_base)
            
            for position in range(1, 37):
                fov = fov_seq[position - 1]
                psi = np.random.uniform(1000, 3000)
                log_psi = np.log10(psi / 1000.0)
                
                # Dynamic Effects
                psi_effect = -recovery_factor * log_psi
                position_effect = fatigue_slope * position
                
                # Spatial Effects
                fov_effect = 0.0
                if fov == 'Right':
                    fov_effect = -(lat_rt_diff + subj_lat_bias) # Right is fundamentally faster
                elif fov == 'Left':
                    fov_effect = (lat_rt_diff + subj_lat_bias)  # Left is slower
                elif fov == 'Center':
                    fov_effect = center_rt_diff                 # Center is generally fastest
                
                noise = np.random.normal(0, noise_std)
                
                rt = subj_intercept + test_shifter + psi_effect + position_effect + fov_effect + noise
                rt = max(150.0, rt)
                
                records.append({
                    'SubjectID': subject_id,
                    'TestBlock': test,
                    'Position': position,
                    'FieldOfView': fov,
                    'PSI': psi,
                    'log_PSI': log_psi,
                    'RT': rt
                })

    return pd.DataFrame(records)

if __name__ == "__main__":
    df = generate_fov_synthetic_data()
    print(f"Generated {len(df)} trials.")
    print(df['FieldOfView'].value_counts())
