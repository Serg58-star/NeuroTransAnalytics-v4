import pandas as pd
import numpy as np
import random
import os

# Set reproducibility
np.random.seed(42)
random.seed(42)

def generate_mock_data(n_subjects=10, trials_per_subject=72):
    \"\"\"
    Generates synthetic data matching the schema needed for Stage G legacy audit.
    Includes intentional structural biases for validation.
    \"\"\"
    
    rows = []
    
    colors = ['red', 'green', 'blue']
    positions = ['left', 'center', 'right']
    
    # Task 1: Intentional bias in P(color | position)
    # Let's make 'red' more likely in 'center' and 'green' more likely on 'left'
    
    for subj in range(1, n_subjects + 1):
        subj_id = f\"S{subj:03d}\"
        
        # Track previous context to build runs/correlations
        prev_dominant = random.choice(['G', 'B'])
        
        for trial in range(1, trials_per_subject + 1):
            
            # Position
            pos = random.choice(positions)
            
            # Color (with bias)
            if pos == 'center':
                col = np.random.choice(['red', 'green', 'blue'], p=[0.6, 0.2, 0.2])
            elif pos == 'left':
                col = np.random.choice(['red', 'green', 'blue'], p=[0.2, 0.6, 0.2])
            else:
                col = random.choice(colors)
                
            # PSI (with some bias towards specific triples later)
            psi = np.random.uniform(500, 3000)
            
            # Generate triples
            # We use letters: Ж=green, С=blue, К=red
            # Let's create an intentional Markov dependence
            if prev_dominant == 'G':
                curr_dominant = np.random.choice(['G', 'B'], p=[0.7, 0.3])
            else:
                curr_dominant = np.random.choice(['G', 'B'], p=[0.3, 0.7])
                
            n_triples = np.random.randint(2, 6)
            mask_list = []
            
            for _ in range(n_triples):
                if curr_dominant == 'G':
                    t = \"\".join(np.random.choice(['Ж', 'С'], size=3, p=[0.8, 0.2]))
                else:
                    t = \"\".join(np.random.choice(['Ж', 'С'], size=3, p=[0.2, 0.8]))
                mask_list.append(t)
                
            mask_triples = \" \".join(mask_list)
            
            # Test triple (target)
            if col == 'red':
                test_t = ['Ж', 'С', 'К']
            elif col == 'green':
                test_t = ['К', 'С', 'Ж']
            else:
                test_t = ['Ж', 'К', 'С']
                
            random.shuffle(test_t)
            test_triple = \"\".join(test_t)
            
            prev_dominant = curr_dominant
            
            # Generate RT based on Channel Balance (Task 5, Task 8)
            # P = num_green, K = num_blue
            num_green = sum(t.count('Ж') for t in mask_list)
            num_blue = sum(t.count('С') for t in mask_list)
            
            # Entropy
            import math
            def calc_ent(s):
                counts = {'Ж': s.count('Ж'), 'С': s.count('С'), 'К': s.count('К')}
                ent = 0
                for v in counts.values():
                    if v > 0:
                        p = v / 3
                        ent -= p * math.log2(p)
                return ent
                
            avg_ent = np.mean([calc_ent(t) for t in mask_list])
            
            # Model RT
            base_rt = 300
            ent_effect = avg_ent * 50
            pos_effect = -20 if pos == 'center' else 10
            
            rt = base_rt + ent_effect + pos_effect + np.random.normal(0, 20)
            
            # Drift across stimulus index
            # later trials (higher index) have more blue
            if trial > trials_per_subject * 0.6:
                if random.random() < 0.3:
                    mask_triples = mask_triples.replace('Ж', 'С')
                    
            rows.append({
                'subject_id': subj_id,
                'stimulus_index': trial,
                'test_type': 'color_red',
                'color': col,
                'position': pos,
                'psi': psi,
                'mask_triples': mask_triples,
                'test_triple': test_triple,
                'rt': rt,
                'delta_v4': rt - 50,  # mock
                'delta_v5_mt': rt - 30 # mock
            })
            
    df = pd.DataFrame(rows)
    return df

if __name__ == \"__main__\":
    print(\"Generating Stage G synthetic dataset...\")
    df_mock = generate_mock_data()
    
    out_dir = \"C:/NeuroTransAnalytics-v4/analysis/mock_data\"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, \"stage_G_mock.csv\")
    df_mock.to_csv(out_path, index=False)
    print(f\"Saved synthetic data to {out_path} [{len(df_mock)} rows]\")
