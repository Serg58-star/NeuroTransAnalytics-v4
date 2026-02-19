"""
Symmetric Regression Analyzer for Tasks 27.2A, 27.2B, 27.2C

Performs comprehensive field-by-field regression analysis to validate
ΔV4 and ΔV5 independence from baseline speed and assess hemispheric asymmetries.

Task 27.2A: Symmetric regression, residuals, nonlinearity, hemispheric comparisons
Task 27.2B: Standardization, heteroscedasticity, PSI tau stability, nested model tests
Task 27.2C: Distribution validation, robust SE (HC3), practical significance

REQUIREMENTS:
- REAL data ONLY (synthetic data prohibited)
- Numerical analysis only (no visualization, clustering, PCA)
- Modular design with structured reporting
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class SymmetricRegressionAnalyzer:
    """
    Analyzes feature independence through symmetric field-by-field regression.
    
    Task 27.2A: Symmetric regression analysis
    Task 27.2B: Methodological validation checks
    Task 27.2C: Final stabilization checks
    """
    
    def __init__(self):
        """Initialize the symmetric regression analyzer."""
        # Task 27.2A results
        self.linear_results = {}
        self.multiple_results = {}
        self.residual_correlations = {}
        self.nonlinearity_tests = {}
        self.hemispheric_comparisons = {}
        self.center_control = {}
        
        # Task 27.2B results
        self.heteroscedasticity_tests = {}
        self.psi_tau_stability = {}
        self.nested_model_tests = {}
        
        # Task 27.2C results
        self.distribution_validation = {}
        self.standardization_doc = {}
        self.robust_se_results = {}
    
    def run_complete_analysis(self, features_df: pd.DataFrame, 
                              include_27_2b: bool = True,
                              include_27_2c: bool = True,
                              trials_df: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Run complete symmetric regression analysis (Tasks 27.2A, 27.2B, 27.2C).
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix with real data (subjects × features)
        include_27_2b : bool
            Include Task 27.2B methodological checks
        include_27_2c : bool
            Include Task 27.2C final stabilization checks
        trials_df : pd.DataFrame, optional
            Trial-level data required for PSI tau stability analysis
        
        Returns
        -------
        dict
            Complete analysis results with all regression outputs
        """
        results = {}
        
        # Task 27.2C: Distribution validation (pre-regression)
        if include_27_2c:
            results['distributions'] = self._validate_distributions(features_df)
        
        # Task 27.2A: Core regression analysis
        results['linear'] = self._run_linear_regression(features_df)
        results['multiple'] = self._run_multiple_regression(features_df)
        results['residuals'] = self._analyze_residual_structure(features_df)
        results['nonlinearity'] = self._test_nonlinearity(features_df)
        results['center_control'] = self._run_center_control(features_df)
        results['hemispheric'] = self._compare_hemispheric(results)
        
        # Task 27.2B: Methodological validation checks
        if include_27_2b:
            results['heteroscedasticity'] = self._test_heteroscedasticity(features_df, results['linear'])
            results['nested_model_ftests'] = self._test_nested_models(features_df, results['multiple'])
            
            if trials_df is not None:
                results['psi_tau_stability'] = self._analyze_psi_tau_stability(trials_df, features_df)
        
        # Task 27.2C: Additional stabilization checks
        if include_27_2c:
            results['standardization'] = self._document_standardization(features_df, results['multiple'])
            
            # Robust SE if heteroscedasticity detected
            if include_27_2b and results.get('heteroscedasticity'):
                results['robust_se'] = self._compute_robust_se_all(features_df, results)
        
        # Store for report generation
        self.linear_results = results['linear']
        self.multiple_results = results['multiple']
        self.residual_correlations = results['residuals']
        self.nonlinearity_tests = results['nonlinearity']
        self.hemispheric_comparisons = results['hemispheric']
        self.center_control = results.get('center_control', {})
        self.heteroscedasticity_tests = results.get('heteroscedasticity', {})
        self.psi_tau_stability = results.get('psi_tau_stability', {})
        self.nested_model_tests = results.get('nested_model_ftests', {})
        self.distribution_validation = results.get('distributions', {})
        self.standardization_doc = results.get('standardization', {})
        self.robust_se_results = results.get('robust_se', {})
        
        return results
    
    def _run_linear_regression(self, features_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Run field-by-field linear regression (Task 27.2A Section I).
        
        Models:
        - ΔV4_left ~ Median_ΔV1_left
        - ΔV4_right ~ Median_ΔV1_right
        - ΔV5_left ~ Median_ΔV1_left
        - ΔV5_right ~ Median_ΔV1_right
        """
        linear_results = {}
        
        for pathway in ['delta_v4', 'delta_v5']:
            for field in ['left', 'right']:
                outcome = f'{pathway}_{field}'
                predictor = f'median_dv1_{field}'
                
                # Get clean data
                data = features_df[[outcome, predictor]].dropna()
                
                if len(data) < 10:
                    continue
                
                X = data[predictor].values.reshape(-1, 1)
                y = data[outcome].values
                
                # Fit OLS
                model = LinearRegression()
                model.fit(X, y)
                
                # Predictions and residuals
                y_pred = model.predict(X)
                residuals = y - y_pred
                
                # Statistics
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                
                n = len(data)
                adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - 2) if n > 2 else r_squared
                
                # Standard error of regression
                se = np.sqrt(ss_res / (n - 2)) if n > 2 else np.nan
                
                # Coefficient standard error and p-value
                X_centered = X - np.mean(X)
                se_beta = se / np.sqrt(np.sum(X_centered ** 2)) if np.sum(X_centered ** 2) > 0 else np.nan
                t_stat = model.coef_[0] / se_beta if se_beta > 0 else np.nan
                p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2)) if n > 2 and not np.isnan(t_stat) else np.nan
                
                # Residual variance ratio
                resid_var = np.var(residuals)
                orig_var = np.var(y)
                resid_ratio = resid_var / orig_var if orig_var > 0 else np.nan
                
                linear_results[outcome] = {
                    'n': n,
                    'r_squared': r_squared,
                    'adj_r_squared': adj_r_squared,
                    'beta': model.coef_[0],
                    'intercept': model.intercept_,
                    'se_regression': se,
                    'se_beta': se_beta,
                    'p_value': p_value,
                    'residuals': residuals,
                    'residual_variance': resid_var,
                    'original_variance': orig_var,
                    'residual_ratio': resid_ratio
                }
        
        return linear_results
    
    def _run_multiple_regression(self, features_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Run multiple regression with MAD control (Task 27.2A Section II).
        
        Models:
        - ΔV4_field ~ Median_ΔV1_field + MAD_ΔV1_field
        - ΔV5_field ~ Median_ΔV1_field + MAD_ΔV1_field
        """
        multiple_results = {}
        
        for pathway in ['delta_v4', 'delta_v5']:
            for field in ['left', 'right']:
                outcome = f'{pathway}_{field}'
                pred_median = f'median_dv1_{field}'
                pred_mad = f'mad_dv1_{field}'
                
                # Check if columns exist
                if not all(col in features_df.columns for col in [outcome, pred_median, pred_mad]):
                    continue
                
                # Get clean data
                data = features_df[[outcome, pred_median, pred_mad]].dropna()
                
                if len(data) < 10:
                    continue
                
                X = data[[pred_median, pred_mad]].values
                y = data[outcome].values
                
                # Standardize for beta coefficients
                scaler = StandardScaler()
                X_std = scaler.fit_transform(X)
                
                # Fit OLS
                model = LinearRegression()
                model.fit(X, y)
                
                # Standardized coefficients
                model_std = LinearRegression()
                model_std.fit(X_std, y)
                standardized_betas = model_std.coef_
                
                # Predictions and residuals
                y_pred = model.predict(X)
                residuals = y - y_pred
                
                # Statistics
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                
                n = len(data)
                adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - 3) if n > 3 else r_squared
                
                # Compare to simple model (R² increase from adding MAD)
                X_simple = data[[pred_median]].values
                model_simple = LinearRegression().fit(X_simple, y)
                y_pred_simple = model_simple.predict(X_simple)
                ss_res_simple = np.sum((y - y_pred_simple) ** 2)
                r_squared_simple = 1 - (ss_res_simple / ss_tot) if ss_tot > 0 else 0
                delta_r_squared = r_squared - r_squared_simple
                
                multiple_results[outcome] = {
                    'n': n,
                    'r_squared': r_squared,
                    'r_squared_simple': r_squared_simple,
                    'delta_r_squared': delta_r_squared,
                    'adj_r_squared': adj_r_squared,
                    'beta_median': model.coef_[0],
                    'beta_mad': model.coef_[1],
                    'standardized_beta_median': standardized_betas[0],
                    'standardized_beta_mad': standardized_betas[1],
                    'intercept': model.intercept_,
                    'residuals': residuals
                }
        
        return multiple_results
    
    def _analyze_residual_structure(self, features_df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Analyze residual correlations (Task 27.2A Section III).
        
        Correlate residuals from linear models with:
        - psi_tau
        - asym_dv1_abs
        - asym_dv1_rel
        
        Threshold: |r| > 0.3 indicates independent latent component
        """
        residual_corrs = {}
        
        # First need to extract residuals from linear regression
        if not self.linear_results:
            return residual_corrs
        
        # Features to correlate with
        latent_features = ['psi_tau', 'asym_dv1_abs', 'asym_dv1_rel']
        
        for outcome, stats_dict in self.linear_results.items():
            residuals = stats_dict.get('residuals', [])
            
            if len(residuals) == 0:
                continue
            
            # Get indices of non-NaN rows for this outcome
            pathway, field = outcome.split('_')[1], outcome.split('_')[2]
            predictor = f'median_dv1_{field}'
            data_indices = features_df[[outcome, predictor]].dropna().index
            
            residual_corrs[outcome] = {}
            
            for latent_feat in latent_features:
                # Get latent feature values for same indices
                latent_vals = features_df.loc[data_indices, latent_feat].values
                
                # Remove any remaining NaN pairs
                valid_mask = ~np.isnan(latent_vals)
                if np.sum(valid_mask) < 10:
                    continue
                
                r, p = stats.pearsonr(residuals[valid_mask], latent_vals[valid_mask])
                
                residual_corrs[outcome][latent_feat] = {
                    'r': r,
                    'p_value': p,
                    'n': np.sum(valid_mask),
                    'independent': abs(r) > 0.3
                }
        
        return residual_corrs
    
    def _test_nonlinearity(self, features_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Test for nonlinearity using quadratic terms (Task 27.2A Section IV).
        
        Models:
        - ΔV4_field ~ Median_ΔV1_field + (Median_ΔV1_field)²
        
        Compare via AIC and BIC.
        """
        nonlinearity_results = {}
        
        for pathway in ['delta_v4', 'delta_v5']:
            for field in ['left', 'right']:
                outcome = f'{pathway}_{field}'
                predictor = f'median_dv1_{field}'
                
                # Get clean data
                data = features_df[[outcome, predictor]].dropna()
                
                if len(data) < 10:
                    continue
                
                y = data[outcome].values
                x = data[predictor].values
                n = len(data)
              
  
                # Linear model
                X_linear = x.reshape(-1, 1)
                model_linear = LinearRegression().fit(X_linear, y)
                y_pred_linear = model_linear.predict(X_linear)
                ss_res_linear = np.sum((y - y_pred_linear) ** 2)
                
                # Quadratic model
                X_quad = np.column_stack([x, x**2])
                model_quad = LinearRegression().fit(X_quad, y)
                y_pred_quad = model_quad.predict(X_quad)
                ss_res_quad = np.sum((y - y_pred_quad) ** 2)
                
                # AIC and BIC
                k_linear = 2  # intercept + slope
                k_quad = 3  # intercept + linear + quadratic
                
                aic_linear = n * np.log(ss_res_linear / n) + 2 * k_linear
                aic_quad = n * np.log(ss_res_quad / n) + 2 * k_quad
                
                bic_linear = n * np.log(ss_res_linear / n) + k_linear * np.log(n)
                bic_quad = n * np.log(ss_res_quad / n) + k_quad * np.log(n)
                
                delta_aic = aic_quad - aic_linear
                delta_bic = bic_quad - bic_linear
                
                nonlinearity_results[outcome] = {
                    'n': n,
                    'aic_linear': aic_linear,
                    'aic_quad': aic_quad,
                    'delta_aic': delta_aic,
                    'bic_linear': bic_linear,
                    'bic_quad': bic_quad,
                    'delta_bic': delta_bic,
                    'quad_improves': delta_aic < -2,  # Standard threshold
                    'beta_quad': model_quad.coef_[1]  # Quadratic coefficient
                }
        
        return nonlinearity_results
    
    def _run_center_control(self, features_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Run center field control analysis (Task 27.2A Section V).
        
        Models:
        - ΔV4_center ~ Median_ΔV1_center
        - ΔV5_center ~ Median_ΔV1_center
        
        Use as benchmark for dependency strength.
        """
        center_results = {}
        
        for pathway in ['delta_v4', 'delta_v5']:
            outcome = f'{pathway}_center'
            predictor = 'median_dv1_center'
            
            # Get clean data
            if outcome not in features_df.columns or predictor not in features_df.columns:
                continue
            
            data = features_df[[outcome, predictor]].dropna()
            
            if len(data) < 10:
                continue
            
            X = data[predictor].values.reshape(-1, 1)
            y = data[outcome].values
            
            # Fit OLS
            model = LinearRegression()
            model.fit(X, y)
            
            y_pred = model.predict(X)
            residuals = y - y_pred
            
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            n = len(data)
            adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - 2) if n > 2 else r_squared
            
            center_results[outcome] = {
                'n': n,
                'r_squared': r_squared,
                'adj_r_squared': adj_r_squared,
                'beta': model.coef_[0],
                'intercept': model.intercept_
            }
        
        return center_results
    
    def _compare_hemispheric(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare left vs right hemispheric patterns (Task 27.2A).
        
        Comparisons:
        - R²_left vs R²_right
        - Residual variance left vs right
        - Asymmetry in residual structure
        """
        comparisons = {}
        
        linear = results.get('linear', {})
        
        for pathway in ['delta_v4', 'delta_v5']:
            left_key = f'{pathway}_left'
            right_key = f'{pathway}_right'
            
            if left_key not in linear or right_key not in linear:
                continue
            
            r2_left = linear[left_key].get('r_squared', np.nan)
            r2_right = linear[right_key].get('r_squared', np.nan)
            
            resid_var_left = linear[left_key].get('residual_variance', np.nan)
            resid_var_right = linear[right_key].get('residual_variance', np.nan)
            
            comparisons[pathway] = {
                'r2_left': r2_left,
                'r2_right': r2_right,
                'r2_diff': r2_left - r2_right,
                'r2_asymmetric': abs(r2_left - r2_right) > 0.15,  # Threshold
                'resid_var_left': resid_var_left,
                'resid_var_right': resid_var_right,
                'resid_var_ratio': resid_var_left / resid_var_right if resid_var_right > 0 else np.nan
            }
        
        return comparisons
    
    # ========================================================================
    # TASK 27.2B: METHODOLOGICAL VALIDATION CHECKS
    # ========================================================================
    
    def _test_heteroscedasticity(self, features_df: pd.DataFrame, 
                                  linear_results: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """
        Test for heteroscedasticity using Breusch-Pagan test (Task 27.2B).
        
        For each linear model, tests if error variance is constant.
        
        Returns
        -------
        dict
            Test statistics, p-values, and heteroscedasticity diagnosis
        """
        hetero_results = {}
        
        for outcome, stats_dict in linear_results.items():
            residuals = stats_dict.get('residuals', [])
            
            if len(residuals) < 10:
                continue
            
            # Get predictor
            field = outcome.split('_')[2]
            predictor = f'median_dv1_{field}'
            
            # Get clean data
            data = features_df[[outcome, predictor]].dropna()
            X = data[predictor].values
            
            # Breusch-Pagan: regress squared residuals on predictor
            squared_resid = residuals ** 2
            
            X_bp = X.reshape(-1, 1)
            model_bp = LinearRegression().fit(X_bp, squared_resid)
            y_pred_bp = model_bp.predict(X_bp)
            
            ss_res_bp = np.sum((squared_resid - y_pred_bp) ** 2)
            ss_tot_bp = np.sum((squared_resid - np.mean(squared_resid)) ** 2)
            r_squared_bp = 1 - (ss_res_bp / ss_tot_bp) if ss_tot_bp > 0 else 0
            
            n = len(residuals)
            lm_statistic = n * r_squared_bp
            p_value = 1 - stats.chi2.cdf(lm_statistic, df=1)
            
            abs_resid_corr, abs_resid_p = stats.pearsonr(np.abs(residuals), X)
            
            hetero_results[outcome] = {
                'n': n,
                'lm_statistic': lm_statistic,
                'p_value': p_value,
                'heteroscedastic': p_value < 0.05,
                'abs_resid_correlation': abs_resid_corr,
                'abs_resid_p_value': abs_resid_p
            }
        
        return hetero_results
    
    def _test_nested_models(self, features_df: pd.DataFrame,
                            multiple_results: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """
        F-test for nested model comparison (Task 27.2B).
        
        Tests if adding MAD significantly improves model fit.
        Includes practical significance interpretation (Task 27.2C).
        """
        ftest_results = {}
        
        for outcome, stats_dict in multiple_results.items():
            n = stats_dict.get('n', 0)
            r2_full = stats_dict.get('r_squared', 0)
            r2_simple = stats_dict.get('r_squared_simple', 0)
            delta_r2 = stats_dict.get('delta_r_squared', 0)
            
            if n < 10:
                continue
            
            # F-test
            q = 1  # Adding MAD
            k = 2  # Full model has 2 predictors
            
            numerator = delta_r2 / q
            denominator = (1 - r2_full) / (n - k - 1) if (n - k - 1) > 0 else np.nan
            
            f_statistic = numerator / denominator if denominator > 0 else np.nan
            p_value = 1 - stats.f.cdf(f_statistic, q, n - k - 1) if not np.isnan(f_statistic) else np.nan
            
            # Practical significance interpretation (Task 27.2C)
            if p_value < 0.05:
                if delta_r2 < 0.02:
                    interpretation = "Statistically significant, practically minimal"
                elif delta_r2 < 0.05:
                    interpretation = "Statistically significant, modest contribution"
                else:
                    interpretation = "Substantial MAD contribution"
            else:
                interpretation = "Not statistically significant"
            
            ftest_results[outcome] = {
                'n': n,
                'delta_r_squared': delta_r2,
                'f_statistic': f_statistic,
                'p_value': p_value,
                'mad_significant': p_value < 0.05 if not np.isnan(p_value) else False,
                'mad_minimal': delta_r2 < 0.02,
                'interpretation': interpretation
            }
        
        return ftest_results
    
    def _analyze_psi_tau_stability(self, trials_df: pd.DataFrame, 
                                     features_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze PSI tau stability and reliability (Task 27.2B + 27.2C).
        
        Includes PSI range dependency check (Task 27.2C Section III).
        Task 27.2D: Enhanced with DataFrame-based index synchronization.
        """
        stability_results = {}
        
        tau_values = features_df['psi_tau'].dropna()
        
        if len(tau_values) < 10:
            return stability_results
        
        stability_results['distribution'] = {
            'mean': np.mean(tau_values),
            'std': np.std(tau_values),
            'median': np.median(tau_values),
            'min': np.min(tau_values),
            'max': np.max(tau_values),
            'cv': np.std(tau_values) / np.mean(tau_values) if np.mean(tau_values) > 0 else np.nan
        }
        
        # Trial-level analysis with DataFrame-based synchronization (Task 27.2D)
        if trials_df is not None and 'subject_id' in trials_df.columns:
            psi_test_types = ['Tst2', 'Tst3', 'Tst4', 'Tst5']
            
            # Build tau analysis DataFrame with explicit index alignment
            tau_analysis_data = []
            
            for subject_id in features_df.index:
                if subject_id not in trials_df['subject_id'].values:
                    continue
                
                # Get tau value
                if subject_id not in tau_values.index:
                    continue
                
                tau_val = tau_values.loc[subject_id]
                
                subject_trials = trials_df[trials_df['subject_id'] == subject_id]
                
                if 'test_type' in subject_trials.columns:
                    psi_trials = subject_trials[subject_trials['test_type'].isin(psi_test_types)]
                    psi_count = len(psi_trials)
                    
                    if psi_count > 0 and 'rt' in psi_trials.columns:
                        psi_range = np.max(psi_trials['rt']) - np.min(psi_trials['rt'])
                        
                        tau_analysis_data.append({
                            'subject_id': subject_id,
                            'tau': tau_val,
                            'psi_count': psi_count,
                            'psi_range': psi_range
                        })
            
            if len(tau_analysis_data) > 0:
                # Create DataFrame with explicit index
                tau_analysis_df = pd.DataFrame(tau_analysis_data).set_index('subject_id')
                
                # Report statistics
                stability_results['psi_observations'] = {
                    'mean_count': np.mean(tau_analysis_df['psi_count']),
                    'std_count': np.std(tau_analysis_df['psi_count']),
                    'min_count': int(np.min(tau_analysis_df['psi_count'])),
                    'max_count': int(np.max(tau_analysis_df['psi_count'])),
                    'subjects_with_insufficient': int(np.sum(tau_analysis_df['psi_count'] < 4)),
                    'total_subjects_analyzed': len(tau_analysis_df),
                    'subjects_excluded': len(features_df) - len(tau_analysis_df)
                }
                
                # Tau dependencies (Task 27.2C: range check) with guaranteed synchronization
                tau_for_corr = tau_analysis_df['tau'].values
                psi_counts_for_corr = tau_analysis_df['psi_count'].values
                psi_ranges_for_corr = tau_analysis_df['psi_range'].values
                
                # Verify alignment (Task 27.2D safety check)
                if len(tau_for_corr) == len(psi_counts_for_corr) == len(psi_ranges_for_corr):
                    r_count, p_count = stats.pearsonr(tau_for_corr, psi_counts_for_corr)
                    r_range, p_range = stats.pearsonr(tau_for_corr, psi_ranges_for_corr)
                    
                    stability_results['tau_dependencies'] = {
                        'r_vs_observation_count': r_count,
                        'p_vs_observation_count': p_count,
                        'r_vs_psi_range': r_range,
                        'p_vs_psi_range': p_range,
                        'dependent_on_count': abs(r_count) > 0.3,
                        'dependent_on_range': abs(r_range) > 0.3,  # Task 27.2C check
                        'n_correlated': len(tau_for_corr)
                    }
        
        return stability_results
    
    # ========================================================================
    # TASK 27.2C: FINAL STABILIZATION CHECKS
    # ========================================================================
    
    def _validate_distributions(self, features_df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Validate feature distributions before regression (Task 27.2C Section V).
        
        Checks skewness, kurtosis, and outliers for all key features.
        """
        from scipy.stats import skew, kurtosis
        
        distribution_results = {}
        
        features_to_check = [
            'delta_v4_left', 'delta_v4_right',
            'delta_v5_left', 'delta_v5_right',
            'psi_tau',
            'median_dv1_left', 'median_dv1_right', 'median_dv1_center',
            'mad_dv1', 'mad_dv1_left', 'mad_dv1_right'
        ]
        
        for feature in features_to_check:
            if feature not in features_df.columns:
                continue
            
            data = features_df[feature].dropna()
            
            if len(data) < 10:
                continue
            
            mean_val = np.mean(data)
            std_val = np.std(data)
            
            # Outliers: > 3 SD from mean
            outliers = np.abs(data - mean_val) > 3 * std_val
            outlier_count = np.sum(outliers)
            outlier_pct = outlier_count / len(data)
            
            distribution_results[feature] = {
                'n': len(data),
                'mean': mean_val,
                'std': std_val,
                'skewness': skew(data),
                'kurtosis': kurtosis(data),
                'outliers_count': int(outlier_count),
                'outliers_pct': outlier_pct,
                'outlier_risk': outlier_pct > 0.05
            }
        
        return distribution_results
    
    def _document_standardization(self, features_df: pd.DataFrame, 
                                    multiple_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Document standardization logic and statistics (Task 27.2C Section I).
        """
        standardization_doc = {
            'method': 'z-score standardization per field (left/right)',
            'note': 'Predictors standardized separately for each regression model',
            'predictors': {}
        }
        
        for field in ['left', 'right']:
            pred_median = f'median_dv1_{field}'
            pred_mad = f'mad_dv1_{field}'
            
            if pred_median in features_df.columns and pred_mad in features_df.columns:
                data = features_df[[pred_median, pred_mad]].dropna()
                
                standardization_doc['predictors'][field] = {
                    'median_dv1': {
                        'n': len(data),
                        'mean': np.mean(data[pred_median]),
                        'std': np.std(data[pred_median])
                    },
                    'mad_dv1': {
                        'n': len(data),
                        'mean': np.mean(data[pred_mad]),
                        'std': np.std(data[pred_mad])
                    }
                }
        
        return standardization_doc
    
    def _compute_robust_se_all(self, features_df: pd.DataFrame, 
                               results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Compute robust standard errors (HC3) for models with heteroscedasticity (Task 27.2C Section II).
        """
        robust_results = {}
        
        hetero_tests = results.get('heteroscedasticity', {})
        
        for outcome, hetero_dict in hetero_tests.items():
            if not hetero_dict.get('heteroscedastic', False):
                continue
            
            field = outcome.split('_')[2]
            predictor = f'median_dv1_{field}'
            
            data = features_df[[outcome, predictor]].dropna()
            
            if len(data) < 10:
                continue
            
            X = data[predictor].values.reshape(-1, 1)
            y = data[outcome].values
            
            model = LinearRegression().fit(X, y)
            residuals = y - model.predict(X)
            
            robust_se_dict = self._compute_robust_se_hc3(X, y, residuals, model.coef_[0])
            
            robust_results[outcome] = robust_se_dict
        
        return robust_results
    
    def _compute_robust_se_hc3(self, X: np.ndarray, y: np.ndarray, 
                                residuals: np.ndarray, beta: float) -> Dict[str, Any]:
        """
        Compute HC3 robust standard errors (Task 27.2C Section II).
        
        HC3 formula: V_HC3 = (X'X)^(-1) X' Omega X (X'X)^(-1)
        where Omega_ii = e_i^2 / (1 - h_ii)^2
        """
        n = len(X)
        
        # Add intercept
        X_with_intercept = np.column_stack([np.ones(n), X])
        
        # Hat matrix diagonal (leverage)
        # Using Moore-Penrose pseudo-inverse for numerical stability
        H = X_with_intercept @ np.linalg.pinv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T
        h = np.diag(H)
        
        # HC3 weights
        omega = residuals ** 2 / (1 - h) ** 2
        
        # Robust covariance matrix
        # Using Moore-Penrose pseudo-inverse for numerical stability
        Omega = np.diag(omega)
        XtX_inv = np.linalg.pinv(X_with_intercept.T @ X_with_intercept)
        V_robust = XtX_inv @ (X_with_intercept.T @ Omega @ X_with_intercept) @ XtX_inv
        
        # Robust SE (for slope coefficient)
        se_robust = np.sqrt(V_robust[1, 1])
        
        # Classical SE
        se_classical = np.sqrt(np.sum(residuals ** 2) / (n - 2)) / np.sqrt(np.sum((X - np.mean(X)) ** 2))
        
        # t-statistics and p-values
        t_classical = beta / se_classical
        t_robust = beta / se_robust
        
        p_classical = 2 * (1 - stats.t.cdf(abs(t_classical), n - 2))
        p_robust = 2 * (1 - stats.t.cdf(abs(t_robust), n - 2))
        
        return {
            'beta': beta,
            'se_classical': se_classical,
            'se_robust_hc3': se_robust,
            't_classical': t_classical,
            't_robust': t_robust,
            'p_classical': p_classical,
            'p_robust': p_robust,
            'significance_changes': (p_classical < 0.05) != (p_robust < 0.05)
        }
    
    
    
    def generate_report(self) -> str:
        """
        Generate comprehensive numerical report (Task 27.3C).
        
        Sections:
        1. Sample size
        2. Linear models
        3. Multiple models
        4. Residual correlations
        5. Heteroscedasticity
        6. Tau stability
        7. Distribution diagnostics
        
        Returns
        -------
        str
            Formatted text report - strictly numerical, no interpretations
        """
        lines = []
        
        def add_header(title, level=1):
            if level == 1:
                lines.append("=" * 80)
                lines.append(title)
                lines.append("=" * 80)
            elif level == 2:
                lines.append("-" * 60)
                lines.append(title)
                lines.append("-" * 60)
            elif level == 3:
                lines.append(f"  {title}")
                lines.append("  " + "-" * 40)
            lines.append("")
        
        def add_row(label, value, indent=4):
            prefix = " " * indent
            if isinstance(value, float):
                if abs(value) < 0.0001 and value != 0:
                    lines.append(f"{prefix}{label}: {value:.6e}")
                else:
                    lines.append(f"{prefix}{label}: {value:.6f}")
            else:
                lines.append(f"{prefix}{label}: {value}")
        
        # ===== HEADER =====
        add_header("SYMMETRIC REGRESSION ANALYSIS REPORT")
        add_header("Task 27.3 Production Run - Numerical Report", 2)
        
        # ===== SECTION 1: SAMPLE SIZE =====
        add_header("1. SAMPLE SIZE", 2)
        
        if self.linear_results:
            first_key = list(self.linear_results.keys())[0]
            n_total = self.linear_results[first_key].get('n', 0)
            add_row("Total subjects in analysis", n_total)
            add_row("Models computed", len(self.linear_results))
            
            for key, res in self.linear_results.items():
                add_row(f"  n ({key})", res.get('n', 0), indent=4)
        lines.append("")
        
        # ===== SECTION 2: LINEAR MODELS =====
        add_header("2. LINEAR MODELS (DV ~ Median_DV1)", 2)
        
        for pathway in ['delta_v4', 'delta_v5']:
            pathway_label = "DV4 ~ DV1" if pathway == 'delta_v4' else "DV5 ~ DV1"
            add_header(f"  {pathway_label}", 3)
            
            for field in ['left', 'right']:
                key = f"{pathway}_{field}"
                if key not in self.linear_results:
                    continue
                
                res = self.linear_results[key]
                lines.append(f"    [{field.upper()}]")
                add_row("n", res.get('n', 0))
                add_row("R2", res.get('r_squared', float('nan')))
                add_row("Adjusted R2", res.get('adj_r_squared', float('nan')))
                add_row("beta", res.get('beta', float('nan')))
                add_row("p-value", res.get('p_value', float('nan')))
                add_row("residual_ratio", res.get('residual_ratio', float('nan')))
                lines.append("")
            
            # Delta R2 left vs right
            left_key = f"{pathway}_left"
            right_key = f"{pathway}_right"
            if left_key in self.linear_results and right_key in self.linear_results:
                r2_left = self.linear_results[left_key].get('r_squared', 0)
                r2_right = self.linear_results[right_key].get('r_squared', 0)
                add_row("DR2_left_vs_right", r2_left - r2_right)
                lines.append("")
        
        # Center control
        if self.center_control:
            add_header("  Center Control", 3)
            for key, res in self.center_control.items():
                lines.append(f"    [{key}]")
                add_row("R2", res.get('r_squared', float('nan')))
                add_row("Adjusted R2", res.get('adj_r_squared', float('nan')))
                add_row("beta", res.get('beta', float('nan')))
                lines.append("")
        
        # Hemispheric comparison
        if self.hemispheric_comparisons:
            add_header("  Hemispheric Comparison", 3)
            for pathway, comp in self.hemispheric_comparisons.items():
                lines.append(f"    [{pathway}]")
                add_row("R2_left", comp.get('r2_left', float('nan')))
                add_row("R2_right", comp.get('r2_right', float('nan')))
                add_row("R2_diff", comp.get('r2_diff', float('nan')))
                add_row("R2_asymmetric", comp.get('r2_asymmetric', False))
                add_row("resid_var_ratio", comp.get('resid_var_ratio', float('nan')))
                lines.append("")
        
        # ===== SECTION 3: MULTIPLE MODELS =====
        add_header("3. MULTIPLE MODELS (DV ~ Median_DV1 + MAD_DV1)", 2)
        
        if self.multiple_results:
            for pathway in ['delta_v4', 'delta_v5']:
                pathway_label = "DV4 ~ DV1 + MAD" if pathway == 'delta_v4' else "DV5 ~ DV1 + MAD"
                add_header(f"  {pathway_label}", 3)
                
                for field in ['left', 'right']:
                    key = f"{pathway}_{field}"
                    if key not in self.multiple_results:
                        continue
                    
                    res = self.multiple_results[key]
                    lines.append(f"    [{field.upper()}]")
                    add_row("R2_simple", res.get('r_squared_simple', float('nan')))
                    add_row("R2_multiple", res.get('r_squared', float('nan')))
                    add_row("DR2", res.get('delta_r_squared', float('nan')))
                    add_row("Adjusted R2", res.get('adj_r_squared', float('nan')))
                    add_row("beta_median (raw)", res.get('beta_median', float('nan')))
                    add_row("beta_mad (raw)", res.get('beta_mad', float('nan')))
                    add_row("std_beta_median", res.get('standardized_beta_median', float('nan')))
                    add_row("std_beta_mad", res.get('standardized_beta_mad', float('nan')))
                    lines.append("")
            
            # Summary: DR2 categories
            lines.append("    DR2 Summary:")
            dr2_low = []
            dr2_high = []
            for key, res in self.multiple_results.items():
                dr2 = res.get('delta_r_squared', 0)
                if dr2 < 0.02:
                    dr2_low.append(f"{key} (DR2={dr2:.6f})")
                if dr2 >= 0.05:
                    dr2_high.append(f"{key} (DR2={dr2:.6f})")
            
            add_row("DR2 < 0.02", "; ".join(dr2_low) if dr2_low else "none")
            add_row("DR2 >= 0.05", "; ".join(dr2_high) if dr2_high else "none")
            lines.append("")
        
        # F-test for nested models
        if self.nested_model_tests:
            add_header("  Nested Model F-tests", 3)
            for key, res in self.nested_model_tests.items():
                lines.append(f"    [{key}]")
                add_row("F-statistic", res.get('f_statistic', float('nan')))
                add_row("p-value", res.get('p_value', float('nan')))
                add_row("significant (p<0.05)", res.get('significant', False))
                lines.append("")
        
        # ===== SECTION 4: RESIDUAL CORRELATIONS =====
        add_header("4. RESIDUAL CORRELATIONS", 2)
        
        if self.residual_correlations:
            for outcome, corrs in self.residual_correlations.items():
                lines.append(f"    [{outcome}]")
                for latent, vals in corrs.items():
                    r_val = vals.get('r', float('nan'))
                    p_val = vals.get('p_value', float('nan'))
                    flag = ""
                    if abs(r_val) >= 0.5:
                        flag = " ***"
                    elif abs(r_val) >= 0.3:
                        flag = " **"
                    add_row(f"Corr(resid, {latent})", f"r={r_val:.6f}, p={p_val:.6e}{flag}")
                lines.append("")
            
            # Summary: flagged correlations
            lines.append("    Flagged correlations:")
            for outcome, corrs in self.residual_correlations.items():
                for latent, vals in corrs.items():
                    r_val = abs(vals.get('r', 0))
                    if r_val >= 0.3:
                        add_row(f"|r| >= 0.3", f"{outcome} x {latent}: r={vals['r']:.6f}")
                    if r_val >= 0.5:
                        add_row(f"|r| >= 0.5", f"{outcome} x {latent}: r={vals['r']:.6f}")
            lines.append("")
        
        # ===== SECTION 5: HETEROSCEDASTICITY =====
        add_header("5. HETEROSCEDASTICITY (Breusch-Pagan)", 2)
        
        if self.heteroscedasticity_tests:
            for key, res in self.heteroscedasticity_tests.items():
                lines.append(f"    [{key}]")
                add_row("BP statistic", res.get('lm_statistic', float('nan')))
                add_row("p-value", res.get('p_value', float('nan')))
                add_row("heteroscedastic", res.get('heteroscedastic', False))
                add_row("|resid| correlation", res.get('abs_resid_correlation', float('nan')))
                add_row("|resid| p-value", res.get('abs_resid_p_value', float('nan')))
                lines.append("")
            
            # Robust SE summary
            if self.robust_se_results:
                add_header("  Robust SE (HC3)", 3)
                for key, res in self.robust_se_results.items():
                    lines.append(f"    [{key}]")
                    add_row("SE_classical", res.get('se_classical', float('nan')))
                    add_row("SE_robust_HC3", res.get('se_robust_hc3', float('nan')))
                    add_row("t_classical", res.get('t_classical', float('nan')))
                    add_row("t_robust", res.get('t_robust', float('nan')))
                    add_row("p_classical", res.get('p_classical', float('nan')))
                    add_row("p_robust", res.get('p_robust', float('nan')))
                    add_row("significance_changes", res.get('significance_changes', False))
                    lines.append("")
        
        # ===== SECTION 6: TAU STABILITY =====
        add_header("6. TAU STABILITY (PSI recovery)", 2)
        
        if self.psi_tau_stability:
            dist = self.psi_tau_stability.get('distribution', {})
            if dist:
                add_row("Mean tau", dist.get('mean', float('nan')))
                add_row("SD tau", dist.get('std', float('nan')))
                add_row("Median tau", dist.get('median', float('nan')))
                add_row("CV tau", dist.get('cv', float('nan')))
                add_row("Min tau", dist.get('min', float('nan')))
                add_row("Max tau", dist.get('max', float('nan')))
                lines.append("")
            
            obs = self.psi_tau_stability.get('psi_observations', {})
            if obs:
                add_row("Mean PSI count", obs.get('mean_count', float('nan')))
                add_row("SD PSI count", obs.get('std_count', float('nan')))
                add_row("Min PSI count", obs.get('min_count', float('nan')))
                add_row("Max PSI count", obs.get('max_count', float('nan')))
                add_row("Subjects < 4 trials", obs.get('subjects_with_insufficient', 0))
                lines.append("")
            
            deps = self.psi_tau_stability.get('tau_dependencies', {})
            if deps:
                add_row("Corr(tau, PSI_count)", f"r={deps.get('r_vs_observation_count', float('nan')):.6f}, p={deps.get('p_vs_observation_count', float('nan')):.6e}")
                add_row("Corr(tau, PSI_range)", f"r={deps.get('r_vs_psi_range', float('nan')):.6f}, p={deps.get('p_vs_psi_range', float('nan')):.6e}")
                add_row("dependent_on_count", deps.get('dependent_on_count', False))
                add_row("dependent_on_range", deps.get('dependent_on_range', False))
                lines.append("")
        else:
            lines.append("    No PSI tau stability data available")
            lines.append("")
        
        # ===== SECTION 7: DISTRIBUTION DIAGNOSTICS =====
        add_header("7. DISTRIBUTION DIAGNOSTICS", 2)
        
        if self.distribution_validation:
            # Table header
            lines.append(f"    {'Feature':<25} {'n':>6} {'Skewness':>10} {'Kurtosis':>10} {'%>3SD':>8} {'Outliers':>8}")
            lines.append("    " + "-" * 70)
            
            for feature, res in self.distribution_validation.items():
                n = res.get('n', 0)
                sk = res.get('skewness', float('nan'))
                ku = res.get('kurtosis', float('nan'))
                pct = res.get('outliers_pct', 0) * 100
                cnt = res.get('outliers_count', 0)
                
                lines.append(f"    {feature:<25} {n:>6} {sk:>10.4f} {ku:>10.4f} {pct:>7.2f}% {cnt:>8}")
            lines.append("")
        
        # ===== NONLINEARITY =====
        if self.nonlinearity_tests:
            add_header("8. NONLINEARITY TESTS (Quadratic)", 2)
            for key, res in self.nonlinearity_tests.items():
                lines.append(f"    [{key}]")
                add_row("AIC_linear", res.get('aic_linear', float('nan')))
                add_row("AIC_quad", res.get('aic_quad', float('nan')))
                add_row("delta_AIC", res.get('delta_aic', float('nan')))
                add_row("BIC_linear", res.get('bic_linear', float('nan')))
                add_row("BIC_quad", res.get('bic_quad', float('nan')))
                add_row("delta_BIC", res.get('delta_bic', float('nan')))
                add_row("quad_improves", res.get('quad_improves', False))
                lines.append("")
        
        # ===== FOOTER =====
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        return "\n".join(lines)
