import sys
import os
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from stage9A_geometric_risk_modeling.common.data_loader import generate_base_data
from stage9A_geometric_risk_modeling.bayesian_model import bayesian_evaluation
from stage9A_geometric_risk_modeling.radial_model import radial_evaluation
from stage9A_geometric_risk_modeling.vector_model import vector_evaluation
from stage9A_geometric_risk_modeling.common.reporting_utils import compute_architectural_verdict

def test_topology(n_samples=5000):
    def gen_data(n_samples=n_samples, seed=44):
        df = generate_base_data(n_samples, seed)
        speed = df['ΔSpeed']
        lateral = df['ΔLateral']
        logits = 1.0 * speed * lateral
        probs = 1.0 / (1.0 + np.exp(-logits))
        rng = np.random.default_rng(seed + 1)
        df['Condition'] = rng.binomial(1, probs)
        return df

    df = gen_data()
    print(f"Class balance: {df['Condition'].mean():.2%}")
    
    metrics = {
        'Radial': radial_evaluation.evaluate_baseline(df),
        'Vector': vector_evaluation.evaluate_baseline(df),
        'Bayesian': bayesian_evaluation.evaluate_baseline(df)
    }
    
    boot = {
        'Radial': radial_evaluation.evaluate_bootstrap(df, 10),
        'Vector': vector_evaluation.evaluate_bootstrap(df, 10),
        'Bayesian': bayesian_evaluation.evaluate_bootstrap(df, 10)
    }
    
    noise = {'0.10': {
        'Radial': {'delta_auc': 0}, 'Vector': {'delta_auc': 0}, 'Bayesian': {'delta_auc': 0}
    }}
    
    v = compute_architectural_verdict(metrics, boot, noise)
    
    for m in ['Radial', 'Vector', 'Bayesian']:
        print(f"--- {m} ---")
        print(f"AUC_boot: {boot[m]['auc_mean']:.4f}")
        print(f"sigma_boot: {boot[m]['auc_sd']:.4f}")
        cal_slope = metrics[m]['calibration_slope']
        print(f"Cal Slope: {cal_slope:.4f}")
        print(f"Cal Pen (0.5 * |1-Slope|): {0.5*abs(1.0 - cal_slope):.4f}")
        print(f"Final Score: {v['scores'][m]:.4f}")
        
    print()
    print("Winner:", v['winner'])
    print("Verdict:", v['final_verdict'])

test_topology(10000)
test_topology(20000)
