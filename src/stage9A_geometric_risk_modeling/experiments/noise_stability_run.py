"""
stage9A_geometric_risk_modeling.experiments.noise_stability_run

Optional isolated runner to specifically stress test the noise bounds validations alone.
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
    
    res = {}
    for level in config['experiments']['noise_levels']:
        print(f"Executing Isolated Noise Sensitivity Test (Level: {level})")
        res[str(level)] = {
            'Radial': radial_evaluation.evaluate_noise(df, level),
            'Vector': vector_evaluation.evaluate_noise(df, level),
            'Bayesian': bayesian_evaluation.evaluate_noise(df, level)
        }
    
    pprint(res)

if __name__ == '__main__':
    main()
