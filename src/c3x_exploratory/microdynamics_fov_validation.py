import numpy as np
import pandas as pd
import statsmodels.api as sm
from typing import Dict, Any

from synthetic_microdynamics_fov import generate_fov_synthetic_data

def evaluate_central_fov_informational_value(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Evaluates the informational value of the Central FOV.
    Per Task 48.4.1 Methodological Controls:
    1. Compares AIC on EXACTLY identical datasets (Model A' vs Model B' on L/R subset).
    2. Checks the stabilizing role of Center on the L-R variance.
    3. Performs Power Recalibration for 36 vs 24 stimuli.
    """
    results = {}
    
    # 1. AIC Identical Dataset Rule (Подход А)
    # Subset to ONLY Left/Right trials (N=24 per block) for strict comparison
    df_lr = df[df['FieldOfView'].isin(['Left', 'Right'])].copy()
    
    # Dummy code purely to establish structural equivalence 
    # (Center code will be 0 identically, acts as placeholder for Model A structurally in patsy/statsmodels)
    dummies_lr = pd.get_dummies(df_lr['FieldOfView'], drop_first=False).astype(float) 
    
    # Model A': "L+R+C" structure applied strictly to L/R data
    X_A_prime = dummies_lr[['Left', 'Right']] # No center column effectively simulates its removal from the explanatory matrix
    X_A_prime['log_PSI'] = df_lr['log_PSI']
    X_A_prime['Position'] = df_lr['Position']
    X_A_prime = sm.add_constant(X_A_prime)
    
    # Model B': Standard L/R model
    X_B_prime = dummies_lr[['Left']] # Using Left as the single dummy variable (Right is reference)
    X_B_prime['log_PSI'] = df_lr['log_PSI']
    X_B_prime['Position'] = df_lr['Position']
    X_B_prime = sm.add_constant(X_B_prime)
    
    y_lr = df_lr['RT']
    
    # Fit the 24-trial models
    model_a_prime = sm.OLS(y_lr, X_A_prime).fit(cov_type='HC3')
    model_b_prime = sm.OLS(y_lr, X_B_prime).fit(cov_type='HC3')
    
    # If the AIC is basically identical, Center adds no unique structural information to the lateralized subset
    results['AIC_Delta'] = model_a_prime.aic - model_b_prime.aic
    
    # Full Model A to evaluate R^2 of Center
    dummies_full = pd.get_dummies(df['FieldOfView'], drop_first=False).astype(float)
    X_full = dummies_full[['Left', 'Center']] # Right is reference
    X_full['log_PSI'] = df['log_PSI']
    X_full['Position'] = df['Position']
    X_full = sm.add_constant(X_full)
    
    model_full = sm.OLS(df['RT'], X_full).fit(cov_type='HC3')
    results['Center_Partial_PValue'] = model_full.pvalues.get('Center', 1.0)
    
    # 2. L-R Variance Stabilization
    # We calculate the deviation (Left RT - Right RT) using adjacent or block-averaged trials
    # Group by subject and test to isolate variances
    lr_var_with_center = []
    lr_var_without_center = []
    
    for _, grp in df.groupby(['SubjectID', 'TestBlock']):
        lefts = grp[grp['FieldOfView'] == 'Left']['RT'].values
        rights = grp[grp['FieldOfView'] == 'Right']['RT'].values
        
        # Taking absolute variance of the means / lists
        if len(lefts) > 0 and len(rights) > 0:
            # Variance of the lateralization proxy (mean Left - mean Right) over blocks
            pass # Simplified: we look at standard deviation of slope estimates
            
    # Correct Variance check per subject OLS
    var_slopes_36 = []
    var_slopes_24 = []
    
    for subj, grp in df.groupby('SubjectID'):
        # 36 trials
        X_36 = pd.get_dummies(grp['FieldOfView']).astype(float)[['Left']]
        X_36['Position'] = grp['Position']
        X_36['log_PSI'] = grp['log_PSI']
        X_36 = sm.add_constant(X_36)
        m_36 = sm.OLS(grp['RT'], X_36).fit()
        var_slopes_36.append(m_36.bse.get('Left', 0))
        
        # 24 trials
        grp_24 = grp[grp['FieldOfView'].isin(['Left', 'Right'])]
        X_24 = pd.get_dummies(grp_24['FieldOfView']).astype(float)[['Left']]
        X_24['Position'] = grp_24['Position']
        X_24['log_PSI'] = grp_24['log_PSI']
        X_24 = sm.add_constant(X_24)
        m_24 = sm.OLS(grp_24['RT'], X_24).fit()
        var_slopes_24.append(m_24.bse.get('Left', 0))
        
    results['LR_Slope_Variance_36'] = np.mean(var_slopes_36)
    results['LR_Slope_Variance_24'] = np.mean(var_slopes_24)
    results['Variance_Inflation_Ratio'] = np.mean(var_slopes_24) / np.mean(var_slopes_36)
    
    # 3. Power Recalibration
    # Standard Errors for Position and PSI slopes in Full vs Subtracted Model
    se_pos_36 = model_full.bse['Position']
    se_psi_36 = model_full.bse['log_PSI']
    
    se_pos_24 = model_b_prime.bse['Position']
    se_psi_24 = model_b_prime.bse['log_PSI']
    
    z_multiplier = 2.802 # power = 80%, alpha = 0.05
    results['Power'] = {
        'MDE_Pos_36': se_pos_36 * z_multiplier,
        'MDE_Pos_24': se_pos_24 * z_multiplier,
        'MDE_PSI_36': se_psi_36 * z_multiplier,
        'MDE_PSI_24': se_psi_24 * z_multiplier,
        'Power_Loss_Ratio': (se_pos_24 / se_pos_36) - 1.0
    }
    
    # 4. Final Verdict Logic Flags
    results['Verdict'] = {
        'Center_Needed_AIC': results['AIC_Delta'] > 10,
        'Center_Needed_PVal': results['Center_Partial_PValue'] < 0.05,
        'Center_Needed_Stability': results['Variance_Inflation_Ratio'] > 1.25, # 25% inflation is significant
        'Center_Needed_Power': results['Power']['Power_Loss_Ratio'] > 0.30 # 30% loss of sensitivity
    }
    
    res_bools = list(results['Verdict'].values())
    results['Final_Redundancy_Status'] = "REDUNDANT" if sum(res_bools) == 0 else "NECESSARY"

    return results

if __name__ == "__main__":
    df = generate_fov_synthetic_data(seed=124)
    print("=== SYNTHETIC FOV EVALUATION VALIDATION ===")
    res = evaluate_central_fov_informational_value(df)
    
    print(f"AIC Delta (Should be ~0 if redundant): {res['AIC_Delta']:.2f}")
    print(f"Center Factor P-Value: {res['Center_Partial_PValue']:.4e} (Must be < 0.05 to retain)")
    print(f"L-R Variance Base (36): {res['LR_Slope_Variance_36']:.3f}")
    print(f"L-R Variance Pruned (24): {res['LR_Slope_Variance_24']:.3f}")
    print(f"Variance Inflation Ratio: {res['Variance_Inflation_Ratio']:.2f}x")
    print(f"Power MDE Position 36->24: {res['Power']['MDE_Pos_36']:.3f} -> {res['Power']['MDE_Pos_24']:.3f}")
    print(f"Calculated Sensitivity Loss: {res['Power']['Power_Loss_Ratio']:.2%}")
    print(f"--> Final Derived Status: {res['Final_Redundancy_Status']}")
