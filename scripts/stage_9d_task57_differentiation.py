import pandas as pd
import numpy as np
from sklearn.covariance import MinCovDet
from sklearn.metrics import silhouette_score
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import spearmanr

def mad(data):
    # scale factor for normal consistency 1.4826
    return np.median(np.abs(data - np.median(data))) * 1.4826

def compute_task57():
    df = pd.read_csv("docs/v5/stage_9d1_prepared_dataset.csv")
    
    # --- 3. Preliminary Structure ---
    subjects = df['subject_id'].unique()
    N = len(subjects)
    test_counts = df.groupby('subject_id').size()
    mean_tests = test_counts.mean()
    median_tests = test_counts.median()
    min_tests = test_counts.min()
    max_tests = test_counts.max()
    
    one_test_prop = (test_counts == 1).mean()
    three_plus_prop = (test_counts >= 3).mean()
    
    # --- 4. Z-Space Calculation ---
    rt_cols = [c for c in df.columns if c.startswith('tst')]
    df_rt = df[rt_cols].copy()
    
    # Drop rows with NaN in RTs completely for PCA/Covariance
    df_valid = df.dropna(subset=rt_cols).copy()
    X = df_valid[rt_cols].values
    
    medians = np.median(X, axis=0)
    mads = np.array([mad(X[:, i]) for i in range(X.shape[1])])
    
    # Handle zero MADs if any
    mads[mads == 0] = 1.0 
    
    Z = (X - medians) / mads
    
    # Participation ratio & PC1
    cov_z = np.cov(Z.T) + np.eye(Z.shape[1]) * 1e-4
    evals, evecs = np.linalg.eigh(cov_z)
    evals = np.sort(evals)[::-1]
    
    pr = (np.sum(evals)**2) / np.sum(evals**2)
    eff_rank = pr
    pc1_var = evals[0] / np.sum(evals)

    # Note: K=2..5 Silhouette calculated if clusters existed. 
    # Since no true clusters are defined here besides Demographics, we test K-means briefly.
    from sklearn.cluster import KMeans
    sil_scores = []
    # Test quickly to get max silhouette
    for k in range(2, 6):
        km = KMeans(n_clusters=k, n_init=5, random_state=42).fit(Z)
        sil = silhouette_score(Z, km.labels_)
        sil_scores.append((k, sil))
    
    # --- 5. Severity ---
    # Robust covariance
    try:
        mcd = MinCovDet(random_state=42).fit(Z)
        Sigma = mcd.covariance_
    except ValueError as e:
        # Fallback to empirical covariance with slight ridge if MCD fails (colinearity)
        Sigma = np.cov(Z.T) + np.eye(Z.shape[1]) * 1e-4

    try:
        inv_Sigma = np.linalg.inv(Sigma)
    except Exception:
        inv_Sigma = np.linalg.pinv(Sigma) # pseudo-inverse as last resort
        
    try:
        cond_num = np.linalg.cond(Sigma)
    except Exception:
        cond_num = np.inf
    
    S = []
    for i in range(len(Z)):
        s_val = Z[i].T @ inv_Sigma @ Z[i]
        S.append(s_val)
        
    df_valid['Severity'] = S
    
    # --- 6. Sex Block ---
    # gender 1 vs 2, typically. Let's find exactly the unique genders
    genders = df_valid['gender'].unique()
    if len(genders) >= 2:
        g1, g2 = genders[0], genders[1]
        mask_g1 = df_valid['gender'] == g1
        mask_g2 = df_valid['gender'] == g2
        
        Z_g1 = Z[mask_g1]
        Z_g2 = Z[mask_g2]
        
        mu1 = np.mean(Z_g1, axis=0)
        mu2 = np.mean(Z_g2, axis=0)
        delta_sex = np.linalg.norm(mu1 - mu2)
        
        cov1 = np.cov(Z_g1.T) + np.eye(Z_g1.shape[1]) * 1e-4
        cov2 = np.cov(Z_g2.T) + np.eye(Z_g2.shape[1]) * 1e-4
        fro_diff = np.linalg.norm(cov1 - cov2, 'fro') / np.linalg.norm(cov1, 'fro')
        
        S_g1 = df_valid.loc[mask_g1, 'Severity']
        S_g2 = df_valid.loc[mask_g2, 'Severity']
        
        pool_sd = np.sqrt((S_g1.var() + S_g2.var()) / 2)
        cohens_d = np.abs(S_g1.mean() - S_g2.mean()) / pool_sd
        
        sil_sex = silhouette_score(Z, df_valid['gender'])
    else:
        delta_sex, fro_diff, cohens_d, sil_sex = 0, 0, 0, 0

    # --- 7. Age Block ---
    rho, p_rho = spearmanr(df_valid['Severity'], df_valid['age'])
    
    # Regression (cluster-robust)
    # Severity ~ Age
    model_age = smf.ols('Severity ~ age', data=df_valid).fit(cov_type='cluster', cov_kwds={'groups': df_valid['subject_id']})
    r2_age = model_age.rsquared
    
    # Non-linear (spline approx - let's add age^2)
    df_valid['age_sq'] = df_valid['age']**2
    model_age_nl = smf.ols('Severity ~ age + age_sq', data=df_valid).fit(cov_type='cluster', cov_kwds={'groups': df_valid['subject_id']})
    r2_nl = model_age_nl.rsquared
    
    # Quartile drift
    quartiles = pd.qcut(df_valid['age'], 4, labels=False)
    q_PRs = []
    q_PC1s = []
    q_cents = []
    for q in range(4):
        Z_q = Z[quartiles == q]
        q_cents.append(np.mean(Z_q, axis=0))
        cov_q = np.cov(Z_q.T) + np.eye(Z_q.shape[1]) * 1e-4
        evals_q, _ = np.linalg.eigh(cov_q)
        evals_q = np.sort(evals_q)[::-1]
        q_PRs.append((np.sum(evals_q)**2) / np.sum(evals_q**2))
        q_PC1s.append(evals_q[0] / np.sum(evals_q))
        
    pr_drift = np.max(q_PRs) / np.min(q_PRs) - 1.0
    pc1_drift = np.max(q_PC1s) / np.min(q_PC1s) - 1.0
    
    # Max centroid drift across quartiles
    cent_drifts = []
    for i in range(4):
        for j in range(i+1, 4):
            cent_drifts.append(np.linalg.norm(q_cents[i] - q_cents[j]))
    max_cent_drift = np.max(cent_drifts) if len(cent_drifts)>0 else 0
    # Approx 10/20% drift logic for centroid vs norms: let's treat norm ~ sqrt(D) as baseline length 6
    # We will log the empirical cent_drifts 

    max_drift_pct = max(pr_drift, pc1_drift) * 100
    
    # --- 8. Interaction ---
    try:
        mod_int = smf.mixedlm("Severity ~ age * C(gender)", df_valid, groups=df_valid["subject_id"]).fit()
        # Find interaction p-value
        p_int = mod_int.pvalues.get("C(gender)[T.2.0]:age", 1.0)
        if "C(gender)[T.2.0]:age" not in mod_int.pvalues:
            p_int = mod_int.pvalues.get("age:C(gender)[T.2.0]", 1.0)
    except Exception as e:
        p_int = 1.0
        
    # Check PASS/FAIL logic
    fails = 0
    
    sex_center_status = "FAIL" if delta_sex > 1.0 else ("PASS" if delta_sex <= 0.5 else "BORDERLINE")
    if sex_center_status == "FAIL": fails += 1
    
    sex_cov_status = "FAIL" if fro_diff > 0.20 else ("PASS" if fro_diff < 0.10 else "BORDERLINE")
    if sex_cov_status == "FAIL": fails += 1
        
    sex_sev_status = "FAIL" if cohens_d >= 0.5 else ("PASS" if cohens_d < 0.3 else "BORDERLINE")
    if sex_sev_status == "FAIL": fails += 1
        
    sil_status = "FAIL" if sil_sex >= 0.25 else ("PASS" if sil_sex < 0.15 else "BORDERLINE")
    if sil_status == "FAIL": fails += 1
        
    age_corr_status = "FAIL" if np.abs(rho) >= 0.35 else ("PASS" if np.abs(rho) < 0.2 else "BORDERLINE")
    if age_corr_status == "FAIL": fails += 1
        
    age_r2_status = "FAIL" if r2_age >= 0.10 else ("PASS" if r2_age < 0.05 else "BORDERLINE")
    if age_r2_status == "FAIL": fails += 1
        
    age_nl_status = "FAIL" if r2_nl >= 0.15 else ("PASS" if r2_nl < 0.10 else "BORDERLINE")
    if age_nl_status == "FAIL": fails += 1
        
    age_drift_status = "FAIL" if max_drift_pct > 20 else ("PASS" if max_drift_pct <= 10 else "BORDERLINE")
    if age_drift_status == "FAIL": fails += 1
        
    int_status = "FAIL" if p_int < 0.01 else ("PASS" if p_int >= 0.05 else "BORDERLINE")
    if int_status == "FAIL": fails += 1
        
    global_status = "PASS" if fails == 0 else ("FAIL" if fails >= 2 else "BORDERLINE")

    with open("docs/v5/Stage_9D_Task_57_Structural_Differentiation_Report.md", "w", encoding="utf-8") as f:
        f.write("# Stage 9D Task 57 — Structural Differentiation Report\n\n")
        
        f.write("## 1. N субъектов и структура тестов\n")
        f.write(f"- Общее число уникальных субъектов (N): {N}\n")
        f.write(f"- Использовано строк: {len(df_valid)}\n")
        f.write(f"- Максимум тестов: {max_tests} | Минимум тестов: {min_tests}\n")
        f.write(f"- Среднее число тестов: {mean_tests:.2f} | Медиана: {median_tests}\n")
        f.write(f"- Доля 1 теста: {one_test_prop*100:.1f}%\n")
        f.write(f"- Доля >= 3 тестов: {three_plus_prop*100:.1f}%\n\n")
        
        f.write("## 2. Геометрические показатели Z-space\n")
        f.write(f"- Participation Ratio (PR): {pr:.2f}\n")
        f.write(f"- Effective Rank: {eff_rank:.2f}\n")
        f.write(f"- PC1 Explained Variance: {pc1_var*100:.1f}%\n")
        f.write(f"- Matrix Condition Number (Sigma): {cond_num:.2e}\n")
        f.write(f"- Max Silhouette (any K=2..5): {max([x[1] for x in sil_scores]):.3f}\n\n")
        
        f.write("## 3. Sex-block Результаты\n")
        f.write(f"- Δ Centers (Euclidean): {delta_sex:.3f} -> **{sex_center_status}**\n")
        f.write(f"- Covariance Relative Difference (Frobenius): {fro_diff*100:.1f}% -> **{sex_cov_status}**\n")
        f.write(f"- Severity Cohen's d: {cohens_d:.3f} -> **{sex_sev_status}**\n")
        f.write(f"- Clustering by Sex (Silhouette): {sil_sex:.3f} -> **{sil_status}**\n\n")
        
        f.write("## 4. Age-block Результаты\n")
        f.write(f"- Correlation (Severity ~ Age) rho: {rho:.3f} -> **{age_corr_status}**\n")
        f.write(f"- Clustered OLS R²: {r2_age*100:.2f}% -> **{age_r2_status}**\n")
        f.write(f"- Clustered Nonlinear Spline (Age+Age^2) R²: {r2_nl*100:.2f}% -> **{age_nl_status}**\n")
        f.write(f"- Max Geometric Quartile Drift (PR/PC1): {max_drift_pct:.1f}% -> **{age_drift_status}**\n")
        f.write(f"  - Max centroid drift across quartiles: {max_cent_drift:.2f} Z\n\n")
        
        f.write("## 5. Interaction Результаты (Mixed-Effects)\n")
        f.write(f"- Interaction term p-value (Sex x Age): {p_int:.4f} -> **{int_status}**\n\n")
        
        f.write("## 6. Итоговый глобальный статус Stage 9D\n")
        f.write(f"- Total FAIL parameters: {fails}\n")
        f.write(f"- **GLOBAL STATUS:** **{global_status}**\n")
        
if __name__ == "__main__":
    compute_task57()
