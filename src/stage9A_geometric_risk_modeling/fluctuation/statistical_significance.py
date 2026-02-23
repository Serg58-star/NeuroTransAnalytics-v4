"""
stage9A_geometric_risk_modeling.fluctuation.statistical_significance

Transforms the continuous step-wise vector fluctuations into rigorous local and cumulative Z-scores
representing deviations from empirical population norm geometries.

Operates firmly within the `Stage 9B` architectural firewall (no diagnosis, no C3-Core mutation).
"""

import numpy as np
import pandas as pd

class FluctuationSignificanceModel:
    def __init__(self, epsilon: float = 1e-9, window_size: int = 5, k_min_consecutive: int = 2):
        """
        Args:
            epsilon: Division-by-zero protection for empirical variance constants.
            window_size: W size for rolling variance computation.
            k_min_consecutive: Number of consecutive Z>1.96 observations to trigger an alert.
        """
        self.epsilon = epsilon
        self.window_size = window_size
        self.k_min_consecutive = k_min_consecutive
        self.fitted = False
        
        self.pop_variance = {
            'r_t': 1.0,
            'delta_M': 1.0,
            'delta_S': 1.0,
            'delta_L': 1.0,
            'delta_T': 1.0
        }
        
        # Empirical heavy-tail backups (Task 40.2 Forward Compatibility)
        self.pop_percentiles = {}
        
    def fit_population_variance(self, df_population: pd.DataFrame):
        """
        Derives physiological baseline variances from a raw population fluctuation log.
        Expected columns: ['Radial_Velocity_rt', 'DeltaZ_Speed', 'DeltaZ_Lateral', 'DeltaZ_Tone']
        And calculates Delta_M from Mahalanobis norms.
        """
        # Exclude initial trajectory points (NaN elements)
        valid_steps = df_population.dropna(subset=['Radial_Velocity_rt']).copy()
        
        # We need Delta M for magnitude inflation significance.
        # Ensure we have the absolute Mahalanobis distance columns or compute them if we only have the raw coords
        # For this design, we trust the caller has either provided Mahalanobis or we compute the simplistic delta_M 
        # based on Pythagorean identity: ||delta||^2_Sigma = r_t^2 + tau_t^2
        if 'Mahalanobis_Distance' in valid_steps.columns:
            # We assume df is properly sorted by Subject/Time before diffing
            valid_steps['Delta_M'] = valid_steps.groupby('Subject_ID')['Mahalanobis_Distance'].diff()
        else:
            # If absolute distance isn't logged, we use the vector length ||delta|| as a proxy for delta_M volatility
            delta_sq_norm = valid_steps['Radial_Velocity_rt']**2 + valid_steps['Tangential_Velocity_taut']**2
            valid_steps['Delta_M'] = np.sqrt(np.maximum(delta_sq_norm, 0.0))
            
        valid_steps = valid_steps.dropna(subset=['Delta_M'])
        
        # Calculate base empirical standard deviations (sigma)
        # Using maximum(val, epsilon) to protect against dividing by zero later
        self.pop_variance['r_t'] = max(valid_steps['Radial_Velocity_rt'].var(ddof=1), self.epsilon)
        self.pop_variance['delta_M'] = max(valid_steps['Delta_M'].var(ddof=1), self.epsilon)
        
        self.pop_variance['delta_S'] = max(valid_steps['DeltaZ_Speed'].var(ddof=1), self.epsilon)
        self.pop_variance['delta_L'] = max(valid_steps['DeltaZ_Lateral'].var(ddof=1), self.epsilon)
        self.pop_variance['delta_T'] = max(valid_steps['DeltaZ_Tone'].var(ddof=1), self.epsilon)
        
        # Calculate windowed variances for empirical thresholding
        valid_steps = valid_steps.sort_values(['Subject_ID', 'TimeStep']).copy()
        for col in ['Radial_Velocity_rt', 'Delta_M', 'DeltaZ_Speed', 'DeltaZ_Lateral', 'DeltaZ_Tone']:
            valid_steps[f'var_{col}'] = valid_steps.groupby('Subject_ID')[col].transform(lambda x: x.rolling(self.window_size, min_periods=2).var(ddof=1))
        
        # Extract and store 95th percentiles of absolute magnitude for heavy-tail protection
        self.pop_percentiles = {
            'r_t_p95': valid_steps['Radial_Velocity_rt'].abs().quantile(0.95),
            'delta_M_p95': valid_steps['Delta_M'].abs().quantile(0.95),
            'delta_S_p95': valid_steps['DeltaZ_Speed'].abs().quantile(0.95),
            'delta_L_p95': valid_steps['DeltaZ_Lateral'].abs().quantile(0.95),
            'delta_T_p95': valid_steps['DeltaZ_Tone'].abs().quantile(0.95),
            
            # Non-parametric empirical variance thresholds
            'var_r_t_p95': valid_steps['var_Radial_Velocity_rt'].quantile(0.95),
            'var_delta_M_p95': valid_steps['var_Delta_M'].quantile(0.95),
            'var_delta_S_p95': valid_steps['var_DeltaZ_Speed'].quantile(0.95),
            'var_delta_L_p95': valid_steps['var_DeltaZ_Lateral'].quantile(0.95),
            'var_delta_T_p95': valid_steps['var_DeltaZ_Tone'].quantile(0.95)
        }
        
        self.fitted = True
        
    def compute_significance(self, df_subject: pd.DataFrame) -> pd.DataFrame:
        """
        Takes raw tracking statistics and maps them into longitudinal Z-scores.
        Requires fit_population_variance to have been executed.
        """
        if not self.fitted:
            raise ValueError("FluctuationSignificanceModel must be fitted to population data before scoring.")
            
        out = df_subject.copy()
        out = out.sort_values(['Subject_ID', 'TimeStep']).reset_index(drop=True)
        
        if 'Mahalanobis_Distance' in out.columns:
            out['Delta_M'] = out.groupby('Subject_ID')['Mahalanobis_Distance'].diff()
        else:
            delta_sq_norm = out['Radial_Velocity_rt']**2 + out['Tangential_Velocity_taut']**2
            out['Delta_M'] = np.sqrt(np.maximum(delta_sq_norm, 0.0))
            
        # Standard Z-scores
        out['z_r'] = out['Radial_Velocity_rt'] / np.sqrt(self.pop_variance['r_t'])
        out['z_delta_M'] = out['Delta_M'] / np.sqrt(self.pop_variance['delta_M'])
        
        out['z_delta_S'] = out['DeltaZ_Speed'] / np.sqrt(self.pop_variance['delta_S'])
        out['z_delta_L'] = out['DeltaZ_Lateral'] / np.sqrt(self.pop_variance['delta_L'])
        out['z_delta_T'] = out['DeltaZ_Tone'] / np.sqrt(self.pop_variance['delta_T'])
        
        # Volatility tracking (Rolling Variance calculation)
        for col in ['Radial_Velocity_rt', 'Delta_M', 'DeltaZ_Speed', 'DeltaZ_Lateral', 'DeltaZ_Tone']:
            out[f'var_{col}'] = out.groupby('Subject_ID')[col].transform(lambda x: x.rolling(self.window_size, min_periods=2).var(ddof=1))
            
        out['volatility_r_t'] = (out['var_Radial_Velocity_rt'] > self.pop_percentiles['var_r_t_p95']).fillna(False).astype(int)
        out['volatility_delta_M'] = (out['var_Delta_M'] > self.pop_percentiles['var_delta_M_p95']).fillna(False).astype(int)
        
        # Consecutive Z-score tracking function
        def count_consecutive_z(series, threshold=1.96):
            is_over = (series.abs() > threshold).astype(int)
            blocks = (is_over != is_over.shift()).cumsum()
            return is_over * is_over.groupby(blocks).cumsum()
            
        out['k_z_r'] = out.groupby('Subject_ID')['z_r'].transform(count_consecutive_z)
        out['k_z_delta_M'] = out.groupby('Subject_ID')['z_delta_M'].transform(count_consecutive_z)
        out['k_z_delta_S'] = out.groupby('Subject_ID')['z_delta_S'].transform(count_consecutive_z)
        out['k_z_delta_L'] = out.groupby('Subject_ID')['z_delta_L'].transform(count_consecutive_z)
        out['k_z_delta_T'] = out.groupby('Subject_ID')['z_delta_T'].transform(count_consecutive_z)
        
        # Cumulative Windowed Significance (Z_cum)
        # Z_cum = \sum r_k / \sqrt{T * \sigma_r^2}
        
        # We compute an expanding sum per subject
        # To avoid Pandas apply() multi-index shape errors, we compute isolated series and map back
        z_cum_series = pd.Series(index=out.index, dtype=float)
        
        for _, group in out.groupby('Subject_ID'):
            r_t_clean = group['Radial_Velocity_rt'].fillna(0)
            cum_r_t = r_t_clean.cumsum()
            
            valid_mask = group['Radial_Velocity_rt'].notna()
            time_idx = valid_mask.cumsum() 
            denom = np.sqrt(np.maximum(time_idx * self.pop_variance['r_t'], self.epsilon))
            
            z_cum = cum_r_t / denom
            z_cum[~valid_mask] = np.nan
            
            # Map back exactly to the original dataframe indices for this group
            z_cum_series.loc[group.index] = z_cum
            
        out['z_cum_r'] = z_cum_series
        
        return out
