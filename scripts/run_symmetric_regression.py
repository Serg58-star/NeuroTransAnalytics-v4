"""
Task 27.2A Symmetric Regression Analysis - Ready-to-Run Script

CRITICAL REQUIREMENT: REAL DATA ONLY (synthetic data prohibited)

This script is prepared to run symmetric regression analysis once
real NeuroTransAnalytics database is provided.

To execute:
1. Provide path to real database (SQLite with trial data)
2. Update DATABASE_PATH variable below
3. Run: python scripts/run_symmetric_regression.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor
from exploratory_lab.feature_engineering.symmetric_regression import SymmetricRegressionAnalyzer


# ============================================================================
# CONFIGURATION - UPDATE THIS PATH WITH REAL DATABASE
# ============================================================================

DATABASE_PATH = "neuro_data.db"  # Real database path

# Example:
# DATABASE_PATH = "c:/path/to/real_database.db"

# ============================================================================


def check_data_availability():
    """Check if real data is available."""
    if DATABASE_PATH is None:
        print("=" * 80)
        print("⚠ DATA REQUIRED")
        print("=" * 80)
        print()
        print("Task 27.2A explicitly requires REAL data (synthetic data prohibited).")
        print()
        print("To proceed:")
        print("  1. Set DATABASE_PATH variable in this script")
        print("  2. Ensure database contains trial-level data")
        print("  3. Re-run this script")
        print()
        print("=" * 80)
        return False
    
    if not Path(DATABASE_PATH).exists():
        print(f"⚠ Database not found: {DATABASE_PATH}")
        return False
    
    return True


def load_features_from_real_data(database_path: str):
    """
    Load and extract features from real neuro_data.db database.
    
    Returns
    -------
    tuple
        (features_df, trials_df) for regression analysis and PSI stability
    """
    import sqlite3
    import numpy as np
    
    print("[1/4] Loading trial data from neuro_data.db...")
    
    conn = sqlite3.connect(database_path)
    
    # Load trials table (wide format)
    trials_query = """
    SELECT 
        t.trial_id,
        t.subject_id,
        t.test_date,
        t.tst1_1, t.tst1_2, t.tst1_3, t.tst1_4, t.tst1_5, t.tst1_6,
        t.tst1_7, t.tst1_8, t.tst1_9, t.tst1_10, t.tst1_11, t.tst1_12,
        t.tst1_13, t.tst1_14, t.tst1_15, t.tst1_16, t.tst1_17, t.tst1_18,
        t.tst1_19, t.tst1_20, t.tst1_21, t.tst1_22, t.tst1_23, t.tst1_24,
        t.tst1_25, t.tst1_26, t.tst1_27, t.tst1_28, t.tst1_29, t.tst1_30,
        t.tst1_31, t.tst1_32, t.tst1_33, t.tst1_34, t.tst1_35, t.tst1_36,
        t.tst2_1, t.tst2_2, t.tst2_3, t.tst2_4, t.tst2_5, t.tst2_6,
        t.tst2_7, t.tst2_8, t.tst2_9, t.tst2_10, t.tst2_11, t.tst2_12,
        t.tst2_13, t.tst2_14, t.tst2_15, t.tst2_16, t.tst2_17, t.tst2_18,
        t.tst2_19, t.tst2_20, t.tst2_21, t.tst2_22, t.tst2_23, t.tst2_24,
        t.tst2_25, t.tst2_26, t.tst2_27, t.tst2_28, t.tst2_29, t.tst2_30,
        t.tst2_31, t.tst2_32, t.tst2_33, t.tst2_34, t.tst2_35, t.tst2_36,
        t.tst3_1, t.tst3_2, t.tst3_3, t.tst3_4, t.tst3_5, t.tst3_6,
        t.tst3_7, t.tst3_8, t.tst3_9, t.tst3_10, t.tst3_11, t.tst3_12,
        t.tst3_13, t.tst3_14, t.tst3_15, t.tst3_16, t.tst3_17, t.tst3_18,
        t.tst3_19, t.tst3_20, t.tst3_21, t.tst3_22, t.tst3_23, t.tst3_24,
        t.tst3_25, t.tst3_26, t.tst3_27, t.tst3_28, t.tst3_29, t.tst3_30,
        t.tst3_31, t.tst3_32, t.tst3_33, t.tst3_34, t.tst3_35, t.tst3_36
    FROM trials t
    INNER JOIN users u ON t.subject_id = u.subject_id
    """
    
    trials_wide = pd.read_sql_query(trials_query, conn)
    print(f"  → Loaded {len(trials_wide)} trial sessions from {trials_wide['subject_id'].nunique()} subjects")
    
    # Load metadata
    print("[2/4] Loading stimulus metadata...")
    metadata_simple = pd.read_sql_query("SELECT * FROM metadata_simple", conn)
    metadata_color = pd.read_sql_query("SELECT * FROM metadata_color_red", conn)
    metadata_shift = pd.read_sql_query("SELECT * FROM metadata_shift", conn)
    
    conn.close()
    
    # Reshape to trial-level format
    print("[3/4] Reshaping to trial-level format...")
    trial_level_data = []
    
    for _, session_row in trials_wide.iterrows():
        subject_id = session_row['subject_id']
        trial_id = session_row['trial_id']
        
        # Process Tst1 (simple reaction)
        for stimulus_id in range(1, 37):
            rt = session_row[f'tst1_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_simple[metadata_simple['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id,
                    'session_id': trial_id,
                    'test_type': 'Tst1',
                    'stimulus_id': stimulus_id,
                    'stimulus_location': meta['position'],
                    'stimulus_color': meta['color'],
                    'psi': meta['psi_ms'],
                    'rt': rt,
                    'is_outlier': False  # Basic flag, can be computed later
                })
        
        # Process Tst2 (color discrimination)
        for stimulus_id in range(1, 37):
            rt = session_row[f'tst2_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_color[metadata_color['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id,
                    'session_id': trial_id,
                    'test_type': 'Tst2',
                    'stimulus_id': stimulus_id,
                    'stimulus_location': meta['position'],
                    'stimulus_color': 'red',
                    'psi': meta['psi_ms'],
                    'rt': rt,
                    'is_outlier': False
                })
        
        # Process Tst3 (shift test)
        for stimulus_id in range(1, 37):
            rt = session_row[f'tst3_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_shift[metadata_shift['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id,
                    'session_id': trial_id,
                    'test_type': 'Tst3',
                    'stimulus_id': stimulus_id,
                    'stimulus_location': meta['position'],
                    'stimulus_color': meta['color'],
                    'psi': meta['psi_ms'],
                    'rt': rt,
                    'is_outlier': False
                })
    
    trials_df = pd.DataFrame(trial_level_data)
    print(f"  → Reshaped to {len(trials_df)} trial-level observations")
    
    # Extract features using BaselineFeatureExtractor
    print("[4/4] Extracting features per subject...")
    extractor = BaselineFeatureExtractor()
    
    features_list = []
    subjects = trials_df['subject_id'].unique()
    
    for subject_id in subjects:
        subject_trials = trials_df[trials_df['subject_id'] == subject_id].copy()
        
        try:
            features = extractor.extract_subject_features(subject_trials)
            # Add subject_id directly to the dictionary
            if isinstance(features, dict):
                features['subject_id'] = subject_id
                features_list.append(features)
            else:
                print(f"  ⚠ Warning: Unexpected feature format for subject {subject_id}")
                continue
        except Exception as e:
            # Skip subjects with missing data - this is expected
            continue
    
    features_df = pd.DataFrame(features_list)
    if 'subject_id' in features_df.columns:
        features_df = features_df.set_index('subject_id')
    print(f"  → Extracted features for {len(features_df)} subjects")
    
    return features_df, trials_df


def run_symmetric_analysis(database_path: str):
    """
    Run complete Task 27.3 symmetric regression analysis with all validations.
    """
    print("=" * 80)
    print("TASK 27.3 - SYMMETRIC REGRESSION PRODUCTION RUN")
    print("=" * 80)
    print()
    
    # Load features and trial data
    features_df, trials_df = load_features_from_real_data(database_path)
    print(f"  → Loaded {len(features_df)} subjects with {len(features_df.columns)} features")
    print()
    
    # Verify required features
    required_features = [
        'delta_v4_left', 'delta_v4_right', 'delta_v4_center',
        'delta_v5_left', 'delta_v5_right', 'delta_v5_center',
        'median_dv1_left', 'median_dv1_right', 'median_dv1_center',
        'mad_dv1_left', 'mad_dv1_right', 'mad_dv1_center',
        'psi_tau', 'asym_dv1_abs', 'asym_dv1_rel'
    ]
    
    missing = [f for f in required_features if f not in features_df.columns]
    if missing:
        print(f"⚠ Missing required features: {missing}")
        print("Please ensure feature extraction includes all 17 features.")
        return
    
    # Run symmetric regression analysis (Tasks 27.2A/B/C/D)
    print("[Running Analysis] Symmetric regression with full validation...")
    analyzer = SymmetricRegressionAnalyzer()
    results = analyzer.run_complete_analysis(
        features_df,
        include_27_2b=True,
        include_27_2c=True,
        trials_df=trials_df
    )
    print("  → Analysis complete")
    print()
    
    # Generate report
    print("[Generating Report] Comprehensive numerical report...")
    report = analyzer.generate_report()
    print()
    
    # Display report
    print(report)
    print()
    
    # Save results
    output_dir = Path("data/exploratory/symmetric_regression")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = output_dir / "Task_27_3_Production_Run_Report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report saved to: {report_path}")
    print()
    
    # Save detailed results as CSV
    linear_df = pd.DataFrame(results['linear']).T
    linear_df.to_csv(output_dir / "linear_regression_results.csv")
    
    if results.get('multiple'):
        multiple_df = pd.DataFrame(results['multiple']).T
        multiple_df.to_csv(output_dir / "multiple_regression_results.csv")
    
    if results.get('heteroscedasticity'):
        hetero_df = pd.DataFrame(results['heteroscedasticity']).T
        hetero_df.to_csv(output_dir / "heteroscedasticity_tests.csv")
    
    print(f"Detailed CSV results saved to: {output_dir}")
    print()
    
    print("=" * 80)
    print("PRODUCTION RUN COMPLETE")
    print("=" * 80)
    
    return results


def main():
    """Main execution function."""
    if not check_data_availability():
        return
    
    try:
        results = run_symmetric_analysis(DATABASE_PATH)
    except NotImplementedError as e:
        print()
        print("=" * 80)
        print("⚠ IMPLEMENTATION REQUIRED")
        print("=" * 80)
        print()
        print(str(e))
        print()
        print("Please implement load_features_from_real_data() function")
        print("in this script to match your database schema.")
        print()
    except Exception as e:
        print()
        print("=" * 80)
        print("⚠ ERROR")
        print("=" * 80)
        print()
        print(f"Error occurred: {e}")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
