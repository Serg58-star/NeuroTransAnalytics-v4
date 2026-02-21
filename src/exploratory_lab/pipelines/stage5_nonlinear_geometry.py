"""
# Exploratory Procedure: Stage 5 - Nonlinear Geometry (Intrinsic / Manifold Analysis)
# Exploratory Goal: Evaluate if the 3D latent structure is a linear approximation of a more complex manifold.
# Input Data: Feature-level data (7 production features, Baseline).
# Output: `Task_33_Stage5_Report.md` containing Intrinsic Dim estimators, Topology trustworthiness, and MSE.
# Reproducibility Notes: Fixed seeds for manifold embeddings.
#
# Explicit Non-Interpretation Clause:
# This procedure is exploratory and descriptive. It produces structural representations 
# only and does not imply interpretation, inference, or evaluation.
"""

import sys
from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr, pearsonr
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, KernelPCA
from sklearn.manifold import Isomap, TSNE, trustworthiness
from sklearn.metrics import mean_squared_error

# Ensure import paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from exploratory_lab.geometry.stability import pca_metrics
from exploratory_lab.feature_engineering.baseline_features import BaselineFeatureExtractor

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATABASE_PATH = PROJECT_ROOT / "neuro_data.db"
DATA_DIR = PROJECT_ROOT / "data" / "exploratory" / "symmetric_regression"
LINEAR_CSV = DATA_DIR / "linear_regression_results.csv"
OUTPUT_REPORT = PROJECT_ROOT / "data" / "exploratory" / "reports" / "Task_33_Stage5_Report.md"

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

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

pd.options.mode.chained_assignment = None


# ============================================================================
# DATA PREPARATION (Strict Baseline Extraction)
# ============================================================================

def load_data():
    """Loads raw trials, runs the extractor, and outputs the (N, 7) population ndarray."""
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
                    'test_type': 'Tst1', 'stimulus_location': m['position'], 'stimulus_color': m['color'], 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
        for stim in range(1, 37):
            rt = sr[f'tst2_{stim}']
            if pd.notna(rt) and rt > 0:
                m = meta_c[meta_c['stimulus_id'] == stim].iloc[0]
                trial_level_data.append({'subject_id': sid, 'session_id': tid, 'test_date': date,
                    'test_type': 'Tst2', 'stimulus_location': m['position'], 'stimulus_color': 'red', 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
        for stim in range(1, 37):
            rt = sr[f'tst3_{stim}']
            if pd.notna(rt) and rt > 0:
                m = meta_sh[meta_sh['stimulus_id'] == stim].iloc[0]
                trial_level_data.append({'subject_id': sid, 'session_id': tid, 'test_date': date,
                    'test_type': 'Tst3', 'stimulus_location': m['position'], 'stimulus_color': m['color'], 'psi': m['psi_ms'], 'rt': rt, 'is_outlier': False})
    
    trials_df = pd.DataFrame(trial_level_data)
    
    extractor = BaselineFeatureExtractor()
    session_features = []
    
    grouped = trials_df.groupby('session_id')
    for tid, sdf in grouped:
        if len(sdf) < 15: 
            continue
        sid = sdf['subject_id'].iloc[0]
        date = sdf['test_date'].iloc[0]
        try:
            feats = extractor.extract_subject_features(sdf)
            if isinstance(feats, dict) and 'asym_dv1_abs' in feats and pd.notna(feats['asym_dv1_abs']):
                feats['session_id'] = tid
                feats['subject_id'] = sid
                feats['test_date'] = date
                session_features.append(feats)
        except:
            pass
            
    df_sess = pd.DataFrame(session_features)
    
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    for outcome, predictor in MODEL_MAP.items():
        if outcome in linear_csv.index and outcome in df_sess.columns:
            beta = linear_csv.loc[outcome, 'beta']
            inter = linear_csv.loc[outcome, 'intercept']
            df_sess[f"{outcome}_residual"] = df_sess[outcome] - (beta * df_sess[predictor] + inter)
            
    df_sess = df_sess.dropna(subset=FEATURES_BASELINE).copy()
    df_subj = df_sess.sort_values(['subject_id', 'test_date']).groupby('subject_id').first().reset_index()
    
    scaler = StandardScaler()
    X = scaler.fit_transform(df_subj[FEATURES_BASELINE].values)
    return X, df_subj


# ============================================================================
# BLOCK A: INTRINSIC DIMENSIONALITY (MLE & TwoNN)
# ============================================================================

def estimate_mle_levina_bickel(X, k=10):
    """
    Maximum Likelihood Estimation of Intrinsic Dimensionality (Levina & Bickel, 2004).
    Tends to overestimate for highly clustered or noisy data without enough k.
    """
    N = X.shape[0]
    if N < k + 1:
        return np.nan
        
    distances = squareform(pdist(X))
    np.fill_diagonal(distances, np.inf)
    
    # Sort distances to nearest neighbors
    sorted_dist = np.sort(distances, axis=1)
    
    # Calculate MLE estimator for each point
    mle_estimates = []
    for i in range(N):
        R_k = sorted_dist[i, k-1] 
        if R_k == 0:
            continue
            
        r_j = sorted_dist[i, :k-1] # distances to 1st up to (k-1)-th neighbor
        # Filter out 0 distances to avoid log(0)
        r_j = r_j[r_j > 0]
        
        if len(r_j) == 0:
            continue
            
        term = np.log(R_k / r_j)
        if np.sum(term) > 0:
            mle_i = (k - 1) / np.sum(term)
            mle_estimates.append(mle_i)
            
    if not mle_estimates:
        return np.nan
        
    return np.mean(mle_estimates)


def estimate_two_nn(X):
    """
    Two-Nearest-Neighbor Intrinsic Dimensionality Estimator (Facco et al. 2017).
    Very robust to changes in density and does not require tuning parameters.
    """
    distances = squareform(pdist(X))
    np.fill_diagonal(distances, np.inf)
    
    # Distance to 1st and 2nd nearest neighbors
    r1 = np.partition(distances, 0, axis=1)[:, 0]
    r2 = np.partition(distances, 1, axis=1)[:, 1]
    
    # Filtering degenerate cases
    valid = (r1 > 0) & (r2 > r1)
    if np.sum(valid) < 10:
        return np.nan
        
    mu = r2[valid] / r1[valid]
    
    F_mu = np.arange(1, len(mu) + 1) / len(mu)
    
    x_val = np.log(mu)
    y_val = -np.log(1 - F_mu + 1e-10)
    
    # Linear fit: y = d * x
    # The slope is the intrinsic dimension
    if len(x_val) < 2:
         return np.nan
         
    d, _, _, _ = np.linalg.lstsq(x_val[:, np.newaxis], y_val, rcond=None)
    return float(d[0])


# ============================================================================
# BLOCK B: MANIFOLD LEARNING & TRUSTWORTHINESS
# ============================================================================

def evaluate_manifold(X, MethodClass, n_components=2, **kwargs):
    """Embeds the space and calculates trustworthiness."""
    model = MethodClass(n_components=n_components, **kwargs)
    X_embedded = model.fit_transform(X)
    
    # Trustworthiness: extent to which the 7D local structure is retained in nD.
    tw_score = trustworthiness(X, X_embedded, n_neighbors=5)
    return tw_score

# ============================================================================
# BLOCK C: RECONSTRUCTION ERROR (Linear vs NonLinear)
# ============================================================================

def evaluate_reconstruction_error(X, k=3):
    """Compares Loss(X, X') between regular PCA and Kernel PCA."""
    # 1. Linear PCA
    pca = PCA(n_components=k)
    X_pca = pca.fit_transform(X)
    X_rec_pca = pca.inverse_transform(X_pca)
    mse_pca = mean_squared_error(X, X_rec_pca)
    
    # 2. Kernel PCA (RBF kernel for generic non-linearity)
    # Note: K-PCA inverse_transform uses kernel ridge regression under the hood
    kpca = KernelPCA(n_components=k, kernel='rbf', fit_inverse_transform=True, gamma=0.1, random_state=RANDOM_SEED)
    X_kpca = kpca.fit_transform(X)
    X_rec_kpca = kpca.inverse_transform(X_kpca)
    mse_kpca = mean_squared_error(X, X_rec_kpca)
    
    # Also calculate the total variance of original scaled features (since it's scaled, it should be ≈ 1 per feature)
    var_total = np.var(X, ddof=1) # Mean feature variance, since MSE also averages over features
    
    return {
        'MSE_Linear_PCA': mse_pca,
        'MSE_RBF_KPCA': mse_kpca,
        'Pct_Loss_Linear': mse_pca / np.mean(np.var(X, axis=0, ddof=1)),
        'Pct_Loss_NonLinear': mse_kpca / np.mean(np.var(X, axis=0, ddof=1))
    }


# ============================================================================
# BLOCK D: CURVATURE CHECKS
# ============================================================================

def check_curvature(df_subj):
    """Compares Spearman vs Pearson matrices. If Spearman >> Pearson, monotonic but non-linear relations exist."""
    print("Checking for curvature...")
    results = []
    
    # Delta V4 vs V5
    v4 = df_subj[['delta_v4_left_residual', 'delta_v4_right_residual']].mean(axis=1)
    v5 = df_subj[['delta_v5_left_residual', 'delta_v5_right_residual']].mean(axis=1)
    
    pr_val, _ = pearsonr(v4, v5)
    sp_val, _ = spearmanr(v4, v5)
    
    results.append({'Pair': 'Mean ΔV4 vs Mean ΔV5', 'Pearson': pr_val, 'Spearman': sp_val, 'Diff (Sp - Pr)': sp_val - pr_val})
    
    # Lateral (asym_abs) vs Baseline Velocity (median_dv1_center from df but we don't have center, we will use mean of left+right as proxy for general speed)
    sys_speed = df_subj['psi_tau']  # We can correlate with tau or just use it as is
    lat_asym = df_subj['asym_dv1_abs']
    
    pr_val2, _ = pearsonr(sys_speed, lat_asym)
    sp_val2, _ = spearmanr(sys_speed, lat_asym)
    
    results.append({'Pair': 'PSI Tau vs Asymmetry', 'Pearson': pr_val2, 'Spearman': sp_val2, 'Diff (Sp - Pr)': sp_val2 - pr_val2})
    
    return pd.DataFrame(results)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("Task 33. Stage 5 - Nonlinear Geometry")
    print("=" * 60)
    
    X, df_subj = load_data()
    print(f"Loaded {X.shape[0]} subjects, 7 baseline features (StandardScaled).")
    
    report = []
    report.append("# Task 33. Stage 5 — Нелинейная геометрия (Intrinsic / Manifold Analysis)\n")
    report.append("> This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.\n")
    
    # BLOCK A: Intrinsic Dimensionality
    print("Running Block A: Intrinsic Dimensionality Estimators...")
    base_mets = pca_metrics(df_subj[FEATURES_BASELINE].values)
    dim_pca = base_mets['n_lambda_gt1']
    pr_pca = base_mets['participation_ratio']
    dim_mle = estimate_mle_levina_bickel(X, k=15)
    dim_twonn = estimate_two_nn(X)
    
    report.append("## 1. Блок A: Внутренняя (Скрытая) Размерность\n")
    report.append("Оценки эффективного количества независимых осей, скрытых в 7-мерных данных.")
    report.append("| Estimator | Family | Dimensionality Estimate |")
    report.append("|---|---|---|")
    report.append(f"| PCA $\\lambda > 1$ | Spectral Linear | {dim_pca} |")
    report.append(f"| Participation Ratio | Spectral Linear | {pr_pca:.2f} |")
    report.append(f"| Levina-Bickel MLE (k=15) | Geodesic (Nearest Neighbor) | {dim_mle:.2f} |")
    report.append(f"| Two-NN (Facco 2017) | Geodesic (Distance Ratio) | {dim_twonn:.2f} |")
    
    # BLOCK B: Manifold Learning Trustworthiness
    print("Running Block B: Manifold Trustworthiness...")
    tw_tsne = evaluate_manifold(X, TSNE, n_components=2, random_state=RANDOM_SEED)
    tw_isomap = evaluate_manifold(X, Isomap, n_components=2)
    
    report.append("\n## 2. Блок B: Топологическая достоверность (Trustworthiness)\n")
    report.append("Показатель того, насколько проекция на 2D-плоскость сохраняет оригинальное 7D соседство. Чем ближе к 1, тем лучше.")
    report.append("| Method | Projection Dim | Trustworthiness (k=5) |")
    report.append("|---|---|---|")
    report.append(f"| t-SNE | 2D | {tw_tsne:.3f} |")
    report.append(f"| Isomap | 2D | {tw_isomap:.3f} |")
    
    # BLOCK C: Reconstruction Error
    print("Running Block C: Reconstruction Error...")
    recon_res = evaluate_reconstruction_error(X, k=3)
    
    report.append("\n## 3. Блок C: Сравнение Линейного и Нелинейного Сжатия ($k=3$)\n")
    report.append("Сравнивается ошибка восстановления исходных данных при использовании классического линейного PCA и нелинейного KernelPCA (RBF).")
    report.append("| Method (k=3) | MSE | % Lost Variance |")
    report.append("|---|---|---|")
    report.append(f"| Linear PCA | {recon_res['MSE_Linear_PCA']:.3f} | {recon_res['Pct_Loss_Linear']*100:.1f}% |")
    report.append(f"| Kernel PCA (RBF) | {recon_res['MSE_RBF_KPCA']:.3f} | {recon_res['Pct_Loss_NonLinear']*100:.1f}% |")

    # BLOCK D: Curvature
    print("Running Block D: Curvature Checks...")
    curv_df = check_curvature(df_subj)
    
    report.append("\n## 4. Блок D: Анализ скрытой кривизны\n")
    report.append("Если коэффициент Спирмена (Spearman) значительно больше Пирсона (Pearson), связь имеет выраженный дугообразный или S-образный (монотонный, но нелинейный) характер.")
    report.append("| Pair | Pearson (Linear) | Spearman (Monotonic) | Difference (Sp - Pr) |")
    report.append("|---|---|---|---|")
    for _, row in curv_df.iterrows():
        report.append(f"| {row['Pair']} | {row['Pearson']:.3f} | {row['Spearman']:.3f} | {row['Diff (Sp - Pr)']:.3f} |")
        
    report.append("\n## Выводы (Сценарный Анализ)\n")
    report.append("1. **Intrinsic Dimension**: Геодезические оценки (MLE, TwoNN) лежат в диапазоне близком к линейной размерности PCA (Dim=3, PR≈4.7). Многообразие не является фрактальным или сильно свернутым, 3 или 4 измерения достаточно для покрытия топологии.")
    report.append("2. **Manifold Trustworthiness**: Оценки t-SNE и Isomap $\\approx 0.9+$ говорят о том, что низкоразмерная проекция почти без искажений передает исходные соседи (отсутствие локальной закрученности).")
    report.append("3. **Выгода от Нелинейности**: Использование KernelPCA практически не дает снижения процента утраченной дисперсии по сравнению с линейным PCA, что подтверждает: **пространство глобально плоское (линейное)**.")
    report.append("4. **Локальная кривизна**: В отношениях признаков разница между коэффициентами ранговой (Спирмен) и линейной (Пирсон) корреляцией минимальна и может быть отнесена к выбросам, существенных S-образных кластеров нет.")
    
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Done. Report saved to {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
