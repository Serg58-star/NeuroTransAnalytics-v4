"""
# Exploratory Procedure: Stage 3 - Channel Reconstruction (Task 31)
# Exploratory Goal: Evaluate if structural geometry replicates under functional Parvo/Magno channel projection.
# Input Data: Feature-level data (7 production features). No trial-level modification.
# Parameters: Block A (Channel indices mapping), Block B (Compressed 3D Space), Block C (Correlations).
# Output: `Task_31_Stage3_Report.md` containing performance metrics and loadings.
# Reproducibility Notes: Fixed seeds for bootstrap and split-half.
#
# Explicit Non-Interpretation Clause:
# This procedure is exploratory and descriptive. It produces structural representations 
# only and does not imply interpretation, inference, or evaluation.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Ensure import paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from exploratory_lab.geometry.stability import pca_metrics, run_bootstrap, run_split_half

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATABASE_PATH = PROJECT_ROOT / "neuro_data.db"
DATA_DIR = PROJECT_ROOT / "data" / "exploratory" / "symmetric_regression"
LINEAR_CSV = DATA_DIR / "linear_regression_results.csv"
OUTPUT_REPORT = PROJECT_ROOT / "data" / "exploratory" / "reports" / "Task_31_Stage3_Report.md"

N_BOOTSTRAP = 1000
N_SPLITS = 500
RANDOM_SEED = 42

MODEL_MAP = {
    "delta_v4_left":  "median_dv1_left",
    "delta_v4_right": "median_dv1_right",
    "delta_v5_left":  "median_dv1_left",
    "delta_v5_right": "median_dv1_right",
}

CORE_RESIDUALS = [
    "delta_v4_left_residual", "delta_v4_right_residual",
    "delta_v5_left_residual", "delta_v5_right_residual",
]
FEATURES_BASELINE = CORE_RESIDUALS + ["asym_dv1_abs", "asym_dv1_rel", "psi_tau"]

FEATURES_BLOCK_A = [
    "parvo_mean", "magno_mean", "parvo_diff", "magno_diff", "asym_dv1_abs", "asym_dv1_rel", "psi_tau"
]

FEATURES_BLOCK_B = [
    "parvo_index", "magno_index", "lateral_index"
]

np.random.seed(RANDOM_SEED)
RNG = np.random.default_rng(RANDOM_SEED)


# ============================================================================
# DATA PREPARATION (Reusing Stage 1/2 exactly)
# ============================================================================

def load_data():
    """Loads session-level features and reconstructs residuals."""
    import sqlite3
    from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor
    
    conn = sqlite3.connect(DATABASE_PATH)
    trials_query = """
    SELECT 
        t.trial_id as session_id, t.subject_id, t.test_date,
        t.tst1_1, t.tst1_2, t.tst1_3, t.tst1_4, t.tst1_5, t.tst1_6, t.tst1_7, t.tst1_8, t.tst1_9, t.tst1_10, t.tst1_11, t.tst1_12,
        t.tst1_13, t.tst1_14, t.tst1_15, t.tst1_16, t.tst1_17, t.tst1_18, t.tst1_19, t.tst1_20, t.tst1_21, t.tst1_22, t.tst1_23, t.tst1_24,
        t.tst1_25, t.tst1_26, t.tst1_27, t.tst1_28, t.tst1_29, t.tst1_30, t.tst1_31, t.tst1_32, t.tst1_33, t.tst1_34, t.tst1_35, t.tst1_36,
        t.tst2_1, t.tst2_2, t.tst2_3, t.tst2_4, t.tst2_5, t.tst2_6, t.tst2_7, t.tst2_8, t.tst2_9, t.tst2_10, t.tst2_11, t.tst2_12,
        t.tst2_13, t.tst2_14, t.tst2_15, t.tst2_16, t.tst2_17, t.tst2_18, t.tst2_19, t.tst2_20, t.tst2_21, t.tst2_22, t.tst2_23, t.tst2_24,
        t.tst2_25, t.tst2_26, t.tst2_27, t.tst2_28, t.tst2_29, t.tst2_30, t.tst2_31, t.tst2_32, t.tst2_33, t.tst2_34, t.tst2_35, t.tst2_36,
        t.tst3_1, t.tst3_2, t.tst3_3, t.tst3_4, t.tst3_5, t.tst3_6, t.tst3_7, t.tst3_8, t.tst3_9, t.tst3_10, t.tst3_11, t.tst3_12,
        t.tst3_13, t.tst3_14, t.tst3_15, t.tst3_16, t.tst3_17, t.tst3_18, t.tst3_19, t.tst3_20, t.tst3_21, t.tst3_22, t.tst3_23, t.tst3_24,
        t.tst3_25, t.tst3_26, t.tst3_27, t.tst3_28, t.tst3_29, t.tst3_30, t.tst3_31, t.tst3_32, t.tst3_33, t.tst3_34, t.tst3_35, t.tst3_36
    FROM trials t INNER JOIN users u ON t.subject_id = u.subject_id
    """
    trials_wide = pd.read_sql_query(trials_query, conn)
    
    meta_s = pd.read_sql_query("SELECT * FROM metadata_simple", conn)
    meta_c = pd.read_sql_query("SELECT * FROM metadata_color_red", conn)
    meta_sh = pd.read_sql_query("SELECT * FROM metadata_shift", conn)
    conn.close()

    trial_level_data = []
    for _, sr in trials_wide.iterrows():
        sid, tid, date = sr['subject_id'], sr['session_id'], sr['test_date']
        for stim in range(1, 37):
            rt = sr[f'tst1_{stim}']
            if pd.notna(rt) and rt > 0:
                m = meta_s[meta_s['stimulus_id'] == stim].iloc[0]
                trial_level_data.append({'subject_id': sid, 'session_id': tid, 'test_date': date,
                    'test_type': 'Tst1', 'stimulus_id': stim, 'stimulus_location': m['position'], 'stimulus_color': m['color'], 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
        for stim in range(1, 37):
            rt = sr[f'tst2_{stim}']
            if pd.notna(rt) and rt > 0:
                m = meta_c[meta_c['stimulus_id'] == stim].iloc[0]
                trial_level_data.append({'subject_id': sid, 'session_id': tid, 'test_date': date,
                    'test_type': 'Tst2', 'stimulus_id': stim, 'stimulus_location': m['position'], 'stimulus_color': 'red', 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
        for stim in range(1, 37):
            rt = sr[f'tst3_{stim}']
            if pd.notna(rt) and rt > 0:
                m = meta_sh[meta_sh['stimulus_id'] == stim].iloc[0]
                trial_level_data.append({'subject_id': sid, 'session_id': tid, 'test_date': date,
                    'test_type': 'Tst3', 'stimulus_id': stim, 'stimulus_location': m['position'], 'stimulus_color': m['color'], 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
    
    trials_df = pd.DataFrame(trial_level_data)
    
    # Extract session features
    extractor = BaselineFeatureExtractor()
    session_features = []
    for tid in trials_df['session_id'].unique():
        sdf = trials_df[trials_df['session_id'] == tid]
        sid = sdf['subject_id'].iloc[0]
        date = sdf['test_date'].iloc[0]
        try:
            feats = extractor.extract_subject_features(sdf)
            if isinstance(feats, dict) and 'asym_dv1_abs' in feats and pd.notna(feats['asym_dv1_abs']):
                feats['session_id'] = tid
                feats['subject_id'] = sid
                feats['test_date'] = date
                session_features.append(feats)
        except Exception as e:
            print(f"Extraction failed for session {tid}: {e}")
            
    df_sess = pd.DataFrame(session_features)
    
    # Reconstruct residuals
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    for outcome, predictor in MODEL_MAP.items():
        if outcome in linear_csv.index and outcome in df_sess.columns:
            beta = linear_csv.loc[outcome, 'beta']
            inter = linear_csv.loc[outcome, 'intercept']
            df_sess[f"{outcome}_residual"] = df_sess[outcome] - (beta * df_sess[predictor] + inter)
            
    df_sess = df_sess.dropna(subset=FEATURES_BASELINE).copy()
    
    # Create Subject-level DF (first session per subject)
    df_subj = df_sess.sort_values(['subject_id', 'test_date']).groupby('subject_id').first().reset_index()
    
    return df_sess, df_subj


# ============================================================================
# METRIC EVALUATION
# ============================================================================

def calc_between_within(df_sess_tf, features):
    """Computes Between/Within variance ratio explicitly matching Task 27.3J."""
    subs = df_sess_tf['subject_id'].unique()
    first_visits = df_sess_tf.sort_values(['subject_id', 'test_date']).groupby('subject_id').first()
    pop_data = first_visits[features].values
    
    scaler = StandardScaler()
    pop_std = scaler.fit_transform(pop_data)
    cov = np.cov(pop_std, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvectors = eigenvectors[:, idx]
    
    pop_pc_scores = pop_std @ eigenvectors
    var_between = np.var(pop_pc_scores[:, 0], ddof=1)
    
    var_withins = []
    for sid in subs:
        subj_data = df_sess_tf[df_sess_tf['subject_id'] == sid]
        if len(subj_data) > 1:
            subj_feat = subj_data[features].values
            subj_std = scaler.transform(subj_feat) 
            pc_scores = subj_std @ eigenvectors
            var_withins.append(np.var(pc_scores[:, 0], ddof=1))
            
    if len(var_withins) == 0:
        return np.nan
        
    mean_var_within = np.mean(var_withins)
    if mean_var_within == 0:
        return np.inf
        
    return var_between / mean_var_within


def extract_loadings(data, features):
    """Extracts PC1 and PC2 loadings."""
    scaler = StandardScaler()
    scaled = scaler.fit_transform(data)
    
    if len(features) < 2:
        return None
        
    pca = PCA()
    pca.fit(scaled)
    
    comps = min(2, len(features))
    
    loadings = pd.DataFrame(
        pca.components_[:comps, :].T, 
        columns=[f'PC{i+1}' for i in range(comps)], 
        index=features
    )
    return loadings


def evaluate_transformation(name, df_sess, df_subj, features):
    """Run all metrics on the transformed datasets."""
    data_subj = df_subj[features].values
    
    base_mets = pca_metrics(data_subj)
    bs_df = run_bootstrap(data_subj, N_BOOTSTRAP, RNG)
    sh_df = run_split_half(data_subj, N_SPLITS, RNG)
    
    bw_ratio = calc_between_within(df_sess, features)
    loadings = extract_loadings(data_subj, features)
    
    return {
        'Transformation': name,
        'Dim': base_mets['n_lambda_gt1'],
        'PC1%': base_mets['pc1_pct'],
        'PR': base_mets['participation_ratio'],
        'Boot SD': bs_df['pc1_pct'].std(),
        'SH ΔPC1': sh_df['diff_pc1_pct'].mean(),
        'B/W Ratio': bw_ratio,
        'Loadings': loadings
    }


# ============================================================================
# TRANSFORMATIONS (BLOCK A & B)
# ============================================================================

def transform_block_a(df):
    """Block A: Build channel indices (Parvo_mean, Magno_mean, Parvo_diff, Magno_diff)."""
    tf = df.copy()
    tf['parvo_mean'] = (tf['delta_v4_left_residual'] + tf['delta_v4_right_residual']) / 2
    tf['magno_mean'] = (tf['delta_v5_left_residual'] + tf['delta_v5_right_residual']) / 2
    tf['parvo_diff'] = tf['delta_v4_left_residual'] - tf['delta_v4_right_residual']
    tf['magno_diff'] = tf['delta_v5_left_residual'] - tf['delta_v5_right_residual']
    return tf

def transform_block_b(df, lateral_model_scaler=None, lateral_model_pca=None):
    """
    Block B: Construct compressed 3D Channel space.
    lateral_index is the PC1 score of the 4 asymmetry features.
    If models are provided, use them to transform (essential for B/W ratio where diff is applied to df_sess).
    Returns (transformed_df, scaler_used, pca_used)
    """
    tf = df.copy()
    LAT_FEATURES = ['parvo_diff', 'magno_diff', 'asym_dv1_abs', 'asym_dv1_rel']
    
    lat_data = tf[LAT_FEATURES].values
    
    if lateral_model_scaler is None:
        scaler = StandardScaler()
        lat_scaled = scaler.fit_transform(lat_data)
        pca = PCA(n_components=1)
        lat_score = pca.fit_transform(lat_scaled)[:, 0]
    else:
        scaler = lateral_model_scaler
        pca = lateral_model_pca
        lat_scaled = scaler.transform(lat_data)
        lat_score = pca.transform(lat_scaled)[:, 0]

    res = pd.DataFrame(index=tf.index)
    res['subject_id'] = tf['subject_id']
    res['test_date'] = tf['test_date']
    
    res['parvo_index'] = tf['parvo_mean']
    res['magno_index'] = tf['magno_mean']
    res['lateral_index'] = lat_score
    
    return res, scaler, pca


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("Task 31. Stage 3 - Channel Reconstruction (Parvo/Magno)")
    print("=" * 60)
    
    df_sess, df_subj = load_data()
    print(f"Loaded {len(df_sess)} sessions, {len(df_subj)} subjects.")
    
    results = []
    
    # 0. Baseline (No transformation - just for table comparison)
    print("Evaluating 0. Baseline...")
    res_base = evaluate_transformation("Baseline", df_sess, df_subj, FEATURES_BASELINE)
    results.append(res_base)
    
    # 1. Block A (Channel indices)
    print("Evaluating Block A (Channels Expansion)...")
    sess_A = transform_block_a(df_sess)
    subj_A = transform_block_a(df_subj)
    res_A = evaluate_transformation("Block A (Channels)", sess_A, subj_A, FEATURES_BLOCK_A)
    results.append(res_A)
    
    # 2. Block B (Compressed 3D Space)
    print("Evaluating Block B (Compressed 3D Channels)...")
    subj_B, lat_scaler, lat_pca = transform_block_b(subj_A)
    sess_B, _, _ = transform_block_b(sess_A, lateral_model_scaler=lat_scaler, lateral_model_pca=lat_pca)
    res_B = evaluate_transformation("Block B (Aggregated 3D)", sess_B, subj_B, FEATURES_BLOCK_B)
    results.append(res_B)
    
    # 3. Block C (Correlation Matrix)
    print("Evaluating Block C (Channel Correlations)...")
    # Compute correlation on the population level (df_subj)
    corr_matrix = subj_B[['parvo_index', 'magno_index', 'lateral_index']].corr()
    
    # Generage Report
    print("Generating report...")
    report = []
    report.append("# Task 31. Stage 3 — Канальная реконструкция (Parvo / Magno / Koniocellular)\n")
    report.append("> This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.\n")
    
    report.append("## 1. Сравнительные метрики\n")
    report.append("| Transformation | Dim (λ>1) | PC1 % | PR | Boot SD | SH ΔPC1 | B/W Ratio |")
    report.append("|---|---|---|---|---|---|---|")
    
    for r in results:
        report.append(f"| {r['Transformation']} | {r['Dim']} | {r['PC1%']:.2f} | {r['PR']:.3f} | {r['Boot SD']:.2f} | {r['SH ΔPC1']:.2f} | {r['B/W Ratio']:.2f} |")
    
    report.append("\n## 2. PC1 и PC2 Loadings (Block A: Channels)\n")
    
    loadings_a = res_A['Loadings']
    report.append("| Feature | PC1 | PC2 |")
    report.append("|---|---|---|")
    for feat, row in loadings_a.iterrows():
         report.append(f"| `{feat}` | {row['PC1']:.3f} | {row['PC2']:.3f} |")
         
    report.append("\n## 3. Корреляционная матрица каналов (Block C)\n")
    report.append("| Channel | Parvo Index | Magno Index | Lateral Index |")
    report.append("|---|---|---|---|")
    for ch in ['parvo_index', 'magno_index', 'lateral_index']:
        report.append(f"| **{ch}** | {corr_matrix.loc[ch, 'parvo_index']:.3f} | {corr_matrix.loc[ch, 'magno_index']:.3f} | {corr_matrix.loc[ch, 'lateral_index']:.3f} |")
    
    report.append("\n## 4. Сценарный анализ\n")
    report.append("Сценарии:\n")
    
    # Logic for scenarios
    parvo_magno_corr = abs(corr_matrix.loc['parvo_index', 'magno_index'])
    
    if parvo_magno_corr < 0.3 and res_B['Dim'] >= 2:
         report.append("1. **Parvo и Magno образуют две устойчивые (ортогональные) оси**. Корреляция слабая, размерность сохраняется.")
    elif parvo_magno_corr >= 0.3 and res_B['Dim'] >= 2:
         report.append("2. **Один канал доминирует, второй зависим (вторичен)**. Значимая корреляция между каналами свидетельствует о перекрытии дисперсии.")
    else:
         report.append("3. **Канальная агрегация разрушает структуру**. Размерность падает ниже 2, что говорит о некорректности предложенной декомпозиции.")

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Done. Report saved to {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
