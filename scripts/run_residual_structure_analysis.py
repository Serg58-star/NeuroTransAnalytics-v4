"""
Task 27.3D — Residual Structure Analysis

Reconstructs regression residuals from stored β/intercept and computes
correlations with PSI_tau, Asym_abs, Asym_rel.

Requires: neuro_data.db (for feature extraction)
Uses:     linear_regression_results.csv (for stored β/intercept)

Outputs:
    - residual_structure_results.csv
    - Task_27_3_Residual_Analysis_Report.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
from scipy import stats as sp_stats

from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor


# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / "neuro_data.db"
DATA_DIR = PROJECT_ROOT / "data" / "exploratory" / "symmetric_regression"

LINEAR_CSV = DATA_DIR / "linear_regression_results.csv"
OUTPUT_CSV = DATA_DIR / "residual_structure_results.csv"
OUTPUT_REPORT = DATA_DIR / "Task_27_3_Residual_Analysis_Report.md"


# ============================================================================
# MODEL DEFINITIONS
# ============================================================================

# outcome → predictor mapping for residual reconstruction
MODEL_MAP = {
    "delta_v4_left":  "median_dv1_left",
    "delta_v4_right": "median_dv1_right",
    "delta_v5_left":  "median_dv1_left",
    "delta_v5_right": "median_dv1_right",
}

LATENT_VARS = ["psi_tau", "asym_dv1_abs", "asym_dv1_rel"]


# ============================================================================
# DATA LOADING  (reuses logic from run_symmetric_regression.py)
# ============================================================================

def load_features(database_path: str) -> pd.DataFrame:
    """Load features from neuro_data.db via BaselineFeatureExtractor."""
    import sqlite3

    print("[1/4] Loading trial data from neuro_data.db...")
    conn = sqlite3.connect(database_path)

    trials_query = """
    SELECT 
        t.trial_id, t.subject_id, t.test_date,
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
    print(f"  → Loaded {len(trials_wide)} sessions from {trials_wide['subject_id'].nunique()} subjects")

    print("[2/4] Loading stimulus metadata...")
    metadata_simple = pd.read_sql_query("SELECT * FROM metadata_simple", conn)
    metadata_color = pd.read_sql_query("SELECT * FROM metadata_color_red", conn)
    metadata_shift = pd.read_sql_query("SELECT * FROM metadata_shift", conn)
    conn.close()

    print("[3/4] Reshaping to trial-level format...")
    trial_level_data = []

    for _, session_row in trials_wide.iterrows():
        subject_id = session_row['subject_id']
        trial_id = session_row['trial_id']

        for stimulus_id in range(1, 37):
            rt = session_row[f'tst1_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_simple[metadata_simple['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id, 'session_id': trial_id,
                    'test_type': 'Tst1', 'stimulus_id': stimulus_id,
                    'stimulus_location': meta['position'], 'stimulus_color': meta['color'],
                    'psi': meta['psi_ms'], 'rt': rt, 'is_outlier': False
                })

        for stimulus_id in range(1, 37):
            rt = session_row[f'tst2_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_color[metadata_color['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id, 'session_id': trial_id,
                    'test_type': 'Tst2', 'stimulus_id': stimulus_id,
                    'stimulus_location': meta['position'], 'stimulus_color': 'red',
                    'psi': meta['psi_ms'], 'rt': rt, 'is_outlier': False
                })

        for stimulus_id in range(1, 37):
            rt = session_row[f'tst3_{stimulus_id}']
            if pd.notna(rt) and rt > 0:
                meta = metadata_shift[metadata_shift['stimulus_id'] == stimulus_id].iloc[0]
                trial_level_data.append({
                    'subject_id': subject_id, 'session_id': trial_id,
                    'test_type': 'Tst3', 'stimulus_id': stimulus_id,
                    'stimulus_location': meta['position'], 'stimulus_color': meta['color'],
                    'psi': meta['psi_ms'], 'rt': rt, 'is_outlier': False
                })

    trials_df = pd.DataFrame(trial_level_data)
    print(f"  → Reshaped to {len(trials_df)} trial-level observations")

    print("[4/4] Extracting features per subject...")
    extractor = BaselineFeatureExtractor()
    features_list = []

    for subject_id in trials_df['subject_id'].unique():
        subject_trials = trials_df[trials_df['subject_id'] == subject_id].copy()
        try:
            features = extractor.extract_subject_features(subject_trials)
            if isinstance(features, dict):
                features['subject_id'] = subject_id
                features_list.append(features)
        except Exception:
            continue

    features_df = pd.DataFrame(features_list)
    if 'subject_id' in features_df.columns:
        features_df = features_df.set_index('subject_id')
    print(f"  → Extracted features for {len(features_df)} subjects")

    return features_df


# ============================================================================
# RESIDUAL RECONSTRUCTION
# ============================================================================

def reconstruct_residuals(features_df: pd.DataFrame,
                          linear_csv: pd.DataFrame) -> pd.DataFrame:
    """
    Reconstruct residuals: residual = y - (β * x + intercept).
    Uses stored β and intercept from linear_regression_results.csv.
    """
    residuals_df = pd.DataFrame(index=features_df.index)

    for outcome, predictor in MODEL_MAP.items():
        if outcome not in linear_csv.index:
            continue
        if outcome not in features_df.columns or predictor not in features_df.columns:
            continue

        beta = linear_csv.loc[outcome, 'beta']
        intercept = linear_csv.loc[outcome, 'intercept']

        data = features_df[[outcome, predictor]].dropna()
        y_pred = beta * data[predictor] + intercept
        residuals = data[outcome] - y_pred

        col_name = f"{outcome}_residual"
        residuals_df.loc[residuals.index, col_name] = residuals

    return residuals_df


# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================

def compute_correlations(residuals_df: pd.DataFrame,
                         features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Section II: Pearson + Spearman correlations of each residual
    with PSI_tau, Asym_abs, Asym_rel.
    """
    rows = []

    resid_cols = [c for c in residuals_df.columns if c.endswith("_residual")]

    for resid_col in resid_cols:
        for latent in LATENT_VARS:
            if latent not in features_df.columns:
                continue

            # Align
            combined = pd.DataFrame({
                'resid': residuals_df[resid_col],
                'latent': features_df[latent]
            }).dropna()

            if len(combined) < 10:
                continue

            r_pearson, p_pearson = sp_stats.pearsonr(combined['resid'], combined['latent'])
            r_spearman, p_spearman = sp_stats.spearmanr(combined['resid'], combined['latent'])

            flag = ""
            if abs(r_pearson) >= 0.5:
                flag = "|r|≥0.5"
            elif abs(r_pearson) >= 0.3:
                flag = "|r|≥0.3"

            rows.append({
                'residual': resid_col,
                'latent_variable': latent,
                'n': len(combined),
                'pearson_r': r_pearson,
                'pearson_p': p_pearson,
                'spearman_rho': r_spearman,
                'spearman_p': p_spearman,
                'flag': flag,
            })

    return pd.DataFrame(rows)


def compute_cross_component(residuals_df: pd.DataFrame) -> pd.DataFrame:
    """
    Section III.1: ΔV4_residual vs ΔV5_residual per field.
    """
    rows = []
    for field in ['left', 'right']:
        col_v4 = f"delta_v4_{field}_residual"
        col_v5 = f"delta_v5_{field}_residual"
        if col_v4 not in residuals_df.columns or col_v5 not in residuals_df.columns:
            continue

        combined = residuals_df[[col_v4, col_v5]].dropna()
        if len(combined) < 10:
            continue

        r_p, p_p = sp_stats.pearsonr(combined[col_v4], combined[col_v5])
        r_s, p_s = sp_stats.spearmanr(combined[col_v4], combined[col_v5])

        flag = ""
        if abs(r_p) >= 0.5:
            flag = "|r|≥0.5"
        elif abs(r_p) >= 0.3:
            flag = "|r|≥0.3"

        rows.append({
            'pair': f"ΔV4_{field} vs ΔV5_{field}",
            'n': len(combined),
            'pearson_r': r_p, 'pearson_p': p_p,
            'spearman_rho': r_s, 'spearman_p': p_s,
            'flag': flag,
        })
    return pd.DataFrame(rows)


def compute_interhemispheric(residuals_df: pd.DataFrame) -> pd.DataFrame:
    """
    Section III.2: left vs right residuals per pathway.
    """
    rows = []
    for pathway in ['delta_v4', 'delta_v5']:
        col_left = f"{pathway}_left_residual"
        col_right = f"{pathway}_right_residual"
        if col_left not in residuals_df.columns or col_right not in residuals_df.columns:
            continue

        combined = residuals_df[[col_left, col_right]].dropna()
        if len(combined) < 10:
            continue

        r_p, p_p = sp_stats.pearsonr(combined[col_left], combined[col_right])
        r_s, p_s = sp_stats.spearmanr(combined[col_left], combined[col_right])

        flag = ""
        if abs(r_p) >= 0.5:
            flag = "|r|≥0.5"
        elif abs(r_p) >= 0.3:
            flag = "|r|≥0.3"

        label = "ΔV4" if "v4" in pathway else "ΔV5"
        rows.append({
            'pair': f"{label}_left vs {label}_right",
            'n': len(combined),
            'pearson_r': r_p, 'pearson_p': p_p,
            'spearman_rho': r_s, 'spearman_p': p_s,
            'flag': flag,
        })
    return pd.DataFrame(rows)


# ============================================================================
# REPORT GENERATION
# ============================================================================

def fmt(v, precision=6):
    if isinstance(v, (float, np.floating)):
        if pd.isna(v):
            return "—"
        if abs(v) < 0.0001 and v != 0:
            return f"{v:.6e}"
        return f"{v:.{precision}f}"
    return str(v)


def generate_md_report(corr_df: pd.DataFrame,
                        cross_df: pd.DataFrame,
                        inter_df: pd.DataFrame) -> str:
    """Generate the markdown report with 4 tables."""
    lines = []
    lines.append("# Task 27.3D — Residual Structure Analysis Report")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table 1: Correlations (Pearson)
    lines.append("## 1. Корреляции residual с латентными переменными (Pearson)")
    lines.append("")
    lines.append("| Residual | Latent Variable | n | Pearson r | p-value | Flag |")
    lines.append("|---|---|---|---|---|---|")
    for _, row in corr_df.iterrows():
        lines.append(
            f"| {row['residual']} "
            f"| {row['latent_variable']} "
            f"| {row['n']} "
            f"| {fmt(row['pearson_r'])} "
            f"| {fmt(row['pearson_p'])} "
            f"| {row['flag']} |"
        )
    lines.append("")

    # Table 2: Correlations (Spearman)
    lines.append("## 2. Корреляции residual с латентными переменными (Spearman)")
    lines.append("")
    lines.append("| Residual | Latent Variable | n | Spearman ρ | p-value | Flag |")
    lines.append("|---|---|---|---|---|---|")
    for _, row in corr_df.iterrows():
        flag_s = ""
        if abs(row['spearman_rho']) >= 0.5:
            flag_s = "|r|≥0.5"
        elif abs(row['spearman_rho']) >= 0.3:
            flag_s = "|r|≥0.3"
        lines.append(
            f"| {row['residual']} "
            f"| {row['latent_variable']} "
            f"| {row['n']} "
            f"| {fmt(row['spearman_rho'])} "
            f"| {fmt(row['spearman_p'])} "
            f"| {flag_s} |"
        )
    lines.append("")

    # Table 3: Cross-component residual correlations
    lines.append("## 3. Cross-component residual correlations (ΔV4 vs ΔV5)")
    lines.append("")
    lines.append("| Pair | n | Pearson r | p-value | Spearman ρ | p-value | Flag |")
    lines.append("|---|---|---|---|---|---|---|")
    for _, row in cross_df.iterrows():
        lines.append(
            f"| {row['pair']} "
            f"| {row['n']} "
            f"| {fmt(row['pearson_r'])} "
            f"| {fmt(row['pearson_p'])} "
            f"| {fmt(row['spearman_rho'])} "
            f"| {fmt(row['spearman_p'])} "
            f"| {row['flag']} |"
        )
    lines.append("")

    # Table 4: Inter-hemispheric residual correlations
    lines.append("## 4. Межполушарные residual correlations (left vs right)")
    lines.append("")
    lines.append("| Pair | n | Pearson r | p-value | Spearman ρ | p-value | Flag |")
    lines.append("|---|---|---|---|---|---|---|")
    for _, row in inter_df.iterrows():
        lines.append(
            f"| {row['pair']} "
            f"| {row['n']} "
            f"| {fmt(row['pearson_r'])} "
            f"| {fmt(row['pearson_p'])} "
            f"| {fmt(row['spearman_rho'])} "
            f"| {fmt(row['spearman_p'])} "
            f"| {row['flag']} |"
        )
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("Task 27.3D — Residual Structure Analysis")
    print("=" * 60)
    print()

    # Check prerequisites
    if not DATABASE_PATH.exists():
        print(f"ERROR: Database not found: {DATABASE_PATH}")
        return 1
    if not LINEAR_CSV.exists():
        print(f"ERROR: Linear results not found: {LINEAR_CSV}")
        return 1

    # Load features
    features_df = load_features(str(DATABASE_PATH))
    print()

    # Load stored regression parameters
    print("[5/7] Loading stored β/intercept from CSV...")
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    print(f"  → Loaded parameters for {len(linear_csv)} models")
    print()

    # Reconstruct residuals
    print("[6/7] Reconstructing residuals from stored β/intercept...")
    residuals_df = reconstruct_residuals(features_df, linear_csv)
    for col in residuals_df.columns:
        n_valid = residuals_df[col].notna().sum()
        print(f"  → {col}: {n_valid} valid residuals")
    print()

    # Compute correlations
    print("[7/7] Computing correlations...")

    corr_df = compute_correlations(residuals_df, features_df)
    print(f"  → Latent variable correlations: {len(corr_df)} pairs")

    cross_df = compute_cross_component(residuals_df)
    print(f"  → Cross-component correlations: {len(cross_df)} pairs")

    inter_df = compute_interhemispheric(residuals_df)
    print(f"  → Inter-hemispheric correlations: {len(inter_df)} pairs")
    print()

    # Save CSV (all correlation results combined)
    all_results = pd.concat([
        corr_df.assign(analysis_type="latent_variable"),
        cross_df.rename(columns={'pair': 'residual'}).assign(
            latent_variable="—", analysis_type="cross_component"),
        inter_df.rename(columns={'pair': 'residual'}).assign(
            latent_variable="—", analysis_type="interhemispheric"),
    ], ignore_index=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_results.to_csv(OUTPUT_CSV, index=False)
    print(f"  → CSV saved to: {OUTPUT_CSV}")

    # Generate markdown report
    report = generate_md_report(corr_df, cross_df, inter_df)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  → Report saved to: {OUTPUT_REPORT}")
    print()

    # Summary
    print("=" * 60)
    flagged = corr_df[corr_df['flag'] != '']
    if len(flagged) > 0:
        print(f"Flagged correlations (|r| >= 0.3): {len(flagged)}")
        for _, row in flagged.iterrows():
            print(f"  {row['flag']}: {row['residual']} × {row['latent_variable']} "
                  f"(r={row['pearson_r']:.4f})")
    else:
        print("No correlations flagged at |r| >= 0.3 threshold")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
