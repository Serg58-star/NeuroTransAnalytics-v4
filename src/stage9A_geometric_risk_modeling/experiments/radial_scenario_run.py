"""
stage9A_geometric_risk_modeling.experiments.radial_scenario_run

Executes the model comparison framework strictly against a RADIALLY-dominant 
synthetic dataset to verify the architecture correctly assigns the RADIAL_DOMINANT verdict.
"""

import sys
import os
import yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from stage9A_geometric_risk_modeling.common.data_loader import generate_radial_dominant_data
from stage9A_geometric_risk_modeling.radial_model import radial_evaluation
from stage9A_geometric_risk_modeling.vector_model import vector_evaluation
from stage9A_geometric_risk_modeling.bayesian_model import bayesian_evaluation
from stage9A_geometric_risk_modeling.common.reporting_utils import generate_report_markdown

def main():
    config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    n_samples = config['dataset']['n_samples']
    seed = config['dataset']['base_seed']
    
    print("Generating Synthetic Benchmark (Radial-Dominant Data)...")
    df = generate_radial_dominant_data(n_samples=n_samples, seed=seed)
    
    dataset_info = {
        'n_samples': n_samples,
        'condition_type': 'Binary (Radial Dominant)',
        'class_balance': f"{df['Condition'].mean():.2%} Positives",
        'label_source': 'Synthetic (Stage 9A strict isolated test)'
    }
    
    print("Evaluating Baseline Models...")
    baseline_metrics = {
        'Radial': radial_evaluation.evaluate_baseline(df),
        'Vector': vector_evaluation.evaluate_baseline(df),
        'Bayesian': bayesian_evaluation.evaluate_baseline(df)
    }
    
    print("Evaluating Bootstrap Stability...")
    n_boot = config['experiments']['bootstrap_iterations']
    bootstrap_metrics = {
        'Radial': radial_evaluation.evaluate_bootstrap(df, n_boot),
        'Vector': vector_evaluation.evaluate_bootstrap(df, n_boot),
        'Bayesian': bayesian_evaluation.evaluate_bootstrap(df, n_boot)
    }
    
    print("Evaluating Noise Stability...")
    noise_metrics = {}
    for level in config['experiments']['noise_levels']:
        lvl_str = f"{level:.2f}"
        print(f"  Level: {lvl_str}")
        noise_metrics[lvl_str] = {
            'Radial': radial_evaluation.evaluate_noise(df, level),
            'Vector': vector_evaluation.evaluate_noise(df, level),
            'Bayesian': bayesian_evaluation.evaluate_noise(df, level)
        }
        
    # Empirical Verdict Calculation (Task 39.1 Formal Rule)
    from stage9A_geometric_risk_modeling.common.reporting_utils import compute_architectural_verdict
    verdict = compute_architectural_verdict(baseline_metrics, bootstrap_metrics, noise_metrics)
    
    print("Generating Final Comparative Report...")
    report_md = generate_report_markdown(dataset_info, baseline_metrics, bootstrap_metrics, noise_metrics, verdict)
    
    report_dir = os.path.join(os.path.dirname(__file__), '../reports')
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, 'task39_1_radial_scenario_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
        
    print(f"Task 39.1 Radial Scenario Execution Complete. Output: {report_path}")

if __name__ == '__main__':
    main()
