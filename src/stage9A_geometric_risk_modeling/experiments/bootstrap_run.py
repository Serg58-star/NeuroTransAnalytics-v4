"""
stage9A_geometric_risk_modeling.experiments.bootstrap_run

Optional isolated runner to specifically stress test the bootstrap validations alone.
(Actual reporting uses baseline_run.py for the unified pipeline)
"""

import sys
import os
import yaml
from pprint import pprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from stage9A_geometric_risk_modeling.common.data_loader import generate_vector_sensitive_data
from stage9A_geometric_risk_modeling.radial_model import radial_evaluation
from stage9A_geometric_risk_modeling.vector_model import vector_evaluation
from stage9A_geometric_risk_modeling.bayesian_model import bayesian_evaluation

def main():
    config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    df = generate_vector_sensitive_data(config['dataset']['n_samples'], config['dataset']['base_seed'])
    n_boot = config['experiments']['bootstrap_iterations']
    
    print(f"Executing Isolated Bootstrap Stress Test (Iterations: {n_boot})")
    
    res = {
        'Radial': radial_evaluation.evaluate_bootstrap(df, n_boot),
        'Vector': vector_evaluation.evaluate_bootstrap(df, n_boot),
        'Bayesian': bayesian_evaluation.evaluate_bootstrap(df, n_boot)
    }
    
    pprint(res)

if __name__ == '__main__':
    main()
