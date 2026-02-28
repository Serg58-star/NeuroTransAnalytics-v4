import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
import warnings
from typing import Dict, Any, Tuple

from synthetic_microdynamics_b1_a2 import generate_microdynamic_synthetic_data

warnings.filterwarnings('ignore')

def run_microdynamic_diagnostics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validates B1 (PSI Recovery) and A2 (Position Fatigue) effects on a trial-level dataframe.
    Includes Power Analysis (Minimum Detectable Effect) and Heteroskedasticity checks.
    """
    results = {}
    
    # 1. B1 Scenario: RT ~ log(PSI)
    # We use log10(PSI/1000) to match the synthetic generator scaling
    df['log_PSI'] = np.log10(df['PSI'] / 1000.0)
    
    X_b1 = sm.add_constant(df['log_PSI'])
    y = df['RT']
    
    model_b1 = sm.OLS(y, X_b1).fit()
    
    # Heteroskedasticity diagnostic for B1
    _, pval_bp_b1, _, _ = het_breuschpagan(model_b1.resid, model_b1.model.exog)
    
    if pval_bp_b1 < 0.05:
        # Re-fit with robust standard errors (HC3) due to heteroskedasticity
        model_b1_robust = sm.OLS(y, X_b1).fit(cov_type='HC3')
        b1_slope = model_b1_robust.params['log_PSI']
        b1_p = model_b1_robust.pvalues['log_PSI']
        b1_se = model_b1_robust.bse['log_PSI']
        b1_het = True
    else:
        b1_slope = model_b1.params['log_PSI']
        b1_p = model_b1.pvalues['log_PSI']
        b1_se = model_b1.bse['log_PSI']
        b1_het = False
        
    results['B1_Recovery'] = {
        'slope': b1_slope,
        'p_value': b1_p,
        'robust_se_used': b1_het,
        'bp_test_p': pval_bp_b1
    }

    # 2. A2 Scenario: RT ~ Position
    X_a2 = sm.add_constant(df['Position'])
    model_a2 = sm.OLS(y, X_a2).fit()
    
    # Heteroskedasticity diagnostic for A2
    _, pval_bp_a2, _, _ = het_breuschpagan(model_a2.resid, model_a2.model.exog)
    
    if pval_bp_a2 < 0.05:
        model_a2_robust = sm.OLS(y, X_a2).fit(cov_type='HC3')
        a2_slope = model_a2_robust.params['Position']
        a2_p = model_a2_robust.pvalues['Position']
        a2_se = model_a2_robust.bse['Position']
        a2_het = True
    else:
        a2_slope = model_a2.params['Position']
        a2_p = model_a2.pvalues['Position']
        a2_se = model_a2.bse['Position']
        a2_het = False

    results['A2_Fatigue'] = {
        'slope': a2_slope,
        'p_value': a2_p,
        'robust_se_used': a2_het,
        'bp_test_p': pval_bp_a2
    }
    
    # 3. Power Analysis estimation (simplified MDE calculation at alpha=0.05, power=0.80)
    # MDE ≈ 2.8 * SE (based on z_alpha/2 + z_beta for normal dist)
    z_multiplier = 2.802 
    results['Power_Analysis'] = {
        'MDE_B1_slope': z_multiplier * b1_se,
        'MDE_A2_slope': z_multiplier * a2_se,
        'Sample_Size (Total Trials)': len(df)
    }

    return results

if __name__ == "__main__":
    print("=== SYNTHETIC VALIDATION PHASE ===")
    # Generate data with known parameters: fatigue = 2.5, recovery = 30.0
    synth_df = generate_microdynamic_synthetic_data(n_subjects=50, fatigue_slope=2.5, recovery_factor=30.0, seed=123)
    
    res = run_microdynamic_diagnostics(synth_df)
    
    print("\n--- B1: PSI Recovery ---")
    print(f"Detected Recovery Slope (Expected ~ -30.0): {res['B1_Recovery']['slope']:.3f} (p={res['B1_Recovery']['p_value']:.4e})")
    print(f"Breusch-Pagan p-val: {res['B1_Recovery']['bp_test_p']:.4f}  |  Robust HC3 Used: {res['B1_Recovery']['robust_se_used']}")
    print(f"Minimum Detectable Effect (MDE): {res['Power_Analysis']['MDE_B1_slope']:.3f}")

    print("\n--- A2: Intra-block Fatigue ---")
    print(f"Detected Fatigue Slope (Expected ~ 2.5): {res['A2_Fatigue']['slope']:.3f} (p={res['A2_Fatigue']['p_value']:.4e})")
    print(f"Breusch-Pagan p-val: {res['A2_Fatigue']['bp_test_p']:.4f}  |  Robust HC3 Used: {res['A2_Fatigue']['robust_se_used']}")
    print(f"Minimum Detectable Effect (MDE): {res['Power_Analysis']['MDE_A2_slope']:.3f}")
    
    print("\n--- Power Conclusive Assessment ---")
    print(f"N=50 subjects * 3 tests * 36 trials = {res['Power_Analysis']['Sample_Size (Total Trials)']} trials.")
    print("If MDE < Expected True Effect, then statistical power is sufficient (>80%).")
