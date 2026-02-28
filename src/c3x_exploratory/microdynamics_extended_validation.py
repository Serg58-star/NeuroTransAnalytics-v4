import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.mixed_linear_model import MixedLM
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings

from synthetic_microdynamics_extended import generate_extended_synthetic_data

warnings.filterwarnings('ignore')

def run_extended_diagnostics(df: pd.DataFrame, verbose=False) -> dict:
    results = {}
    
    # Precompute squared terms
    df['log_PSI_sq'] = df['log_PSI'] ** 2
    df['Position_sq'] = df['Position'] ** 2
    df['Interaction'] = df['log_PSI'] * df['Position']
    
    # 1. Interaction Model
    X_int = sm.add_constant(df[['log_PSI', 'Position', 'Interaction']])
    y = df['RT']
    model_int = sm.OLS(y, X_int).fit(cov_type='HC3')
    results['Interaction'] = {
        'coef': model_int.params.get('Interaction', 0),
        'p_value': model_int.pvalues.get('Interaction', 1),
        'AIC': model_int.aic,
        'BIC': model_int.bic
    }
    
    # 2. Non-Linear Models (Polynomial)
    X_nl_psi = sm.add_constant(df[['log_PSI', 'log_PSI_sq']])
    model_nl_psi = sm.OLS(y, X_nl_psi).fit(cov_type='HC3')
    results['NonLinear_PSI'] = {
        'coef_sq': model_nl_psi.params.get('log_PSI_sq', 0),
        'p_value_sq': model_nl_psi.pvalues.get('log_PSI_sq', 1),
        'AIC': model_nl_psi.aic
    }

    X_nl_pos = sm.add_constant(df[['Position', 'Position_sq']])
    model_nl_pos = sm.OLS(y, X_nl_pos).fit(cov_type='HC3')
    results['NonLinear_Position'] = {
        'coef_sq': model_nl_pos.params.get('Position_sq', 0),
        'p_value_sq': model_nl_pos.pvalues.get('Position_sq', 1),
        'AIC': model_nl_pos.aic
    }
    
    # Linear baseline for AIC/BIC comparison (same N, same y)
    X_lin = sm.add_constant(df[['log_PSI', 'Position']])
    model_lin = sm.OLS(y, X_lin).fit(cov_type='HC3')
    results['Linear_Baseline'] = {
        'AIC': model_lin.aic,
        'BIC': model_lin.bic
    }
    
    # 3. Mixed-Effects Model with Fallbacks
    mixed_fallback_used = "None"
    try:
        # Full Model
        md = smf.mixedlm("RT ~ log_PSI + Position", df, groups=df["SubjectID"], re_formula="~log_PSI + Position")
        mdf = md.fit(method='lbfgs')
        mixed_fallback_used = "Full (Random Slopes PSI & Position)"
    except Exception as e:
        try:
            # Fallback 1
            md = smf.mixedlm("RT ~ log_PSI + Position", df, groups=df["SubjectID"], re_formula="~Position")
            mdf = md.fit(method='lbfgs')
            mixed_fallback_used = "Fallback 1 (Random Slope Position)"
        except Exception as e2:
            # Fallback 2
            md = smf.mixedlm("RT ~ log_PSI + Position", df, groups=df["SubjectID"])
            mdf = md.fit(method='lbfgs')
            mixed_fallback_used = "Fallback 2 (Random Intercept Only)"
            
    results['MixedLM'] = {
        'fallback_used': mixed_fallback_used,
        'converged': mdf.converged
    }
    
    # 4. Clustering (Extract individual OLS slopes per subject to cluster)
    subject_slopes = []
    for subj, grp in df.groupby('SubjectID'):
        X_s = sm.add_constant(grp[['log_PSI', 'Position']])
        y_s = grp['RT']
        m_s = sm.OLS(y_s, X_s).fit()
        subject_slopes.append({
            'SubjectID': subj,
            'Intercept': m_s.params['const'],
            'PSI_Slope': m_s.params['log_PSI'],
            'Pos_Slope': m_s.params['Position']
        })
    
    slopes_df = pd.DataFrame(subject_slopes)
    X_cluster = slopes_df[['Intercept', 'PSI_Slope', 'Pos_Slope']].values
    
    kmeans = KMeans(n_clusters=2, random_state=42).fit(X_cluster)
    score = silhouette_score(X_cluster, kmeans.labels_)
    results['Clustering'] = {
        'silhouette': score,
        'centers': kmeans.cluster_centers_
    }
    
    return results

def run_fpr_checks(n_iters=50):
    print("=== SYNTHETIC NEGATIVE CONTROL FPR CHECK ===")
    
    # Interaction FPR
    false_pos_int = 0
    for i in range(n_iters):
        df_null = generate_extended_synthetic_data(scenario="ZERO_INTERACTION", seed=i+100)
        res = run_extended_diagnostics(df_null)
        if res['Interaction']['p_value'] < 0.05:
            false_pos_int += 1
            
    fpr_int = false_pos_int / n_iters
    print(f"Interaction False Positive Rate: {fpr_int:.2%} (Expected ~ 5%)")
    
    # Nonlinearity FPR
    false_pos_nl_pos = 0
    for i in range(n_iters):
        df_null = generate_extended_synthetic_data(scenario="ZERO_NONLINEARITY", seed=i+200)
        res = run_extended_diagnostics(df_null)
        if res['NonLinear_Position']['p_value_sq'] < 0.05:
            false_pos_nl_pos += 1
            
    fpr_nl = false_pos_nl_pos / n_iters
    print(f"Non-Linearity False Positive Rate: {fpr_nl:.2%} (Expected ~ 5%)")
    
    if fpr_int > 0.10 or fpr_nl > 0.10:
        print("WARNING: FPR too high. Algorithm is hallucinating effects.")
    else:
        print("FPR Check Passed. Algorithm avoids hallucination.")

if __name__ == "__main__":
    # 1. Run rigorous positive check on FULL data
    print("=== SYNTHETIC POSITIVE VALIDATION ===")
    df_full = generate_extended_synthetic_data(scenario="FULL", seed=42)
    res_full = run_extended_diagnostics(df_full, verbose=True)
    
    print(f"Interaction (GT=0.5): Coef={res_full['Interaction']['coef']:.3f}, p={res_full['Interaction']['p_value']:.4e}")
    print(f"NonLinear Position (GT=0.05): Coef={res_full['NonLinear_Position']['coef_sq']:.3f}, p={res_full['NonLinear_Position']['p_value_sq']:.4e}")
    print(f"AIC Improvement (Interaction over Linear): {res_full['Linear_Baseline']['AIC'] - res_full['Interaction']['AIC']:.1f}")
    print(f"MixedLM Fallback Route: {res_full['MixedLM']['fallback_used']} (Converged: {res_full['MixedLM']['converged']})")
    print(f"Clustering Silhouette Score (Expect > 0.5 for clean clusters): {res_full['Clustering']['silhouette']:.3f}")
    
    # 2. Run FPR control loops
    run_fpr_checks(n_iters=50)
