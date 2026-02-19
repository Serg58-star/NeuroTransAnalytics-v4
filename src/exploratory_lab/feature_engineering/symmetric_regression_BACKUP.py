"""
Symmetric Regression Analyzer for Tasks 27.2A & 27.2B

Performs comprehensive field-by-field regression analysis to validate
ΔV4 and ΔV5 independence from baseline speed and assess hemispheric asymmetries.

Task 27.2A: Symmetric regression, residuals, nonlinearity, hemispheric comparisons
Task 27.2B: Standardization, heteroscedasticity, PSI tau stability, nested model tests

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
    """
    
    def __init__(self):
        """Initialize the symmetric regression analyzer."""
        self.linear_results = {}
        self.multiple_results = {}
        self.residual_correlations = {}
        self.nonlinearity_tests = {}
        self.hemispheric_comparisons = {}
        # Task 27.2B additions
        self.heteroscedasticity_tests = {}
        self.psi_tau_stability = {}
        self.nested_model_tests = {}
        # Task 27.2C additions
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
        self.heteroscedasticity_tests = results.get('heteroscedasticity', {})
        self.psi_tau_stability = results.get('psi_tau_stability', {})
        self.nested_model_tests = results.get('nested_model_ftests', {})
        
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
        Test for heteroscedasticity using Breusch-Pagan test (Task 27.2B Section II).
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix
        linear_results : dict
            Results from linear regression
        
        Returns
        -------
        dict
            Heteroscedasticity test results with p-values and diagnoses
        """
        hetero_results = {}
        
        for outcome, stats_dict in linear_results.items():
            residuals = stats_dict.get('residuals', [])
            
            if len(residuals) < 10:
                continue
            
            # Get predictor
            field = outcome.split('_')[2]  # Extract field (left/right)
            predictor = f'median_dv1_{field}'
            
            # Get clean data
            data = features_df[[outcome, predictor]].dropna()
            X = data[predictor].values
            
            # Breusch-Pagan test: regress squared residuals on predictor
            squared_resid = residuals ** 2
            
            # Fit auxiliary regression
            from sklearn.linear_model import LinearRegression
            X_bp = X.reshape(-1, 1)
            model_bp = LinearRegression().fit(X_bp, squared_resid)
            y_pred_bp = model_bp.predict(X_bp)
            
            # Calculate test statistic
            ss_res_bp = np.sum((squared_resid - y_pred_bp) ** 2)
            ss_tot_bp = np.sum((squared_resid - np.mean(squared_resid)) ** 2)
            r_squared_bp = 1 - (ss_res_bp / ss_tot_bp) if ss_tot_bp > 0 else 0
            
            n = len(residuals)
            lm_statistic = n * r_squared_bp  # n*R² follows chi-squared(1)
            
            # p-value from chi-squared distribution (df=1 for single predictor)
            p_value = 1 - stats.chi2.cdf(lm_statistic, df=1)
            
            # Additional: correlation between |residuals| and predictor
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
    
    def _analyze_psi_tau_stability(self, trials_df: pd.DataFrame, 
                                     features_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze PSI tau stability and reliability (Task 27.2B Section III).
        
        Parameters
        ----------
        trials_df : pd.DataFrame
            Trial-level data with PSI observations per subject
        features_df : pd.DataFrame
            Feature matrix with psi_tau values
        
        Returns
        -------
        dict
            PSI tau stability metrics and correlations
        """
        stability_results = {}
        
        # Extract tau values from features
        tau_values = features_df['psi_tau'].dropna()
        
        if len(tau_values) < 10:
            return stability_results
        
        # Distribution of tau
        stability_results['distribution'] = {
            'mean': np.mean(tau_values),
            'std': np.std(tau_values),
            'median': np.median(tau_values),
            'min': np.min(tau_values),
            'max': np.max(tau_values),
            'cv': np.std(tau_values) / np.mean(tau_values) if np.mean(tau_values) > 0 else np.nan
        }
        
        # If trial-level data available, analyze PSI observation count per subject
        if trials_df is not None and 'subject_id' in trials_df.columns:
            # Count PSI observations per subject (assuming PSI test types exist)
            psi_test_types = ['Tst2', 'Tst3', 'Tst4', 'Tst5']  # Common PSI test types
            
            subject_psi_counts = []
            subject_psi_ranges = []
            
            for subject_id in features_df.index:
                if subject_id not in trials_df['subject_id'].values:
                    continue
                
                subject_trials = trials_df[trials_df['subject_id'] == subject_id]
                
                # Count PSI trials
                if 'test_type' in subject_trials.columns:
                    psi_trials = subject_trials[subject_trials['test_type'].isin(psi_test_types)]
                    psi_count = len(psi_trials)
                    
                    if psi_count > 0 and 'rt' in psi_trials.columns:
                        psi_range = np.max(psi_trials['rt']) - np.min(psi_trials['rt'])
                        subject_psi_counts.append(psi_count)
                        subject_psi_ranges.append(psi_range)
            
            if len(subject_psi_counts) > 0:
                stability_results['psi_observations'] = {
                    'mean_count': np.mean(subject_psi_counts),
                    'std_count': np.std(subject_psi_counts),
                    'min_count': np.min(subject_psi_counts),
                    'max_count': np.max(subject_psi_counts),
                    'subjects_with_insufficient': np.sum(np.array(subject_psi_counts) < 4)
                }
                
                # Correlation: tau vs observation count
                valid_indices = features_df.index.isin(trials_df['subject_id'].unique())
                tau_subset = tau_values[valid_indices]
                
                if len(tau_subset) == len(subject_psi_counts):
                    r_count, p_count = stats.pearsonr(tau_subset, subject_psi_counts)
                    r_range, p_range = stats.pearsonr(tau_subset, subject_psi_ranges)
                    
                    stability_results['tau_dependencies'] = {
                        'r_vs_observation_count': r_count,
                        'p_vs_observation_count': p_count,
                        'r_vs_psi_range': r_range,
                        'p_vs_psi_range': p_range,
                        'dependent_on_count': abs(r_count) > 0.3
                    }
        
        return stability_results
    
    def _test_nested_models(self, features_df: pd.DataFrame,
                            multiple_results: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """
        F-test for nested model comparison (Task 27.2B Section IV).
        
        Tests if adding MAD significantly improves model fit.
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix
        multiple_results : dict
            Results from multiple regression
        
        Returns
        -------
        dict
            F-test results with p-values and significance
        """
        ftest_results = {}
        
        for outcome, stats_dict in multiple_results.items():
            n = stats_dict.get('n', 0)
            r2_full = stats_dict.get('r_squared', 0)
            r2_simple = stats_dict.get('r_squared_simple', 0)
            delta_r2 = stats_dict.get('delta_r_squared', 0)
            
            if n < 10:
                continue
            
            # F-test for nested models
            # F = (R²_full - R²_simple) / q / [(1 - R²_full) / (n - k - 1)]
            # where q = number of additional predictors (1 for MAD)
            # k = total predictors in full model (2: median + MAD)
            
            q = 1  # Adding MAD
            k = 2  # Full model has 2 predictors
            
            numerator = delta_r2 / q
            denominator = (1 - r2_full) / (n - k - 1) if (n - k - 1) > 0 else np.nan
            
            f_statistic = numerator / denominator if denominator > 0 else np.nan
            
            # p-value from F-distribution
            if not np.isnan(f_statistic):
                p_value = 1 - stats.f.cdf(f_statistic, q, n - k - 1)
            else:
                p_value = np.nan
            
            ftest_results[outcome] = {
                'n': n,
                'delta_r_squared': delta_r2,
                'f_statistic': f_statistic,
                'p_value': p_value,
                'mad_significant': p_value < 0.05 if not np.isnan(p_value) else False,
                'mad_minimal': delta_r2 < 0.02
            }
        
        return ftest_results
