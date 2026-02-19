"""
Test script for Task 27.2 regression validation.

Runs complete validation pipeline and generates numerical report.
NO visualization, clustering, or UMAP - numerical validation only.
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor
from exploratory_lab.feature_engineering.regression_validator import RegressionValidator


def create_validation_data(n_subjects=50):
    """Create synthetic data for regression validation."""
    np.random.seed(42)
    
    features_list = []
    
    for subject_id in range(n_subjects):
        # Base speed (general factor)
        base_speed = np.random.normal(250, 50)
        
        # ΔV1 by field (with slight asymmetry)
        dv1_left = base_speed + np.random.normal(-5, 10)
        dv1_center = base_speed + np.random.normal(0, 10)
        dv1_right = base_speed + np.random.normal(5, 10)
        
        # Asymmetries
        asym_abs = abs(dv1_right - dv1_left)
        asym_rel = (dv1_right - dv1_left) / ((dv1_right + dv1_left) / 2)
        
        # MAD
        mad = np.random.uniform(10, 30)
        
        # ΔV4: moderate correlation with ΔV1 (R² ~0.4)
        dv4_left = 0.3 * dv1_left + np.random.normal(50, 20)
        dv4_center = 0.3 * dv1_center + np.random.normal(50, 20)
        dv4_right = 0.3 * dv1_right + np.random.normal(50, 20)
        
        # ΔV5: similar moderate correlation
        dv5_left = 0.25 * dv1_left + np.random.normal(70, 25)
        dv5_center = 0.25 * dv1_center + np.random.normal(70, 25)
        dv5_right = 0.25 * dv1_right + np.random.normal(70, 25)
        
        # PSI tau: weak correlation with speed
        psi_tau = 300 + 0.1 * base_speed + np.random.normal(0, 80)
        psi_tau = max(10, min(2000, psi_tau))  # Bound check
        
        # PSI slope (linear)
        psi_slope = np.random.normal(-0.05, 0.02)
        
        features_list.append({
            'subject_id': f'S{subject_id:03d}',
            'median_dv1_left': dv1_left,
            'median_dv1_center': dv1_center,
            'median_dv1_right': dv1_right,
            'asym_dv1_abs': asym_abs,
            'asym_dv1_rel': asym_rel,
            'mad_dv1': mad,
            'delta_v4_left': dv4_left,
            'delta_v4_center': dv4_center,
            'delta_v4_right': dv4_right,
            'delta_v5_left': dv5_left,
            'delta_v5_center': dv5_center,
            'delta_v5_right': dv5_right,
            'psi_tau': psi_tau,
            'psi_slope_linear': psi_slope
        })
    
    return pd.DataFrame(features_list).set_index('subject_id')


def run_validation():
    """Run complete Task 27.2 validation."""
    print("=" * 70)
    print("TASK 27.2 - PRE-LAUNCH REGRESSION VALIDATION")
    print("=" * 70)
    print()
    
    # Create synthetic data
    print("[1/3] Generating synthetic validation data...")
    features_df = create_validation_data(n_subjects=50)
    print(f"  → Created {len(features_df)} subjects with {len(features_df.columns)} features")
    print()
    
    # Run regression validation
    print("[2/3] Running regression independence checks...")
    validator = RegressionValidator()
    results = validator.validate(features_df)
    print("  → Validation complete")
    print()
    
    # Generate report
    print("[3/3] Generating numerical report...")
    report = validator.generate_report()
    print()
    
    # Display report
    print(report)
    print()
    
    # Save to file
    output_dir = Path("data/exploratory/validation")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / "regression_validation_report.txt"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"Report saved to: {report_path}")
    print()
    
    # Summary conclusions
    print("=" * 70)
    print("SUMMARY CONCLUSIONS")
    print("=" * 70)
    for feature, conclusion in results['conclusions'].items():
        print(f"{feature:25s} → {conclusion}")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    results = run_validation()
