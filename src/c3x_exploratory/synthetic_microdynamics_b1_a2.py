import numpy as np
import pandas as pd
from typing import Dict, Any

def generate_microdynamic_synthetic_data(
    n_subjects: int = 50,
    fatigue_slope: float = 2.5,        # ms increase per trial (A2 effect)
    recovery_factor: float = 30.0,     # ms decrease per log(PSI) (B1 effect)
    base_rt: float = 350.0,
    noise_std: float = 40.0,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates synthetic trial-level data for 3 test blocks (Tst1, Tst2, Tst3), each with 36 trials.
    Injects Ground Truth effects for:
    - Intra-block fatigue (Position 1-36 mapping to a linear RT increase).
    - PSI recovery (Longer PSI maps to faster RT logarithmically).
    
    Includes an anti-CV truncation logic: if within a block the running CV > 15%, 
    subsequent trials have their noise reduced/truncated to simulate experimental suppression.
    """
    np.random.seed(seed)
    
    records = []
    tests = ['Tst1', 'Tst2', 'Tst3']
    fields = ['Left', 'Center', 'Right']
    colors = ['Red', 'Green', 'Blue']
    
    for subject_id in range(1, n_subjects + 1):
        # Subject-specific base RT shifter
        subject_baseline = np.random.normal(loc=base_rt, scale=30.0)
        
        for test in tests:
            test_shifter = 0 if test == 'Tst1' else (50 if test == 'Tst2' else 100)
            
            # Anti-CV state tracker
            running_rt_list = []
            anti_cv_active = False
            
            for position in range(1, 37):
                # Structural parameters
                fov = np.random.choice(fields)
                color = np.random.choice(colors)
                psi = np.random.uniform(1000, 3000) # PSI in ms
                
                # Baseline for this specific trial
                trial_base = subject_baseline + test_shifter
                
                # B1 Effect: Recovery (faster RT with longer PSI)
                # We use log10(PSI/1000) so a 1000ms PSI is baseline, 3000ms is log10(3) * recovery_factor
                psi_effect = -recovery_factor * np.log10(psi / 1000.0)
                
                # A2 Effect: Fatigue (slower RT with position)
                position_effect = fatigue_slope * position
                
                # Noise
                current_noise_std = noise_std
                
                # Anti-CV suppression logic (simulated by truncation if CV goes high)
                if len(running_rt_list) >= 5:
                    current_cv = np.std(running_rt_list) / np.mean(running_rt_list)
                    if current_cv > 0.15:
                        anti_cv_active = True
                
                if anti_cv_active:
                    # Truncate variation to artificially reduce CV (as historical systems did by repeating trials)
                    current_noise_std = noise_std * 0.5
                
                noise = np.random.normal(0, current_noise_std)
                
                # Compile final RT
                rt = trial_base + psi_effect + position_effect + noise
                
                # Ensure no absolute negative or impossibly fast RTs
                rt = max(150.0, rt)
                
                running_rt_list.append(rt)
                
                records.append({
                    'SubjectID': subject_id,
                    'TestBlock': test,
                    'FieldOfView': fov,
                    'Color': color,
                    'Position': position,
                    'PSI': psi,
                    'RT': rt,
                    'AntiCV_Active': int(anti_cv_active)
                })
                
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_microdynamic_synthetic_data()
    print(f"Generated {len(df)} trials.")
    print(df.head(10))
