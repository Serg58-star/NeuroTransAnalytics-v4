"""
Regression Validator for Pre-Launch Feature Independence Checks (Task 27.2)

Validates that ΔV4 and ΔV5 are not simply derivatives of baseline speed (ΔV1).
Performs mandatory regression checks before launching geometric analysis.

NO visualization, clustering, or UMAP - numerical validation only.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from scipy import stats
from sklearn.linear_model import LinearRegression


class RegressionValidator:
    """
    Validates feature independence through regression analysis.
    
    Task 27.2: Checks if ΔV4 and ΔV5 are independent from baseline speed.
    """
    
    def __init__(self):
        """Initialize the regression validator."""
        self.regression_results = {}
        self.partial_correlations = {}
        self.asymmetry_redundancy = None
    
    def validate(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform complete regression validation.
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix (subjects × features)
        
        Returns
        -------
        dict
            Validation results with:
            - regression_dv4: R² values for ΔV4 ~ ΔV1
            - regression_dv5: R² values for ΔV5 ~ ΔV1
            - tau_correlations: PSI tau correlations
            - asymmetry_redundancy: abs vs rel correlation
            - independence_conclusions: Feature-by-feature assessment
        """
        results = {}
        
        # 1. Regression independence checks (ΔV4, ΔV5 ~ ΔV1)
        results['regression_dv4'] = self._check_regression_independence(
            features_df, 'delta_v4', 'median_dv1'
        )
        results['regression_dv5'] = self._check_regression_independence(
            features_df, 'delta_v5', 'median_dv1'
        )
        
        # 2. PSI tau partial correlations
        results['tau_correlations'] = self._check_tau_correlations(features_df)
        
        # 3. Asymmetry redundancy
        results['asymmetry_redundancy'] = self._check_asymmetry_redundancy(features_df)
        
        # 4. Generate conclusions
        results['conclusions'] = self._generate_conclusions(results)
        
        # Store for report generation
        self.regression_results = results
        
        return results
    
    def _check_regression_independence(
        self, 
        features_df: pd.DataFrame,
        target_prefix: str,
        predictor_prefix: str
    ) -> Dict[str, Dict[str, float]]:
        """
        Check regression independence for a target feature vs predictor.
        
        For each field (left, right, center):
        - Fit: target_field ~ predictor_field
        - Calculate R², adjusted R², residual variance
        
        Parameters
        ----------
        target_prefix : str
            Prefix of target features (e.g., 'delta_v4')
        predictor_prefix : str
            Prefix of predictor features (e.g., 'median_dv1')
        
        Returns
        -------
        dict
            Regression statistics for each field
        """
        regression_stats = {}
        
        for field in ['left', 'center', 'right']:
            target_col = f'{target_prefix}_{field}'
            predictor_col = f'{predictor_prefix}_{field}'
            
            # Check if columns exist
            if target_col not in features_df.columns or predictor_col not in features_df.columns:
                continue
            
            # Get clean data (no NaN)
            data = features_df[[target_col, predictor_col]].dropna()
            
            if len(data) < 10:
                regression_stats[field] = {
                    'n': len(data),
                    'r_squared': np.nan,
                    'adj_r_squared': np.nan,
                    'residual_variance': np.nan,
                    'original_variance': np.nan,
                    'residual_ratio': np.nan
                }
                continue
            
            X = data[predictor_col].values.reshape(-1, 1)
            y = data[target_col].values
            
            # Fit linear regression
            model = LinearRegression()
            model.fit(X, y)
            
            # Predictions and residuals
            y_pred = model.predict(X)
            residuals = y - y_pred
            
            # Calculate R²
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            # Adjusted R²
            n = len(data)
            adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - 2) if n > 2 else r_squared
            
            # Residual variance vs original variance
            residual_var = np.var(residuals)
            original_var = np.var(y)
            residual_ratio = residual_var / original_var if original_var > 0 else np.nan
            
            regression_stats[field] = {
                'n': n,
                'r_squared': r_squared,
                'adj_r_squared': adj_r_squared,
                'residual_variance': residual_var,
                'original_variance': original_var,
                'residual_ratio': residual_ratio,
                'slope': model.coef_[0],
                'intercept': model.intercept_
            }
        
        return regression_stats
    
    def _check_tau_correlations(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Check PSI tau correlations with ΔV1 fields.
        
        Calculate:
        - Simple correlations: tau vs ΔV1_left, ΔV1_right, ΔV1_center
        - Partial correlation: controlling for mean speed
        
        Returns
        -------
        dict
            Correlation results with interpretation
        """
        if 'psi_tau' not in features_df.columns:
            return {'error': 'psi_tau not in features'}
        
        tau = features_df['psi_tau'].dropna()
        
        correlations = {}
        
        # Simple correlations with each field
        for field in ['left', 'center', 'right']:
            col = f'median_dv1_{field}'
            if col in features_df.columns:
                # Get paired data
                paired = features_df[[col, 'psi_tau']].dropna()
                if len(paired) >= 10:
                    r, p = stats.pearsonr(paired[col], paired['psi_tau'])
                    correlations[f'tau_vs_dv1_{field}'] = {
                        'r': r,
                        'p_value': p,
                        'n': len(paired)
                    }
        
        # Partial correlation (controlling for mean speed)
        if all(f'median_dv1_{f}' in features_df.columns for f in ['left', 'right']):
            # Calculate mean speed across fields
            features_df_copy = features_df.copy()
            features_df_copy['mean_dv1'] = features_df_copy[[
                'median_dv1_left', 'median_dv1_right'
            ]].mean(axis=1)
            
            # Partial correlation: tau vs dv1_left controlling for mean_dv1
            partial_corr = self._partial_correlation(
                features_df_copy, 'psi_tau', 'median_dv1_left', 'mean_dv1'
            )
            correlations['partial_tau_vs_dv1_left'] = partial_corr
        
        return correlations
    
    def _partial_correlation(
        self,
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        control_col: str
    ) -> Dict[str, float]:
        """
        Calculate partial correlation between x and y, controlling for control variable.
        
        Uses residual method:
        1. Regress x ~ control, get residuals_x
        2. Regress y ~ control, get residuals_y
        3. Correlate residuals_x with residuals_y
        """
        # Get clean data
        data = df[[x_col, y_col, control_col]].dropna()
        
        if len(data) < 10:
            return {'r': np.nan, 'n': len(data)}
        
        # Residualize x
        X = data[control_col].values.reshape(-1, 1)
        y_x = data[x_col].values
        model_x = LinearRegression().fit(X, y_x)
        resid_x = y_x - model_x.predict(X)
        
        # Residualize y
        y_y = data[y_col].values
        model_y = LinearRegression().fit(X, y_y)
        resid_y = y_y - model_y.predict(X)
        
        # Correlate residuals
        r, p = stats.pearsonr(resid_x, resid_y)
        
        return {'r': r, 'p_value': p, 'n': len(data)}
    
    def _check_asymmetry_redundancy(self, features_df: pd.DataFrame) -> Dict[str, float]:
        """
        Check correlation between asym_abs and asym_rel.
        
        If |r| > 0.9, one metric is redundant.
        """
        if 'asym_dv1_abs' not in features_df.columns or 'asym_dv1_rel' not in features_df.columns:
            return {'error': 'Asymmetry features not found'}
        
        data = features_df[['asym_dv1_abs', 'asym_dv1_rel']].dropna()
        
        if len(data) < 10:
            return {'r': np.nan, 'n': len(data)}
        
        r, p = stats.pearsonr(data['asym_dv1_abs'], data['asym_dv1_rel'])
        
        return {
            'r': r,
            'p_value': p,
            'n': len(data),
            'redundant': abs(r) > 0.9
        }
    
    def _generate_conclusions(self, results: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate interpretation for each validation check.
        
        Returns
        -------
        dict
            Feature-by-feature independence conclusions
        """
        conclusions = {}
        
        # ΔV4 independence
        for field, stats_dict in results.get('regression_dv4', {}).items():
            r2 = stats_dict.get('r_squared', np.nan)
            if pd.isna(r2):
                conclusions[f'delta_v4_{field}'] = 'Insufficient data'
            elif r2 > 0.7:
                conclusions[f'delta_v4_{field}'] = f'NOT INDEPENDENT (R²={r2:.2f} > 0.7)'
            elif r2 > 0.5:
                conclusions[f'delta_v4_{field}'] = f'Moderate dependence (R²={r2:.2f})'
            else:
                conclusions[f'delta_v4_{field}'] = f'Independent (R²={r2:.2f} < 0.5)'
        
        # ΔV5 independence
        for field, stats_dict in results.get('regression_dv5', {}).items():
            r2 = stats_dict.get('r_squared', np.nan)
            if pd.isna(r2):
                conclusions[f'delta_v5_{field}'] = 'Insufficient data'
            elif r2 > 0.7:
                conclusions[f'delta_v5_{field}'] = f'NOT INDEPENDENT (R²={r2:.2f} > 0.7)'
            elif r2 > 0.5:
                conclusions[f'delta_v5_{field}'] = f'Moderate dependence (R²={r2:.2f})'
            else:
                conclusions[f'delta_v5_{field}'] = f'Independent (R²={r2:.2f} < 0.5)'
        
        # PSI tau
        tau_corrs = results.get('tau_correlations', {})
        max_r = max([abs(v.get('r', 0)) for k, v in tau_corrs.items() 
                     if isinstance(v, dict) and 'r' in v], default=0)
        if max_r > 0.6:
            conclusions['psi_tau'] = f'Possibly derivative of speed (max |r|={max_r:.2f})'
        else:
            conclusions['psi_tau'] = f'Independent from baseline speed (max |r|={max_r:.2f})'
        
        # Asymmetry redundancy
        asym_result = results.get('asymmetry_redundancy', {})
        if asym_result.get('redundant', False):
            r = asym_result.get('r', 0)
            conclusions['asymmetry'] = f'REDUNDANT (r={r:.3f} > 0.9) - consider keeping one'
        else:
            r = asym_result.get('r', 0)
            conclusions['asymmetry'] = f'Both metrics useful (r={r:.3f})'
        
        return conclusions
    
    def generate_report(self) -> str:
        """
        Generate text report of validation results.
        
        Returns
        -------
        str
            Formatted text report (no visualization)
        """
        if not self.regression_results:
            return "No validation results available. Run validate() first."
        
        results = self.regression_results
        lines = []
        
        lines.append("=" * 70)
        lines.append("TASK 27.2 - PRE-LAUNCH REGRESSION VALIDATION REPORT")
        lines.append("=" * 70)
        lines.append("")
        
        # 1. ΔV4 Regression Independence
        lines.append("I. ΔV4 ~ ΔV1 Regression Analysis")
        lines.append("-" * 70)
        dv4_results = results.get('regression_dv4', {})
        for field in ['left', 'center', 'right']:
            if field in dv4_results:
                stats_dict = dv4_results[field]
                lines.append(f"\n{field.upper()} field:")
                lines.append(f"  N: {stats_dict['n']}")
                lines.append(f"  R²: {stats_dict.get('r_squared', np.nan):.4f}")
                lines.append(f"  Adjusted R²: {stats_dict.get('adj_r_squared', np.nan):.4f}")
                lines.append(f"  Residual variance ratio: {stats_dict.get('residual_ratio', np.nan):.4f}")
                lines.append(f"  → {results['conclusions'].get(f'delta_v4_{field}', 'N/A')}")
        
        lines.append("")
        
        # 2. ΔV5 Regression Independence
        lines.append("II. ΔV5 ~ ΔV1 Regression Analysis")
        lines.append("-" * 70)
        dv5_results = results.get('regression_dv5', {})
        for field in ['left', 'center', 'right']:
            if field in dv5_results:
                stats_dict = dv5_results[field]
                lines.append(f"\n{field.upper()} field:")
                lines.append(f"  N: {stats_dict['n']}")
                lines.append(f"  R²: {stats_dict.get('r_squared', np.nan):.4f}")
                lines.append(f"  Adjusted R²: {stats_dict.get('adj_r_squared', np.nan):.4f}")
                lines.append(f"  Residual variance ratio: {stats_dict.get('residual_ratio', np.nan):.4f}")
                lines.append(f"  → {results['conclusions'].get(f'delta_v5_{field}', 'N/A')}")
        
        lines.append("")
        
        # 3. PSI Tau Correlations
        lines.append("III. PSI Tau Correlations")
        lines.append("-" * 70)
        tau_corrs = results.get('tau_correlations', {})
        for key, val in tau_corrs.items():
            if isinstance(val, dict) and 'r' in val:
                lines.append(f"{key}: r={val['r']:.4f}, p={val.get('p_value', np.nan):.4f}, n={val['n']}")
        lines.append(f"→ {results['conclusions'].get('psi_tau', 'N/A')}")
        
        lines.append("")
        
        # 4. Asymmetry Redundancy
        lines.append("IV. Asymmetry Redundancy Check")
        lines.append("-" * 70)
        asym_result = results.get('asymmetry_redundancy', {})
        lines.append(f"Correlation (abs vs rel): r={asym_result.get('r', np.nan):.4f}")
        lines.append(f"→ {results['conclusions'].get('asymmetry', 'N/A')}")
        
        lines.append("")
        lines.append("=" * 70)
        lines.append("END OF REGRESSION VALIDATION REPORT")
        lines.append("=" * 70)
        
        return "\n".join(lines)
